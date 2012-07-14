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

import wx, os
from constants import *
import CeciliaLib

def buildFileTree():
    root = MODULES_PATH
    directories = []
    files = {}
    for dir in os.listdir(MODULES_PATH):
        if not dir.startswith('.'):
            directories.append(dir)
            files[dir] = []
            for f in os.listdir(os.path.join(root, dir)):
                if not f.startswith('.'):
                    files[dir].append(f)
    return root, directories, files

class InterfaceMenuBar(wx.MenuBar):
    def __init__(self, frame, mainFrame=None):
        wx.MenuBar.__init__(self, wx.MB_DOCKABLE)
        self.frame = frame
        if mainFrame:
            self.mainFrame = mainFrame
        else:
            self.mainFrame = CeciliaLib.getVar("mainFrame")

        # File Menu
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(ID_OPEN, 'Open...\tCtrl+O', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onOpen, id=ID_OPEN)
        self.fileMenu.Append(ID_OPEN_RANDOM, 'Open Random...\tShift+Ctrl+O', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onOpenRandom, id=ID_OPEN_RANDOM)

        ######## Implement the Open builtin menu #########
        self.root, self.directories, self.files = buildFileTree()
        self.openBuiltinMenu = wx.Menu()
        subId1 = ID_OPEN_BUILTIN
        for dir in self.directories:
            menu = wx.Menu()
            self.openBuiltinMenu.AppendMenu(-1, dir, menu)
            for f in self.files[dir]:
                menu.Append(subId1, f)
                self.frame.Bind(wx.EVT_MENU, self.mainFrame.onOpenBuiltin, id=subId1)
                subId1 += 1
                
        prefPath = CeciliaLib.getVar("prefferedPath")
        if prefPath:
            for path in prefPath.split(';'):
                if not os.path.isdir(path):
                    continue
                menu = wx.Menu(os.path.split(path)[1])
                self.openBuiltinMenu.AppendMenu(-1, os.path.split(path)[1], menu)
                files = os.listdir(path)
                for file in files:
                    if os.path.isfile(os.path.join(path, file)):
                        ok = False
                        try:
                            ext = file.rsplit('.')[1]
                            if ext == FILE_EXTENSION:
                                ok = True
                        except:
                            ok = False 
                        if ok:
                            menu.Append(subId1, file)
                            self.frame.Bind(wx.EVT_MENU, self.mainFrame.onOpenPrefModule, id=subId1)
                            subId1 += 1
                
        self.fileMenu.AppendMenu(-1, 'Modules', self.openBuiltinMenu)

        self.openRecentMenu = wx.Menu()
        subId2 = ID_OPEN_RECENT
        recentFiles = []
        filename = os.path.join(TMP_PATH,'.recent.txt')
        if os.path.isfile(filename):
            f = open(filename, "r")
            for line in f.readlines():
                recentFiles.append(line)
            f.close()    
        if recentFiles:
            for file in recentFiles:
                self.openRecentMenu.Append(subId2, file)
                subId2 += 1
        if subId2 > ID_OPEN_RECENT:
            for i in range(ID_OPEN_RECENT,subId2):
                self.frame.Bind(wx.EVT_MENU, self.mainFrame.openRecent, id=i) 

        self.fileMenu.AppendMenu(-1,'Open Recent', self.openRecentMenu, 'Access previously opened files in Cecilia')
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(ID_SAVE, 'Save\tCtrl+S', 'Save changes made on the current module', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onSave, id=ID_SAVE)
        self.fileMenu.Append(ID_SAVEAS, 'Save as...\tShift+Ctrl+s', 'Save the current module as... (.cec file)', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onSaveAs, id=ID_SAVEAS)
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(ID_UPDATE_INTERFACE, 'Reload module\tCtrl+R', 'Reload the current module', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.reloadCurrentModule, id=ID_UPDATE_INTERFACE)
        self.fileMenu.AppendSeparator()
        pref_item = self.fileMenu.Append(wx.ID_PREFERENCES, 'Preferences...\tCtrl+,', 'Open Cecilia preferences pane', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onPreferences, pref_item)
        self.fileMenu.AppendSeparator()
        quit_item = self.fileMenu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit Cecilia', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onQuit, quit_item)

        # Edit Menu
        self.editMenu = wx.Menu()
        self.editMenu.Append(ID_UNDO, 'Undo\tCtrl+Z', 'Undo the last change', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.frame.onUndo, id=ID_UNDO)
        self.editMenu.Append(ID_REDO, 'Redo\tShift+Ctrl+Z', 'Redo the last change', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.frame.onRedo, id=ID_REDO)
        self.editMenu.AppendSeparator()
        self.editMenu.Append(ID_COPY, 'Copy\tCtrl+C', 'Copy the text selected in the clipboard', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.frame.onCopy, id=ID_COPY)
        self.editMenu.Append(ID_PASTE, 'Paste\tCtrl+V', 'Paste the text in the clipboard', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.frame.onPaste, id=ID_PASTE)
        self.editMenu.AppendSeparator()
        self.editMenu.Append(ID_REMEMBER, 'Remember input sound', 'Find an expression in the text and replace it', kind=wx.ITEM_CHECK)
        self.editMenu.FindItemById(ID_REMEMBER).Check(CeciliaLib.getVar("rememberedSound"))
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onRememberInputSound, id=ID_REMEMBER)

        # Action Options Menu
        actionMenu = wx.Menu()
        actionMenu.Append(ID_PLAY_STOP, 'Play / Stop\tCtrl+.', 'Start and stop audio server')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onShortPlayStop, id=ID_PLAY_STOP)
        actionMenu.AppendSeparator()
        actionMenu.Append(ID_BOUNCE, 'Bounce to disk\tCtrl+B', 'Record the audio processing in a soundfile')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onBounceToDisk, id=ID_BOUNCE)
        actionMenu.AppendSeparator()
        actionMenu.Append(ID_USE_MIDI, 'Use MIDI', 'Allow Cecilia to use a midi device.', kind=wx.ITEM_CHECK)
        if CeciliaLib.getVar("useMidi") == 1: midiCheck = True
        else: midiCheck = False
        actionMenu.FindItemById(ID_USE_MIDI).Check(midiCheck)
        actionMenu.FindItemById(ID_USE_MIDI).Enable(False)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onUseMidi, id=ID_USE_MIDI)
    
        windowMenu = wx.Menu()
        windowMenu.Append(3002, 'Eh Oh Mario!\tShift+Ctrl+E', '', kind=wx.ITEM_CHECK)
        self.frame.Bind(wx.EVT_MENU, self.marioSwitch, id=3002)

        helpMenu = wx.Menu()        
        helpItem = helpMenu.Append(wx.ID_ABOUT, '&About %s %s' % (APP_NAME, APP_VERSION), 'wxPython RULES!!!')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onHelpAbout, helpItem)
        infoItem = helpMenu.Append(ID_MODULE_INFO, 'Show module info\tCtrl+I', '')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onModuleAbout, infoItem)
 
        self.Append(self.fileMenu, '&File')
        self.Append(self.editMenu, '&Edit')
        self.Append(actionMenu, '&Action')
        self.Append(windowMenu, '&Window')
        self.Append(helpMenu, '&Help')

    def marioSwitch(self, evt):
        if evt.GetInt() == 1:
            self.FindItemById(3002).Check(1)
            for slider in CeciliaLib.getVar("userSliders"):
                slider.slider.useMario = True
                slider.slider.Refresh()
        else:
            self.FindItemById(3002).Check(0)
            for slider in CeciliaLib.getVar("userSliders"):
                slider.slider.useMario = False 
                slider.slider.Refresh()
               
