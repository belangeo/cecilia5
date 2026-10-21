"""Native popup menus that keep queued GUI updates moving on Windows."""

import wx


def popup_menu(window, menu, position=wx.DefaultPosition):
    if wx.Platform != '__WXMSW__':
        return window.PopupMenu(menu, position)

    # TrackPopupMenu runs a native event loop, bypassing wx's normal pending
    # event processing. A native timer keeps CallAfter updates flowing even
    # when the mouse is still. Do not yield into another native event loop.
    processing = False

    def process_pending():
        nonlocal processing
        if processing:
            return
        processing = True
        try:
            wx.GetApp().ProcessPendingEvents()
        finally:
            processing = False

    timer = wx.PyTimer(process_pending)
    timer.Start(30)
    try:
        return window.PopupMenu(menu, position)
    finally:
        timer.Stop()
