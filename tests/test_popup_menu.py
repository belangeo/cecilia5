"""Popup event delivery, plus an opt-in native Windows regression test."""

import importlib.util
import os
from pathlib import Path
import runpy
import sys
import types
import unittest
from unittest.mock import Mock, patch


POPUP_MODULE = Path(__file__).resolve().parents[1] / 'Resources' / 'PopupMenu.py'


class PopupMenuTests(unittest.TestCase):
    def setUp(self):
        self.app = Mock()
        self.timer = Mock()
        self.wx = types.SimpleNamespace(
            Platform='__WXMSW__', DefaultPosition=object(),
            PyTimer=Mock(return_value=self.timer), GetApp=Mock(return_value=self.app))
        with patch.dict(sys.modules, {'wx': self.wx}):
            self.popup_menu = runpy.run_path(str(POPUP_MODULE))['popup_menu']
        self.window = Mock()
        self.menu = object()

    def test_pending_updates_run_while_menu_is_open(self):
        position = (10, 20)

        def native_menu(menu, pos):
            self.assertIs(menu, self.menu)
            self.assertEqual(pos, position)
            self.timer.Start.assert_called_once_with(30)
            self.timer.Stop.assert_not_called()
            tick = self.wx.PyTimer.call_args.args[0]
            tick()
            tick()
            self.assertEqual(self.app.ProcessPendingEvents.call_count, 2)
            return True

        self.window.PopupMenu.side_effect = native_menu
        self.assertTrue(self.popup_menu(self.window, self.menu, position))
        self.timer.Stop.assert_called_once_with()

    def test_timer_stops_if_menu_raises(self):
        self.window.PopupMenu.side_effect = RuntimeError('menu failed')
        with self.assertRaisesRegex(RuntimeError, 'menu failed'):
            self.popup_menu(self.window, self.menu)
        self.timer.Stop.assert_called_once_with()

    def test_nested_event_loop_does_not_reenter_pending_processing(self):
        def native_menu(menu, pos):
            tick = self.wx.PyTimer.call_args.args[0]
            self.app.ProcessPendingEvents.side_effect = tick
            tick()
            self.app.ProcessPendingEvents.assert_called_once_with()

        self.window.PopupMenu.side_effect = native_menu
        self.popup_menu(self.window, self.menu)

    def test_other_platforms_use_the_normal_popup(self):
        self.wx.Platform = '__WXGTK__'
        result = self.popup_menu(self.window, self.menu)
        self.assertIs(result, self.window.PopupMenu.return_value)
        self.window.PopupMenu.assert_called_once_with(self.menu, self.wx.DefaultPosition)
        self.wx.PyTimer.assert_not_called()


@unittest.skipUnless(sys.platform == 'win32' and
                     os.environ.get('CECILIA_GUI_TESTS') == '1' and
                     importlib.util.find_spec('wx') is not None,
                     'Requires Windows, wx and CECILIA_GUI_TESTS=1')
class NativePopupMenuTests(unittest.TestCase):
    def test_thread_updates_arrive_before_menu_closes_without_mouse_input(self):
        import ctypes
        import threading
        import time
        import wx

        popup_menu = runpy.run_path(str(POPUP_MODULE))['popup_menu']
        app = wx.GetApp() or wx.App(False)
        frame = wx.Frame(None, title='Popup update regression test')
        frame.Show()
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, 'Editor')
        menu.Append(wx.ID_ANY, 'Routing')
        opened = threading.Event()
        menu.Bind(wx.EVT_MENU_OPEN, lambda event: opened.set())
        delivered, before_close, errors = [], [], []

        def queue_updates():
            if opened.wait(2):
                for index in range(3):
                    time.sleep(.05)
                    wx.CallAfter(delivered.append, index)

        worker = threading.Thread(target=queue_updates)
        worker.start()

        def close_menu():
            before_close.extend(delivered)
            ctypes.windll.user32.EndMenu()

        # This native timer only dismisses the menu. All updates above come
        # from a worker thread, with no mouse or keyboard events to wake wx.
        closer = wx.PyTimer(close_menu)

        def open_menu():
            closer.Start(500, oneShot=True)
            try:
                popup_menu(frame, menu, (10, 10))
            except Exception as error:
                errors.append(error)
            finally:
                closer.Stop()
                app.ExitMainLoop()

        wx.CallAfter(open_menu)
        try:
            app.MainLoop()
            worker.join(3)
            self.assertEqual(errors, [])
            self.assertTrue(opened.is_set())
            self.assertEqual(before_close, [0, 1, 2])
        finally:
            menu.Destroy()
            frame.Destroy()
            app.ProcessPendingEvents()


if __name__ == '__main__':
    unittest.main()
