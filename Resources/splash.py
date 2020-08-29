"""
Copyright 2019 iACT, Universite de Montreal,
Jean Piche, Olivier Belanger, Jean-Michel Dumas

This file is part of Cecilia 5.

Cecilia 5 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Cecilia 5 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cecilia 5.  If not, see <http://www.gnu.org/licenses/>.
"""

import wx, sys, os
from .constants import *

def GetRoundBitmap(w, h, r):
    maskColour = wx.Colour(0, 0, 0)
    if sys.platform == "darwin":
        shownColour = wx.Colour(5, 5, 5, wx.ALPHA_TRANSPARENT)
    else:
        shownColour = wx.Colour(5, 5, 5)
    b = wx.EmptyBitmap(w, h)
    dc = wx.MemoryDC(b)
    dc.SetBrush(wx.Brush(maskColour))
    dc.DrawRectangle(0, 0, w, h)
    dc.SetBrush(wx.Brush(shownColour))
    dc.SetPen(wx.Pen(shownColour))
    dc.DrawRoundedRectangle(0, 0, w, h, r)
    dc.SelectObject(wx.NullBitmap)
    b.SetMaskColour(maskColour)
    return b

def GetRoundShape(w, h, r):
    return wx.Region(GetRoundBitmap(w, h, r))

class CeciliaSplashScreen(wx.Frame):
    def __init__(self, parent, img, callback):
        display = wx.Display(0)
        size = display.GetGeometry()[2:]
        wx.Frame.__init__(self, parent, -1, "", pos=(-1, size[1] // 6),
                         style=wx.FRAME_SHAPED | wx.BORDER_SIMPLE | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.SetBackgroundColour(wx.Colour(0, 0, 0, wx.ALPHA_TRANSPARENT))

        self.callback = callback

        self.bmp = wx.Bitmap(os.path.join(img), wx.BITMAP_TYPE_PNG)
        self.w, self.h = self.bmp.GetWidth(), self.bmp.GetHeight()
        self.SetClientSize((self.w, self.h))

        if wx.Platform == "__WXGTK__":
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
        else:
            self.SetWindowShape()

        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bmp, 0, 0, True)

        wx.CallLater(2500, self.OnClose)

        self.Center(wx.HORIZONTAL)
        if sys.platform == 'win32':
            self.Center(wx.VERTICAL)

        wx.CallAfter(self.Show)

    def SetWindowShape(self, *evt):
        r = GetRoundShape(self.w, self.h, 17)
        self.SetShape(r)

    def OnPaint(self, evt):
        w, h = self.GetSize()
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0, wx.ALPHA_TRANSPARENT)))
        dc.SetBrush(wx.Brush(wx.Colour(0, 0, 0, wx.ALPHA_TRANSPARENT)))
        dc.DrawRectangle(0, 0, w, h)
        dc.DrawBitmap(self.bmp, 0, 0, True)
        dc.SetTextForeground("#333333")
        font, psize = dc.GetFont(), dc.GetFont().GetPointSize()
        if sys.platform != "win32":
            font.SetFaceName("Monaco")
            if sys.platform.startswith("linux"):
                font.SetPointSize(psize - 2)
            else:
                font.SetPointSize(psize)
        dc.SetFont(font)
        dc.DrawLabel("Cecilia %s" % APP_VERSION, wx.Rect(280, 185, 200, 15), wx.ALIGN_RIGHT)
        dc.DrawLabel("Spirit of the project: Jean Piche", wx.Rect(280, 200, 200, 15), wx.ALIGN_RIGHT)
        dc.DrawLabel("Programmed by: Olivier Belanger", wx.Rect(280, 215, 200, 15), wx.ALIGN_RIGHT)
        dc.DrawLabel(APP_COPYRIGHT, wx.Rect(280, 230, 200, 15), wx.ALIGN_RIGHT)

    def OnClose(self):
        self.callback()
        self.Destroy()