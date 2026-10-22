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
