#! /usr/bin/env python
# encoding: utf-8
"""
Copyright 2011 iACT, Universite de Montreal, Jean Piche, Olivier Belanger, Jean-Michel Dumas

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

import wx
import os, sys
from Resources import audio, CeciliaMainFrame
from Resources.constants import *
import Resources.CeciliaLib as CeciliaLib

def GetRoundBitmap( w, h, r ):
    maskColor = wx.Color(0,0,0)
    shownColor = wx.Color(5,5,5)
    b = wx.EmptyBitmap(w,h)
    dc = wx.MemoryDC(b)
    dc.SetBrush(wx.Brush(maskColor))
    dc.DrawRectangle(0,0,w,h)
    dc.SetBrush(wx.Brush(shownColor))
    dc.SetPen(wx.Pen(shownColor))
    dc.DrawRoundedRectangle(0,0,w,h,r)
    dc.SelectObject(wx.NullBitmap)
    b.SetMaskColour(maskColor)
    return b

def GetRoundShape( w, h, r ):
    return wx.RegionFromBitmap(GetRoundBitmap(w,h,r))

class CeciliaApp(wx.PySimpleApp):
    def __init__(self, *args, **kwargs):
        wx.PySimpleApp.__init__(self, *args, **kwargs)
 
    def MacOpenFile(self, filename):
        CeciliaLib.getVar("mainFrame").onOpen(filename)

class CeciliaSplashScreen(wx.Frame):
    def __init__(self, parent, y_pos):
        wx.Frame.__init__(self, parent, -1, "", pos=(-1, y_pos),
                         style = wx.FRAME_SHAPED | wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self.bmp = wx.Bitmap(os.path.join(RESOURCES_PATH, "Cecilia_splash.png"), wx.BITMAP_TYPE_PNG)
        w, h = self.bmp.GetWidth(), self.bmp.GetHeight()
        self.SetClientSize((w, h))

        if CeciliaLib.getVar("systemPlatform") == 'linux2':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
        else:
            self.SetWindowShape()

        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bmp, 0,0,True)

        self.fc = wx.FutureCall(2000, self.OnClose)

        self.Center(wx.HORIZONTAL)
        if CeciliaLib.getVar("systemPlatform") == 'win32':
            self.Center(wx.VERTICAL)
            
        self.Show(True)
        
    def SetWindowShape(self, *evt):
        r = GetRoundShape(502,248,10)
        self.hasShape = self.SetShape(r)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0,0,True)
     
    def OnClose(self):
        self.Destroy()
        #if not CeciliaLib.getVar("useMidi"):
        #    CeciliaLib.showErrorDialog("Midi not initialized!", "If you want to use Midi, please connect your interface and restart Cecilia")    
        
if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    global ceciliaPreferences

    if not os.path.isdir(TMP_PATH):
        os.mkdir(TMP_PATH)
    if not os.path.isfile(os.path.join(TMP_PATH,'.recent.txt')):    
        f = open(os.path.join(TMP_PATH,'.recent.txt'), "w")
        f.close()
    if not os.path.isdir(AUTOMATION_SAVE_PATH):
        os.mkdir(AUTOMATION_SAVE_PATH)

    file = None
    if len(sys.argv) >= 2:
        file = sys.argv[1]

    audioServer = audio.AudioServer()
    CeciliaLib.setVar("audioServer", audioServer)
    
    app = CeciliaApp()
    wx.SetDefaultPyEncoding('utf-8')
    X,Y = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X), wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
    if CeciliaLib.getVar("systemPlatform") == 'linux2':
        bmp = wx.Bitmap(os.path.join(RESOURCES_PATH, "Cecilia_splash.png"), wx.BITMAP_TYPE_PNG)
        sp = wx.SplashScreen(bitmap=bmp, splashStyle=wx.SPLASH_TIMEOUT, milliseconds=3000, parent=None)
        sp.Center()
    else:
        sp_y = Y/4
        sp = CeciliaSplashScreen(None, sp_y)
    display = wx.Display()
    numDisp = display.GetCount()
    CeciliaLib.setVar("numDisplays", numDisp)
    print 'Numbers of displays:', numDisp
    displays = []
    displayOffset = []
    displaySize = []
    for i in range(numDisp):
        displays.append(wx.Display(i))
        offset = displays[i].GetGeometry()[:2]
        size = displays[i].GetGeometry()[2:]
        print 'display %d:' % i
        print '    pos =', offset
        print '    size =', size
        displayOffset.append(offset)
        displaySize.append(size)
    CeciliaLib.setVar("displayOffset", displayOffset)
    CeciliaLib.setVar("displaySize", displaySize)

    ceciliaMainFrame = CeciliaMainFrame.CeciliaMainFrame(None, -1)
    CeciliaLib.setVar("mainFrame", ceciliaMainFrame)
    
    try:
        CeciliaLib.queryAudioMidiDrivers()
    except:
        pass
    
    if file:
        ceciliaMainFrame.onOpen(file)
    else:
        ceciliaMainFrame.onOpen(os.path.join(MODULES_PATH, "Dynamics", "ArcTanDisto.cec"))

    app.MainLoop()

