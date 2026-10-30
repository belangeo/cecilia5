"""Routing canvas gestures without a display or audio hardware."""
import ast
import math
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
from unittest.mock import Mock, patch


class Rect:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height

    def Contains(self, point):
        return self.x <= point[0] < self.x + self.width and self.y <= point[1] < self.y + self.height

    def Intersects(self, other):
        return (self.x < other.x + other.width and other.x < self.x + self.width
                and self.y < other.y + other.height and other.y < self.y + self.height)


class RoutingSelectionTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'Resources/RoutingGraph.py').read_text())
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef))
        self.history = Mock()
        self.graph = SimpleNamespace(
            modules=[SimpleNamespace(id=name) for name in ('source', 'a', 'b')],
            source_ids={'source'}, positions={'a': [280, 150], 'b': [490, 275]},
            history=self.history)
        namespace = {'wx': SimpleNamespace(ScrolledWindow=object, Rect=Rect, WXK_ESCAPE=27, WXK_DELETE=127, WXK_BACK=8),
                     'CeciliaLib': SimpleNamespace(session=self.graph), 'math': math,
                     '__name__': 'Resources.RoutingGraph', '__package__': 'Resources'}
        exec(compile(ast.Module(body=[cls], type_ignores=[]), '<routing canvas>', 'exec'), namespace)
        self.canvas = object.__new__(namespace['RoutingGraph'])
        canvas = self.canvas
        canvas.frame = Mock()
        canvas.running = False
        canvas.selected_nodes = set()
        canvas.selected_edge = canvas.drag = canvas.move_before = None
        canvas.cables = []
        canvas.rects = {'source': Rect(24, 40, 160, 82),
                        'a': Rect(280, 150, 160, 82), 'b': Rect(490, 275, 160, 82),
                        None: Rect(800, 40, 160, 82)}
        for name in ('SetFocus', 'Refresh', 'CaptureMouse', 'ReleaseMouse', 'rebuild'):
            setattr(canvas, name, Mock())
        canvas.HasCapture = lambda: True
        canvas.point = lambda event: event.point
        canvas.hit_port = lambda point: None
        self.chain_ui = patch.dict(sys.modules, {'Resources.ChainUI': SimpleNamespace(select=Mock())})
        self.chain_ui.start()
        self.addCleanup(self.chain_ui.stop)

    def event(self, point, shift=False):
        return SimpleNamespace(point=point, ShiftDown=lambda: shift)

    def marquee(self, start, end, shift=False):
        self.canvas.press(self.event(start, shift))
        self.canvas.motion(self.event(end))
        self.canvas.release(self.event(end))

    def test_reverse_marquee_selects_processors_and_group_drag_records_one_action(self):
        self.marquee((980, 400), (10, 10))
        self.assertEqual(self.canvas.selected_nodes, {'a', 'b'})
        self.history.record.assert_not_called()
        self.canvas.press(self.event((300, 170)))
        self.canvas.motion(self.event((350, 200)))
        self.canvas.motion(self.event((360, 210)))
        self.canvas.release(self.event((360, 210)))
        self.assertEqual(self.graph.positions, {'a': [340, 190], 'b': [550, 315]})
        self.history.record.assert_called_once_with('Move modules', self.history.snapshot.return_value)

    def test_shift_marquee_adds_and_empty_click_clears(self):
        self.marquee((260, 130), (450, 240))
        self.assertEqual(self.canvas.selected_nodes, {'a'})
        self.marquee((470, 250), (670, 370), shift=True)
        self.assertEqual(self.canvas.selected_nodes, {'a', 'b'})
        self.marquee((700, 450), (700, 450))
        self.assertEqual(self.canvas.selected_nodes, set())

    def test_group_clamps_as_a_unit_and_escape_restores_positions(self):
        self.canvas.selected_nodes = {'a', 'b'}
        self.canvas.press(self.event((300, 170)))
        self.canvas.motion(self.event((-100, -100)))
        self.assertEqual(self.graph.positions, {'a': [220, 16], 'b': [430, 141]})
        self.canvas.key(SimpleNamespace(GetKeyCode=lambda: 27))
        self.assertEqual(self.graph.positions, {'a': [280, 150], 'b': [490, 275]})
        self.history.record.assert_not_called()
        self.assertIsNone(self.canvas.drag)

    def test_playback_allows_marquee_and_group_movement(self):
        self.canvas.running = True
        self.marquee((260, 130), (680, 400))
        self.assertEqual(self.canvas.selected_nodes, {'a', 'b'})
        self.canvas.press(self.event((300, 170)))
        self.canvas.motion(self.event((360, 210)))
        self.canvas.release(self.event((360, 210)))
        self.assertEqual(self.graph.positions, {'a': [340, 190], 'b': [550, 315]})
        self.history.record.assert_called_once_with('Move modules', self.history.snapshot.return_value)

    def test_escape_marquee_restores_previous_selection(self):
        self.canvas.selected_nodes = {'a'}
        self.canvas.press(self.event((470, 250)))
        self.canvas.motion(self.event((670, 370)))
        self.assertEqual(self.canvas.selected_nodes, {'b'})
        self.canvas.key(SimpleNamespace(GetKeyCode=lambda: 27))
        self.assertEqual(self.canvas.selected_nodes, {'a'})

    def test_delete_and_backspace_remove_entire_selection(self):
        for key in (127, 8):
            with self.subTest(key=key):
                self.canvas.selected_nodes = {'a', 'b'}
                self.graph.selected = self.graph.modules[0]
                lib = self.canvas.key.__globals__['CeciliaLib']
                lib.removeChainModules = Mock()
                self.canvas.key(SimpleNamespace(GetKeyCode=lambda: key))
                lib.removeChainModules.assert_called_once_with(self.graph.modules[1:])

    def test_playback_blocks_deleting_selection(self):
        self.canvas.running = True
        self.canvas.selected_nodes = {'a', 'b'}
        lib = self.canvas.key.__globals__['CeciliaLib']
        lib.removeChainModules = Mock()
        event = Mock()
        event.GetKeyCode.return_value = 127
        self.canvas.key(event)
        lib.removeChainModules.assert_not_called()

    def test_mute_button_toggles_without_dragging_or_changing_selection(self):
        graph, canvas = self.graph, self.canvas
        graph.muted_ids = []
        graph.modules[1].state = {'currentModuleName': 'Effect'}
        graph.set_muted = Mock(side_effect=lambda module, muted:
                               graph.muted_ids.append(module.id) if muted else graph.muted_ids.remove(module.id))
        lib = canvas.toggle_mute.__globals__['CeciliaLib']
        server = Mock()
        lib.getVar = lambda name: server
        canvas.selected_nodes = {'a', 'b'}
        canvas.press(self.event((350, 210)))
        self.assertEqual(graph.muted_ids, ['a'])
        self.assertIsNone(canvas.drag)
        self.assertEqual(canvas.selected_nodes, {'a', 'b'})
        self.history.record.assert_called_once_with('Mute Effect', self.history.snapshot.return_value)
        canvas.press(self.event((350, 210)))
        self.assertEqual(graph.muted_ids, [])
        self.assertEqual(server.setModuleMute.call_count, 2)
        canvas.running = True
        canvas.press(self.event((350, 210)))
        self.assertEqual(graph.muted_ids, ['a'])
        self.assertEqual(server.setModuleMute.call_count, 3)
        server.cleanup_module.assert_not_called()
