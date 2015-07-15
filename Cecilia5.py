#! /usr/bin/env python
# encoding: utf-8
"""
Copyright 2013 iACT, Universite de Montreal, Jean Piche, Olivier Belanger, Jean-Michel Dumas

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
from Resources.constants import *
import wx
import os, sys, random
from Resources import audio, CeciliaMainFrame
import Resources.CeciliaLib as CeciliaLib
from Resources.splash import CeciliaSplashScreen

class CeciliaApp(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)

    def MacOpenFile(self, filename):
        CeciliaLib.getVar("mainFrame").onOpen(filename)

def onStart():
    ceciliaMainFrame = CeciliaMainFrame.CeciliaMainFrame(None, -1)
    CeciliaLib.setVar("mainFrame", ceciliaMainFrame)

    file = None
    if len(sys.argv) >= 2:
        file = sys.argv[1]

    if file:
        ceciliaMainFrame.onOpen(file)
    else:
        categories = [folder for folder in os.listdir(MODULES_PATH) if not folder.startswith(".")]
        category = random.choice(categories)
        files = [f for f in os.listdir(os.path.join(MODULES_PATH, category)) if f.endswith(FILE_EXTENSION)]
        file = random.choice(files)
        ceciliaMainFrame.onOpen(os.path.join(MODULES_PATH, category, file), True)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    if not os.path.isdir(TMP_PATH):
        os.mkdir(TMP_PATH)
    if not os.path.isfile(os.path.join(TMP_PATH,'.recent.txt')):
        f = open(os.path.join(TMP_PATH,'.recent.txt'), "w")
        f.close()
    if not os.path.isdir(AUTOMATION_SAVE_PATH):
        os.mkdir(AUTOMATION_SAVE_PATH)

    audioServer = audio.AudioServer()
    CeciliaLib.setVar("audioServer", audioServer)

    try:
        CeciliaLib.queryAudioMidiDrivers()
    except:
        pass

    app = CeciliaApp(redirect=False)
    wx.Log.SetLogLevel(0)
    wx.SetDefaultPyEncoding('utf-8')

    try:
        display = wx.Display()
        numDisp = display.GetCount()
        if CeciliaLib.getVar("DEBUG"):
            print 'Numbers of displays:', numDisp
        displays = []
        displayOffset = []
        displaySize = []
        for i in range(numDisp):
            displays.append(wx.Display(i))
            offset = displays[i].GetGeometry()[:2]
            size = displays[i].GetGeometry()[2:]
            if CeciliaLib.getVar("DEBUG"):
                print 'display %d:' % i
                print '    pos =', offset
                print '    size =', size
                print
            displayOffset.append(offset)
            displaySize.append(size)
    except:
        numDisp = 1
        displayOffset = [(0, 0)]
        displaySize = [(1024, 768)]

    CeciliaLib.setVar("numDisplays", numDisp)
    CeciliaLib.setVar("displayOffset", displayOffset)
    CeciliaLib.setVar("displaySize", displaySize)

    sp = CeciliaSplashScreen(None, img=CeciliaLib.ensureNFD(SPLASH_FILE_PATH), callback=onStart)

    app.MainLoop()
