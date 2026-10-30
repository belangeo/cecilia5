"""Muted routing nodes preserve graph topology and bypass processing."""
import ast
import copy
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import Mock

from Resources.Session import (ChainSession, ModuleInstance, instance_context,
                               active_instance, read_session, write_session)


class Signal:
    def __init__(self, value=0, **kwargs):
        self._value = value

    @property
    def value(self):
        value = self._value() if callable(self._value) else self._value
        return value.value if isinstance(value, Signal) else value

    @value.setter
    def value(self, value):
        self._value = value

    def __mul__(self, other):
        return Signal(lambda: self.value * other)

    def __add__(self, other):
        return Signal(lambda: self.value + other.value)


def interpolate(processed, bypass, fade):
    return Signal(lambda: Signal(bypass if fade.value else processed).value)


def module(output=None):
    class Processor:
        def __init__(self):
            owner = active_instance.get()
            self.out = output if output is not None else owner.upstream * .25

        def _createOpenSndCtrlReceivers(self):
            pass

        def _setWidgetValues(self):
            pass

    return ModuleInstance('test.c5', Processor, [{'type': 'csampler', 'name': 'snd'}])


class RoutingMuteTests(unittest.TestCase):
    def setUp(self):
        self.graph = ChainSession()
        self.source, self.effect, self.tail = module(1), module(), module()
        for node in (self.source, self.effect, self.tail):
            self.graph.append(node)
        self.graph.connect(self.source.id, self.effect.id)
        self.graph.connect(self.effect.id, self.tail.id)
        self.graph.output_connections = [self.tail.id]

    def render(self):
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'Resources/audio.py').read_text())
        method = next(node for node in ast.walk(tree)
                      if isinstance(node, ast.FunctionDef) and node.name == 'loadChain')
        self.lib = SimpleNamespace(session=self.graph, getVar=lambda name: 2,
                                   showErrorDialog=Mock(), resetControls=Mock())
        namespace = {'__package__': 'Resources', 'CeciliaLib': self.lib,
                     'instance_context': instance_context, 'Sig': Signal, 'SigTo': Signal, 'Interp': interpolate,
                     'Mix': lambda value, voices: value}
        exec(compile(ast.Module(body=[method], type_ignores=[]), '<audio builder>', 'exec'), namespace)
        server = SimpleNamespace(cleanup_module=Mock(), moduleMuteSignals={}, runtimeModules=[], _loadOutputPlugins=Mock())
        self.assertTrue(namespace['loadChain'](server))
        self.lib.showErrorDialog.assert_not_called()
        return server

    def test_muted_processor_passes_downstream_but_silences_its_final_output(self):
        self.graph.set_muted(self.effect, True)
        self.graph.output_connections.append(self.effect.id)
        server = self.render()
        self.assertAlmostEqual(server.out.value, .25 * .707)
        self.assertIsNotNone(self.effect.state['currentModule'])
        self.assertEqual(len(server.runtimeModules), 3)
        self.assertEqual(self.graph.connections, [[self.source.id, self.effect.id],
                                                  [self.effect.id, self.tail.id]])

    def test_muted_merge_preserves_input_mixing_gain(self):
        other = module(2)
        self.graph.append(other, as_source=True)
        self.graph.connect(other.id, self.effect.id)
        self.graph.set_muted(self.effect, True)
        self.assertAlmostEqual(self.render().out.value, (1 + 2) * .707 * .25)

    def test_unmute_restores_processing(self):
        self.graph.set_muted(self.effect, True)
        self.assertEqual(self.render().out.value, .25)
        self.graph.set_muted(self.effect, False)
        self.assertEqual(self.render().out.value, .0625)

    def test_muted_source_is_silent(self):
        self.graph.output_connections = [self.source.id]
        self.graph.set_muted(self.source, True)
        server = self.render()
        self.assertEqual(server.out.value, 0)
        self.assertEqual(len(server.runtimeModules), 1)

    def test_save_restore_and_remove_mute_state(self):
        self.graph.set_muted(self.effect, True)
        snapshot = dict(self.graph.routing_snapshot(),
                        modules=[{'id': node.id, 'module_path': node.path} for node in self.graph.modules],
                        output={})
        with tempfile.TemporaryDirectory() as root:
            path = str(Path(root) / 'mute.c5chain')
            write_session(path, snapshot)
            restored = ChainSession()
            restored.modules = list(self.graph.modules)
            restored.restore_routing(read_session(path))
            restored.validate_graph()
            self.assertEqual(restored.muted_ids, [self.effect.id])
        replacement = module()
        self.graph.replace(self.effect, replacement)
        self.assertEqual(self.graph.muted_ids, [replacement.id])
        self.graph.remove(replacement)
        self.assertEqual(self.graph.muted_ids, [])

    def test_older_sessions_default_to_unmuted_and_invalid_ids_rejected(self):
        snapshot = self.graph.routing_snapshot()
        snapshot.pop('muted_ids')
        self.graph.restore_routing(snapshot)
        self.assertEqual(self.graph.muted_ids, [])
        for ids in ([self.effect.id, self.effect.id], ['missing'], 'invalid'):
            self.graph.muted_ids = ids
            with self.assertRaisesRegex(ValueError, 'muted'):
                self.graph.validate_graph()

    def test_live_toggle_reuses_running_graph_in_both_directions(self):
        self.graph.set_muted(self.effect, True)
        server = self.render()
        output = server.out
        modules = list(server.runtimeModules)
        self.assertEqual(output.value, .25)
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'Resources/audio.py').read_text())
        method = next(node for node in ast.walk(tree)
                      if isinstance(node, ast.FunctionDef) and node.name == 'setModuleMute')
        namespace = {}
        exec(compile(ast.Module(body=[method], type_ignores=[]), '<live mute>', 'exec'), namespace)
        namespace['setModuleMute'](server, self.effect.id, False)
        self.assertEqual(output.value, .0625)
        namespace['setModuleMute'](server, self.effect.id, True)
        self.assertEqual(output.value, .25)
        self.assertIs(server.out, output)
        self.assertEqual(server.runtimeModules, modules)
        server.cleanup_module.assert_called_once()  # Only at initial construction.

    def test_mute_history_replays_live_without_rebuilding(self):
        from Resources.SessionHistory import Action
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'Resources/SessionHistory.py').read_text())
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'SessionHistory')
        methods = [node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name in ('record', 'apply')]
        for method in methods:
            method.body = [node for node in method.body if not isinstance(node, ast.ImportFrom)]
        server, frame = Mock(), Mock()
        lib = SimpleNamespace(getVar=lambda name: server if name == 'audioServer' else frame)
        namespace = {'Action': Action, 'lib': lib, 'copy': copy}
        exec(compile(ast.Module(body=methods, type_ignores=[]), '<mute history>', 'exec'), namespace)
        before = dict(modules=list(self.graph.modules), routing=self.graph.routing_snapshot(), selected=self.effect.id)
        self.graph.set_muted(self.effect, True)
        after = dict(modules=list(self.graph.modules), routing=self.graph.routing_snapshot(), selected=self.effect.id)
        history = SimpleNamespace(session=self.graph, replaying=False, snapshot=lambda: after, append=Mock())
        namespace['record'](history, 'Mute effect', before)
        action = history.append.call_args.args[0]
        self.assertFalse(action.stop)
        namespace['apply'](history, before)
        self.assertEqual(self.graph.muted_ids, [])
        server.setModuleMute.assert_any_call(self.effect.id, False)
        namespace['apply'](history, after)
        self.assertEqual(self.graph.muted_ids, [self.effect.id])
        server.setModuleMute.assert_any_call(self.effect.id, True)
        server.cleanup_module.assert_not_called()
        server.stop.assert_not_called()
        # Layout-only actions also replay without touching the audio graph.
        server.reset_mock()
        before = dict(modules=list(self.graph.modules), routing=self.graph.routing_snapshot(), selected=self.effect.id)
        self.graph.positions[self.effect.id] = [400, 200]
        after = dict(modules=list(self.graph.modules), routing=self.graph.routing_snapshot(), selected=self.effect.id)
        history.snapshot = lambda: after
        namespace['record'](history, 'Move module', before)
        self.assertFalse(history.append.call_args.args[0].stop)
        namespace['apply'](history, before)
        self.assertEqual(self.graph.positions, before['routing']['positions'])
        namespace['apply'](history, after)
        self.assertEqual(self.graph.positions[self.effect.id], [400, 200])
        server.cleanup_module.assert_not_called()
        server.setModuleMute.assert_not_called()
        server.stop.assert_not_called()

    def test_terminal_processor_mutes_to_silence_and_unmutes_live(self):
        self.graph.set_muted(self.tail, True)
        server = self.render()
        self.assertEqual(server.out.value, 0)
        server.moduleMuteSignals[self.tail.id].value = 0
        self.assertEqual(server.out.value, .0625)
        server.moduleMuteSignals[self.tail.id].value = 1
        self.assertEqual(server.out.value, 0)

    def test_live_mute_updates_both_branches_without_adding_dry_to_final_mix(self):
        self.graph.output_connections.append(self.effect.id)
        server = self.render()
        self.assertAlmostEqual(server.out.value, (.25 + .0625) * .707)
        server.moduleMuteSignals[self.effect.id].value = 1
        self.assertAlmostEqual(server.out.value, .25 * .707)
        server.moduleMuteSignals[self.effect.id].value = 0
        self.assertAlmostEqual(server.out.value, (.25 + .0625) * .707)
