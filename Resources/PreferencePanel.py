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
import Resources.CeciliaLib as CeciliaLib
from .constants import *
from .Widgets import *

PADDING = 10

class PreferenceFrame(wx.Frame):
    def __init__(self, parent):
        style = (wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT)
        wx.Frame.__init__(self, parent, style=style)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.parent = parent

        self.font = wx.Font(MENU_FONT, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        self.SetClientSize((350, 390))

        panel = wx.Panel(self, -1, style=wx.BORDER_SIMPLE)
        w, h = self.GetSize()
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)

        title = FrameLabel(panel, "Cecilia Preferences", size=(w - 2, 24))
        box.Add(title, 0, wx.ALL, 1)

        headerSizer = wx.FlexGridSizer(1, 2, 5, 5)
        self.panelTitles = ['  Paths', '  Audio', '    Midi', 'Export', 'Cecilia']
        choice = PreferencesRadioToolBox(panel, size=(125, 25), outFunction=self.onPageChange)
        self.panelTitle = wx.StaticText(panel, -1, 'Paths')
        self.panelTitle.SetForegroundColour(PREFS_FOREGROUND)
        self.panelTitle.SetFont(self.font)
        headerSizer.AddMany([(choice, 0, wx.LEFT, 1), (self.panelTitle, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 90)])

        box.Add(headerSizer, 0, wx.ALL, 1)
        box.Add(wx.StaticLine(panel, -1, size=(346, 1)), 0, wx.LEFT, 2)
        box.AddSpacer(5)

        self.panelsBox = wx.BoxSizer(wx.HORIZONTAL)
        pathsPane = self.createPathsPanel(panel)
        audioPane = self.createAudioPanel(panel)
        audioPane.Hide()
        midiPane = self.createMidiPanel(panel)
        midiPane.Hide()
        csoundPane = self.createFileExportPanel(panel)
        csoundPane.Hide()
        ceciliaPane = self.createCeciliaPanel(panel)
        ceciliaPane.Hide()
        self.panels = [pathsPane, audioPane, midiPane, csoundPane, ceciliaPane]
        self.currentPane = 0
        self.panelsBox.Add(self.panels[self.currentPane])
        box.Add(self.panelsBox, 0, wx.TOP, 10)

        box.AddSpacer(100)
        box.Add(Separator(panel), 0, wx.EXPAND | wx.BOTTOM, 10)
        closerBox = wx.BoxSizer(wx.HORIZONTAL)
        closer = CloseBox(panel, outFunction=self.onClose)
        closerBox.Add(closer, 0, wx.LEFT, 288)
        box.Add(closerBox)

        panel.SetSizerAndFit(box)

    def onClose(self, event=None):
        CeciliaLib.writeVarToDisk()
        self.Destroy()

    def onPageChange(self, index):
        self.panels[self.currentPane].Hide()
        self.panels[index].Show()
        self.panels[index].SetPosition(self.panelsBox.GetPosition())
        self.panelsBox.Replace(self.panels[self.currentPane], self.panels[index])
        self.currentPane = index
        self.panelTitle.SetLabel(self.panelTitles[self.currentPane])
        wx.CallAfter(self.Refresh)

    def createPathsPanel(self, panel):
        pathsPanel = wx.Panel(panel)
        pathsPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        # Soundfile Player
        textSfPlayerLabel = wx.StaticText(pathsPanel, -1, 'Soundfile Player :')
        textSfPlayerLabel.SetForegroundColour(PREFS_FOREGROUND)
        textSfPlayerLabel.SetFont(self.font)
        self.textSfPlayerPath = wx.TextCtrl(pathsPanel, -1, CeciliaLib.getVar("soundfilePlayer"), size=(260, 16), style=wx.TE_PROCESS_ENTER | wx.NO_BORDER)
        self.textSfPlayerPath.SetFont(self.font)
        self.textSfPlayerPath.Bind(wx.EVT_TEXT_ENTER, self.handleEditPlayerPath)
        self.textSfPlayerPath.SetForegroundColour(PREFS_FOREGROUND)
        self.textSfPlayerPath.SetBackgroundColour(PREFS_PATH_BACKGROUND)
        buttonSfPlayerPath = CloseBox(pathsPanel, outFunction=self.changeSfPlayer, label='Set...')

        # Soundfile Editor
        textSfEditorLabel = wx.StaticText(pathsPanel, -1, 'Soundfile Editor :')
        textSfEditorLabel.SetForegroundColour(PREFS_FOREGROUND)
        textSfEditorLabel.SetFont(self.font)
        self.textSfEditorPath = wx.TextCtrl(pathsPanel, -1, CeciliaLib.getVar("soundfileEditor"), size=(260, 16), style=wx.TE_PROCESS_ENTER | wx.NO_BORDER)
        self.textSfEditorPath.SetFont(self.font)
        self.textSfEditorPath.Bind(wx.EVT_TEXT_ENTER, self.handleEditEditorPath)
        self.textSfEditorPath.SetForegroundColour(PREFS_FOREGROUND)
        self.textSfEditorPath.SetBackgroundColour(PREFS_PATH_BACKGROUND)
        buttonSfEditorPath = CloseBox(pathsPanel, outFunction=self.changeSfEditor, label='Set...')

        # Text Editor
        textTxtEditorLabel = wx.StaticText(pathsPanel, -1, 'Text Editor :')
        textTxtEditorLabel.SetForegroundColour(PREFS_FOREGROUND)
        textTxtEditorLabel.SetFont(self.font)
        self.textTxtEditorPath = wx.TextCtrl(pathsPanel, -1, CeciliaLib.getVar("textEditor"), size=(260, 16), style=wx.TE_PROCESS_ENTER | wx.NO_BORDER)
        self.textTxtEditorPath.SetFont(self.font)
        self.textTxtEditorPath.Bind(wx.EVT_TEXT_ENTER, self.handleEditTextEditorPath)
        self.textTxtEditorPath.SetForegroundColour(PREFS_FOREGROUND)
        self.textTxtEditorPath.SetBackgroundColour(PREFS_PATH_BACKGROUND)
        buttonTxtEditorPath = CloseBox(pathsPanel, outFunction=self.changeTxtEditor, label='Set...')

        # Preferred Paths
        textPrefPathLabel = wx.StaticText(pathsPanel, -1, 'Preferred paths :')
        textPrefPathLabel.SetForegroundColour(PREFS_FOREGROUND)
        textPrefPathLabel.SetFont(self.font)
        self.textPrefPath = wx.TextCtrl(pathsPanel, -1, CeciliaLib.getVar("prefferedPath"), size=(260, 16), style=wx.TE_PROCESS_ENTER | wx.NO_BORDER)
        self.textPrefPath.SetFont(self.font)
        self.textPrefPath.Bind(wx.EVT_TEXT_ENTER, self.handleEditPrefPath)
        self.textPrefPath.SetForegroundColour(PREFS_FOREGROUND)
        self.textPrefPath.SetBackgroundColour(PREFS_PATH_BACKGROUND)
        buttonPrefPath = CloseBox(pathsPanel, outFunction=self.addPrefPath, label='Add...')

        # item, pos, span, flag, border
        gridSizer = wx.GridBagSizer(2, PADDING)
        gridSizer.Add(textSfPlayerLabel, pos=(0, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
        gridSizer.Add(self.textSfPlayerPath, pos=(1, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT, border=5)
        gridSizer.Add(buttonSfPlayerPath, pos=(1, 2), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=5)

        gridSizer.Add(textSfEditorLabel, pos=(2, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
        gridSizer.Add(self.textSfEditorPath, pos=(3, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT, border=5)
        gridSizer.Add(buttonSfEditorPath, pos=(3, 2), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=5)

        gridSizer.Add(textTxtEditorLabel, pos=(4, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
        gridSizer.Add(self.textTxtEditorPath, pos=(5, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT, border=5)
        gridSizer.Add(buttonTxtEditorPath, pos=(5, 2), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=5)

        gridSizer.Add(textPrefPathLabel, pos=(6, 0), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
        gridSizer.Add(self.textPrefPath, pos=(7, 0), span=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM | wx.LEFT, border=5)
        gridSizer.Add(buttonPrefPath, pos=(7, 2), span=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=5)

        pathsPanel.SetSizerAndFit(gridSizer)

        self.textSfPlayerPath.Navigate()
        return pathsPanel

    def createCeciliaPanel(self, panel):
        ceciliaPanel = wx.Panel(panel)
        ceciliaPanel.SetBackgroundColour(BACKGROUND_COLOUR)
        gridSizer = wx.FlexGridSizer(5, 3, 10, 3)

        textTotalTime = wx.StaticText(ceciliaPanel, 0, 'Total time default (sec) :')
        textTotalTime.SetForegroundColour(PREFS_FOREGROUND)
        textTotalTime.SetFont(self.font)
        self.choiceTotalTime = CustomMenu(ceciliaPanel, size=(80, 20),
                                    choice=["10.0", "30.0", "60.0", "120.0", "300.0", "600.0", "1200.0", "2400.0", "3600.0"],
                                    init=str(CeciliaLib.getVar("defaultTotalTime")), outFunction=self.changeDefaultTotalTime)

        textGlobalFade = wx.StaticText(ceciliaPanel, 0, 'Global fadein/fadeout (sec) :')
        textGlobalFade.SetForegroundColour(PREFS_FOREGROUND)
        textGlobalFade.SetFont(self.font)
        self.choiceGlobalFade = CustomMenu(ceciliaPanel, size=(80, 20),
                                    choice=["0.0", "0.001", "0.002", "0.003", "0.004", "0.005", "0.01", "0.015", "0.02",
                                            "0.025", "0.03", "0.05", "0.075", "0.1", "0.2", "0.3", "0.4", "0.5"],
                                    init=str(CeciliaLib.getVar("globalFade")), outFunction=self.changeGlobalFade)

        textUseTooltips = wx.StaticText(ceciliaPanel, 0, 'Use tooltips :')
        textUseTooltips.SetForegroundColour(PREFS_FOREGROUND)
        textUseTooltips.SetFont(self.font)
        self.tooltipsToggle = Toggle(ceciliaPanel, CeciliaLib.getVar("useTooltips"), outFunction=self.enableTooltips)

        textgraphTexture = wx.StaticText(ceciliaPanel, 0, 'Use grapher texture :')
        textgraphTexture.SetForegroundColour(PREFS_FOREGROUND)
        textgraphTexture.SetFont(self.font)
        self.textureToggle = Toggle(ceciliaPanel, CeciliaLib.getVar("graphTexture"), outFunction=self.enableGraphTexture)

        textVerbose = wx.StaticText(ceciliaPanel, 0, 'Verbose :')
        textVerbose.SetForegroundColour(PREFS_FOREGROUND)
        textVerbose.SetFont(self.font)
        self.verboseToggle = Toggle(ceciliaPanel, CeciliaLib.getVar("DEBUG"), outFunction=self.enableVerbose)

        if CeciliaLib.getVar("systemPlatform").startswith("linux"):
            spacerSize = 82
        else:
            spacerSize = 86
        gridSizer.AddMany([
                            (textTotalTime, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(ceciliaPanel, -1, '', size=(spacerSize, -1)), 1, wx.EXPAND),
                            (self.choiceTotalTime, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textGlobalFade, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(ceciliaPanel, -1, '', size=(spacerSize, -1)), 1, wx.EXPAND),
                            (self.choiceGlobalFade, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textUseTooltips, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(ceciliaPanel, -1, ''), 1, wx.EXPAND),
                            (self.tooltipsToggle, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textgraphTexture, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(ceciliaPanel, -1, ''), 1, wx.EXPAND),
                            (self.textureToggle, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textVerbose, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(ceciliaPanel, -1, ''), 1, wx.EXPAND),
                            (self.verboseToggle, 0, wx.ALIGN_CENTER_VERTICAL),
                         ])

        gridSizer.AddGrowableCol(1, 1)
        ceciliaPanel.SetSizerAndFit(gridSizer)
        return ceciliaPanel

    def createFileExportPanel(self, panel):
        fileExportPanel = wx.Panel(panel)
        fileExportPanel.SetBackgroundColour(BACKGROUND_COLOUR)
        gridSizer = wx.FlexGridSizer(2, 3, 10, 3)

        # File Format
        textFileFormat = wx.StaticText(fileExportPanel, 0, 'File Format :')
        textFileFormat.SetForegroundColour(PREFS_FOREGROUND)
        textFileFormat.SetFont(self.font)
        self.choiceFileFormat = CustomMenu(fileExportPanel, choice=sorted(AUDIO_FILE_FORMATS.keys()),
                                      init=CeciliaLib.getVar("audioFileType"), outFunction=self.changeFileType)

        # Bit depth
        textBD = wx.StaticText(fileExportPanel, 0, 'Bit Depth :')
        textBD.SetForegroundColour(PREFS_FOREGROUND)
        textBD.SetFont(self.font)
        self.choiceBD = CustomMenu(fileExportPanel, choice=sorted(BIT_DEPTHS.keys()), outFunction=self.changeSampSize)
        for item in BIT_DEPTHS.items():
            if item[1] == CeciliaLib.getVar("sampSize"):
                self.choiceBD.setStringSelection(item[0])

        gridSizer.AddMany([
                            (textFileFormat, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(fileExportPanel, -1, '', size=(153, -1)), 1, wx.EXPAND),
                            (self.choiceFileFormat, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textBD, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(fileExportPanel, -1, ''), 1, wx.EXPAND),
                            (self.choiceBD, 0, wx.ALIGN_CENTER_VERTICAL),
                         ])

        gridSizer.AddGrowableCol(1, 1)
        fileExportPanel.SetSizerAndFit(gridSizer)
        return fileExportPanel

    def createMidiPanel(self, panel):
        midiParamPanel = wx.Panel(panel)
        midiParamPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        box = wx.BoxSizer(wx.VERTICAL)

        gridSizer1 = wx.FlexGridSizer(5, 3, 5, 5)
        # Audio driver
        textInOutConfig = wx.StaticText(midiParamPanel, 0, 'Midi Driver :')
        textInOutConfig.SetForegroundColour(PREFS_FOREGROUND)
        textInOutConfig.SetFont(self.font)
        self.midiDriverChoice = CustomMenu(midiParamPanel, choice=['PortMidi'],
                                       init='PortMidi', outFunction=self.onMidiDriverPageChange)

        gridSizer1.AddMany([(textInOutConfig, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (self.midiDriverChoice, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 156)])

        self.midiDriverBox = wx.BoxSizer(wx.VERTICAL)
        self.midiDriverCurrentPane = self.midiDriverChoice.getIndex()
        self.midiDriverPanels = []
        portmidiPane = self.createPortmidiPane(midiParamPanel)
        if self.midiDriverCurrentPane != 0:
            portmidiPane.Hide()
        self.midiDriverPanels.append(portmidiPane)
        self.midiDriverBox.Add(self.midiDriverPanels[self.midiDriverCurrentPane])

        gridSizer2 = wx.FlexGridSizer(5, 3, 5, 5)
        textAutoBinding = wx.StaticText(midiParamPanel, 0, 'Automatic Midi Bindings :')
        textAutoBinding.SetForegroundColour(PREFS_FOREGROUND)
        textAutoBinding.SetFont(self.font)
        self.autoMidiToggle = Toggle(midiParamPanel, CeciliaLib.getVar("automaticMidiBinding"), outFunction=self.enableAutomaticBinding)
        gridSizer2.AddMany([(textAutoBinding, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (self.autoMidiToggle, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 174)])

        gridSizer1.AddGrowableCol(1, 1)
        box.Add(gridSizer1)
        box.AddSpacer(20)
        box.Add(self.midiDriverBox)
        box.AddSpacer(20)
        box.Add(gridSizer2)
        midiParamPanel.SetSizerAndFit(box)
        return midiParamPanel

    def createAudioPanel(self, panel):
        audioParamPanel = wx.Panel(panel)
        audioParamPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        box = wx.BoxSizer(wx.VERTICAL)

        gridSizer1 = wx.FlexGridSizer(5, 3, 5, 5)

        # Audio driver
        textInOutConfig = wx.StaticText(audioParamPanel, 0, 'Audio Driver :')
        textInOutConfig.SetForegroundColour(PREFS_FOREGROUND)
        textInOutConfig.SetFont(self.font)
        self.driverChoice = CustomMenu(audioParamPanel, choice=AUDIO_DRIVERS,
                                       init=CeciliaLib.getVar("audioHostAPI"),
                                       outFunction=self.onDriverPageChange)

        gridSizer1.AddMany([(textInOutConfig, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (self.driverChoice, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 147)])

        # Audio driver panels
        self.driverBox = wx.BoxSizer(wx.VERTICAL)
        self.driverCurrentPane = self.driverChoice.getLabel()
        self.driverPanels = {}
        coreaudioPane = self.createCoreaudioPane(audioParamPanel)
        portaudioPane = self.createPortaudioPane(audioParamPanel)
        jackPane = self.createJackPane(audioParamPanel)
        if self.driverCurrentPane != 'coreaudio':
            coreaudioPane.Hide()
        if self.driverCurrentPane != 'portaudio':
            portaudioPane.Hide()
        if self.driverCurrentPane != 'jack':
            jackPane.Hide()
        self.driverPanels['coreaudio'] = coreaudioPane
        self.driverPanels['portaudio'] = portaudioPane
        self.driverPanels['jack'] = jackPane
        self.driverBox.Add(self.driverPanels[self.driverCurrentPane])

        gridSizer3 = wx.FlexGridSizer(6, 3, 5, 5)

        # Sample precision
        textSamplePrecision = wx.StaticText(audioParamPanel, 0, 'Sample Precision :')
        textSamplePrecision.SetForegroundColour(PREFS_FOREGROUND)
        textSamplePrecision.SetFont(self.font)
        self.choiceSamplePrecision = CustomMenu(audioParamPanel, choice=['32 bit', '64 bit'],
                                                init=CeciliaLib.getVar("samplePrecision"),
                                                outFunction=self.changeSamplePrecision)

        # Bit depth
        textBufferSize = wx.StaticText(audioParamPanel, 0, 'Buffer Size :')
        textBufferSize.SetForegroundColour(PREFS_FOREGROUND)
        textBufferSize.SetFont(self.font)
        self.choiceBufferSize = CustomMenu(audioParamPanel, choice=BUFFER_SIZES,
                                           init=CeciliaLib.getVar("bufferSize"),
                                           outFunction=self.changeBufferSize)

        # Number of channels
        textNCHNLS = wx.StaticText(audioParamPanel, 0, 'Default # of channels :')
        textNCHNLS.SetForegroundColour(PREFS_FOREGROUND)
        textNCHNLS.SetFont(self.font)
        self.choiceNCHNLS = CustomMenu(audioParamPanel, choice=[str(x) for x in range(1, 37)],
                                       init=str(CeciliaLib.getVar("defaultNchnls")),
                                       outFunction=self.changeNchnls)

        # Sampling rate
        textSR = wx.StaticText(audioParamPanel, 0, 'Sample Rate :')
        textSR.SetForegroundColour(PREFS_FOREGROUND)
        textSR.SetFont(self.font)
        self.comboSR = CustomMenu(audioParamPanel, choice=SAMPLE_RATES,
                            init=str(CeciliaLib.getVar("sr")), outFunction=self.changeSr)

        # First physical input
        textFPI = wx.StaticText(audioParamPanel, 0, 'First Physical Input :')
        textFPI.SetForegroundColour(PREFS_FOREGROUND)
        textFPI.SetFont(self.font)
        self.choiceFPI = CustomMenu(audioParamPanel, choice=[str(x) for x in range(36)],
                                    init=str(CeciliaLib.getVar("defaultFirstInput")),
                                    outFunction=self.changeFPI)

        # First physical output
        textFPO = wx.StaticText(audioParamPanel, 0, 'First Physical Output :')
        textFPO.SetForegroundColour(PREFS_FOREGROUND)
        textFPO.SetFont(self.font)
        self.choiceFPO = CustomMenu(audioParamPanel, choice=[str(x) for x in range(36)],
                                    init=str(CeciliaLib.getVar("defaultFirstOutput")),
                                    outFunction=self.changeFPO)

        gridSizer3.AddMany([(textSamplePrecision, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, '', size=(98, -1)), 1, wx.EXPAND),
                            (self.choiceSamplePrecision, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textBufferSize, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, ''), 1, wx.EXPAND),
                            (self.choiceBufferSize, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textNCHNLS, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, ''), 1, wx.EXPAND),
                            (self.choiceNCHNLS, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textSR, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, ''), 1, wx.EXPAND),
                            (self.comboSR, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textFPI, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, ''), 1, wx.EXPAND),
                            (self.choiceFPI, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textFPO, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(audioParamPanel, -1, ''), 1, wx.EXPAND),
                            (self.choiceFPO, 0, wx.ALIGN_CENTER_VERTICAL)])

        gridSizer1.AddGrowableCol(1, 1)
        gridSizer3.AddGrowableCol(1, 1)
        box.Add(gridSizer1)
        box.AddSpacer(20)
        box.Add(self.driverBox)
        box.AddSpacer([60, 30, 20, 60][['coreaudio', 'portaudio', 'jack'].index(self.driverCurrentPane)])
        box.Add(gridSizer3)
        audioParamPanel.SetSizerAndFit(box)
        return audioParamPanel

    def createPortmidiPane(self, panel):
        portmidiPanel = wx.Panel(panel)
        portmidiPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        gridSizer = wx.FlexGridSizer(5, 3, 5, 5)
        # Input
        textIn = wx.StaticText(portmidiPanel, 0, 'Input Device :')
        textIn.SetForegroundColour(PREFS_FOREGROUND)
        textIn.SetFont(self.font)
        availableMidiIns = []
        for d in CeciliaLib.getVar("availableMidiInputs"):
            availableMidiIns.append(CeciliaLib.ensureNFD(d))
        try:
            initInput = availableMidiIns[CeciliaLib.getVar("availableMidiInputIndexes").index(CeciliaLib.getVar("midiDeviceIn"))]
        except:
            if len(availableMidiIns) >= 1:
                initInput = availableMidiIns[0]
            else:
                initInput = ''
        self.midiChoiceInput = CustomMenu(portmidiPanel, choice=availableMidiIns, init=initInput,
                                          size=(168, 20), outFunction=self.changeMidiInput)

        gridSizer.AddMany([(textIn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                           (wx.StaticText(portmidiPanel, -1, '', size=(75, -1)), 1, wx.EXPAND),
                           (self.midiChoiceInput, 0, wx.ALIGN_CENTER_VERTICAL)])

        gridSizer.AddGrowableCol(1, 1)
        portmidiPanel.SetSizerAndFit(gridSizer)
        return portmidiPanel

    def createPortaudioPane(self, panel):
        portaudioPanel = wx.Panel(panel)
        portaudioPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        gridSizer = wx.FlexGridSizer(5, 3, 5, 5)
        # Input
        textIn = wx.StaticText(portaudioPanel, 0, 'Input Device :')
        textIn.SetForegroundColour(PREFS_FOREGROUND)
        textIn.SetFont(self.font)
        availableAudioIns = []
        for d in CeciliaLib.getVar("availableAudioInputs"):
            availableAudioIns.append(CeciliaLib.ensureNFD(d))
        try:
            initInput = availableAudioIns[CeciliaLib.getVar("availableAudioInputIndexes").index(CeciliaLib.getVar("audioInput"))]
        except:
            if len(availableAudioIns) >= 1:
                initInput = availableAudioIns[0]
            else:
                initInput = ''
        self.choiceInput = CustomMenu(portaudioPanel, choice=availableAudioIns, init=initInput,
                                      size=(168, 20), outFunction=self.changeAudioInput)
        if CeciliaLib.getVar("enableAudioInput") == 0:
            initInputState = 0
        else:
            initInputState = 1
        self.inputToggle = Toggle(portaudioPanel, initInputState, outFunction=self.enableAudioInput)

        # Output
        textOut = wx.StaticText(portaudioPanel, 0, 'Output Device :')
        textOut.SetForegroundColour(PREFS_FOREGROUND)
        textOut.SetFont(self.font)
        availableAudioOuts = []
        for d in CeciliaLib.getVar("availableAudioOutputs"):
            availableAudioOuts.append(CeciliaLib.ensureNFD(d))
        try:
            initOutput = availableAudioOuts[CeciliaLib.getVar("availableAudioOutputIndexes").index(CeciliaLib.getVar("audioOutput"))]
        except:
            if len(availableAudioOuts) >= 1:
                initOutput = availableAudioOuts[0]
            else:
                initOutput = ''
        self.choiceOutput = CustomMenu(portaudioPanel, choice=availableAudioOuts, init=initOutput,
                                       size=(168, 20), outFunction=self.changeAudioOutput)

        gridSizer.AddMany([(textIn, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (self.inputToggle, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 45),
                            (self.choiceInput, 0, wx.ALIGN_CENTER_VERTICAL),
                            (textOut, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(portaudioPanel, -1, '', size=(65, -1)), 1, wx.EXPAND),
                            (self.choiceOutput, 0, wx.ALIGN_CENTER_VERTICAL)])
        gridSizer.AddGrowableCol(1, 1)
        portaudioPanel.SetSizerAndFit(gridSizer)
        return portaudioPanel

    def createCoreaudioPane(self, panel):
        return self.createPortaudioPane(panel)

    def createJackPane(self, panel):
        jackPanel = wx.Panel(panel)
        jackPanel.SetBackgroundColour(BACKGROUND_COLOUR)

        gridSizer = wx.FlexGridSizer(3, 3, 5, 5)

        jackClientLabel = wx.StaticText(jackPanel, -1, 'Jack client :')
        jackClientLabel.SetForegroundColour(PREFS_FOREGROUND)
        jackClientLabel.SetFont(self.font)
        self.jackClient = wx.TextCtrl(jackPanel, -1, CeciliaLib.getVar("jack")['client'], size=(235, -1), style=wx.TE_PROCESS_ENTER | wx.NO_BORDER)
        self.jackClient.SetFont(self.font)
        self.jackClient.Bind(wx.EVT_TEXT_ENTER, self.changeJackClient)
        self.jackClient.SetForegroundColour(PREFS_FOREGROUND)
        self.jackClient.SetBackgroundColour(PREFS_PATH_BACKGROUND)

        gridSizer.AddMany([(jackClientLabel, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, PADDING),
                            (wx.StaticText(jackPanel, -1, '', size=(17, -1)), 1, wx.EXPAND),
                            (self.jackClient, 0, wx.ALIGN_CENTER_VERTICAL),
                            (wx.StaticText(jackPanel, -1, '', size=(17, -1)), 1, wx.EXPAND),
                            (wx.StaticText(jackPanel, -1, '', size=(17, -1)), 1, wx.EXPAND),
                            (wx.StaticText(jackPanel, -1, '', size=(17, -1)), 1, wx.EXPAND),
                            (wx.StaticText(jackPanel, -1, '', size=(17, -1)), 1, wx.EXPAND),
                            (wx.StaticText(jackPanel, -1, '', size=(17, -1)), 1, wx.EXPAND),
                            (wx.StaticText(jackPanel, -1, '', size=(17, -1)), 1, wx.EXPAND)])

        gridSizer.AddGrowableCol(1, 1)
        jackPanel.SetSizerAndFit(gridSizer)
        return jackPanel

    def onDriverPageChange(self, index, label):
        CeciliaLib.setVar("audioHostAPI", label)
        self.driverPanels[self.driverCurrentPane].Hide()
        self.driverPanels[label].Show()
        self.driverPanels[label].SetPosition(self.driverBox.GetPosition())
        self.driverBox.Replace(self.driverPanels[self.driverCurrentPane], self.driverPanels[label])
        self.driverCurrentPane = label
        wx.CallAfter(self.Refresh)

    def onMidiDriverPageChange(self, index, label):
        pass

    def enableAudioInput(self, state):
        CeciliaLib.setVar('enableAudioInput', state)
        if state == 1:
            CeciliaLib.setVar("audioInput", self.choiceInput.getIndex())
        else:
            CeciliaLib.setVar("audioInput", 0)

    def changeAudioInput(self, index, label):
        deviceIndex = CeciliaLib.getVar("availableAudioInputIndexes")[index]
        CeciliaLib.setVar("audioInput", deviceIndex)

    def changeAudioOutput(self, index, label):
        deviceIndex = CeciliaLib.getVar("availableAudioOutputIndexes")[index]
        CeciliaLib.setVar("audioOutput", deviceIndex)

    def changeMidiInput(self, index, label):
        deviceIndex = CeciliaLib.getVar("availableMidiInputIndexes")[index]
        CeciliaLib.setVar("midiDeviceIn", deviceIndex)

    def changeSfPlayer(self):
        CeciliaLib.loadPlayerEditor("soundfile player")
        self.textSfPlayerPath.SetValue(CeciliaLib.getVar("soundfilePlayer"))

    def changeSfEditor(self):
        CeciliaLib.loadPlayerEditor("soundfile editor")
        self.textSfEditorPath.SetValue(CeciliaLib.getVar("soundfileEditor"))

    def changeTxtEditor(self):
        CeciliaLib.loadPlayerEditor("text editor")
        self.textTxtEditorPath.SetValue(CeciliaLib.getVar("textEditor"))

    def addPrefPath(self):
        currentPath = CeciliaLib.getVar("prefferedPath")

        path = ''
        dlg = wx.DirDialog(self, message="Choose a folder...",
                                 defaultPath=CeciliaLib.ensureNFD(os.path.expanduser('~')))

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        dlg.Destroy()

        if path and currentPath != '':
            path = currentPath + ';' + path
        elif not path:
            return

        CeciliaLib.setVar("prefferedPath", path)
        self.textPrefPath.SetValue(path)

    def handleEditPlayerPath(self, event):
        path = self.textSfPlayerPath.GetValue()
        CeciliaLib.setVar("soundfilePlayer", path)
        self.textSfPlayerPath.Navigate()

    def handleEditEditorPath(self, event):
        path = self.textSfEditorPath.GetValue()
        CeciliaLib.setVar("soundfileEditor", path)
        self.textSfEditorPath.Navigate()

    def handleEditTextEditorPath(self, event):
        path = self.textTxtEditorPath.GetValue()
        CeciliaLib.setVar("textEditor", path)
        self.textTxtEditorPath.Navigate()

    def handleEditPrefPath(self, event):
        path = self.textPrefPath.GetValue()
        CeciliaLib.setVar("prefferedPath", path)
        self.textPrefPath.Navigate()

    def changeSamplePrecision(self, index, label):
        CeciliaLib.setVar("samplePrecision", label)

    def changeBufferSize(self, index, label):
        CeciliaLib.setVar("bufferSize", label)

    def changeFileType(self, index, label):
        CeciliaLib.setVar("audioFileType", label)

    def changeSr(self, index, label):
        sr = int(label.strip())
        CeciliaLib.setVar("sr", sr)

    def changeSampSize(self, index, label):
        CeciliaLib.setVar("sampSize", BIT_DEPTHS[label])

    def changeNchnls(self, index, choice):
        nchnls = int(choice)
        CeciliaLib.setVar("defaultNchnls", nchnls)
        CeciliaLib.setVar("nchnls", nchnls)
        CeciliaLib.updateNchnlsDevices()

    def changeFPI(self, index, choice):
        CeciliaLib.setVar("defaultFirstInput", index)

    def changeFPO(self, index, choice):
        CeciliaLib.setVar("defaultFirstOutput", index)

    def changeJackClient(self, event):
        CeciliaLib.setJackParams(client=event.GetString())

    def changeDefaultTotalTime(self, index, label):
        CeciliaLib.setVar("defaultTotalTime", float(self.choiceTotalTime.getLabel().strip()))

    def changeGlobalFade(self, index, label):
        CeciliaLib.setVar("globalFade", float(self.choiceGlobalFade.getLabel().strip()))

    def enableTooltips(self, state):
        CeciliaLib.setVar("useTooltips", state)

    def enableGraphTexture(self, state):
        CeciliaLib.setVar("graphTexture", state)
        if CeciliaLib.getVar("grapher") is not None:
            CeciliaLib.getVar("grapher").plotter.draw()

    def enableAutomaticBinding(self, state):
        CeciliaLib.setVar("automaticMidiBinding", state)

    def enableVerbose(self, state):
        CeciliaLib.setVar("DEBUG", state)
