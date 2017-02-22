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
import os, sys, random
import wx
from Resources.constants import *
from Resources import audio, CeciliaMainFrame
from Resources.splash import CeciliaSplashScreen
import Resources.CeciliaLib as CeciliaLib

class CeciliaApp(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)

    def MacOpenFiles(self, filenames):
        if type(filenames) == list:
            filenames = filenames[0]
        if CeciliaLib.getVar("mainFrame") is not None:
            CeciliaLib.getVar("mainFrame").onOpen(filenames)

    def MacReopenApp(self):
        try:
            CeciliaLib.getVar("mainFrame").Raise()
        except:
            pass

def onStart():
    ceciliaMainFrame = CeciliaMainFrame.CeciliaMainFrame(None, -1)
    CeciliaLib.setVar("mainFrame", ceciliaMainFrame)

    file = ""
    if len(sys.argv) > 1:
        file = sys.argv[1]

    if os.path.isfile(file):
        ceciliaMainFrame.onOpen(file)
    else:
        categories = [folder for folder in os.listdir(MODULES_PATH) if not folder.startswith(".")]
        category = random.choice(categories)
        files = [f for f in os.listdir(os.path.join(MODULES_PATH, category)) if f.endswith(FILE_EXTENSION)]
        file = random.choice(files)
        ceciliaMainFrame.onOpen(os.path.join(MODULES_PATH, category, file), True)

if __name__ == '__main__':

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
    if sys.version_info[0] < 3:
        wx.SetDefaultPyEncoding('utf-8')

    try:
        display = wx.Display()
        numDisp = display.GetCount()
        if CeciliaLib.getVar("DEBUG"):
            print('Numbers of displays:', numDisp)
        displays = []
        displayOffset = []
        displaySize = []
        for i in range(numDisp):
            displays.append(wx.Display(i))
            offset = displays[i].GetGeometry()[:2]
            size = displays[i].GetGeometry()[2:]
            if CeciliaLib.getVar("DEBUG"):
                print('display %d:' % i)
                print('    pos =', offset)
                print('    size =', size)
                print()
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
