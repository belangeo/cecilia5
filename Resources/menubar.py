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
from .constants import *
import Resources.CeciliaLib as CeciliaLib

class InterfaceMenuBar(wx.MenuBar):
    def __init__(self, frame, mainFrame=None):
        wx.MenuBar.__init__(self, wx.MB_DOCKABLE)
        self.frame = frame
        if mainFrame:
            self.mainFrame = mainFrame
        else:
            self.mainFrame = CeciliaLib.getVar("mainFrame")
        inMainFrame = False
        if frame == mainFrame:
            inMainFrame = True

        # File Menu
        self.fileMenu = wx.Menu()
        self.fileMenu.Append(ID_OPEN, 'Open...\tCtrl+O', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onOpen, id=ID_OPEN)
        self.fileMenu.Append(ID_OPEN_RANDOM, 'Open Random...\tShift+Ctrl+O', kind=wx.ITEM_NORMAL)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onOpenRandom, id=ID_OPEN_RANDOM)

        ######## Implement the Open builtin menu #########
        self.root, self.directories, self.files = CeciliaLib.buildFileTree()
        self.openBuiltinMenu = wx.Menu()
        subId1 = ID_OPEN_BUILTIN
        for dir in self.directories:
            menu = wx.Menu()
            self.openBuiltinMenu.AppendSubMenu(menu, dir)
            for f in self.files[dir]:
                menu.Append(subId1, f)
                self.frame.Bind(wx.EVT_MENU, self.mainFrame.onOpenBuiltin, id=subId1)
                subId1 += 1

        prefPath = CeciliaLib.getVar("prefferedPath")
        if prefPath:
            for path in prefPath.split(';'):
                path = CeciliaLib.ensureNFD(path)
                if not os.path.isdir(path):
                    continue
                menu = wx.Menu(os.path.split(path)[1])
                self.openBuiltinMenu.AppendSubMenu(menu, os.path.split(path)[1])
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
                            try:
                                menu.Append(subId1, CeciliaLib.ensureNFD(file))
                                self.frame.Bind(wx.EVT_MENU, self.mainFrame.onOpenPrefModule, id=subId1)
                                subId1 += 1
                            except:
                                pass

        self.fileMenu.AppendSubMenu(self.openBuiltinMenu, 'Modules')

        self.openRecentMenu = wx.Menu()
        subId2 = ID_OPEN_RECENT
        recentFiles = []
        filename = os.path.join(TMP_PATH, '.recent.txt')
        if os.path.isfile(filename):
            f = open(filename, "r")
            for line in f.readlines():
                try:
                    recentFiles.append(line)
                except:
                    pass
            f.close()
        if recentFiles:
            for file in recentFiles:
                try:
                    self.openRecentMenu.Append(subId2, CeciliaLib.ensureNFD(file).replace("\n", ""))
                    subId2 += 1
                except:
                    pass
        if subId2 > ID_OPEN_RECENT:
            for i in range(ID_OPEN_RECENT, subId2):
                self.frame.Bind(wx.EVT_MENU, self.mainFrame.openRecent, id=i)

        self.fileMenu.AppendSubMenu(self.openRecentMenu, 'Open Recent')
        self.fileMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        self.fileMenu.Append(ID_SAVEAS, 'Save Module As...\tShift+Ctrl+s')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onSaveAs, id=ID_SAVEAS)
        self.fileMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        self.fileMenu.Append(ID_OPEN_AS_TEXT, 'Open Module As Text\tCtrl+E')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.openModuleAsText, id=ID_OPEN_AS_TEXT)
        self.fileMenu.Append(ID_UPDATE_INTERFACE, 'Reload Module\tCtrl+R')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.reloadCurrentModule, id=ID_UPDATE_INTERFACE)
        if CeciliaLib.getVar("systemPlatform").startswith("linux") or CeciliaLib.getVar("systemPlatform") == 'win32':
            self.fileMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        pref_item = self.fileMenu.Append(wx.ID_PREFERENCES, 'Preferences...\tCtrl+,')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onPreferences, pref_item)
        if CeciliaLib.getVar("systemPlatform").startswith("linux") or CeciliaLib.getVar("systemPlatform") == 'win32':
            self.fileMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        quit_item = self.fileMenu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onQuit, quit_item)

        # Edit Menu
        self.editMenu = wx.Menu()
        if not inMainFrame:
            self.editMenu.Append(ID_UNDO, 'Undo\tCtrl+Z')
            self.frame.Bind(wx.EVT_MENU, self.frame.onUndo, id=ID_UNDO)
            self.editMenu.Append(ID_REDO, 'Redo\tShift+Ctrl+Z')
            self.frame.Bind(wx.EVT_MENU, self.frame.onRedo, id=ID_REDO)
            self.editMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
            self.editMenu.Append(ID_COPY, 'Copy\tCtrl+C')
            self.frame.Bind(wx.EVT_MENU, self.frame.onCopy, id=ID_COPY)
            self.editMenu.Append(ID_PASTE, 'Paste\tCtrl+V')
            self.frame.Bind(wx.EVT_MENU, self.frame.onPaste, id=ID_PASTE)
            self.editMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
            self.editMenu.Append(ID_SELECT_ALL, 'Select All Points\tCtrl+A')
            self.frame.Bind(wx.EVT_MENU, self.frame.onSelectAll, id=ID_SELECT_ALL)
            self.editMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        self.editMenu.Append(ID_REMEMBER, 'Remember Input Sound', kind=wx.ITEM_CHECK)
        self.editMenu.FindItemById(ID_REMEMBER).Check(CeciliaLib.getVar("rememberedSound"))
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onRememberInputSound, id=ID_REMEMBER)

        # Action Options Menu
        self.actionMenu = wx.Menu()
        self.actionMenu.Append(ID_PLAY_STOP, 'Play / Stop\tCtrl+.')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onShortPlayStop, id=ID_PLAY_STOP)
        self.actionMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        self.actionMenu.Append(ID_BOUNCE, 'Bounce to Disk\tCtrl+B')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onBounceToDisk, id=ID_BOUNCE)
        self.actionMenu.Append(ID_BATCH_PRESET, 'Batch Processing on Preset Sequence')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onBatchProcessing, id=ID_BATCH_PRESET)
        self.actionMenu.Append(ID_BATCH_FOLDER, 'Batch Processing on Sound Folder')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onBatchProcessing, id=ID_BATCH_FOLDER)
        self.actionMenu.Append(ID_USE_SOUND_DUR, 'Use Sound Duration on Folder Batch Processing', kind=wx.ITEM_CHECK)
        if CeciliaLib.getVar("useSoundDur") == 1:
            self.actionMenu.FindItemById(ID_USE_SOUND_DUR).Check(True)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onUseSoundDuration, id=ID_USE_SOUND_DUR)
        self.actionMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        self.actionMenu.Append(ID_SHOW_SPECTRUM, 'Show Spectrum', kind=wx.ITEM_CHECK)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onShowSpectrum, id=ID_SHOW_SPECTRUM)
        if CeciliaLib.getVar('showSpectrum'):
            self.actionMenu.FindItemById(ID_SHOW_SPECTRUM).Check(True)
        self.actionMenu.Append(wx.ID_SEPARATOR, kind=wx.ITEM_SEPARATOR)
        self.actionMenu.Append(ID_USE_MIDI, 'Use MIDI', kind=wx.ITEM_CHECK)
        if CeciliaLib.getVar("useMidi") == 1: midiCheck = True
        else: midiCheck = False
        self.actionMenu.FindItemById(ID_USE_MIDI).Check(midiCheck)
        self.actionMenu.FindItemById(ID_USE_MIDI).Enable(False)
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onUseMidi, id=ID_USE_MIDI)

        windowMenu = wx.Menu()
        windowMenu.Append(ID_MARIO, 'Eh Oh Mario!\tShift+Ctrl+E', kind=wx.ITEM_CHECK)
        self.frame.Bind(wx.EVT_MENU, self.marioSwitch, id=ID_MARIO)

        helpMenu = wx.Menu()
        helpItem = helpMenu.Append(wx.ID_ABOUT, '&About %s %s' % (APP_NAME, APP_VERSION))
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onHelpAbout, helpItem)
        infoItem = helpMenu.Append(ID_MODULE_INFO, 'Show Module Info\tCtrl+I')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onModuleAbout, infoItem)
        docItem = helpMenu.Append(ID_DOC_FRAME, 'Show API Documentation\tCtrl+D')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onDocFrame, docItem)
        graphItem = helpMenu.Append(ID_GRAPH_FRAME, 'Show Grapher Help\tCtrl+G')
        self.frame.Bind(wx.EVT_MENU, self.mainFrame.onGraphFrame, graphItem)

        self.Append(self.fileMenu, '&File')
        self.Append(self.editMenu, '&Edit')
        self.Append(self.actionMenu, '&Action')
        self.Append(windowMenu, '&Window')
        self.Append(helpMenu, '&Help')

    def spectrumSwitch(self, state):
        self.actionMenu.FindItemById(ID_SHOW_SPECTRUM).Check(state)

    def marioSwitch(self, evt):
        if evt.GetInt() == 1:
            self.FindItemById(ID_MARIO).Check(1)
            for slider in CeciliaLib.getVar("userSliders"):
                slider.slider.useMario = True
                slider.slider.Refresh()
        else:
            self.FindItemById(ID_MARIO).Check(0)
            for slider in CeciliaLib.getVar("userSliders"):
                slider.slider.useMario = False
                slider.slider.Refresh()
