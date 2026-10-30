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
        self.exception_patch = patch('sys.excepthook', side_effect=lambda kind, value, tb:
            self.errors.append(('Unhandled GUI callback', str(value), ''.join(traceback.format_exception(kind, value, tb)))))
        self.exception_patch.start()
        self.error_patch = patch.object(self.lib, 'showErrorDialog', side_effect=lambda title, message: self.errors.append((title, message, traceback.format_exc())))
        self.error_patch.start()
        self.discard_patch = patch.object(self.lib, 'confirmSessionDiscard', return_value=True)
        self.discard_patch.start()
        self.lib.session.clear()
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
        self.lib.session.clear()
        self.lib.session.selected_id = None
        self.app.Yield()
        self.error_patch.stop()
        self.discard_patch.stop()
        self.exception_patch.stop()

    def test_popup_text_fields_use_centered_native_editor_heights(self):
        from Resources.Widgets import ListEntryPopupFrame, OSCPopupFrame, BatchPopupFrame
        controls = [ListEntryPopupFrame(self.frame, '1, 2'),
                    OSCPopupFrame(self.frame, self.first.state['userSliders'][0]),
                    BatchPopupFrame(self.frame, Mock())]
        for popup in controls:
            self.addCleanup(lambda popup=popup: popup.Destroy() if popup else None)
            popup.Show()
            self.app.Yield()
            entries = [popup.entry]
            if hasattr(popup, 'entry2'):
                entries.append(popup.entry2)
            for entry in entries:
                with self.subTest(popup=type(popup).__name__):
                    field = entry.GetParent()
                    top = entry.GetPosition().y
                    bottom = field.GetClientSize().height - top - entry.GetSize().height
                    self.assertLessEqual(abs(top - bottom), 1)
                    self.assertGreaterEqual(top, 2)
                    self.assertGreaterEqual(entry.GetClientSize().height, entry.GetTextExtent('Ag').height)
                    self.assertEqual(entry.GetBackgroundColour(), field.GetBackgroundColour())
                    position = field.GetPosition()
                    self.assertLessEqual(position.y + field.GetSize().height, popup.GetClientSize().height)
                    entry.ChangeValue('test:123')
                    self.assertEqual(entry.GetValue(), 'test:123')
        batch = controls[-1]
        callback = batch.outFunction
        batch.entry.SetValue(' suffix ')
        batch.OnApply()
        self.app.Yield()
        callback.assert_called_once_with('suffix')
        self.assertEqual(self.errors, [])

    def test_entry_edits_survive_slider_repaints_and_commit_values(self):
        self.fixture.write_text(self.fixture.read_text() +
            '\nInterface += [crange(name="band", min=0, max=1, init=[0.2, 0.8], rel="lin"), '
            'csplitter(name="splits", min=0, max=1, init=[0.1, 0.4, 0.9], rel="lin")]\n')
        self.assertTrue(self.lib.openCeciliaFile(self.frame, str(self.fixture), replace=True), self.errors)
        self.app.Yield()
        controls = self.lib.session.selected.state['userSliders']
        self.assertEqual(len(controls), 3)
        for control, text, expected in zip(controls,
                ['0.75', '0.3,0.7', '0.2,0.5,0.8'], [.75, [.3, .7], [.2, .5, .8]]):
            with self.subTest(control=control.name):
                entry = control.entryUnit
                click = Mock()
                click.GetPosition.return_value = self.wx.Point(entry.entryRect.x + entry.entryRect.width // 2,
                                                              entry.entryRect.y + entry.entryRect.height // 2)
                entry.MouseDown(click)
                entry.MouseUp(click)
                self.app.Yield()
                self.assertTrue(entry.HasFocus())
                self.assertTrue(entry.selected)
                for char in text:
                    key = Mock()
                    key.GetKeyCode.return_value = ord(char)
                    entry.onChar(key)
                typed = entry.new
                with patch.object(control, 'sendValue', wraps=control.sendValue) as send:
                    for _ in range(3):
                        control.slider.Refresh()
                        control.slider.Update()
                        self.frame.Refresh()
                        self.app.Yield()
                    send.assert_not_called()
                self.assertTrue(entry.selected)
                self.assertEqual(entry.new, typed)
                # A redundant programmatic value update also leaves editing intact.
                control.slider.SetValue(control.slider.GetValue())
                self.app.Yield()
                self.assertTrue(entry.selected)
                self.assertEqual(entry.new, typed)
                key = Mock()
                key.GetKeyCode.return_value = self.wx.WXK_RETURN
                entry.onChar(key)
                self.app.Yield()
                self.assertFalse(entry.selected)
                self.assertEqual(control.getValue(), expected)
                self.assertEqual(entry.value, expected)
        self.assertEqual(self.errors, [])

    def test_slider_mouse_changes_deliver_values_without_paint(self):
        control = self.first.state['userSliders'][0]
        slider = control.slider
        press = Mock()
        press.GetPosition.return_value = self.wx.Point(slider.GetSize().width - 20, 8)
        with patch.object(control, 'sendValue', wraps=control.sendValue) as send, \
                patch.object(slider, 'Refresh'):
            slider.MouseDown(press)
            slider.MouseUp(press)
            self.app.Yield()
            send.assert_called_once_with(slider.GetValue())
            self.assertAlmostEqual(control.entryUnit.value, slider.GetValue(), places=5)
        self.assertEqual(self.errors, [])

    def test_duration_drag_keeps_capture_across_redraws(self):
        slider = self.frame.controlPanel.durationSlider
        event = Mock()
        event.ShiftDown.return_value = False
        width = slider.GetSize().width
        try:
            event.GetPosition.return_value = self.wx.Point(width // 3, 5)
            slider.MouseDown(event)
            for x in (width // 3, width // 2, width - 20):
                event.GetPosition.return_value = self.wx.Point(x, 5)
                slider.MouseMotion(event)
                slider.Refresh()
                slider.Update()
                self.app.Yield()
                self.assertTrue(slider.HasCapture())
                self.assertAlmostEqual(self.lib.getVar('totalTime'), slider.GetValue())
                self.assertAlmostEqual(self.first.editor.graph.plotter.getTotalTime(), slider.GetValue())
        finally:
            slider.MouseUp(event)
        self.assertFalse(slider.HasCapture())
        self.lib.setVar('totalTime', 12.5)
        self.app.Yield()
        self.assertAlmostEqual(slider.GetValue(), 12.5)
        self.assertEqual(self.errors, [])

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
        previous = self.lib.session.modules[-1] if self.lib.session.modules else None
        self.assertTrue(self.lib.openCeciliaFile(self.main, str(path or self.fixture)), self.errors)
        # Existing serial audio tests explicitly wire each newly added node.
        if previous:
            current = self.lib.session.selected
            self.lib.session.connect(previous.id, current.id)
            if previous.id in self.lib.session.output_connections:
                self.lib.session.disconnect(previous.id)
            self.lib.session.connect(current.id)


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

    def add_unconnected(self, path=None):
        self.assertTrue(self.lib.openCeciliaFile(self.main, str(path or self.fixture)), self.errors)
        node = self.lib.session.selected
        self.assertFalse(any(node.id in edge for edge in self.lib.session.connections))
        self.assertNotIn(node.id, self.lib.session.output_connections)
        return node

    def branch_graph(self):
        left, right, merge = [self.add_unconnected() for _ in range(3)]
        graph = self.lib.session
        graph.disconnect(self.first.id)
        for a, b in [(self.first, left), (self.first, right), (left, merge), (right, merge)]:
            graph.connect(a.id, b.id)
        graph.connect(merge.id)
        return left, right, merge

    def two_sources(self):
        second = self.add_unconnected()
        self.frame.grid.change_source(second, True)
        second.inputs.cfileinList[0].onLoadFile(str(self.source))
        return second

    def test_multiple_source_audio_inputs_selection_and_persistence(self):
        baseline = self.render(self.folder / 'baseline.wav')
        second = self.two_sources()
        graph = self.lib.session
        widget = second.inputs.cfileinList[0]
        self.assertIs(graph.source, second)
        self.assertEqual(self.frame.controlPanel.cfileinList, second.inputs.cfileinList)
        widget.onChangeMode(1)
        self.assertEqual(second.state['userInputs']['snd']['mode'], 1)
        self.assertEqual(self.first.state['userInputs']['snd']['mode'], 0)
        widget.onChangeMode(0)
        graph.connect(second.id)
        mixed = self.render(self.folder / 'mixed-sources.wav')
        self.assertAlmostEqual(mixed / baseline, 2 * .707, delta=.03)
        processor = self.add_unconnected()
        self.assertIs(graph.source, second)
        self.assertTrue(second.inputs.inputPanel.IsShown())
        self.assertFalse(self.first.inputs.inputPanel.IsShown())
        self.assertEqual(self.frame.controlPanel.cfileinList, second.inputs.cfileinList)
        self.ui.select(self.frame, self.first)
        self.assertIs(graph.source, self.first)
        self.ui.select(self.frame, processor)
        self.assertIs(graph.source, self.first)
        self.assertEqual(self.frame.controlPanel.cfileinList, self.first.inputs.cfileinList)
        path = self.folder / 'sources.c5chain'
        self.assertTrue(self.lib.saveChainSession(self.frame, str(path)), self.errors)
        snapshot = self.lib.captureSession()
        self.assertTrue(self.lib.openChainSession(self.frame, str(path)), self.errors)
        self.assertEqual(self.lib.captureSession(), snapshot)
        self.assertEqual(self.lib.session.source_id, self.first.id)
        self.assertEqual(self.lib.session.selected_id, processor.id)
        self.assertEqual(self.errors, [])

    def test_effects_survive_inactive_and_removed_first_source(self):
        self.add_unconnected()  # Effects may be hosted by an inactive processor after removal.
        second = self.two_sources()
        graph = self.lib.session
        graph.disconnect(self.first.id)
        graph.connect(second.id)
        self.frame.controlPanel.replacePlugin(0, 'Filter')
        self.app.Yield()
        before = self.lib.captureSession()['output']
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        self.assertIsNone(self.first.state['currentModule'])
        self.assertIsNotNone(second.state['currentModule'])
        self.assertIs(self.server.pluginObjs[0].input.value, self.server.out)
        self.server.cleanup_module()
        self.server.shutdown()
        self.lib.removeChainModule(self.first)
        self.assertIs(graph.source, second)
        self.assertEqual(self.lib.captureSession()['output'], before)
        self.assertEqual(self.frame.controlPanel.cfileinList, second.inputs.cfileinList)
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        self.server.cleanup_module()
        self.server.shutdown()
        self.assertEqual(self.errors, [])

    def test_selected_source_controls_batch_files_and_duration(self):
        second = self.two_sources()
        other = self.folder / 'alternate.wav'
        with wave.open(str(other), 'wb') as stream:
            stream.setnchannels(2)
            stream.setsampwidth(2)
            stream.setframerate(44100)
            stream.writeframes(b'\0\0\0\0' * 11025)
        second.inputs.cfileinList[0].onLoadFile(str(other))
        self.lib.session.connect(second.id)
        processor = self.add_unconnected()
        self.assertIs(self.lib.session.source, second)
        initial_path = self.first.inputs.cfileinList[0].filePath
        initial_duration = self.lib.getVar('totalTime')
        self.lib.setVar('useSoundDur', 1)
        progress = Mock()
        progress.Update.return_value = (True, False)
        rendered = []
        def render(filename):
            rendered.append((self.first.inputs.cfileinList[0].filePath,
                             second.inputs.cfileinList[0].filePath, self.lib.getVar('totalTime')))
        with patch.object(self.wx, 'ProgressDialog', return_value=progress), \
                patch.object(self.frame.controlPanel, 'onBatchProcessing', side_effect=render), \
                patch.object(processor.editor.presets, 'getPresets', return_value=['init', 'one']), \
                patch.object(self.lib, 'loadPresetFromFile'):
            self.main.applyBatchProcessingPreset('source-presets')
            self.assertEqual(rendered[0][0], initial_path)
            self.assertEqual(rendered[0][1], str(other))
            self.assertAlmostEqual(rendered[0][2], .25)
            self.assertEqual(self.lib.getVar('totalTime'), initial_duration)
            rendered.clear()
            self.main.applyBatchProcessingFolder('source-folder')
        self.assertTrue(rendered)
        for first_path, second_path, duration in rendered:
            self.assertEqual(first_path, initial_path)
            self.assertAlmostEqual(duration, .25 if second_path == str(other) else .5)
        self.assertEqual(self.lib.getVar('totalTime'), initial_duration)
        self.assertIs(self.lib.session.source, second)
        self.lib.setVar('useSoundDur', 0)
        self.assertEqual(self.errors, [])

    def test_live_mute_and_history_leave_audio_running(self):
        effect = self.add_unconnected()
        graph, canvas = self.lib.session, self.frame.grid
        graph.disconnect(self.first.id)
        graph.connect(self.first.id, effect.id)
        graph.connect(effect.id)
        graph.set_muted(effect, True)
        self.server.server.reinit(audio='manual')
        self.lib.setVar('audioHostAPI', 'manual')
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        self.server.start(timer=False)
        self.ui.playback_state(self.frame, True)
        graph.history.clear()
        output, runtime = self.server.out, list(self.server.runtimeModules)
        for muted in (False, True, False):
            canvas.toggle_mute(effect)
            for _ in range(8):
                self.server.server.process()
            self.assertTrue(self.server.isAudioServerRunning())
            self.assertEqual(effect.id in graph.muted_ids, muted)
            self.assertEqual(self.server.moduleMuteSignals[effect.id].value, int(muted))
            self.assertIs(self.server.out, output)
            self.assertEqual(self.server.runtimeModules, runtime)
        graph.history.step()
        self.assertTrue(self.server.isAudioServerRunning())
        self.assertIn(effect.id, graph.muted_ids)
        graph.history.step(redo=True)
        self.assertTrue(self.server.isAudioServerRunning())
        self.assertNotIn(effect.id, graph.muted_ids)
        self.ui.show_view(self.frame, 'chain')
        self.app.Yield()
        graph.history.clear()
        rect = canvas.rects[effect.id]
        original = list(graph.positions[effect.id])

        def event(point):
            mock = Mock()
            mock.GetPosition.return_value = self.wx.Point(*canvas.CalcScrolledPosition(*point))
            mock.ShiftDown.return_value = False
            return mock

        canvas.press(event((rect.x - 20, rect.y - 20)))
        canvas.motion(event((rect.x + 180, rect.y + 100)))
        canvas.release(event((rect.x + 180, rect.y + 100)))
        self.assertEqual(canvas.selected_nodes, {effect.id})
        canvas.press(event((rect.x + 30, rect.y + 20)))
        canvas.motion(event((rect.x + 90, rect.y + 60)))
        canvas.release(event((rect.x + 90, rect.y + 60)))
        self.assertEqual(graph.positions[effect.id], [original[0] + 60, original[1] + 40])
        graph.history.step()
        self.assertEqual(graph.positions[effect.id], original)
        graph.history.step(redo=True)
        self.assertEqual(graph.positions[effect.id], [original[0] + 60, original[1] + 40])
        self.assertTrue(self.server.isAudioServerRunning())
        self.assertIs(self.server.out, output)
        self.assertEqual(self.server.runtimeModules, runtime)
        self.assertEqual(self.errors, [])

    def test_muted_sole_output_processor_passes_through_and_undo_restores_effect(self):
        baseline = self.render(self.folder / 'mute-baseline.wav')
        effect = self.add_unconnected()
        graph, canvas = self.lib.session, self.frame.grid
        graph.disconnect(self.first.id)
        graph.connect(self.first.id, effect.id)
        graph.connect(effect.id)
        processed = self.render(self.folder / 'mute-processed.wav')
        graph.history.clear()
        canvas.toggle_mute(effect)
        self.assertIn(effect.id, graph.muted_ids)
        bypassed = self.render(self.folder / 'mute-bypassed.wav')
        self.assertAlmostEqual(bypassed / baseline, 1, delta=.02)
        self.assertAlmostEqual(processed / baseline, .5, delta=.02)
        graph.history.step()
        self.assertNotIn(effect.id, graph.muted_ids)
        graph.history.step(redo=True)
        self.assertIn(effect.id, graph.muted_ids)
        self.assertEqual(self.errors, [])

    def test_branching_audio_mix_levels_and_inactive_module(self):
        baseline = self.render(self.folder / 'baseline.wav')
        left, right, merge = self.branch_graph()
        broken = self.folder / 'inactive.c5'
        broken.write_text(self.fixture.read_text().replace(
            'self.out = self.addSampler("snd") * self.level',
            'raise RuntimeError("inactive node must not be built")'))
        inactive = self.add_unconnected(broken)
        merged = self.render(self.folder / 'merged.wav')
        self.assertAlmostEqual(merged / baseline, .3535, delta=.02)
        self.lib.session.connect(left.id)
        mixed = self.render(self.folder / 'mixed.wav')
        self.assertAlmostEqual(mixed / baseline, (.3535 + .5) * .707, delta=.02)
        self.lib.session.connect(self.first.id)
        three = self.render(self.folder / 'three.wav')
        self.assertAlmostEqual(three / baseline, (1 + .3535 + .5) * .707, delta=.02)
        self.assertIsNone(inactive.state['currentModule'])
        self.assertEqual(self.errors, [])

    def test_drag_compatible_source_into_processing_area(self):
        graph, canvas = self.lib.session, self.frame.grid
        self.ui.show_view(self.frame, 'chain')
        self.app.Yield()
        def event(point):
            mock = Mock()
            mock.GetPosition.return_value = self.wx.Point(*canvas.CalcScrolledPosition(*point))
            return mock
        def move(module, x):
            rect = canvas.rects[module.id]
            canvas.press(event((rect.x + 40, rect.y + 20)))
            canvas.motion(event((x + 40, 140)))
            canvas.release(event((x + 40, 140)))
        move(self.first, 300)
        self.assertIn(self.first.id, graph.source_ids)
        second = self.two_sources()
        self.ui.show_view(self.frame, 'chain')
        self.app.Yield()
        move(self.first, 100)
        self.assertIn(self.first.id, graph.source_ids)
        original_outputs = list(graph.output_connections)
        self.ui.playback_state(self.frame, True)
        move(self.first, 300)
        self.assertIn(self.first.id, graph.source_ids)
        self.lib.resetControls()
        move(self.first, 300)
        self.assertNotIn(self.first.id, graph.source_ids)
        self.assertIs(graph.source, second)
        self.assertEqual(graph.output_connections, original_outputs)
        self.assertEqual(graph.positions[self.first.id], [300, 120])
        self.assertGreater(canvas.rects[self.first.id].x, canvas.SOURCE_DIVIDER_X)
        self.assertEqual(self.frame.controlPanel.cfileinList, second.inputs.cfileinList)
        self.assertFalse(self.first.inputs.cfileinList[0].IsEnabled())
        graph.connect(second.id, self.first.id)
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        self.server.cleanup_module()
        self.server.shutdown()
        source_only = self.folder / 'generator.c5'
        source_only.write_text('class Module(BaseModule):\n'
            '    def __init__(self):\n'
            '        BaseModule.__init__(self)\n'
            '        self.out = Sig(0)\n'
            'Interface = []\n')
        self.assertTrue(self.lib.openCeciliaFile(self.frame, str(source_only)), self.errors)
        generator = graph.selected
        self.ui.show_view(self.frame, 'chain')
        self.app.Yield()
        move(generator, 450)
        self.assertIn(generator.id, graph.source_ids)
        self.assertEqual(canvas.rects[generator.id].x, 24)
        self.assertEqual(self.errors, [])

    def test_marquee_group_move_and_undo(self):
        first, second = self.add_unconnected(), self.add_unconnected()
        graph, canvas = self.lib.session, self.frame.grid
        self.ui.show_view(self.frame, 'chain')
        self.app.Yield()
        graph.positions[first.id] = [280, 150]
        graph.positions[second.id] = [490, 275]
        canvas.rebuild()

        def event(point):
            mock = Mock()
            mock.GetPosition.return_value = self.wx.Point(*canvas.CalcScrolledPosition(*point))
            mock.ShiftDown.return_value = False
            return mock

        canvas.press(event((260, 130)))
        canvas.motion(event((670, 375)))
        canvas.release(event((670, 375)))
        self.assertEqual(canvas.selected_nodes, {first.id, second.id})
        canvas.press(event((300, 170)))
        canvas.motion(event((360, 210)))
        canvas.release(event((360, 210)))
        self.assertEqual(graph.positions[first.id], [340, 190])
        self.assertEqual(graph.positions[second.id], [550, 315])
        self.assertFalse(canvas.HasCapture())
        graph.history.step()
        self.assertEqual(graph.positions[first.id], [280, 150])
        self.assertEqual(graph.positions[second.id], [490, 275])
        graph.history.step(redo=True)
        self.assertEqual(graph.positions[first.id], [340, 190])
        self.assertEqual(graph.positions[second.id], [550, 315])
        self.assertEqual(self.errors, [])

    def test_canvas_connections_positions_and_playback_lock(self):
        node = self.add_unconnected()
        graph, canvas = self.lib.session, self.frame.grid
        self.ui.show_view(self.frame, 'chain')
        self.app.Yield()
        def event(point):
            mock = Mock()
            mock.GetPosition.return_value = self.wx.Point(*canvas.CalcScrolledPosition(*point))
            return mock
        canvas.press(event(canvas.port(self.first.id, True)))
        canvas.release(event(canvas.port(self.first.id, True)))
        self.assertFalse(canvas.HasCapture())
        canvas.motion(event(canvas.port(node.id, False)))
        self.assertNotIn([self.first.id, node.id], graph.connections)
        canvas.release(event(canvas.port(node.id, False)))
        self.assertNotIn([self.first.id, node.id], graph.connections)
        canvas.press(event(canvas.port(node.id, False)))
        canvas.release(event(canvas.port(node.id, False)))
        self.assertIn([self.first.id, node.id], graph.connections)
        canvas.press(event(canvas.port(node.id, True)))
        canvas.release(event(canvas.port(node.id, True)))
        canvas.motion(event(canvas.port(None, False)))
        canvas.press(event(canvas.port(None, False)))
        canvas.release(event(canvas.port(None, False)))
        self.assertIn(node.id, graph.output_connections)
        canvas.press(event(canvas.port(node.id, True)))
        canvas.release(event(canvas.port(node.id, True)))
        cancel = Mock()
        cancel.GetKeyCode.return_value = self.wx.WXK_ESCAPE
        canvas.key(cancel)
        self.assertIsNone(canvas.drag)
        canvas.press(event(canvas.port(node.id, True)))
        canvas.release(event(canvas.port(node.id, True)))
        canvas.press(event((20, 300)))
        self.assertIsNone(canvas.drag)
        rect = canvas.rects[node.id]
        canvas.press(event((rect.x + 40, rect.y + 20)))
        canvas.motion(event((rect.x + 100, rect.y + 80)))
        canvas.release(event((rect.x + 100, rect.y + 80)))
        position = list(graph.positions[node.id])
        self.assertEqual(position, [rect.x + 60, rect.y + 60])
        self.ui.playback_state(self.frame, True)
        canvas.selected_edge = (self.first.id, node.id)
        key = Mock()
        key.GetKeyCode.return_value = self.wx.WXK_DELETE
        canvas.key(key)
        self.assertIn([self.first.id, node.id], graph.connections)
        self.lib.resetControls()
        canvas.key(key)
        self.assertNotIn([self.first.id, node.id], graph.connections)
        path = self.folder / 'position.c5chain'
        self.assertTrue(self.lib.saveChainSession(self.frame, str(path)))
        self.assertTrue(self.lib.openChainSession(self.frame, str(path)))
        self.assertEqual(self.lib.session.positions[node.id], position)
        self.assertEqual(self.errors, [])

    def test_canvas_delete_selection_is_one_undo_action(self):
        first, second = self.add_unconnected(), self.add_unconnected()
        graph, canvas = self.lib.session, self.frame.grid
        graph.connect(self.first.id, first.id)
        graph.connect(first.id, second.id)
        graph.connect(second.id)
        self.ui.show_view(self.frame, 'chain')
        self.app.Yield()
        before = graph.routing_snapshot()
        graph.history.clear()
        canvas.selected_nodes = {first.id, second.id}
        event = Mock()
        event.GetKeyCode.return_value = self.wx.WXK_DELETE
        canvas.key(event)
        self.assertEqual(graph.modules, [self.first])
        self.assertFalse(graph.connections)
        self.assertNotIn(second.id, graph.output_connections)
        self.assertFalse(canvas.selected_nodes)
        self.assertEqual(len(graph.history.undo_stack), 1)
        graph.history.step()
        self.assertIn(first, graph.modules)
        self.assertIn(second, graph.modules)
        self.assertEqual(graph.routing_snapshot(), before)
        graph.history.step(redo=True)
        self.assertEqual(graph.modules, [self.first])
        self.assertEqual(self.errors, [])

    def test_canvas_delete_and_backspace_remove_selected_module(self):
        graph, canvas = self.lib.session, self.frame.grid
        self.ui.show_view(self.frame, 'chain')
        for code in (self.wx.WXK_DELETE, self.wx.WXK_BACK):
            with self.subTest(key=code):
                node = self.add_unconnected()
                self.ui.select(self.frame, node, change_view=False)
                key = Mock()
                key.GetKeyCode.return_value = code
                self.ui.playback_state(self.frame, True)
                canvas.key(key)
                self.assertIn(node, graph.modules)
                self.lib.resetControls()
                self.ui.select(self.frame, self.first, change_view=False)
                canvas.key(key)
                self.assertIn(self.first, graph.modules)
                self.ui.select(self.frame, node, change_view=False)
                graph.connect(self.first.id, node.id)
                canvas.selected_edge = (self.first.id, node.id)
                canvas.key(key)
                self.assertIn(node, graph.modules)
                self.assertNotIn([self.first.id, node.id], graph.connections)
                canvas.key(key)
                self.assertNotIn(node, graph.modules)
                self.assertIs(graph.selected, self.first)
                self.assertFalse(canvas.HasCapture())
        # The final remaining module can also be removed.
        canvas.key(key)
        self.assertEqual(graph.modules, [])
        canvas.key(key)
        self.assertEqual(self.errors, [])

    def test_routing_history_restores_modules_without_reverting_controls(self):
        graph, history = self.lib.session, self.lib.session.history
        self.ui.show_view(self.frame, 'chain')
        history.clear()
        node = self.add_unconnected()
        editor = node.editor
        first_editor = self.first.editor
        node.state['userSliders'][0].setValue(.73)
        self.app.Yield()
        curve_history = json.dumps(editor.graph.plotter._history)
        self.lib.removeChainModule(node)
        self.assertTrue(node.retired)
        self.assertIs(node.editor, editor)
        self.assertEqual(len(history.undo_stack), 2)
        history.step()
        self.assertIn(node, graph.modules)
        self.assertIs(node.editor, editor)
        self.assertFalse(node.retired)
        self.assertEqual(json.dumps(editor.graph.plotter._history), curve_history)
        self.assertAlmostEqual(node.state['userSliders'][0].getValue(), .73)
        self.first.state['userSliders'][0].setValue(.31)
        self.lib.setVar('totalTime', 12)
        history.step(redo=True)
        self.assertNotIn(node, graph.modules)
        history.step()
        history.step()
        self.assertNotIn(node, graph.modules)
        history.step(redo=True)
        self.assertIs(node.editor, editor)
        self.assertIs(self.first.editor, first_editor)
        self.assertAlmostEqual(self.first.state['userSliders'][0].getValue(), .31)
        self.assertEqual(self.lib.getVar('totalTime'), 12)
        self.assertEqual(node.editor.graph.plotter.getTotalTime(), 12)
        self.assertEqual(self.errors, [])

    def test_routing_history_canvas_transactions_and_limits(self):
        graph, canvas, history = self.lib.session, self.frame.grid, self.lib.session.history
        node = self.add_unconnected()
        self.ui.show_view(self.frame, 'chain')
        self.app.Yield()
        history.clear()
        def click(point):
            event = Mock()
            event.GetPosition.return_value = self.wx.Point(*canvas.CalcScrolledPosition(*point))
            canvas.press(event)
            canvas.release(event)
        click(canvas.port(self.first.id, True))
        self.assertFalse(history.available())
        click(canvas.port(node.id, False))
        self.assertEqual(len(history.undo_stack), 1)
        history.step()
        self.assertNotIn([self.first.id, node.id], graph.connections)
        history.step(redo=True)
        self.assertIn([self.first.id, node.id], graph.connections)
        original = list(graph.positions[node.id])
        rect = canvas.rects[node.id]
        event = Mock()
        event.GetPosition.return_value = self.wx.Point(*canvas.CalcScrolledPosition(rect.x+40, rect.y+20))
        canvas.press(event)
        for delta in (10, 30, 60):
            event.GetPosition.return_value = self.wx.Point(*canvas.CalcScrolledPosition(rect.x+40+delta, rect.y+20+delta))
            canvas.motion(event)
        canvas.release(event)
        self.assertEqual(len(history.undo_stack), 2)
        history.step()
        self.assertEqual(graph.positions[node.id], original)
        # An unchanged click leaves redo intact.
        rect = canvas.rects[node.id]
        click((rect.x+30, rect.y+20))
        self.assertEqual(len(history.redo_stack), 1)
        # Replay availability no longer depends on playback: unsafe actions
        # stop the engine automatically rather than skipping the next action.
        self.assertTrue(history.available())
        self.lib.removeChainModule(node)
        self.assertFalse(history.redo_stack)
        history.clear()
        self.assertIsNone(node.editor)
        self.assertEqual(self.errors, [])

    def test_routing_history_empty_session_effects_and_menu_dispatch(self):
        from Resources.constants import ID_UNDO, ID_REDO
        history = self.lib.session.history
        self.frame.controlPanel.replacePlugin(0, 'Filter')
        self.app.Yield()
        effects = self.lib.captureSession()['output']['plugins']
        history.clear()
        self.ui.show_view(self.frame, 'chain')
        self.lib.removeChainModule(self.first)
        self.frame.onUndo(Mock())
        self.app.Yield()
        self.assertEqual(self.lib.captureSession()['output']['plugins'], effects)
        undo = self.frame.menubar.FindItemById(ID_UNDO)
        redo = self.frame.menubar.FindItemById(ID_REDO)
        self.assertFalse(undo.IsEnabled())
        self.assertTrue(redo.IsEnabled())
        self.assertIn('Remove', redo.GetItemLabel())
        self.ui.show_view(self.frame, 'graph')
        with patch.object(history, 'step') as unified:
            self.frame.onUndo(Mock())
            unified.assert_called_once_with()
        self.ui.show_view(self.frame, 'chain')
        self.frame.onRedo(Mock())
        self.assertEqual(self.lib.session.modules, [])
        self.frame.onUndo(Mock())
        self.app.Yield()
        self.assertEqual(self.lib.captureSession()['output']['plugins'], effects, repr((history.active, [a.label for a in history.undo_stack], [a.label for a in history.redo_stack], self.errors)))
        self.assertEqual(self.errors, [])

    def test_routing_history_roles_limits_and_failed_replay(self):
        graph, canvas, history = self.lib.session, self.frame.grid, self.lib.session.history
        node = self.add_unconnected()
        self.ui.show_view(self.frame, 'chain')
        history.clear()
        canvas.change_source(node, True)
        self.assertIn(node.id, graph.source_ids)
        history.step()
        self.assertNotIn(node.id, graph.source_ids)
        history.step(redo=True)
        self.assertIn(node.id, graph.source_ids)
        current = graph.routing_snapshot()
        # Invalid replay targets must leave the session and cursor untouched.
        action = history.undo_stack[-1]
        action[1]['routing']['connections'] = [['missing', node.id]]
        history.step()
        self.assertEqual(graph.routing_snapshot(), current)
        self.assertEqual(len(history.undo_stack), 1)
        self.assertFalse(history.redo_stack)
        self.assertEqual(len(self.errors), 1)
        self.errors.clear()
        history.clear()
        original_limit = history.limit
        try:
            history.limit = 1
            self.lib.removeChainModule(node)
            self.assertIsNotNone(node.editor)
            other = self.add_unconnected()
            self.assertIsNone(node.editor)
            history.step()
            self.assertTrue(history.redo_stack)
            # A failed module load preserves redo and the current editors.
            self.assertFalse(self.lib.openCeciliaFile(self.main, str(self.folder / 'missing.c5')))
            self.assertTrue(history.redo_stack)
            self.errors.clear()
            path = self.folder / 'history.c5chain'
            self.assertTrue(self.lib.saveChainSession(self.frame, str(path)))
            self.assertTrue(history.redo_stack)
            self.assertTrue(self.lib.openChainSession(self.frame, str(path)))
            self.assertFalse(history.undo_stack or history.redo_stack)
            self.assertIsNone(other.editor)
        finally:
            history.limit = original_limit

    def test_routing_history_output_cables_and_native_text_undo(self):
        from Resources.constants import ID_UNDO
        graph, canvas, history = self.lib.session, self.frame.grid, self.lib.session.history
        self.ui.show_view(self.frame, 'chain')
        history.clear()
        canvas.selected_edge = (self.first.id, None)
        key = Mock()
        key.GetKeyCode.return_value = self.wx.WXK_DELETE
        canvas.key(key)
        self.assertNotIn(self.first.id, graph.output_connections)
        history.step()
        self.assertIn(self.first.id, graph.output_connections)
        history.step(redo=True)
        self.assertNotIn(self.first.id, graph.output_connections)
        # Native text undo must not consume the available routing undo.
        entry = self.wx.TextCtrl(self.frame)
        try:
            entry.Show()
            entry.SetFocus()
            self.app.Yield()
            with patch.object(entry, 'CanUndo', return_value=True), \
                    patch.object(entry, 'Undo') as undo:
                event = Mock()
                event.GetId.return_value = ID_UNDO
                self.frame.updateUndoRedo(event)
                event.Enable.assert_called_once_with(True)
                self.frame.onUndo(Mock())
                undo.assert_called_once_with()
            self.assertNotIn(self.first.id, graph.output_connections)
            self.assertEqual(len(history.undo_stack), 1)
        finally:
            entry.Destroy()
        self.assertEqual(self.errors, [])

    def test_unified_history_interleaves_controls_routing_and_curves(self):
        history = self.lib.session.history
        history.clear()
        first = self.first.state['userSliders'][0]
        first.entryReturn(.65)
        node = self.add_unconnected()
        node.state['userSliders'][0].entryReturn(.8)
        self.assertEqual(len(history.undo_stack), 3)
        self.ui.show_view(self.frame, 'chain')
        self.frame.onUndo(Mock())
        self.assertEqual(self.lib.session.view, 'graph')
        self.assertIs(self.lib.session.selected, node)
        self.assertAlmostEqual(node.state['userSliders'][0].getValue(), .5)
        self.frame.onUndo(Mock())
        self.assertNotIn(node, self.lib.session.modules)
        self.assertEqual(self.lib.session.view, 'chain')
        self.frame.onUndo(Mock())
        self.assertIs(self.lib.session.selected, self.first)
        self.assertAlmostEqual(first.getValue(), .5)
        for _ in range(3):
            self.frame.onRedo(Mock())
        self.assertAlmostEqual(node.state['userSliders'][0].getValue(), .8)
        # Programmatic/runtime updates do not create entries or invalidate redo.
        count = len(history.undo_stack)
        first.setValue(.23)
        self.app.Yield()
        self.assertEqual(len(history.undo_stack), count)
        self.frame.onUndo(Mock())
        self.assertAlmostEqual(first.getValue(), .23)
        self.assertEqual(self.errors, [])

    def test_unified_history_effect_selection_from_popup(self):
        history = self.lib.session.history
        panel = self.frame.controlPanel
        history.clear()
        def choose(control, menu, position):
            control.setByIndex(control.choice.index('Filter'), True)
        with patch('Resources.Widgets.popup_menu', side_effect=choose):
            panel.plugins[0].choice.MouseDown(Mock())
        self.wx.MilliSleep(100)
        self.app.Yield()
        self.assertEqual(panel.plugins[0].getName(), 'Filter')
        self.assertEqual(len(history.undo_stack), 1)
        history.step()
        self.assertEqual(panel.plugins[0].getName(), 'None')
        history.step(redo=True)
        self.assertEqual(panel.plugins[0].getName(), 'Filter')
        self.assertEqual(self.errors, [])

    def test_unified_history_soundfile_failure_and_effect_identity(self):
        history = self.lib.session.history
        widget = self.first.inputs.cfileinList[0]
        original = widget.filePath
        other = self.folder / 'other.wav'
        other.write_bytes(self.source.read_bytes())
        history.clear()
        # Popup selection owns the outer gesture; onLoadFile is nested within it.
        with history.transaction('Select input sound'):
            self.assertTrue(widget.onLoadFile(str(other)))
        self.assertEqual(len(history.undo_stack), 1)
        widget.samplerFrame.Hide()
        history.step()
        self.assertEqual(widget.filePath, original)
        self.assertFalse(widget.samplerFrame.IsShown())
        history.step(redo=True)
        self.assertEqual(widget.filePath, str(other))
        self.assertFalse(widget.samplerFrame.IsShown())
        history.step()
        other.unlink()
        history.step(redo=True)
        self.assertEqual(widget.filePath, original)
        self.assertEqual(len(history.redo_stack), 1)
        self.assertEqual(len(self.errors), 1)
        self.errors.clear()
        history.clear()
        with history.transaction('Replace effect'):
            self.frame.controlPanel.replacePlugin(0, 'Filter')
        ident = history.effect_ids()[0]
        with history.transaction('Change effect'):
            self.lib.getVar('plugins')[0].getKnobs()[0].SetValue(2)
        self.assertFalse(history.undo_stack[-1].stop)
        with history.transaction('Move effect'):
            self.frame.controlPanel.movePlugin(0, 1)
        self.assertFalse(history.undo_stack[-1].stop)
        self.assertEqual(history.effect_ids()[1], ident)
        history.step()
        self.assertEqual(history.effect_ids()[0], ident)
        history.step()
        history.step()
        self.assertIsNone(self.lib.getVar('plugins')[0])
        for _ in range(3):
            history.step(redo=True)
        self.assertEqual(history.effect_ids()[1], ident)
        self.assertEqual(self.errors, [])

    def test_unified_history_slider_gesture_and_compound_duration(self):
        history = self.lib.session.history
        history.clear()
        slider = self.first.state['userSliders'][0].slider
        event = Mock()
        event.GetPosition.return_value = self.wx.Point(70, 8)
        event.Dragging.return_value = event.LeftIsDown.return_value = True
        slider.MouseDown(event)
        self.assertFalse(history.available())
        for x in (80, 100, 130):
            event.GetPosition.return_value = self.wx.Point(x, 8)
            slider.MouseMotion(event)
        slider.MouseUp(event)
        self.assertEqual(len(history.undo_stack), 1)
        current = slider.GetValue()
        slider.Refresh()
        slider.Update()
        self.app.Yield()
        self.assertEqual(len(history.undo_stack), 1)
        history.step()
        self.assertAlmostEqual(slider.GetValue(), .5)
        history.step(redo=True)
        self.assertAlmostEqual(slider.GetValue(), current)
        before = self.first.editor.graph.plotter.getData()[0].getLineState()
        with history.transaction('Change duration'):
            self.frame.controlPanel.setTotalTime(4)
        self.assertEqual(len(history.undo_stack), 2)
        history.step()
        self.assertAlmostEqual(self.lib.getVar('totalTime'), .2)
        self.assertEqual(self.first.editor.graph.plotter.getData()[0].getLineState(), before)
        self.assertEqual(self.errors, [])

    def test_unified_history_range_splitter_toggle_popup_list_and_sampler(self):
        self.fixture.write_text(self.fixture.read_text() +
            '\nInterface += [crange(name="band", min=0, max=1, init=[0.2, 0.8], rel="lin"), '
            'csplitter(name="splits", min=0, max=1, init=[0.1, 0.4, 0.9], rel="lin"), '
            'ctoggle(name="flag", init=0, rate="i"), '
            'cpopup(name="choice", value=["a", "b"], init="a", rate="i"), '
            'cgen(name="partials", init=[1, 0.5], rate="i")]\n')
        self.assertTrue(self.lib.openCeciliaFile(self.frame, str(self.fixture), replace=True), self.errors)
        self.first = self.lib.session.selected
        history = self.lib.session.history
        history.clear()
        sliders = self.first.state['userSliders']
        sliders[1].entryReturn([.3, .7])
        sliders[2].entryReturn([.2, .5, .8])
        widgets = {w.getName(): w for w in self.first.state['userTogglePopups']}
        widgets['flag'].toggle.MouseDown(Mock())
        def choose(control, menu, position):
            control.setByIndex(1, True)
        with patch('Resources.Widgets.popup_menu', side_effect=choose):
            widgets['choice'].popup.MouseDown(Mock())
        from Resources.Widgets import ListEntryPopupFrame
        popup = ListEntryPopupFrame(widgets['partials'].entry, '1, 0.5')
        popup.entry.SetValue('1, 0.3, 0.1')
        popup.OnApply()
        self.assertEqual(len(history.undo_stack), 5)
        for _ in range(5):
            history.step()
        self.assertEqual(widgets['flag'].getValue(), 0)
        self.assertEqual(widgets['choice'].getValue(), 0)
        self.assertEqual(widgets['partials'].getValue(), [1, .5])
        self.assertAlmostEqual(sliders[1].getValue()[0], .2)
        for _ in range(5):
            history.step(redo=True)
        self.assertEqual(widgets['partials'].getValue(), [1, .3, .1])
        sampler = self.first.inputs.cfileinList[0].samplerFrame
        original = sampler.getLoopIn()
        with history.transaction('Change loop in'):
            sampler.loopInSlider.setValue(.1)
        history.step()
        self.assertAlmostEqual(sampler.getLoopIn()[0], original[0])
        self.assertTrue(sampler.IsShown())
        self.assertEqual(self.errors, [])

    def test_unified_history_actual_playback_and_completed_take(self):
        history = self.lib.session.history
        slider = self.first.state['userSliders'][0]
        self.frame.controlPanel.setTotalTime(2)
        self.server.shutdown()
        self.server.server.reinit(audio='manual')
        self.lib.setVar('audioHostAPI', 'manual')
        original_to_dac = self.lib.getVar('toDac')
        self.addCleanup(self.lib.setVar, 'toDac', original_to_dac)
        self.lib.setVar('toDac', True)
        history.clear()
        # Use the real record-arm button, transport, pyo buffers and conversion.
        event = Mock()
        event.GetPosition.return_value = self.wx.Point(30, 8)
        slider.buttons.MouseDown(event)
        line = next(line for line in self.first.editor.graph.plotter.getData() if line.getName() == slider.getName())
        before = line.getLineState()
        self.lib.startCeciliaSound()
        self.assertTrue(self.server.isAudioServerRunning())
        self.assertIsNotNone(history.take)
        for i in range(60):
            self.server.server.process()
            if i % 10 == 0:
                self.app.Yield()
        # A UI edit during recording remains its own action, not a runtime tick.
        slider.entryReturn(.7)
        for _ in range(20):
            self.server.server.process()
        self.lib.stopCeciliaSound()
        self.assertEqual(history.undo_stack[-1].label, 'Record automation')
        self.assertEqual(len(history.undo_stack), 3)
        history.step()
        self.assertEqual(line.getLineState(), before)
        self.assertAlmostEqual(slider.getValue(), .7)
        history.step()
        self.assertAlmostEqual(slider.getValue(), .5)
        # Live-safe value replay leaves a running manual engine running.
        slider.setRec(False)
        self.lib.startCeciliaSound()
        history.step(redo=True)
        self.assertTrue(self.server.isAudioServerRunning())
        self.assertAlmostEqual(slider.getValue(), .7)
        # Curve restoration is unsafe and stops playback automatically.
        history.step(redo=True)
        self.assertFalse(self.server.isAudioServerRunning())
        # Undo during an active take first finalizes and undoes that take.
        slider.buttons.MouseDown(event)
        self.lib.startCeciliaSound()
        for i in range(50):
            self.server.server.process()
            if i % 10 == 0:
                self.app.Yield()
        history.step()
        self.assertFalse(self.server.isAudioServerRunning())
        self.assertEqual(history.redo_stack[-1].label, 'Record automation')
        self.assertEqual(self.errors, [])

    def test_unified_history_graph_gesture_groups_motion_until_release(self):
        history = self.lib.session.history
        self.ui.show_view(self.frame, 'graph')
        self.app.Yield()
        graph = self.first.editor.graph.plotter
        line = next(line for line in graph.getData() if line.getName() == 'level')
        graph.setSelected(graph.getData().index(line))
        graph.setTool(1)
        self.app.Yield()
        history.clear()
        before = line.getLineState()
        event = Mock()
        event.GetPosition.return_value = self.wx.Point(100, 100)
        event.LeftIsDown.return_value = True
        with patch.object(graph, '_getXY', return_value=(.04, .3)), \
                patch.object(graph, 'GetXY', return_value=(.04, .3)), \
                patch.object(graph, 'GetClosestPointOnCurve', return_value=None):
            graph.OnMouseLeftDown(event)
            self.assertIsNotNone(history.active)
            self.assertTrue(graph.canvas.HasCapture())
            with patch.object(graph, 'GetXY', return_value=(.08, .6)):
                graph.OnMotion(event)
            graph.OnMouseLeftUp(event)
        self.assertFalse(graph.canvas.HasCapture())
        self.assertEqual(len(history.undo_stack), 1)
        changed = line.getLineState()
        self.assertNotEqual(changed, before)
        self.ui.show_view(self.frame, 'chain')
        history.step()
        self.assertEqual(self.lib.session.view, 'graph')
        self.assertEqual(graph.getSelected(), graph.getData().index(line))
        self.assertEqual(line.getLineState(), before)
        history.step(redo=True)
        for actual, expected in zip(line.getLineState()['data'], changed['data']):
            for a, b in zip(actual, expected):
                self.assertAlmostEqual(a, b)
        self.assertEqual(self.errors, [])

    def test_unified_history_preset_mapping_and_retained_reload(self):
        from Resources.Widgets import OSCPopupFrame
        history = self.lib.session.history
        slider = self.first.state['userSliders'][0]
        history.clear()
        slider.entryReturn(.75)
        self.lib.savePresetToFile('history-preset')
        self.assertEqual(len(history.undo_stack), 1)
        slider.entryReturn(.25)
        self.first.editor.presets.onPresetSelect(1, 'history-preset')
        self.assertEqual(len(history.undo_stack), 3)
        history.step()
        self.assertAlmostEqual(slider.getValue(), .25)
        history.step(redo=True)
        self.assertAlmostEqual(slider.getValue(), .75)
        self.assertTrue(self.first.editor.presets.presetChoice.HasFocus())
        popup = OSCPopupFrame(self.frame, slider)
        popup.entry.SetValue('9000:/level')
        popup.entry2.SetValue('')
        popup.OnApply()
        self.assertEqual(slider.getOpenSndCtrl(), (9000, '/level'))
        history.step()
        self.assertIsNone(slider.getOpenSndCtrl())
        history.step(redo=True)
        original = self.first
        self.assertTrue(self.lib.openCeciliaFile(self.frame, str(self.fixture), replace=True), self.errors)
        replacement = self.lib.session.selected
        self.assertIsNot(replacement, original)
        history.step()
        self.assertIs(self.lib.session.selected, original)
        self.fixture.unlink()
        history.step(redo=True)
        self.assertIs(self.lib.session.selected, replacement)
        self.assertEqual(self.lib.session.view, 'graph')
        self.assertEqual(self.errors, [])

    def test_unified_history_keyboard_shortcuts_with_graph_focus(self):
        history = self.lib.session.history
        slider = self.first.state['userSliders'][0]
        history.clear()
        slider.entryReturn(.8)
        graph = self.first.editor.graph.plotter
        self.ui.show_view(self.frame, 'graph')
        self.frame.Raise()
        graph.canvas.SetFocus()
        self.app.Yield()
        self.assertTrue(graph.canvas.HasFocus())
        simulator = self.wx.UIActionSimulator()
        simulator.Char(ord('Z'), self.wx.MOD_CONTROL)
        for _ in range(5):
            self.wx.MilliSleep(10)
            self.app.Yield()
        self.assertAlmostEqual(slider.getValue(), .5)
        graph.canvas.SetFocus()
        simulator.Char(ord('Z'), self.wx.MOD_CONTROL | self.wx.MOD_SHIFT)
        for _ in range(5):
            self.wx.MilliSleep(10)
            self.app.Yield()
        self.assertAlmostEqual(slider.getValue(), .8)
        self.assertIsNone(history.active)
        self.assertEqual(len(history.undo_stack), 1)
        self.assertEqual(self.errors, [])

    def test_invalid_graph_load_preserves_open_session_and_v1_migration(self):
        self.branch_graph()
        path = self.folder / 'graph.c5chain'
        self.assertTrue(self.lib.saveChainSession(self.frame, str(path)))
        snapshot = self.lib.captureSession()
        original = json.loads(path.read_text())
        invalid = json.loads(path.read_text())
        invalid['connections'].append([invalid['modules'][1]['id'], invalid['source_id']])
        path.write_text(json.dumps(invalid))
        self.assertFalse(self.lib.openChainSession(self.frame, str(path)))
        self.assertEqual(self.lib.captureSession(), snapshot)
        self.errors.clear()
        original['version'] = 1
        for key in ('source_id', 'connections', 'output_connections', 'positions'):
            original.pop(key)
        path.write_text(json.dumps(original))
        self.assertTrue(self.lib.openChainSession(self.frame, str(path)), self.errors)
        ids = [m.id for m in self.lib.session.modules]
        self.assertEqual(self.lib.session.connections, [list(edge) for edge in zip(ids, ids[1:])])
        self.assertEqual(self.lib.session.output_connections, ids[-1:])
        self.assertEqual(self.errors, [])

    def test_graph_bounce_and_batch_rendering(self):
        self.branch_graph()
        self.lib.setVar('audioFileType', 'wav')
        self.lib.setVar('sampSize', 0)
        progress = Mock()
        progress.Update.return_value = (True, False)
        bounce = self.folder / 'bounce.wav'
        panel = self.frame.controlPanel
        panel.outputFilename = str(bounce)
        with patch.object(panel, 'showBounceDialog'):
            panel.onBounceToDisk()
        import time
        deadline = time.monotonic() + 10
        while self.server.isAudioServerRunning() and time.monotonic() < deadline:
            time.sleep(.05)
        self.assertFalse(self.server.isAudioServerRunning())
        self.lib.stopCeciliaSound()
        self.assertTrue(bounce.is_file())
        self.assertFalse(self.frame.grid.running)
        presets = self.lib.session.selected.editor.presets
        with patch.object(self.wx, 'ProgressDialog', return_value=progress), \
                patch.object(presets, 'getPresets', return_value=['init', 'one', 'two']), \
                patch.object(self.lib, 'loadPresetFromFile'):
            self.main.applyBatchProcessingPreset('presets-render')
            self.main.applyBatchProcessingFolder('folder-render')
        for filename in ('presets-render/source-one.wav', 'presets-render/source-two.wav',
                         'folder-render/source-folder-render.wav'):
            with wave.open(str(self.folder / filename), 'rb') as stream:
                self.assertGreaterEqual(stream.getnframes(), 8820)
        self.assertFalse(self.frame.grid.running)
        self.assertTrue(self.frame.addModuleButton._enable)
        self.assertTrue(all(m.editor.presets.presetChoice._enable for m in self.lib.session.modules))
        self.assertEqual(self.errors, [])

    def test_both_batch_modes_restore_graph_controls(self):
        self.branch_graph()
        presets = self.lib.session.selected.editor.presets
        progress = Mock()
        progress.Update.return_value = (True, False)
        def render(filename):
            self.ui.playback_state(self.frame, True)
        with patch.object(self.frame.controlPanel, 'onBatchProcessing', side_effect=render) as batch, \
                patch.object(self.wx, 'ProgressDialog', return_value=progress), \
                patch.object(presets, 'getPresets', return_value=['init', 'one', 'two']), \
                patch.object(self.lib, 'loadPresetFromFile') as load:
            for method in (self.main.applyBatchProcessingPreset, self.main.applyBatchProcessingFolder):
                method('batch-results')
                self.assertFalse(self.frame.grid.running)
                self.assertTrue(self.frame.addModuleButton._enable)
                self.assertTrue(all(m.editor.presets.presetChoice._enable for m in self.lib.session.modules))
            self.assertEqual([call.args[0] for call in load.call_args_list], ['one', 'two'])
            self.assertGreaterEqual(batch.call_count, 3)
        self.assertEqual(self.errors, [])

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
        with self.lib.session.history.transaction('Edit curve', {'module': self.first.id}):
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
        self.assertIn('deliberate stage failure', self.errors[-1][1])

    def test_first_only_module_adds_independent_source(self):
        self.add()
        graph = self.lib.session
        previous = list(graph.modules)
        routes = graph.routing_snapshot()
        source_file = self.folder / 'table.c5'
        source_file.write_text(
            'class Module(BaseModule):\n'
            '    def __init__(self):\n'
            '        BaseModule.__init__(self)\n'
            '        self.table = self.addFilein("snd")\n'
            '        self.out = TableRead(self.table, freq=self.table.getRate()).play()\n'
            'Interface = [cfilein(name="snd")]\n')
        self.assertTrue(self.lib.openCeciliaFile(self.frame, str(source_file)), self.errors)
        second = graph.selected
        self.assertEqual(graph.modules[:-1], previous)
        self.assertEqual(graph.connections, routes['connections'])
        self.assertEqual(graph.output_connections, routes['output_connections'])
        self.assertIn(second.id, graph.source_ids)
        self.assertIs(graph.source, second)
        second.inputs.cfileinList[0].onLoadFile(str(self.source))
        graph.connect(second.id, previous[-1].id)
        self.assertTrue(self.server.loadChain(), self.errors)
        self.assertEqual(self.errors, [])

    def test_single_source_replacement_keeps_shared_settings(self):
        data = self.lib.capturePresetData()
        data.update(totalTime=11, nchnls=1, gainSlider=-20, plugins={})
        first_only = self.folder / 'replacement.c5'
        first_only.write_text(
            'class Module(BaseModule):\n'
            '    def __init__(self):\n'
            '        BaseModule.__init__(self)\n'
            '        self.table = self.addFilein("snd")\n'
            '        self.out = TableRead(self.table, freq=self.table.getRate()).play()\n'
            'Interface = [cfilein(name="snd")]\n'
            'CECILIA_PRESETS = ' + repr({'last save': data}) + '\n')
        self.frame.controlPanel.replacePlugin(0, 'Filter')
        self.app.Yield()
        before = self.lib.captureSession()['output']
        self.assertTrue(self.lib.openCeciliaFile(self.frame, str(first_only), replace=True), self.errors)
        self.assertEqual(self.lib.captureSession()['output'], before)
        self.assertEqual(self.lib.session.source.inputs.cfileinList[0].filePath, str(self.source))
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

    def test_loaded_chain_can_change_first_input_sound(self):
        import shutil
        self.add()
        path = self.folder / 'session.c5chain'
        self.assertTrue(self.lib.saveChainSession(self.frame, str(path)), self.errors)
        self.assertTrue(self.lib.openChainSession(self.frame, str(path)), self.errors)
        self.app.Yield()
        first, second = self.lib.session.modules
        self.server.server.reinit(audio='manual')
        self.server.boot()
        self.assertTrue(self.server.loadChain(), self.errors)
        self.server.start()
        self.ui.playback_state(self.frame, True)
        replacement = self.folder / 'replacement.wav'
        shutil.copyfile(self.source, replacement)
        widget = first.inputs.cfileinList[0]
        for selected in (first, second):
            self.ui.select(self.frame, selected)
            self.app.Yield()
            self.assertTrue(widget.IsEnabled())
            self.assertTrue(widget.IsShownOnScreen())
            self.assertTrue(widget.fileMenu._enable)
            event = Mock()
            event.GetPosition.return_value = self.wx.Point(5, 5)
            with patch.object(self.lib, 'openAudioFileDialog', return_value=str(replacement)) as dialog:
                widget.fileMenu.MouseDown(event)
            dialog.assert_called_once()
            self.assertEqual(widget.filePath, str(replacement))
            self.assertEqual(first.state['userInputs']['snd']['path'], str(replacement))
            self.assertEqual(second.state['userInputs']['snd']['path'], '')
        self.server.server.process()
        self.server.stop()
        self.lib.resetControls()
        self.assertTrue(widget.IsEnabled())
        self.assertFalse(second.inputs.cfileinList[0].IsEnabled())

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
        self.lib.session.disconnect(self.first.id, second.id)
        self.lib.session.connect(self.first.id)
        self.assertEqual([line.getLineState() for line in self.first.editor.graph.plotter.getData()
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
    def test_reroute_remove_reload_and_auxiliary_assets(self):
        self.add()
        second = self.lib.session.modules[1]
        self.lib.session.disconnect(self.first.id, second.id)
        self.lib.session.connect(self.first.id)
        self.assertIs(self.lib.session.source, self.first)
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
        for module in reversed(list(self.lib.session.modules)):
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
