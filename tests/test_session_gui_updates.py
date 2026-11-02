"""Session restoration settles deferred control updates before its saved baseline."""
import ast
import copy
from contextlib import contextmanager, nullcontext
from contextvars import ContextVar
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

from Resources.Session import active_instance, instance_context


class SessionGuiUpdateTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'Resources/CeciliaLib.py').read_text())
        methods = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                   and node.name in ('callAfter', '_finishSessionGuiUpdates', 'sessionControlValue', 'setRuntimeValue')]
        self.wx = SimpleNamespace(Window=type('Window', (), {}), CallAfter=Mock())
        namespace = dict(copy=copy, contextmanager=contextmanager, active_instance=active_instance,
                         instance_context=instance_context, wx=self.wx,
                         _session_gui_updates=ContextVar('test_session_gui_updates', default=None),
                         session=SimpleNamespace(history=SimpleNamespace(
                             active=None, replaying=False, suspend=nullcontext)))
        exec(compile(ast.Module(body=methods, type_ignores=[]), '<session GUI updates>', 'exec'), namespace)
        self.session_value = namespace['sessionControlValue']
        self.runtime_value = namespace['setRuntimeValue']
        self.call_after = namespace['callAfter']
        self.finish_updates = namespace['_finishSessionGuiUpdates']

    def test_restoration_includes_nested_callbacks_before_capturing_baseline(self):
        state = {'gain': 0}
        def restore():
            state['gain'] = -6
            self.call_after(state.update, {'duration': 12})
        with self.finish_updates():
            self.call_after(restore)
            self.assertEqual(state, {'gain': 0})
        baseline = dict(state)
        self.assertEqual(baseline, {'gain': -6, 'duration': 12})
        self.wx.CallAfter.assert_not_called()
        # Normal callbacks still use wx's event queue after restoration.
        self.call_after(state.update, {'gain': -3})
        self.wx.CallAfter.call_args.args[0]()
        self.assertNotEqual(state, baseline)

    def test_failed_restore_discards_callbacks_and_restores_normal_dispatch(self):
        callback = Mock()
        with self.assertRaises(ValueError):
            with self.finish_updates():
                self.call_after(callback)
                raise ValueError('Restore failed')
        callback.assert_not_called()
        self.call_after(callback)
        self.wx.CallAfter.assert_called_once()
        self.wx.CallAfter.call_args.args[0]()
        callback.assert_called_once()

    def test_runtime_values_do_not_replace_edited_values(self):
        widget = SimpleNamespace(value=.5)
        widget.getValue = lambda: widget.value
        widget.setValue = lambda value: setattr(widget, 'value', value)
        self.runtime_value(widget, .2)
        self.runtime_value(widget, .7)
        self.assertEqual(widget.getValue(), .7)
        self.assertEqual(self.session_value(widget), .5)
        widget.setValue(.9)  # A real control edit must still persist.
        self.assertEqual(self.session_value(widget), .9)
        self.runtime_value(widget, .3)
        self.assertEqual(self.session_value(widget), .9)

    def test_range_runtime_values_are_copied(self):
        widget = SimpleNamespace(value=[.2, .8])
        widget.getValue = lambda: widget.value
        widget.setValue = lambda value: setattr(widget, 'value', value)
        self.runtime_value(widget, [.3, .7])
        saved = self.session_value(widget)
        saved[0] = 0
        self.assertEqual(self.session_value(widget), [.2, .8])
