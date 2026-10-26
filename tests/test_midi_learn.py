"""MIDI learning cancellation without audio hardware or a GUI."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


class MidiLearnTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'Resources/audio.py').read_text())
        methods = [node for node in ast.walk(tree)
                   if isinstance(node, ast.FunctionDef)
                   and node.name in ('midiLearn', '_historyMidiAssignment')]
        self.lib = SimpleNamespace(callAfter=lambda callback: callback())
        self.scan = Mock()
        namespace = {'CeciliaLib': self.lib, 'CtlScan2': Mock(return_value=self.scan)}
        exec(compile(ast.Module(body=methods, type_ignores=[]), '<audio methods>', 'exec'), namespace)
        self.server = SimpleNamespace(
            shutdown=Mock(), boot=Mock(), server=Mock(), stop=Mock(),
            getMidiCtlNumber=Mock())
        self.learn = lambda slider, ranged=False: namespace['midiLearn'](self.server, slider, ranged)
        self.assignment = namespace['_historyMidiAssignment']

    def test_second_click_cancels_and_preserves_binding(self):
        widget = SimpleNamespace(midiLearn=False, midictl='7:1', Refresh=Mock())
        slider = SimpleNamespace(slider=widget)
        self.assertTrue(self.learn(slider))
        widget.midiLearn = True  # The label handler activates the indicator.
        generation = self.server._midiLearnGeneration
        self.assertFalse(self.learn(slider))
        self.scan.stop.assert_called_once()
        self.server.stop.assert_called_once()
        self.assertFalse(widget.midiLearn)
        self.assertEqual(widget.midictl, '7:1')
        self.assertIsNone(self.server.midiLearnSlider)
        self.assertGreater(self.server._midiLearnGeneration, generation)
        # A queued assignment must return before importing GUI/session code.
        self.assignment(self.server, 10, 1, generation)
        self.assertTrue(self.learn(slider, True))
        self.assertTrue(self.server.midiLearnRange)
        self.assignment(self.server, 10, 1, generation)

    def test_plugin_control_can_cancel_without_a_nested_slider(self):
        knob = SimpleNamespace(midiLearn=False, Refresh=Mock())
        self.assertTrue(self.learn(knob))
        knob.midiLearn = True
        self.assertFalse(self.learn(knob))
        self.assertFalse(knob.midiLearn)

    def test_label_second_right_click_stops_running_learning_server(self):
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'Resources/Widgets.py').read_text())
        label_class = next(node for node in tree.body
                           if isinstance(node, ast.ClassDef) and node.name == 'Label')
        handler = next(node for node in label_class.body
                       if isinstance(node, ast.FunctionDef) and node.name == 'OnRightDown')
        self.lib.getVar = lambda name: self.server
        namespace = {'CeciliaLib': self.lib}
        exec(compile(ast.Module(body=[handler], type_ignores=[]), '<label handler>', 'exec'), namespace)
        self.server.isAudioServerRunning = Mock(return_value=False)
        self.server.server.start.side_effect = lambda: self.server.isAudioServerRunning.configure_mock(return_value=True)
        self.server.stop.side_effect = self.server.server.stop
        widget = SimpleNamespace(midiLearn=False, Refresh=Mock())
        label = SimpleNamespace(GetSize=lambda: (100, 20), label='Gain')
        slider = SimpleNamespace(slider=widget, label=label)

        def click(*args, **kwargs):
            if self.learn(slider):
                widget.midiLearn = True

        label.outFunction = Mock(side_effect=click)
        event = SimpleNamespace(GetPosition=lambda: (10, 5), ShiftDown=lambda: False)
        right_click = namespace['OnRightDown']
        right_click(label, event)
        self.assertTrue(widget.midiLearn)
        self.server.server.start.assert_called_once()
        right_click(label, event)
        self.assertEqual(label.outFunction.call_count, 2)
        self.assertFalse(widget.midiLearn)
        self.server.server.stop.assert_called_once()
        self.scan.stop.assert_called_once()
        # Normal playback still blocks MIDI learning from label clicks.
        right_click(label, event)
        self.assertEqual(label.outFunction.call_count, 2)
