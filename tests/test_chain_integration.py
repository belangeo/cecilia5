"""Opt-in tests using actual wx editors and pyo audio processing.

Run from the repository root with CECILIA_GUI_TESTS=1 and a working DISPLAY.
All preferences, module fixtures, audio and session files use a temporary profile.
"""

import importlib.util
import json
import math
import os
from pathlib import Path
import struct
import tempfile
import traceback
import unittest
from unittest.mock import Mock, patch
import wave


GUI_AVAILABLE = (os.environ.get('CECILIA_GUI_TESTS') == '1' and
                 importlib.util.find_spec('pyo') is not None and
                 importlib.util.find_spec('wx') is not None)


@unittest.skipUnless(GUI_AVAILABLE, 'Requires CECILIA_GUI_TESTS=1, wx, pyo and a display')
class ChainIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = tempfile.TemporaryDirectory(prefix='cecilia-chain-tests-')
        original_expanduser = os.path.expanduser
        with patch('os.path.expanduser', side_effect=lambda path: cls.profile.name if path == '~' else original_expanduser(path)):
            import wx
            cls.wx = wx
            cls.app = wx.App(False)
            from Resources import CeciliaLib, Variables, audio, ChainUI
            from Resources.CeciliaMainFrame import CeciliaMainFrame
            cls.lib, cls.audio, cls.ui = CeciliaLib, audio, ChainUI
            Variables.loadBitmaps()
            cls.lib.setVar('displaySize', [(1280, 900)])
            cls.lib.setVar('displayOffset', [(0, 0)])
            cls.main = CeciliaMainFrame(None, -1)
            cls.lib.setVar('mainFrame', cls.main)

    @classmethod
    def tearDownClass(cls):
        cls.main.api_doc_frame.Destroy()
        cls.main.mod_doc_frame.Destroy()
        cls.main.Destroy()
        cls.app.Yield()
        cls.profile.cleanup()

    def setUp(self):
        self.folder = Path(tempfile.mkdtemp(dir=self.profile.name))
        self.errors = []
        self.error_patch = patch.object(self.lib, 'showErrorDialog', side_effect=lambda title, message: self.errors.append((title, message, traceback.format_exc())))
        self.error_patch.start()
        self.discard_patch = patch.object(self.lib, 'confirmSessionDiscard', return_value=True)
        self.discard_patch.start()
        self.lib.session.modules = []
        self.lib.session.selected_id = None
        self.lib.session.saved_snapshot = None
        self.lib.session.path = None
        self.lib.session.view = 'graph'
        self.lib.setVar('audioHostAPI', 'offline')
        self.lib.setVar('totalTime', 0.2)
        self.lib.setVar('startOffset', 0)
        self.lib.setVar('plugins', [None] * self.lib.NUM_OF_PLUGINS)
        self.lib.setVar('gainSlider', None)
        self.lib.setVar('nchnls', 2)
        self.lib.setVar('globalFade', 0.005)
        self.server = self.audio.AudioServer()
        self.lib.setVar('audioServer', self.server)
        self.fixture = self.folder / (self._testMethodName + '.c5')
        self.fixture.write_text(
            'class Module(BaseModule):\n'
            '    def __init__(self):\n'
            '        BaseModule.__init__(self)\n'
            '        self.out = self.addSampler("snd") * self.level\n'
            'Interface = [csampler(name="snd"), cslider(name="level", min=0, max=1, init=0.5)]\n'
        )
        self.source = self.folder / 'source.wav'
        with wave.open(str(self.source), 'wb') as stream:
            stream.setnchannels(2)
            stream.setsampwidth(2)
            stream.setframerate(44100)
            stream.writeframes(b''.join(struct.pack('<hh', *([int(5000 * math.sin(2*math.pi*440*i/44100))] * 2))
                                       for i in range(22050)))
        self.add()
        self.first = self.lib.session.modules[0]
        self.first.inputs.cfileinList[0].onLoadFile(str(self.source))
        self.frame = self.lib.getVar('interface')
        self.frame.controlPanel.setTotalTime(0.2)
        self.app.Yield()

    def tearDown(self):
        if self.server.isAudioServerRunning():
            self.server.stop()
        self.server.cleanup_module()
        if self.server.isAudioServerBooted():
            self.server.shutdown()
        frame = self.lib.getVar('interface')
        if frame:
            frame.destroySessionWindow()
        self.lib.session.modules = []
        self.lib.session.selected_id = None
        self.app.Yield()
        self.error_patch.stop()
        self.discard_patch.stop()

    def test_graph_texture_uses_current_plot_geometry_without_resize(self):
        plot = self.first.editor.graph.plotter
        texture = self.lib.getVar('graphTexture')
        yspec = plot._ySpec
        try:
            self.lib.setVar('graphTexture', True)
            # Simulate a draw before the canvas size event has caught up.
            plot._Buffer = self.wx.Bitmap(100, 100)
            plot._setSize(100, 100)
            plot._background_size = None
            plot._Draw(*plot.last_draw)
            self.assertEqual(plot._Buffer.GetSize(), plot.canvas.GetClientSize())
            self.assertEqual((plot.width, plot.height), tuple(plot.canvas.GetClientSize()))
            previous = plot._scaled_background_bitmap.GetSize()
            # Changing label margins must recrop even at the same canvas size.
            plot._ySpec = 'none'
            plot._Draw(*plot.last_draw)
            _, xaxis, yaxis = plot.last_draw
            _, _, width, height = plot._point2ClientCoord(
                (xaxis[0], yaxis[0]), (xaxis[1], yaxis[1]))
            self.assertEqual(plot._scaled_background_bitmap.GetSize(), (int(width), int(height)))
            self.assertNotEqual(previous, plot._scaled_background_bitmap.GetSize())
        finally:
            plot._ySpec = yspec
            self.lib.setVar('graphTexture', texture)

    def test_preferences_pages_keep_window_and_close_button_fixed(self):
        from Resources.PreferencePanel import PreferenceFrame
        from Resources.Widgets import CloseBox
        frame = PreferenceFrame(self.main)
        try:
            frame.Show()
            self.app.Yield()
            def descendants(window):
                for child in window.GetChildren():
                    yield child
                    yield from descendants(child)
            closer = next(child for child in descendants(frame) if isinstance(child, CloseBox) and child.label == 'Close')
            size = frame.GetSize()
            position = closer.GetScreenPosition()
            for index in (1, 2, 3, 4, 0):
                frame.onPageChange(index)
                self.app.Yield()
                self.assertEqual(frame.GetSize(), size)
                self.assertEqual(closer.GetScreenPosition(), position)
                pane = frame.panels[index]
                self.assertGreaterEqual(pane.GetSize().width, pane.GetBestSize().width)
                self.assertGreaterEqual(pane.GetSize().height, pane.GetBestSize().height)
                self.assertLess(pane.GetScreenRect().bottom, closer.GetScreenRect().top)
        finally:
            frame.Destroy()

    def test_documentation_uses_system_colours_in_both_themes(self):
        from Resources import DocFrame
        import wx.stc as stc
        wx = self.wx
        original = wx.SystemSettings.GetColour
        for background, foreground in (('#FAFAFA', '#202020'), ('#202020', '#EEEEEE')):
            def colour(role):
                return wx.Colour({wx.SYS_COLOUR_WINDOW: background,
                                  wx.SYS_COLOUR_WINDOWTEXT: foreground}.get(role, original(role)))
            with patch.object(wx.SystemSettings, 'GetColour', side_effect=colour):
                for frame in (self.main.api_doc_frame, self.main.mod_doc_frame):
                    frame.applySystemTheme()
                    tree = frame.doc_panel.GetTreeCtrl()
                    self.assertEqual(tree.GetBackgroundColour(), wx.Colour(background))
                    page = frame.doc_panel.GetPage(frame.doc_panel.GetSelection())
                    editor = page.win
                    self.assertEqual(editor.StyleGetBackground(stc.STC_STYLE_DEFAULT), wx.Colour(background))
                    self.assertEqual(editor.StyleGetForeground(stc.STC_P_IDENTIFIER), wx.Colour(foreground))
                editor = stc.StyledTextCtrl(self.frame)
                try:
                    DocFrame._ed_set_style_p(editor)
                    self.assertEqual(editor.StyleGetBackground(stc.STC_P_STRING), wx.Colour(background))
                    self.assertEqual(editor.StyleGetForeground(stc.STC_P_IDENTIFIER), wx.Colour(foreground))
                finally:
                    editor.Destroy()
        self.main.api_doc_frame.applySystemTheme()
        self.main.mod_doc_frame.applySystemTheme()

    def test_grapher_hover_does_not_activate_inactive_editor(self):
        graph = self.first.editor.graph.plotter
        event = Mock()
        self.lib.setVar('canGrabFocus', True)
        with patch.object(graph, 'GetTopLevelParent') as top, patch.object(graph, 'SetFocus') as focus:
            top.return_value.IsActive.return_value = False
            graph.OnGrabFocus(event)
            focus.assert_not_called()
            top.return_value.IsActive.return_value = True
            graph.OnGrabFocus(event)
            focus.assert_called_once()
        self.assertEqual(event.Skip.call_count, 2)

    def test_recent_sessions_and_title_follow_saved_session(self):
        path = self.folder / 'My chain.c5chain'
        self.assertTrue(self.lib.saveChainSession(self.frame, str(path)), self.errors)
        self.assertIn(path.name, self.frame.GetTitle())
        self.add()
        self.assertIn(path.name, self.frame.GetTitle())
        self.assertTrue(self.lib.openChainSession(self.frame, str(path)), self.errors)
        self.assertIn(path.name, self.frame.GetTitle())
        self.main.updateTitle()
        self.assertIn(path.name, self.frame.GetTitle())
        for window in (self.main, self.frame):
            items = window.menubar.openRecentSessionMenu.GetMenuItems()
            self.assertEqual(items[0].GetItemLabelText(), str(path))
            self.assertEqual(sum(item.GetItemLabelText() == str(path) for item in items), 1)
        self.assertTrue(self.lib.newChainSession(self.frame))
        self.assertNotIn(path.name, self.frame.GetTitle())

    def test_file_menu_replaces_chain_and_refreshes_recent_menus(self):
        self.add()
        previous = list(self.lib.session.modules)
        with patch.object(self.lib, 'confirmSessionDiscard', return_value=False):
            self.assertFalse(self.main.openModuleFromMenu(str(self.fixture)))
        self.assertEqual(self.lib.session.modules, previous)
        self.assertTrue(self.main.openModuleFromMenu(str(self.fixture)), self.errors)
        self.assertEqual(len(self.lib.session.modules), 1)
        self.assertNotIn(self.lib.session.selected, previous)
        for window in (self.main, self.frame):
            labels = [item.GetItemLabelText() for item in window.menubar.openRecentMenu.GetMenuItems()]
            self.assertIn(str(self.fixture), labels)
        self.main.addingChainModule = True
        try:
            self.assertTrue(self.main.openModuleFromMenu(str(self.fixture)), self.errors)
        finally:
            self.main.addingChainModule = False
        self.assertEqual(len(self.lib.session.modules), 2)

    def add(self, path=None):
        self.assertTrue(self.lib.openCeciliaFile(self.main, str(path or self.fixture)), self.errors)

    def render(self, filename):
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        self.server.server.recordOptions(dur=0.2, filename=str(filename), fileformat=0, sampletype=0)
        self.server.start(timer=False)
        with wave.open(str(filename), 'rb') as stream:
            values = struct.unpack('<' + 'h' * (stream.getnframes() * stream.getnchannels()),
                                   stream.readframes(stream.getnframes()))
        # Offline pyo renders whole buffers; the final buffer may extend the file.
        self.assertGreaterEqual(len(values), 17640)
        self.assertLessEqual(len(values), 17640 + int(self.lib.getVar('bufferSize')) * 2)
        self.server.cleanup_module()
        self.server.shutdown()
        values = values[2048:12000]
        return math.sqrt(sum(x*x for x in values)/len(values))

    def test_serial_audio_duplicate_instances_and_repeat_cleanup(self):
        baseline = self.render(self.folder / 'single.wav')
        self.add()
        second = self.lib.session.modules[1]
        self.assertIsNot(self.first.module_class, second.module_class)
        self.assertIsNot(self.first.state['userSliders'][0], second.state['userSliders'][0])
        chain = self.render(self.folder / 'chain.wav')
        self.assertAlmostEqual(chain / baseline, 0.5, delta=0.02)
        repeated = self.render(self.folder / 'repeated.wav')
        self.assertAlmostEqual(chain, repeated, delta=1)
        self.assertTrue(all(m.state['currentModule'] is None for m in self.lib.session.modules))
        self.assertEqual(self.errors, [])

    def test_editor_switch_while_running_and_hidden_callback_ownership(self):
        self.add()
        second = self.lib.session.modules[1]
        self.server.server.reinit(audio='manual')
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        self.server.start()
        self.ui.playback_state(self.frame, True)
        first_runtime = self.first.state['currentModule']
        self.ui.select(self.frame, second)
        self.ui.show_view(self.frame, 'chain')
        self.assertTrue(second.editor.sliders.IsShown())
        self.assertFalse(second.editor.graph.IsShown())
        self.ui.select(self.frame, second)
        self.first.state['userSliders'][0].sendValue(0.3)
        for _ in range(12):
            self.server.server.process()
        self.assertIs(self.first.state['currentModule'], first_runtime)
        self.assertAlmostEqual(first_runtime._sliders['level'].slider.value, 0.3)
        self.assertAlmostEqual(second.state['currentModule']._sliders['level'].slider.value, 0.5)
        self.assertEqual(second.state['currentModule']._samplers['snd'].mode, 1)
        self.assertIs(self.frame.controlPanel.cfileinList[0], self.first.inputs.cfileinList[0])
        self.assertTrue(self.first.inputs.inputPanel.IsShownOnScreen())
        self.assertGreater(self.first.inputs.inputPanel.GetSize().height, 40)
        self.assertTrue(self.first.inputs.cfileinList[0].IsShownOnScreen())
        self.assertFalse(self.lib.openCeciliaFile(self.frame, str(self.fixture), replace=True))
        self.server.stop()
        self.lib.resetControls()

    def test_editor_selection_preserves_graph_history_and_selected_curve(self):
        self.add()
        second = self.lib.session.modules[1]
        plotter = self.first.editor.graph.plotter
        plotter.addHistory()
        line = plotter.getData()[0]
        before = line.getLineState()
        line.setPoint(0, [0, 0.25])
        plotter.addHistory()
        history = list(plotter._history)
        self.ui.select(self.frame, second)
        self.ui.select(self.frame, self.first)
        self.assertEqual(plotter._history, history)
        self.assertIs(self.frame.grapher.plotter, plotter)
        self.assertIs(plotter.getLine(plotter.getSelected()), line)
        self.assertTrue(plotter.menubarUndo.IsEnabled())
        plotter.undoRedo(1)
        self.assertEqual(line.getLineState(), before)

    def test_recording_gain_and_spectrum_use_the_final_signal(self):
        baseline = self.render(self.folder / 'baseline.wav')
        self.add()
        self.server.shutdown()
        self.server.server.reinit(audio='manual')
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        recorded = self.folder / 'recorded.wav'
        self.lib.setVar('outputFile', str(recorded))
        self.lib.setVar('audioFileType', 'wav')
        self.lib.setVar('sampSize', 0)
        self.lib.setVar('showSpectrum', 1)
        self.server.setAmp(-6)
        try:
            self.server.start(rec=True)
            self.assertIs(self.server.specamp.mul, self.server.output)
            for _ in range(20):
                self.server.server.process()
            self.server.stop()
        finally:
            self.lib.setVar('showSpectrum', 0)
        with wave.open(str(recorded), 'rb') as stream:
            self.assertEqual(stream.getnchannels(), 2)
            values = struct.unpack('<' + 'h' * (stream.getnframes() * stream.getnchannels()),
                                   stream.readframes(stream.getnframes()))[2048:12000]
        self.assertTrue(values)
        recorded_rms = math.sqrt(sum(x*x for x in values)/len(values))
        self.assertAlmostEqual(recorded_rms / baseline, 0.5 * 10**(-6/20), delta=0.02)
        self.assertEqual(self.errors, [])

    def test_presets_do_not_replace_session_output_or_other_instances(self):
        from Resources.Session import instance_context
        self.add()
        second = self.lib.session.modules[1]
        with instance_context(second):
            data = self.lib.capturePresetData()
            data['totalTime'] = 17
            data['gainSlider'] = -12
            data['nchnls'] = 1
            self.lib.restorePresetData(data, 'saved')
        self.assertEqual(self.lib.getVar('totalTime'), 0.2)
        self.assertEqual(self.lib.getVar('nchnls'), 2)
        self.assertEqual(self.lib.getVar('gainSlider').GetValue(), 0)
        self.assertEqual(self.first.inputs.cfileinList[0].filePath, str(self.source))
        self.assertEqual(self.errors, [])

    def test_single_module_legacy_presets_restore_input_and_output(self):
        from Resources.Session import instance_context
        with instance_context(self.first):
            data = self.lib.capturePresetData()
        data['totalTime'] = 0.35
        data['nchnls'] = 1
        data['gainSlider'] = -3
        source = self.fixture.read_text() + '\nCECILIA_PRESETS = ' + repr({'Example': data}) + '\n'
        self.fixture.write_text(source)
        self.assertTrue(self.lib.openCeciliaFile(self.frame, str(self.fixture), replace=True), self.errors)
        selected = self.lib.session.selected
        self.assertIn('Example', selected.state['presetPanel'].getPresets())
        with instance_context(selected):
            self.lib.loadPresetFromFile('Example')
        self.app.Yield()
        self.assertEqual(self.lib.getVar('totalTime'), 0.35)
        self.assertEqual(self.lib.getVar('nchnls'), 1)
        self.assertEqual(self.lib.getVar('gainSlider').GetValue(), -3)
        self.assertEqual(selected.inputs.cfileinList[0].filePath, str(self.source))
        self.assertEqual(self.fixture.read_text(), source)
        self.assertEqual(self.errors, [])

    def test_runtime_failure_cleans_partial_chain_and_preserves_editors(self):
        broken = self.folder / 'broken.c5'
        broken.write_text(self.fixture.read_text().replace(
            'self.out = self.addSampler("snd") * self.level',
            'raise RuntimeError("deliberate stage failure")'))
        self.add(broken)
        snapshot = self.lib.captureSession()
        self.assertFalse(self.server.loadChain())
        self.assertTrue(all(module.state['currentModule'] is None for module in self.lib.session.modules))
        self.assertIsNone(self.server.output)
        self.assertEqual(self.lib.captureSession(), snapshot)
        self.assertIn('stage 2', self.errors[-1][1])

    def test_first_only_module_offers_insertion_and_preserves_chain(self):
        self.add()
        previous = list(self.lib.session.modules)
        first_only = self.folder / 'table.c5'
        first_only.write_text(
            'class Module(BaseModule):\n'
            '    def __init__(self):\n'
            '        BaseModule.__init__(self)\n'
            '        self.table = self.addFilein("snd")\n'
            '        self.out = TableRead(self.table, freq=self.table.getRate()).play()\n'
            'Interface = [cfilein(name="snd")]\n')
        snapshot = self.lib.captureSession()
        with patch.object(self.lib, 'confirmFirstStageInsertion', return_value=False) as offer:
            self.assertFalse(self.lib.openCeciliaFile(self.frame, str(first_only)))
            offer.assert_called_once()
        self.assertEqual(self.lib.captureSession(), snapshot)
        with patch.object(self.lib, 'confirmFirstStageInsertion', return_value=True) as offer:
            self.assertTrue(self.lib.openCeciliaFile(self.frame, str(first_only)), self.errors)
            offer.assert_called_once()
        self.assertEqual(self.lib.session.modules[1:], previous)
        inserted = self.lib.session.modules[0]
        self.assertIs(self.lib.session.selected, inserted)
        self.assertEqual(inserted.inputs.cfileinList[0].filePath, str(self.source))
        self.assertTrue(self.server.loadChain(), self.errors)
        # Replacement targets the first stage even when a downstream editor is selected.
        self.ui.select(self.frame, previous[-1])
        replacement = self.folder / 'replacement_table.c5'
        replacement.write_text(first_only.read_text())
        snapshot = self.lib.captureSession()
        with patch.object(self.lib, 'confirmFirstStageReplacement', return_value=False) as offer:
            self.assertFalse(self.lib.openCeciliaFile(self.frame, str(replacement)))
            offer.assert_called_once()
        self.assertEqual(self.lib.captureSession(), snapshot)
        with patch.object(self.lib, 'confirmFirstStageReplacement', return_value=True) as offer:
            self.assertTrue(self.lib.openCeciliaFile(self.frame, str(replacement)), self.errors)
            offer.assert_called_once()
        self.assertEqual(self.lib.session.modules[1:], previous)
        replaced = self.lib.session.modules[0]
        self.assertEqual(replaced.path, str(replacement))
        self.assertIs(self.lib.session.selected, replaced)
        self.assertTrue(inserted.retired)
        self.assertEqual(replaced.inputs.cfileinList[0].filePath, str(self.source))
        self.assertTrue(self.server.loadChain(), self.errors)
        self.assertEqual(self.errors, [])

    def test_malformed_effect_settings_roll_back_shared_output(self):
        self.add()
        path = self.folder / 'session.c5chain'
        self.assertTrue(self.lib.saveChainSession(self.frame, str(path)), self.errors)
        snapshot = self.lib.captureSession()
        document = json.loads(path.read_text())
        document['output']['totalTime'] = 3.25
        document['output']['gainSlider'] = -12
        document['output']['plugins']['0'] = ['Filter', [], [[0, 0, None]] * 3]
        path.write_text(json.dumps(document))
        self.assertFalse(self.lib.openChainSession(self.frame, str(path)))
        self.app.Yield()
        self.assertEqual(self.lib.captureSession(), snapshot)

    def test_frequency_shift_uses_equal_power_voice_gains(self):
        self.first.state['userSliders'][0].entryReturn(1.0)
        baseline = self.render(self.folder / 'unshifted.wav')
        self.add(Path(self.lib.MODULES_PATH) / 'Pitch' / 'FreqShift.c5')
        shifted = self.render(self.folder / 'shifted.wav')
        self.assertAlmostEqual(shifted / baseline, 0.707, delta=0.025)
        self.assertEqual(self.errors, [])

    def test_shipped_stream_modules_use_upstream_and_shared_duration(self):
        self.add(Path(self.lib.MODULES_PATH) / 'Dynamics' / 'Degrade.c5')
        self.add(Path(self.lib.MODULES_PATH) / 'Filters' / 'StateVar.c5')
        self.assertTrue(self.server.loadChain(), self.errors)
        for module in self.lib.session.modules:
            self.assertEqual(module.state['currentModule'].totalTime, 0.2)
        for module in self.lib.session.modules[1:]:
            self.assertEqual(module.state['currentModule']._samplers[module.primary_input].mode, 1)
            self.assertIsNotNone(module.upstream)
        self.assertEqual(self.errors, [])

    def test_session_round_trip_missing_assets_and_failed_append(self):
        self.add()
        path = self.folder / 'session.c5chain'
        self.assertTrue(self.lib.saveChainSession(self.frame, str(path)), self.errors)
        snapshot = self.lib.captureSession()
        self.assertTrue(self.lib.openChainSession(self.frame, str(path)), self.errors)
        self.app.Yield()
        self.assertEqual(self.lib.captureSession(), snapshot)

        invalid = self.folder / 'invalid.c5'
        invalid.write_text('invalid syntax!')
        self.assertFalse(self.lib.openCeciliaFile(self.frame, str(invalid)))
        self.assertEqual(self.lib.captureSession(), snapshot)
        document = json.loads(path.read_text())
        document['modules'][0]['settings']['userInputs']['snd']['path'] = 'missing.wav'
        path.write_text(json.dumps(document))
        self.assertFalse(self.lib.openChainSession(self.frame, str(path)))
        self.assertEqual(self.lib.captureSession(), snapshot)

    def test_session_round_trip_generator_lists_and_osc_bindings(self):
        self.fixture.write_text(self.fixture.read_text() +
                               '\nInterface += [cgen(name="partials", init=[1, 0.5, 0.25], rate="i"), '
                               'crange(name="band", min=0, max=1, init=[0.2, 0.8], rel="lin")]\n')
        self.assertTrue(self.lib.openCeciliaFile(self.frame, str(self.fixture), replace=True), self.errors)
        selected = self.lib.session.selected
        slider, ranged = selected.state['userSliders']
        slider.setOpenSndCtrl((9000, '/level'))
        slider.setOSCOut(('127.0.0.1', 9001, '/level'))
        ranged.setOpenSndCtrl((9000, '/band'), 'left')
        ranged.setOSCOut(('127.0.0.1', 9001, '/band'), 'left')
        generator = next(widget for widget in selected.state['userTogglePopups'] if widget.name == 'partials')
        generator.setValue([1, 0.3, 0.125])
        self.assertEqual(generator.getValue(), [1, 0.3, 0.125])
        self.assertIsInstance(generator.entry.getValue(), str)
        path = self.folder / 'lists.c5chain'
        self.assertTrue(self.lib.saveChainSession(self.frame, str(path)), self.errors)
        snapshot = self.lib.captureSession()
        self.assertTrue(self.lib.openChainSession(self.frame, str(path)), self.errors)
        # Capture before repaint: restoring list values must not depend on OnPaint.
        self.assertEqual(self.lib.captureSession(), snapshot)
        self.app.Yield()
        self.assertEqual(self.lib.captureSession(), snapshot)
        self.assertEqual(self.errors, [])

    def test_shared_effects_follow_final_stage_and_survive_first_stage_changes(self):
        self.add()
        second = self.lib.session.modules[1]
        self.frame.controlPanel.replacePlugin(0, 'Filter')
        self.app.Yield()
        knobs = self.lib.getVar('plugins')[0].getKnobs()
        names = {knob.getName() for knob in knobs}
        first_lines = [line for line in self.first.editor.graph.plotter.getData() if line.getName() in names]
        self.assertEqual(len(first_lines), 3)
        self.assertFalse(any(line.getName() in names for line in second.editor.graph.plotter.getData()))
        original_states = [line.getLineState() for line in first_lines]
        self.lib.moveChainModule(second, -1)
        self.assertEqual([line.getLineState() for line in second.editor.graph.plotter.getData()
                          if line.getName() in names], original_states)
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        self.assertIs(self.server.pluginObjs[0].input.value, self.server.out)
        self.assertIs(self.server.output.value, self.server.pluginObjs[-1].out)
        self.server.cleanup_module()
        self.server.shutdown()
        path = self.folder / 'effects.c5chain'
        self.assertTrue(self.lib.saveChainSession(self.frame, str(path)), self.errors)
        snapshot = self.lib.captureSession()
        self.assertTrue(self.lib.openChainSession(self.frame, str(path)), self.errors)
        self.app.Yield()
        self.assertEqual(self.lib.captureSession(), snapshot)
        self.assertEqual(self.errors, [])

    def test_builtin_modules_compile_and_declare_safe_downstream_inputs(self):
        compatible = 0
        for path in Path(self.lib.MODULES_PATH).rglob('*.c5'):
            candidate = self.server.compileModule(str(path), builtin=True)
            if candidate.metadata is not None:
                self.assertIsNotNone(candidate.primary_input, str(path))
                compatible += 1
        self.assertGreater(compatible, 30)
    def test_reorder_remove_reload_and_auxiliary_assets(self):
        self.add()
        second = self.lib.session.modules[1]
        self.lib.moveChainModule(second, -1)
        self.assertIs(self.lib.session.modules[0], second)
        self.assertEqual(second.inputs.cfileinList[0].filePath, str(self.source))
        self.assertTrue(self.lib.openCeciliaFile(self.frame, str(self.fixture), replace=True), self.errors)
        self.assertEqual(len(self.lib.session.modules), 2)
        auxiliary = self.folder / 'auxiliary.c5'
        auxiliary.write_text(
            'class Module(BaseModule):\n'
            '    def __init__(self):\n'
            '        BaseModule.__init__(self)\n'
            '        self.asset = self.addFilein("impulse")\n'
            '        self.out = self.addSampler("snd")\n'
            'Interface = [csampler(name="snd"), cfilein(name="impulse")]\n'
            'Chain = {"primary_input": "snd", "auxiliary_inputs": ["impulse"]}\n'
        )
        self.add(auxiliary)
        stage = self.lib.session.modules[-1]
        stage.inputs.getCfileinFromName('impulse').onLoadFile(str(self.source))
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        self.server.cleanup_module()
        self.server.shutdown()
        self.lib.removeChainModule(stage)
        for module in list(self.lib.session.modules):
            self.lib.removeChainModule(module)
        self.assertEqual(self.lib.session.modules, [])
        self.assertEqual(self.lib.session.view, 'chain')
        for action in (self.main.reloadCurrentModule, self.main.openModuleAsText,
                       self.main.onSaveAs, self.main.onModuleAbout, self.main.onBounceToDisk):
            action(None)
        self.app.Yield()
        self.assertEqual(self.errors, [])


if __name__ == '__main__':
    unittest.main()
