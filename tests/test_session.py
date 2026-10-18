import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from Resources.Session import (ChainSession, ModuleInstance, active_instance,
                               bind_instance, instance_context, read_session,
                               write_session)


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
            session.append(module([{'type': 'cfilein', 'name': 'table'}]))
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
