#!/usr/bin/env python
# encoding: utf-8

import wx, sys, os
from Resources.constants import *

def GetRoundBitmap(w, h, r):
    maskColour = wx.Colour(0,0,0)
    shownColour = wx.Colour(5,5,5)
    b = wx.EmptyBitmap(w,h)
    dc = wx.MemoryDC(b)
    dc.SetBrush(wx.Brush(maskColour))
    dc.DrawRectangle(0,0,w,h)
    dc.SetBrush(wx.Brush(shownColour))
    dc.SetPen(wx.Pen(shownColour))
    dc.DrawRoundedRectangle(0, 0, w, h, r)
    dc.SelectObject(wx.NullBitmap)
    b.SetMaskColour(maskColour)
    return b

def GetRoundShape(w, h, r=17):
    return wx.RegionFromBitmap(GetRoundBitmap(w,h,r))

class CeciliaSplashScreen(wx.Frame):
    def __init__(self, parent, img, callback):
        display = wx.Display(0)
        size = display.GetGeometry()[2:]
        wx.Frame.__init__(self, parent, -1, "", pos=(-1, size[1]/6),
                         style = wx.FRAME_SHAPED | wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
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

        self.fc = wx.FutureCall(2500, self.OnClose)

        self.Center(wx.HORIZONTAL)
        if sys.platform == 'win32':
            self.Center(wx.VERTICAL)
            
        wx.CallAfter(self.Show)
        
    def SetWindowShape(self, *evt):
        r = GetRoundShape(self.w, self.h)
        self.hasShape = self.SetShape(r)

    def OnPaint(self, evt):
        w,h = self.GetSize()
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen("#000000"))
        dc.SetBrush(wx.Brush("#000000"))
        dc.DrawRectangle(0,0,w,h)
        dc.DrawBitmap(self.bmp, 0,0,True)
        dc.SetTextForeground("#333333")
        font = dc.GetFont()
        font.SetFaceName(FONT_FACE)
        font.SetPixelSize((15,15))
        dc.SetFont(font)
        dc.DrawLabel("Cecilia %s" % APP_VERSION, wx.Rect(280, 185, 200, 15), wx.ALIGN_RIGHT)
        dc.DrawLabel(u"Spirit of the project: Jean Piché", wx.Rect(280, 200, 200, 15), wx.ALIGN_RIGHT)
        dc.DrawLabel(u"Programmed by: Olivier Bélanger", wx.Rect(280, 215, 200, 15), wx.ALIGN_RIGHT)
        dc.DrawLabel(APP_COPYRIGHT, wx.Rect(280, 230, 200, 15), wx.ALIGN_RIGHT)

    def OnClose(self):
        self.callback()
        self.Destroy()
