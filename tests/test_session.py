import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from Resources.Session import (ChainSession, ModuleInstance, active_instance,
                               bind_instance, instance_context, read_session,
                               write_session, mix_signals, serial_routing)


def module(inputs=None, metadata=None):
    return ModuleInstance('example.c5', type('Module', (), {}),
                          inputs if inputs is not None else [{'type': 'csampler', 'name': 'snd'}],
                          metadata)


class SessionTests(unittest.TestCase):
    def test_duplicate_modules_have_independent_ids_and_state(self):
        first, second = module(), module()
        first.state['userInputs']['snd'] = {'path': 'first.wav'}
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(second.state['userInputs'], {})
        first.interface[0]['name'] = 'changed'
        self.assertEqual(second.interface[0]['name'], 'snd')

    def test_downstream_compatibility_and_auxiliary_metadata(self):
        table = module([{'type': 'cfilein', 'name': 'table'}])
        ambiguous = module([{'type': 'csampler', 'name': 'snd'},
                            {'type': 'cfilein', 'name': 'impulse'}])
        compatible = module(ambiguous.interface,
                            {'primary_input': 'snd', 'auxiliary_inputs': ['impulse']})
        ChainSession.validate_order([table, module(), compatible])
        for invalid in (table, ambiguous):
            with self.assertRaisesRegex(ValueError, 'Stage 2'):
                ChainSession.validate_order([module(), invalid])

    def test_invalid_metadata_cannot_silently_omit_inputs(self):
        invalid = module([{'type': 'csampler', 'name': 'snd'},
                          {'type': 'cfilein', 'name': 'impulse'}],
                         {'primary_input': 'snd', 'auxiliary_inputs': []})
        self.assertIsNone(invalid.primary_input)

    def test_failed_append_and_move_preserve_order_and_selection(self):
        session = ChainSession()
        table = module([{'type': 'cfilein', 'name': 'table'}])
        stream = module()
        session.append(table)
        session.append(stream)
        with self.assertRaises(ValueError):
            session.move(table, 1)
        with self.assertRaises(ValueError):
            duplicate = module()
            duplicate.id = stream.id
            session.append(duplicate)
        self.assertEqual(session.modules, [table, stream])
        self.assertIs(session.selected, stream)

    def test_remove_selection_and_empty_session(self):
        session = ChainSession()
        first, second = module(), module()
        session.append(first)
        session.append(second)
        session.remove(second)
        self.assertIs(session.selected, first)
        session.remove(first)
        self.assertIsNone(session.selected)
        self.assertEqual(session.view, 'chain')

    def test_duplicate_instance_ids_rejected(self):
        first, second = module(), module()
        second.id = first.id
        with self.assertRaisesRegex(ValueError, 'unique'):
            ChainSession.validate_order([first, second])

    def test_branches_mix_outputs_and_inactive_nodes(self):
        session = ChainSession()
        nodes = [module() for _ in range(5)]
        for node in nodes:
            session.append(node)
        source, left, right, merge, inactive = nodes
        self.assertEqual(session.active_modules(), [source])
        session.disconnect(source.id)
        for a, b in [(source, left), (source, right), (left, merge), (right, merge)]:
            session.connect(a.id, b.id)
        session.connect(merge.id)
        session.connect(left.id)
        self.assertEqual(session.active_modules(), nodes[:-1])
        self.assertEqual(len(session.topological_order()), 5)
        snapshot = session.routing_snapshot()
        for a, b in [(merge, source), (merge, left), (left, left), (source, left)]:
            with self.assertRaises(ValueError):
                session.connect(a.id, b.id)
            self.assertEqual(session.routing_snapshot(), snapshot)
        with self.assertRaises(ValueError):
            session.connect(left.id)
        with self.assertRaises(ValueError):
            session.remove(source)
        session.remove(right)
        self.assertTrue(all(right.id not in edge for edge in session.connections))
        self.assertEqual(session.active_modules(), [source, left, merge])
        session.disconnect(source.id, left.id)
        self.assertEqual(session.active_modules(), [])

    def test_source_replacement_preserves_routes_and_positions(self):
        session = ChainSession()
        source, downstream, replacement = module(), module(), module([])
        session.append(source)
        session.append(downstream)
        session.connect(source.id, downstream.id)
        session.positions[downstream.id] = [300, 120]
        session.replace(source, replacement)
        self.assertIs(session.source, replacement)
        self.assertEqual(session.connections, [[replacement.id, downstream.id]])
        self.assertEqual(session.output_connections, [replacement.id])
        self.assertEqual(session.positions[downstream.id], [300, 120])
        session.validate_graph()

    def test_multiple_sources_selection_removal_and_role_changes(self):
        session = ChainSession()
        first, processor, second = module(), module(), module([])
        for node in (first, processor, second):
            session.append(node)
        self.assertEqual(session.sources, [first, second])
        self.assertIs(session.source, second)
        session.select(processor)
        self.assertIs(session.source, second)
        session.connect(second.id, processor.id)
        session.connect(processor.id)
        with self.assertRaises(ValueError):
            session.connect(processor.id, second.id)
        session.remove(first)
        self.assertEqual(session.active_modules(), [second, processor])
        self.assertIs(session.source, second)
        session.remove(processor)
        session.remove(second)
        self.assertEqual(session.source_ids, [])
        self.assertIsNone(session.source)
        first, processor = module(), module()
        session.append(first)
        session.append(processor)
        session.set_source(processor, True)
        self.assertIs(session.source, processor)
        session.set_source(processor, False)
        self.assertIs(session.source, first)
        with self.assertRaises(ValueError):
            session.set_source(first, False)

    def test_version_two_migrates_single_source_graph(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'graph.c5chain'
            path.write_text(json.dumps(dict(format='cecilia-chain', version=2,
                modules=[{'id': 'a'}, {'id': 'b'}], output={}, source_id='a',
                connections=[['a', 'b']], output_connections=['b'], positions={'b': [300, 80]})))
            document = read_session(path)
            self.assertEqual(document['version'], 3)
            self.assertEqual(document['source_ids'], ['a'])
            self.assertEqual(document['source_id'], 'a')
            self.assertEqual(document['positions'], {'b': [300, 80]})

    def test_mix_gain(self):
        self.assertEqual(mix_signals([2]), 2)
        self.assertAlmostEqual(mix_signals([2, 3]), 5 * .707)
        self.assertAlmostEqual(mix_signals([2, 3, 4]), 9 * .707)
        with self.assertRaises(ValueError):
            mix_signals([])

    def test_version_one_migrates_serial_routes(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'old.c5chain'
            path.write_text(json.dumps(dict(format='cecilia-chain', version=1,
                modules=[{'id': 'a'}, {'id': 'b'}, {'id': 'c'}], output={})))
            document = read_session(path)
            self.assertEqual(document['version'], 3)
            self.assertEqual(document['source_id'], 'a')
            self.assertEqual(document['connections'], [['a', 'b'], ['b', 'c']])
            self.assertEqual(document['output_connections'], ['c'])

    def test_invalid_graph_fields_are_rejected(self):
        session = ChainSession()
        source = module()
        session.append(source)
        for routing in [dict(source_id='missing'), dict(connections=[['missing', source.id]]),
                        dict(output_connections=['missing']), dict(positions={source.id: [float('nan'), 0]})]:
            original = session.routing_snapshot()
            session.restore_routing({**original, **routing})
            with self.assertRaises(ValueError):
                session.validate_graph()
            session.restore_routing(original)

    def test_runtime_callbacks_retain_owner_and_restore_nested_context(self):
        @bind_instance
        class Callback:
            def __init__(self):
                pass

            def update(self):
                return active_instance.get()

            def fail(self):
                raise RuntimeError('failure')

        first, second = module(), module()
        with instance_context(first):
            callback = Callback()
        with instance_context(second):
            self.assertIs(callback.update(), first)
            with self.assertRaises(RuntimeError):
                callback.fail()
            self.assertIs(active_instance.get(), second)
        self.assertIsNone(active_instance.get())

    def test_session_round_trip_with_relative_paths_and_embedded_settings(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, 'session.c5chain')
            snapshot = {
                'modules': [{'id': 'a', 'module_path': os.path.join(root, 'module.c5'),
                             'settings': {'userInputs': {'snd': {'path': os.path.join(root, 'sound.wav')}},
                                          'userSliders': {'level': [0.25, 1, 0]}}}],
                'output': {'totalTime': 12, 'plugins': {}}, 'selected_id': 'a', 'view': 'chain',
            }
            snapshot.update(serial_routing(snapshot['modules']))
            write_session(path, snapshot)
            with open(path) as stream:
                encoded = json.load(stream)
            self.assertEqual(encoded['modules'][0]['module_path'], 'module.c5')
            self.assertEqual(encoded['modules'][0]['settings']['userInputs']['snd']['path'], 'sound.wav')
            decoded = read_session(path)
            decoded.pop('version'); decoded.pop('format')
            self.assertEqual(decoded, snapshot)

    def test_failed_save_preserves_previous_file(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, 'session.c5chain')
            Path(path).write_text('previous session')
            with patch('Resources.Session.os.replace', side_effect=OSError('disk failure')):
                with self.assertRaises(OSError):
                    write_session(path, {'modules': [], 'output': {}})
            self.assertEqual(Path(path).read_text(), 'previous session')
            self.assertEqual(os.listdir(root), ['session.c5chain'])

    def test_unknown_session_version_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            path = os.path.join(root, 'session.c5chain')
            Path(path).write_text(json.dumps({'format': 'cecilia-chain', 'version': 99}))
            with self.assertRaisesRegex(ValueError, 'version'):
                read_session(path)


if __name__ == '__main__':
    unittest.main()
