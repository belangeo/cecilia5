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

import wx, os, time, math, sys, copy
from constants import *
import CeciliaLib
from Widgets import *
from subprocess import Popen
from types import ListType
from TogglePopup import SamplerPopup, SamplerToggle  
from Plugins import *
import wx.lib.scrolledpanel as scrolled
import wx.lib.statbmp as statbmp

def chooseColourFromName(name):
    def clip(x):
        val = int(x*255)
        if val < 0: val = 0
        elif val > 255: val = 255
        else: val = val
        return val

    def colour(name):
        vals = COLOUR_CLASSES[name]
        hue = vals[0]
        bright = vals[1]
        sat = vals[2]
        segment = int(math.floor(hue / 60))
        fraction = hue / 60 - segment
        t1 = bright * (1 - sat)
        t2 = bright * (1 - (sat * fraction))
        t3 = bright * (1 - (sat * (1 - fraction)))
        if segment == 0:
            r, g, b = bright, t3, t1
        elif segment == 1:
            r, g, b = t2, bright, t1
        elif segment == 2:
            r, g, b = t1, bright, t3
        elif segment == 3:
            r, g, b = t1, t2, bright
        elif segment == 4:
            r, g, b = t3, t1, bright
        elif segment == 5:
            r, g, b = bright, t1, t2
        return wx.Colour(clip(r),clip(g),clip(b))

    lineColour = colour(name)    
    midColour = colour(name)
    knobColour = colour(name)
    sliderColour = colour(name)

    return [lineColour, midColour, knobColour, sliderColour]
           
class CECControl(scrolled.ScrolledPanel):
    def __init__(self, parent, id=-1, size=(-1,-1), style = wx.NO_BORDER):
        scrolled.ScrolledPanel.__init__(self, parent, id, size=size, style=style)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.parent = parent

        self.outputFilename = ''
        self.cfileinList = []        
        self.peak = ''
        self.time = self.nonZeroTime = 0
        self.charNumForLabel = 34
        self.bounce_dlg = None
        self.tmpTotalTime = CeciliaLib.getVar("totalTime")

        self.sizerMain = wx.FlexGridSizer(3,1)

        self.sizerMain.Add(Separator(self, (230,1), colour=TITLE_BACK_COLOUR), 1, wx.EXPAND)

        ##### Transport Panel #####
        controlPanel = wx.Panel(self, -1, style=wx.NO_BORDER)
        controlPanel.SetBackgroundColour(TITLE_BACK_COLOUR)
        controlSizer = wx.FlexGridSizer(1,4)        
        self.transportButtons = Transport(controlPanel, outPlayFunction=self.onPlayStop, outRecordFunction=self.onRec,
                                                  backgroundColour=TITLE_BACK_COLOUR, borderColour=WIDGET_BORDER_COLOUR)
        self.clocker = Clocker(controlPanel, backgroundColour=TITLE_BACK_COLOUR, borderColour=WIDGET_BORDER_COLOUR)
        controlSizer.Add(self.transportButtons, 0, wx.ALIGN_LEFT | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        fakePanel = wx.Panel(controlPanel, -1, size=(35, self.GetSize()[1]))
        fakePanel.SetBackgroundColour(TITLE_BACK_COLOUR)
        controlSizer.Add(fakePanel)
        controlSizer.Add(self.clocker, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        ffakePanel = wx.Panel(controlPanel, -1, size=(5, self.GetSize()[1]))
        ffakePanel.SetBackgroundColour(TITLE_BACK_COLOUR)
        controlSizer.Add(ffakePanel)
        #controlSizer.AddGrowableCol(1)
        controlPanel.SetSizer(controlSizer)
        self.sizerMain.Add(controlPanel, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.sizerMain.Add(Separator(self, (230,1), colour=TITLE_BACK_COLOUR), 1, wx.EXPAND)
        self.sizerMain.Add(Separator(self, (230,2), colour=BORDER_COLOUR), 1, wx.EXPAND)
        self.sizerMain.AddSpacer((5,1))

        self.tabs = TabsPanel(self, outFunction=self.onTogglePanels)
        self.sizerMain.Add(self.tabs, 1, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 0)

        ##### Input Panel #####
        self.inOutSeparators = []
        isEmpty = self.createInputPanel()
        self.sizerMain.Add(self.inputPanel, 1, wx.EXPAND | wx.ALL, 0)
        if not isEmpty:
            sep = Separator(self, (230,2), colour=BACKGROUND_COLOUR)
            self.sizerMain.Add(sep, 1, wx.EXPAND)
            self.inOutSeparators.append(sep)
            sep = Separator(self, (230,2), colour=BORDER_COLOUR)
            self.sizerMain.Add(sep, 1, wx.EXPAND)
            self.inOutSeparators.append(sep)
            sep = Separator(self, (230,1), colour=BACKGROUND_COLOUR)
            self.sizerMain.Add(sep, 1, wx.EXPAND)
            self.inOutSeparators.append(sep)

        ###### Output Panel #####
        self.createOutputPanel()
        self.sizerMain.Add(self.outputPanel, 1, wx.EXPAND | wx.ALL, 0)
        sep = Separator(self, (230,2), colour=BACKGROUND_COLOUR)
        self.sizerMain.Add(sep, 1, wx.EXPAND)
        self.inOutSeparators.append(sep)
        sep = Separator(self, (230,2), colour=BORDER_COLOUR)
        self.sizerMain.Add(sep, 1, wx.EXPAND)
        self.inOutSeparators.append(sep)
        sep = Separator(self, (230,1), colour=BACKGROUND_COLOUR)
        self.sizerMain.Add(sep, 1, wx.EXPAND)
        self.inOutSeparators.append(sep)

        ### Plugins panel ###
        self.createPluginPanel()
        self.sizerMain.Add(self.pluginsPanel, 1, wx.EXPAND | wx.ALL, 0)
        self.sizerMain.Show(self.pluginsPanel, False)
 
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        controlPanel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        self.inputPanel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        self.outputPanel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        self.peakLabel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        self.durationSlider.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        self.gainSlider.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        self.vuMeter.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        self.pluginsPanel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

        self.SetSizer(self.sizerMain)

        self.SetAutoLayout(1)
        self.SetupScrolling(scroll_x = False)

        wx.CallAfter(self.updateOutputFormat)

    def OnLooseFocus(self, event):
        win = wx.FindWindowAtPointer()
        if win != None:
            win = win.GetTopLevelParent()
            if win not in [CeciliaLib.getVar("mainFrame"), CeciliaLib.getVar("interface"), CeciliaLib.getVar("spectrumFrame")]:
                win.Raise()
        event.Skip()

    def onTogglePanels(self, state):
        if state == 0:
            self.sizerMain.Show(self.pluginsPanel, False, True)
            self.sizerMain.Show(self.inputPanel, True, True)
            self.sizerMain.Show(self.outputPanel, True, True)
            [self.sizerMain.Show(sep, True, True) for sep in self.inOutSeparators]
        else:
            self.sizerMain.Show(self.pluginsPanel, True, True)
            self.sizerMain.Show(self.inputPanel, False, True)
            self.sizerMain.Show(self.outputPanel, False, True)
            [self.sizerMain.Show(sep, False, True) for sep in self.inOutSeparators]
        self.sizerMain.Layout()

    def createGrapherLines(self, plugin):
        knobs = [plugin.knob1, plugin.knob2, plugin.knob3]
        grapher = CeciliaLib.getVar("grapher")
        choice = grapher.toolbar.getPopupChoice()
        choice.extend([knob.getLongLabel() for knob in knobs])
        grapher.toolbar.setPopupChoice(choice)
        for j, knob in enumerate(knobs):
            func = '0 %f 1 %f' % (knob.GetValue(), knob.GetValue())
            func = [float(v.replace('"', '')) for v in func.split()]
            func = [[func[i*2] * CeciliaLib.getVar("totalTime"), func[i*2+1]] for i in range(len(func) / 2)]
            mini = knob.getRange()[0]
            maxi = knob.getRange()[1]
            colour = chooseColourFromName('orange%d' % (j+1))
            label = knob.getLongLabel()
            log = knob.getLog()
            name = knob.getName()
            grapher.plotter.createLine(func, (mini, maxi), colour, label, log, name, 8192, knob, '')
            grapher.plotter.getData()[-1].setShow(0)
            grapher.plotter.draw()

    def removeGrapherLines(self, plugin):
        knobs = [plugin.knob1, plugin.knob2, plugin.knob3]
        tmp = [knob.getLongLabel() for knob in knobs]
        names = [knob.getName() for knob in knobs]
        grapher = CeciliaLib.getVar("grapher")
        choice = grapher.toolbar.getPopupChoice()
        for label in tmp:
            if label in choice:
                choice.remove(label)
        grapher.toolbar.setPopupChoice(choice)
        grapher.plotter.removeLines(names)

    def movePlugin(self, vpos, dir):
        i1 = vpos
        i2 = vpos + dir

        p1 = self.plugins[i1]
        p2 = self.plugins[i2]
            
        p1pos = self.bagSizer.GetItemPosition(p1)
        p2pos = self.bagSizer.GetItemPosition(p2)
        self.bagSizer.SetItemPosition(p1, (8,0))
        self.bagSizer.SetItemPosition(p2, p1pos)
        self.bagSizer.SetItemPosition(p1, p2pos)

        grapher = CeciliaLib.getVar("grapher")
        choice = grapher.toolbar.getPopupChoice()

        for i in [i1, i2]:
            if self.plugins[i].pluginName != 'None':
                for label in self.plugins[i].getKnobLongLabels():
                    choice.remove(label)
       
        self.plugins[i1], self.plugins[i2] = self.plugins[i2], self.plugins[i1]
        self.oldPlugins[i1], self.oldPlugins[i2] = self.oldPlugins[i2], self.oldPlugins[i1]
        self.plugins[i1].vpos = i1
        self.plugins[i2].vpos = i2

        for i in [i1, i2]:
            self.plugins[i].setKnobLabels()
            self.plugins[i].checkArrows()
        self.pluginsPanel.Layout()

        graphData = CeciliaLib.getVar("grapher").getPlotter().getData()
        
        if self.plugins[i1].pluginName == 'None':
            CeciliaLib.setPlugins(None, i1)
        else:
            oldKnobNames = self.plugins[i1].getKnobNames()
            self.plugins[i1].setKnobNames()
            for i, old in enumerate(oldKnobNames):
                for line in graphData:
                    if line.name == old:
                        line.name = self.plugins[i1].getKnobNames()[i]
                        break
            CeciliaLib.setPlugins(self.plugins[i1], i1)
            choice.extend(self.plugins[i1].getKnobLongLabels())
            
        if self.plugins[i2].pluginName == 'None':
            CeciliaLib.setPlugins(None, i2)
        else:
            oldKnobNames = self.plugins[i2].getKnobNames()
            self.plugins[i2].setKnobNames()
            for i, old in enumerate(oldKnobNames):
                for line in graphData:
                    if line.name == old:
                        line.name = self.plugins[i2].getKnobNames()[i]
                        break
            CeciliaLib.setPlugins(self.plugins[i2], i2)
            choice.extend(self.plugins[i2].getKnobLongLabels())

        grapher.toolbar.setPopupChoice(choice)

        if CeciliaLib.getVar("audioServer").isAudioServerRunning():
            CeciliaLib.getVar("audioServer").movePlugin(vpos, dir)

    def replacePlugin(self, order, new):
        self.pluginsParams[order][self.oldPlugins[order]] = self.plugins[order].getParams()
        oldPlugin = self.plugins[order]
        if self.oldPlugins[order] != 0:
            self.removeGrapherLines(oldPlugin)
        plugin = self.pluginsDict[new](self.pluginsPanel, self.replacePlugin, order)

        if new != 'None':    
            CeciliaLib.setPlugins(plugin, order)
            self.createGrapherLines(plugin)
            ind = PLUGINS_CHOICE.index(plugin.getName())
            self.oldPlugins[order] = ind
            plugin.setParams(self.pluginsParams[order][ind])
        else:
            CeciliaLib.setPlugins(None, order)
            self.oldPlugins[order] = 0
            plugin.setParams([0,0,0,0])
        if 1: #CeciliaLib.getVar("systemPlatform")  in 'darwin':
            self.bagSizer.Replace(oldPlugin, plugin)
        else:
            item = self.bagSizer.GetItem(oldPlugin)
            pos = item.GetPos()
            for i, child in enumerate(self.bagSizer.GetChildren()):
                if pos == child.GetPos():
                    break
            item.DeleteWindows()
            self.bagSizer.Add(plugin, pos) 
        self.plugins[order] = plugin       
        self.pluginsPanel.Layout()
        if CeciliaLib.getVar("audioServer").isAudioServerRunning():
            CeciliaLib.getVar("audioServer").setPlugin(order)

    def setPlugins(self, pluginsDict):
        for key in pluginsDict.keys():
            self.replacePlugin(key, pluginsDict[key][0])
            self.plugins[key].setParams(pluginsDict[key][1])
            self.plugins[key].setStates(pluginsDict[key][2])
        for i in range(NUM_OF_PLUGINS):
            if i not in pluginsDict.keys():
                self.replacePlugin(i, "None")

    def updateTime(self, time):
        self.setTime(time)
        self.GetParent().grapher.plotter.drawCursor(time)

    def updateAmps(self, amps):
        self.vuMeter.setAmplitude(amps)

    def createInputPanel(self):
        isEmpty = True
        self.inputPanel = wx.Panel(self, -1, style=wx.NO_BORDER)
        inputSizer = wx.FlexGridSizer(5,1)
        
        self.cfileinList = []
        samplersList = []
        widgets = CeciliaLib.getVar("interfaceWidgets")
        
        for w in range(len(widgets)):
            if widgets[w]['type'] == 'cfilein':
                cFileIn = Cfilein(self.inputPanel, label=widgets[w].get('label', ''), name=widgets[w]['name'])
                self.cfileinList.append(cFileIn)
            elif widgets[w]['type'] == 'csampler':
                cSampler = CSampler(self.inputPanel, label=widgets[w].get('label', ''), name=widgets[w]['name'])
                self.cfileinList.append(cSampler)
                samplersList.append(cSampler)

        CeciliaLib.setVar("userSamplers", samplersList)

        if self.cfileinList != []:
            isEmpty = False
            # Section title
            inputTextPanel = wx.Panel(self.inputPanel, -1, style=wx.NO_BORDER)
            inputTextPanel.SetBackgroundColour(TITLE_BACK_COLOUR)
            inputTextSizer = wx.FlexGridSizer(1,1)
            inputText = wx.StaticText(inputTextPanel, -1, 'INPUT ')
            inputText.SetFont(wx.Font(SECTION_TITLE_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE))
            inputText.SetBackgroundColour(TITLE_BACK_COLOUR)
            inputText.SetForegroundColour(SECTION_TITLE_COLOUR)
            inputTextSizer.Add(inputText, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
            inputTextSizer.AddGrowableCol(0)
            inputTextPanel.SetSizer(inputTextSizer)
            inputSizer.Add(inputTextPanel, 1, wx.EXPAND| wx.ALIGN_RIGHT | wx.ALL, 0)
        
        for i in range(len(self.cfileinList)):
            inputSizer.Add(self.cfileinList[i], 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, -1)
            if i != len(self.cfileinList)-1:
                inputSizer.Add(Separator(self.inputPanel, size=(230,1)), 1, wx.EXPAND)
        
        inputSizer.AddGrowableCol(0)
        self.inputPanel.SetSizer(inputSizer)
        
        return isEmpty

    def createOutputPanel(self):
        self.outputPanel = wx.Panel(self, -1, style=wx.NO_BORDER)
        self.outputPanel.SetBackgroundColour(BACKGROUND_COLOUR)
        outputSizer = wx.FlexGridSizer(5,1)
        
        outputTextPanel = wx.Panel(self.outputPanel, -1, style=wx.NO_BORDER)
        outputTextPanel.SetBackgroundColour(TITLE_BACK_COLOUR)
        outputTextSizer = wx.FlexGridSizer(1,1)
        outputText = wx.StaticText(outputTextPanel, -1, 'OUTPUT ')
        outputText.SetFont(wx.Font(SECTION_TITLE_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE))
        outputText.SetBackgroundColour(TITLE_BACK_COLOUR)
        outputText.SetForegroundColour(SECTION_TITLE_COLOUR)
        outputTextSizer.Add(outputText, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        outputTextSizer.AddGrowableCol(0)
        outputTextPanel.SetSizer(outputTextSizer)
        outputSizer.Add(outputTextPanel, 1, wx.EXPAND| wx.ALIGN_RIGHT | wx.ALL, 0)
        
        outputSizer.AddSpacer((5,7))
              
        outLine1 = wx.BoxSizer(wx.HORIZONTAL)
        
        # File Name Label
        self.filenameLabel = OutputLabel(self.outputPanel, label='', size=(130,20), 
                                        colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onSelectOutputFilename)
        self.filenameLabel.SetToolTip(CECTooltip(TT_OUTPUT))
        self.filenameLabel.setItalicLabel('File name')
        outLine1.Add(self.filenameLabel, 0, wx.RIGHT | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL , 20)
        
        outLine1.AddSpacer((8,1))
 
        outToolbox = ToolBox(self.outputPanel, tools=['play','edit','recycle'],
                            outFunction=[self.listenSoundfile, self.editSoundfile, self.onReuseOutputFile])
        outLine1.Add(outToolbox, 0,  wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 2)
        
        outputSizer.Add(outLine1, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 7)
        
        # Duration Static Text
        durationText = wx.StaticText(self.outputPanel, -1, 'Duration (sec) :')
        durationText.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE))
        durationText.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        outputSizer.Add(durationText, 0, wx.ALIGN_LEFT | wx.LEFT, 9)
        
        # Duration Slider
        outputSizer.AddSpacer((3,1))
        self.durationSlider = ControlSlider(self.outputPanel,
                                                    0.01, 3600, CeciliaLib.getVar("defaultTotalTime"),
                                                    size=(220,15), log=True, outFunction=self.setTotalTime)
        self.durationSlider.setSliderHeight(10)
        self.durationSlider.SetToolTip(CECTooltip(TT_DUR_SLIDER))
        outputSizer.Add(self.durationSlider, 0, wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM, 7)
        
        # Gain Static Text
        gainText = wx.StaticText(self.outputPanel, -1, 'Gain (dB) :')
        gainText.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE))
        gainText.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        outputSizer.Add(gainText, 0, wx.ALIGN_LEFT | wx.LEFT, 9)
        
        # Gain Slider
        outputSizer.AddSpacer((3,1))
        self.gainSlider = ControlSlider(self.outputPanel, -48, 18, 0, size=(220,15),
                                                log=False, outFunction=self.onChangeGain)
        self.gainSlider.setSliderHeight(10)
        self.gainSlider.SetToolTip(CECTooltip(TT_GAIN_SLIDER))
        CeciliaLib.setVar("gainSlider", self.gainSlider)
        outputSizer.Add(self.gainSlider, 0, wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM, 7)

        # VU Meter
        self.meterSizer = wx.BoxSizer()
        self.vuMeter = VuMeter(self.outputPanel)
        self.meterSizer.Add(self.vuMeter, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM, 8)
        CeciliaLib.getVar("audioServer").setAmpCallable(self.vuMeter)

        # Channels choice
        self.lineSizer = wx.BoxSizer(wx.HORIZONTAL)
        formatSizer = wx.BoxSizer(wx.VERTICAL)
        self.formatText = wx.StaticText(self.outputPanel, -1, 'Channels :')
        self.formatText.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE))
        self.formatText.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        formatSizer.Add(self.formatText, 0, wx.ALIGN_LEFT | wx.LEFT, 2)
        
        self.formatChoice = CustomMenu(self.outputPanel,
                                        choice=[str(x) for x in range(1,37)], 
                                        init=str(CeciliaLib.getVar("nchnls")),
                                        outFunction=self.onFormatChange,
                                        colour=CONTROLLABEL_BACK_COLOUR, columns=6)
        self.formatChoice.SetToolTip(CECTooltip(TT_CHANNELS))
        formatSizer.Add(self.formatChoice, 0, wx.ALIGN_LEFT | wx.TOP, 1)
        self.lineSizer.Add(formatSizer, 0, wx.ALIGN_LEFT | wx.RIGHT, 10)
        
        # Peak
        peakSizer = wx.BoxSizer(wx.VERTICAL)
        self.peakText = wx.StaticText(self.outputPanel, -1, 'Peak :')
        self.peakText.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE))
        self.peakText.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        peakSizer.Add(self.peakText, 0, wx.ALIGN_LEFT | wx.LEFT, 2)
        
        self.peakLabel = PeakLabel(self.outputPanel,
                                       label=self.peak,
                                       size=(100,20),
                                       font=None,
                                       colour=CONTROLLABEL_BACK_COLOUR,
                                       gainSlider=self.gainSlider)
        self.peakLabel.SetToolTip(CECTooltip(TT_PEAK))
        peakSizer.Add(self.peakLabel, 0, wx.ALIGN_LEFT | wx.TOP, 1)
        self.lineSizer.Add(peakSizer, 0, wx.ALIGN_LEFT | wx.LEFT, 10)

        outputTextPanel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        outToolbox.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

        outputSizer.Add(self.meterSizer, 1, wx.EXPAND)
        outputSizer.Add(self.lineSizer, 0, wx.ALIGN_LEFT | wx.LEFT | wx.BOTTOM, 7)
        outputSizer.AddGrowableRow(9)
        self.outputPanel.SetSizer(outputSizer)

    def createPluginPanel(self):
        self.oldPlugins = [0] * NUM_OF_PLUGINS
        paramsTemplate = [[0,0,0,0], [.25,1,.5,1], [.25,.7,5000,1], [1,1000,1,1], [.5,.2,.5,1], [1000,1,-3,1], 
                                [0,0,0,1], [-20,3,0,1], [-70,0.005,.01,1], [.7,.7,-12,1], [8,1,0,1], [100,5,1.1,1],
                                [.1,0,0.5,1], [0.5,0.25,0.25,1], [-7,0,0.5,1], [80,2.01,0.33,1], [80,0.5,0.33,1]]
        self.pluginsParams = {}
        for i in range(NUM_OF_PLUGINS):
            CeciliaLib.setPlugins(None, i)
            self.pluginsParams[i] = copy.deepcopy(paramsTemplate)
        self.pluginsDict = {'None': NonePlugin, 'Reverb': ReverbPlugin, 'WGVerb': WGReverbPlugin, 'Filter': FilterPlugin, 'Chorus': ChorusPlugin,
                            'Para EQ': EQPlugin, '3 Bands EQ': EQ3BPlugin, 'Compress': CompressPlugin, 'Gate': GatePlugin,
                            'Disto': DistoPlugin, 'AmpMod': AmpModPlugin, 'Phaser': PhaserPlugin, 'Delay': DelayPlugin,
                            'Flange': FlangePlugin, 'Harmonizer': HarmonizerPlugin, 'Resonators': ResonatorsPlugin,
                            'DeadReson': DeadResonPlugin}
        self.pluginsPanel = wx.Panel(self, -1, style=wx.NO_BORDER)
        self.pluginsPanel.SetBackgroundColour(BACKGROUND_COLOUR)
        self.pluginSizer = wx.BoxSizer(wx.VERTICAL)

        pluginTextPanel = wx.Panel(self.pluginsPanel, -1, style=wx.NO_BORDER)
        pluginTextPanel.SetBackgroundColour(TITLE_BACK_COLOUR)
        pluginTextSizer = wx.FlexGridSizer(1,1)
        pluginText = wx.StaticText(pluginTextPanel, -1, 'POST-PROCESSING ')
        pluginText.SetFont(wx.Font(SECTION_TITLE_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE))
        pluginText.SetBackgroundColour(TITLE_BACK_COLOUR)
        pluginText.SetForegroundColour(SECTION_TITLE_COLOUR)
        pluginTextSizer.Add(pluginText, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        pluginTextSizer.AddGrowableCol(0)
        pluginTextPanel.SetSizer(pluginTextSizer)
        self.pluginSizer.Add(pluginTextPanel, 0, wx.EXPAND| wx.ALIGN_RIGHT, 0)

        self.pluginSizer.AddSpacer((5,3))

        self.bagSizer = wx.GridBagSizer(5, 0)
        self.plugins = []
        for i in range(NUM_OF_PLUGINS):
            plugin = NonePlugin(self.pluginsPanel, self.replacePlugin, i)
            self.bagSizer.Add(plugin, (i*2, 0))
            #self.pluginSizer.AddSpacer((5,7))
            self.bagSizer.Add(Separator(self.pluginsPanel, (230,2), colour=BORDER_COLOUR), (i*2+1, 0))
            #self.pluginSizer.AddSpacer((5,3))
            self.plugins.append(plugin)

        self.pluginSizer.Add(self.bagSizer, 1, wx.EXPAND, 0)
        self.pluginsPanel.SetSizer(self.pluginSizer)

    def getCfileinList(self):
        return self.cfileinList
    
    def getCfileinFromName(self, name):
        good = None
        for cfilein in self.cfileinList:
            if name == cfilein.getName():
                good = cfilein
                break            
        return good
        
    def listenSoundfile(self):
        CeciliaLib.listenSoundfile(self.outputFilename)
    
    def editSoundfile(self):
        CeciliaLib.editSoundfile(self.outputFilename)
    
    def getTime(self):
        return self.time

    def getNonZeroTime(self):
        return self.nonZeroTime

    def setTime(self, time, m, s, c):
        if time != 0:
            self.nonZeroTime = time
        self.time = time
        self.clocker.setTime(m, s, c)

    def resetMeter(self):
        self.updatePeak(0)
        self.resetVuMeter()

    def onPlayStop(self, value):
        if value:
            self.nonZeroTime = 0
            CeciliaLib.setVar("toDac", True)
            CeciliaLib.getVar("grapher").toolbar.loadingMsg.SetForegroundColour("#FFFFFF")
            CeciliaLib.getVar("grapher").toolbar.loadingMsg.Refresh()
            wx.CallLater(50, CeciliaLib.startCeciliaSound, True)
        else:
            CeciliaLib.stopCeciliaSound()

    def onRec(self, value):
        if value:
            if self.outputFilename != '':
                filename = CeciliaLib.autoRename(self.outputFilename)
                self.filenameLabel.setLabel(CeciliaLib.shortenName(os.path.split(filename)[1],self.charNumForLabel))
            if self.outputFilename == '':
                filename = self.onSelectOutputFilename()
                if filename == None:
                    CeciliaLib.stopCeciliaSound()
                    return    
            self.outputFilename = filename
            CeciliaLib.setVar("outputFile", filename)
            self.nonZeroTime = 0
            CeciliaLib.setVar("toDac", True)
            CeciliaLib.getVar("grapher").toolbar.loadingMsg.SetForegroundColour("#FFFFFF")
            CeciliaLib.getVar("grapher").toolbar.loadingMsg.Refresh()
            wx.CallLater(50, CeciliaLib.startCeciliaSound, True, True)
        else:
            CeciliaLib.stopCeciliaSound()

    def onBounceToDisk(self):
        if self.outputFilename != '':
            filename = CeciliaLib.autoRename(self.outputFilename)
            self.filenameLabel.setLabel(CeciliaLib.shortenName(os.path.split(filename)[1],self.charNumForLabel))
        if self.outputFilename == '':
            filename = self.onSelectOutputFilename()
            if filename == None:
                CeciliaLib.stopCeciliaSound()
                return    
        self.outputFilename = filename
        CeciliaLib.setVar("outputFile", filename)
        CeciliaLib.setVar("toDac", False)
        self.showBounceDialog()
        CeciliaLib.startCeciliaSound(timer=False)
        self.updatePeak(0)

    def showBounceDialog(self):
        self.bounce_dlg = wx.Dialog(CeciliaLib.getVar('interface'), -1, "Bounce to disk")
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.bounce_label = wx.StaticText(self.bounce_dlg, -1, "Writing %s on disk..." % self.outputFilename)
        sizer.Add(self.bounce_label, 0, wx.ALIGN_CENTRE|wx.ALL, 25)
        self.bounce_dlg.SetSizerAndFit(sizer)
        self.bounce_dlg.CenterOnParent()
        self.bounce_dlg.Show()
    
    def closeBounceToDiskDialog(self):
        try:
            self.bounce_dlg.Destroy()
        except:
            pass

    def onBatchProcessing(self, filename):
        self.outputFilename = filename
        CeciliaLib.setVar("outputFile", filename)
        CeciliaLib.setVar("toDac", False)
        CeciliaLib.startCeciliaSound(timer=False)
        self.updatePeak(0)

    def onSelectOutputFilename(self):
        if CeciliaLib.getVar("audioFileType") == 'wav':
            wildcard = "Wave file|*.wave;*.WAV;*.WAVE;*.Wav;*.Wave*.wav|" \
                       "All files|*.*"
        else:
            wildcard = "AIFF file|*.aiff;*.aifc;*.AIF;*.AIFF;*.Aif;*.Aiff*.aif|" \
                       "All files|*.*"

        file = CeciliaLib.saveFileDialog(self, wildcard, type='Save audio')

        if file != None:
            self.filenameLabel.setLabel(CeciliaLib.shortenName(os.path.split(file)[1],self.charNumForLabel))
            self.outputFilename = file

        return file

    def updateOutputFormat(self):
        self.vuMeter.updateNchnls()
        x, y = self.meterSizer.GetPosition()
        w, h = self.vuMeter.GetSize()
        self.meterSizer.SetMinSize((w, h+8))
        self.meterSizer.SetDimension(x, y, w, h+8)
        w2, h2 = self.lineSizer.GetSize()
        self.lineSizer.SetDimension(7, y+h+10, w2, h2)
        self.Layout()
        wx.CallAfter(self.Refresh)

    def onFormatChange(self, idx, choice):
        nchnls = int(choice)
        CeciliaLib.setVar("nchnls", nchnls)
        self.updateOutputFormat()

    def onReuseOutputFile(self):
        if os.path.isfile(self.outputFilename):
            if self.cfileinList != []:
                self.cfileinList[0].updateMenuFromPath(self.outputFilename)

    def setTotalTime(self, time, force=False):
        if CeciliaLib.getVar("audioServer").isAudioServerRunning() and not force:
            self.tmpTotalTime = time
        else:
            if self.cfileinList != [] and time == 0:
                time = self.cfileinList[0].getDuration()
                self.durationSlider.SetValue(time)
            CeciliaLib.setVar("totalTime", time)
            if CeciliaLib.getVar("grapher"):
                CeciliaLib.getVar("grapher").setTotalTime(time)
            self.tmpTotalTime = time

    def updateDurationSlider(self):
        self.durationSlider.SetValue(CeciliaLib.getVar("totalTime"))

    def updateNchnls(self):
        self.formatChoice.setStringSelection(str(CeciliaLib.getVar("nchnls")))
        self.updateOutputFormat()

    def onChangeGain(self, gain):
        CeciliaLib.getVar("audioServer").setAmp(gain)

    def updatePeak(self, peak):
        self.peak = peak * 90.0 - 90.0
        label = ''
        if self.peak > 0:
            label += '+'
        label += '%2.2f dB' % self.peak
        self.peakLabel.setLabel(label)

    def resetVuMeter(self):
        self.vuMeter.resetMax()
    
    def getCfileinList(self):
        return self.cfileinList

class CInputBase(wx.Panel):
    def __init__(self, parent, id=-1, label='', size=(-1,-1), style=wx.NO_BORDER, name=''):
        wx.Panel.__init__(self, parent, id, size=size, style=style, name=name)
        self.SetBackgroundColour(BACKGROUND_COLOUR)

        self.frameOpen = False
        self.samplerFrame = None
        self.label = label
        self.name = name
        self.duration = 0
        self.chnls = 0
        self.type = ''
        self.samprate = 0
        self.bitrate = 0       
        self.filePath = ''
        self.folderInfo = None
        self.mode = 0

        mainSizer = wx.FlexGridSizer(4,1)        
        mainSizer.AddSpacer((200,4))

        # Static label for the popup menu
        line1 = wx.BoxSizer(wx.HORIZONTAL)
        textLabel = wx.StaticText(self, -1, self.label + ' :')
        textLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE))
        textLabel.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        line1.Add(textLabel, 0, wx.LEFT, 2)
        mainSizer.Add(line1, 0, wx.LEFT, 8)

        # Popup menu
        line2 = wx.BoxSizer(wx.HORIZONTAL)
        line2.AddSpacer((2,-1))
        self.fileMenu = FolderPopup(self, path=None, init='', outFunction=self.onSelectSound,
                                    emptyFunction=self.onLoadFile, backColour=CONTROLLABEL_BACK_COLOUR, tooltip=TT_SEL_SOUND)
        line2.Add(self.fileMenu, 0, wx.ALIGN_CENTER | wx.RIGHT, 6)
        
        self.inputBitmaps = [ICON_INPUT_1_FILE.GetBitmap(), 
                            ICON_INPUT_2_LIVE.GetBitmap(), 
                            ICON_INPUT_3_MIC.GetBitmap(), 
                            ICON_INPUT_4_MIC_RECIRC.GetBitmap()]
        self.modebutton = statbmp.GenStaticBitmap(self, -1, self.inputBitmaps[0])
        self.modebutton.SetBackgroundColour(BACKGROUND_COLOUR)
        self.modebutton.Bind(wx.EVT_LEFT_DOWN, self.onChangeMode)
        line2.Add(self.modebutton, 0, wx.ALIGN_CENTER | wx.TOP, 2)

        self.toolbox = ToolBox(self, tools=['play','edit','open'],
                               outFunction=[self.listenSoundfile,self.editSoundfile, self.onShowSampler])
        self.toolbox.setOpen(False)
        line2.Add(self.toolbox,0,wx.ALIGN_CENTER | wx.TOP | wx.LEFT, 2)
        
        mainSizer.Add(line2, 1, wx.LEFT, 6)
        mainSizer.AddSpacer((5,2))

        self.createSamplerFrame()

        self.SetSizer(mainSizer)

        CeciliaLib.getVar("userInputs")[self.name] = dict()
        CeciliaLib.getVar("userInputs")[self.name]['path'] = ''

    def enable(self, state):
        self.toolbox.enable(state)

    def onChangeMode(self, evt):
        self.mode = (self.mode + 1) % 4
        self.modebutton.SetBitmap(self.inputBitmaps[self.mode])
        CeciliaLib.getVar("userInputs")[self.name]['mode'] = self.mode
        self.processMode()

    def getMode(self):
        return self.mode

    def onShowSampler(self):
        if self.mode != 1:
            if self.samplerFrame.IsShown():
                self.samplerFrame.Hide()
            else:
                pos = wx.GetMousePosition()
                framepos = (pos[0]+10, pos[1]+20)
                self.samplerFrame.SetPosition(framepos)
                self.samplerFrame.Show()

    def getDuration(self):
        return self.duration
    
    def setTotalTime(self):
        if self.duration:
            CeciliaLib.getControlPanel().setTotalTime(self.duration)
            CeciliaLib.getControlPanel().updateDurationSlider()

    def reset(self):
        self.fileMenu.reset()
        self.filePath = ''
        CeciliaLib.getVar("userInputs")[self.name]['path'] = self.filePath

    def getSoundInfos(self, file):
        file = CeciliaLib.ensureNFD(file)
        self.filePath = CeciliaLib.ensureNFD(self.folderInfo[file]['path'])
        self.duration = self.folderInfo[file]['dur']
        self.chnls = self.folderInfo[file]['chnls']
        self.type = self.folderInfo[file]['type']
        self.samprate = self.folderInfo[file]['samprate']
        self.bitrate = self.folderInfo[file]['bitrate']
        self.samplerFrame.offsetSlider.setEnable(True)
        self.samplerFrame.offsetSlider.SetRange(0,self.duration)
        self.samplerFrame.offsetSlider.SetValue(self.getOffset())
        self.samplerFrame.update(path=self.filePath,
                                 dur=self.duration,
                                 type=self.type,
                                 bitDepth=self.bitrate,
                                 chanNum=self.chnls,
                                 sampRate=self.samprate)    
        CeciliaLib.getVar("userInputs")[self.name]['sr%s' % self.name] = self.samprate
        CeciliaLib.getVar("userInputs")[self.name]['dur%s' % self.name] = self.duration
        CeciliaLib.getVar("userInputs")[self.name]['nchnls%s' % self.name] = self.chnls
        CeciliaLib.getVar("userInputs")[self.name]['off%s' % self.name] = self.getOffset()
        CeciliaLib.getVar("userInputs")[self.name]['path'] = self.filePath

    def onLoadFile(self, filePath=''):
        wildcard = "All files|*.*|" \
                   "AIFF file|*.aif;*.aiff;*.aifc;*.AIF;*.AIFF;*.Aif;*.Aiff|"     \
                   "Wave file|*.wav;*.wave;*.WAV;*.WAVE;*.Wav;*.Wave"

        if filePath == '':        
            path = CeciliaLib.openAudioFileDialog(self, wildcard, 
                    defaultPath=CeciliaLib.getVar("openAudioFilePath", unicode=True))
        elif not os.path.isfile(filePath):
            return
        else:
            path = filePath
        
        if path == None:
            return
        if not CeciliaLib.getVar("audioServer").validateAudioFile(path):
            CeciliaLib.showErrorDialog("Unable to retrieve sound infos", "There is something wrong with this file, please select another one.")
            return

        if path:
            self.updateMenuFromPath(path)
            lastfiles = CeciliaLib.getVar("lastAudioFiles")
            if lastfiles != "":
                lastfiles = lastfiles.split(";")
            else:
                lastfiles = []
            if path in lastfiles:
                return
            if len(lastfiles) >= 10:
                lastfile = lastfiles[1:]
            lastfiles.append(path)
            lastfiles = ";".join(lastfiles)
            CeciliaLib.setVar("lastAudioFiles", lastfiles)

    def updateMenuFromPath(self, path):
        if os.path.isfile(path):
            root = os.path.split(path)[0]
            isfile = True
        elif os.path.isdir(path):
            root = path
            isfile = False
        
        pathList = []
        for p in os.listdir(root):
            pathList.append(os.path.join(root,p))
        self.folderInfo = CeciliaLib.getVar("audioServer").getSoundsFromList(pathList)
        files = self.folderInfo.keys()
        files.sort()
        
        self.fileMenu.setChoice(files)
        if isfile:
            self.fileMenu.setLabel(CeciliaLib.ensureNFD(os.path.split(path)[1]))
        else:
            self.fileMenu.setLabel(CeciliaLib.ensureNFD(files[0]))
            
    def listenSoundfile(self):
        CeciliaLib.listenSoundfile(self.filePath)
    
    def editSoundfile(self):
        CeciliaLib.editSoundfile(self.filePath)

    def onOffsetSlider(self, value):
        CeciliaLib.getVar("userInputs")[self.name]['off%s' % self.name] = value
        if self.mode >= 2:
            newMaxDur = value
        elif self.duration != None:
            newMaxDur = self.duration - value
        CeciliaLib.getVar("userInputs")[self.name]['dur%s' % self.name] = newMaxDur
        try:
            self.samplerFrame.loopInSlider.setRange(0, newMaxDur)
            self.samplerFrame.loopOutSlider.setRange(0, newMaxDur)
        except:
            pass    
    
    def setOffset(self, value):
        CeciliaLib.getVar("userInputs")[self.name]['off%s' % self.name] = value
        self.samplerFrame.offsetSlider.setEnable(True)
        self.samplerFrame.offsetSlider.SetValue(value)

    def getOffset(self):
        return self.samplerFrame.offsetSlider.GetValue()

    def getName(self):
        return self.name

    def getSamplerFrame(self):
        return self.samplerFrame

class Cfilein(CInputBase):
    def __init__(self, parent, id=-1, label='', size=(-1,-1), style = wx.NO_BORDER, name=''):   
        CInputBase.__init__(self, parent, id, label=label, size=size, style=style, name=name)
        CeciliaLib.getVar("userInputs")[self.name]['type'] = 'cfilein'
        
    def processMode(self):
        if self.mode in [1,3]:
            self.mode = (self.mode + 1) % 4
            self.modebutton.SetBitmap(self.inputBitmaps[self.mode])
            CeciliaLib.getVar("userInputs")[self.name]['mode'] = self.mode
        if self.mode == 0:
            self.fileMenu.setEnable(True)
            self.samplerFrame.textOffset.SetLabel('Offset :')
            self.samplerFrame.offsetSlider.SetValue(0)
            self.samplerFrame.liveInputHeader(False)
        elif self.mode == 2:
            self.fileMenu.setEnable(False)
            self.samplerFrame.textOffset.SetLabel('Table Length (sec) :')
            self.samplerFrame.offsetSlider.setEnable(True)
            self.samplerFrame.offsetSlider.SetValue(5)
            self.samplerFrame.liveInputHeader(True)

    def createSamplerFrame(self):
        self.samplerFrame = CfileinFrame(self, self.name)

    def onSelectSound(self, idx, file):
        self.getSoundInfos(file)

class CSampler(CInputBase):
    def __init__(self, parent, id=-1, label='', size=(-1,-1), style = wx.NO_BORDER, name=''):
        CInputBase.__init__(self, parent, id, label=label, size=size, style=style, name=name)

        self.outputChnls = 1
        self.gainMod = None
        self.transMod = None
        self.startPos = None
       
        CeciliaLib.getVar("userInputs")[self.name]['type'] = 'csampler'
        
    def processMode(self):
        grapher = CeciliaLib.getVar('grapher')
        if self.mode == 0:
            self.fileMenu.setEnable(True)
            grapher.setSamplerLineStates(self.name, True)
            self.samplerFrame.textOffset.SetLabel('Offset :')
            self.samplerFrame.offsetSlider.SetValue(0)
            self.samplerFrame.liveInputHeader(False)
        elif self.mode == 1:
            self.fileMenu.setEnable(False)
            grapher.setSamplerLineStates(self.name, False)
            if self.samplerFrame.IsShown():
                self.samplerFrame.Hide()
                self.toolbox.setOpen(False)
        else:
            grapher.setSamplerLineStates(self.name, True)
            self.samplerFrame.textOffset.SetLabel('Table Length (sec) :')
            self.samplerFrame.offsetSlider.setEnable(True)
            self.samplerFrame.offsetSlider.SetValue(5)
            self.samplerFrame.liveInputHeader(True, self.mode)

    def setOutputChnls(self, chnls):
        self.outputChnls = chnls

    def getOutputChnls(self):
        return self.outputChnls

    def createSamplerFrame(self):
        self.samplerFrame = SamplerFrame(self, self.name)

    def onSelectSound(self, idx, file):
        self.getSoundInfos(file)

        for line in CeciliaLib.getVar("grapher").plotter.getData():
            if line.getName() == self.samplerFrame.loopInSlider.getCName() or line.getName() == self.samplerFrame.loopOutSlider.getCName():
                line.changeYrange((0, self.duration))
        
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("currentModule")._samplers[self.name].setSound(self.filePath)
        
    def getSamplerInfo(self):
        info = {}
        info['loopMode'] = self.samplerFrame.getLoopMode()
        info['startFromLoop'] = self.samplerFrame.getStartFromLoop()
        info['loopX'] = self.samplerFrame.getLoopX()
        info['loopIn'] = self.samplerFrame.getLoopIn()
        info['loopOut'] = self.samplerFrame.getLoopOut()
        info['gain'] = self.samplerFrame.getGain()
        info['transp'] = self.samplerFrame.getTransp()
        info['xfadeshape'] = self.samplerFrame.getXfadeShape()
        return info

    def getSamplerSliders(self):
        return self.getSamplerFrame().sliderlist

class CfileinFrame(wx.Frame):
    def __init__(self, parent, name, pos=wx.DefaultPosition):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT)
        wx.Frame.__init__(self, parent, title='', pos=pos, style=style)
        self.parent = parent
        self.name = name
        
        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()
            
        panel = wx.Panel(self, -1)
        w, h = self.GetSize()
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)
        
        # Header
        self.title = FrameLabel(panel, '', size=(w-2, 50))
        box.Add(self.title, 0, wx.ALL, 1)
  
        box.AddSpacer((200,2))

        #toolbox
        toolsBox = wx.BoxSizer(wx.HORIZONTAL)
        tools = ToolBox(panel, size=(80,20), tools=['play', 'edit', 'time' ],
                        outFunction=[self.parent.listenSoundfile,
                                       self.parent.editSoundfile,
                                       self.parent.setTotalTime])
        toolsBox.Add(tools, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 320)       
        box.Add(toolsBox, 0, wx.TOP, 5)

        # Static label for the offset slider
        line3 = wx.BoxSizer(wx.HORIZONTAL)
        textLabel2 = wx.StaticText(self, -1, self.parent.label)
        textLabel2.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        textLabel2.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        textLabel2.SetBackgroundColour(BACKGROUND_COLOUR)
        line3.Add(textLabel2,0,wx.ALL, 0)
        
        self.textOffset = wx.StaticText(self, -1, ' Offset :')
        self.textOffset.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        self.textOffset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        self.textOffset.SetBackgroundColour(BACKGROUND_COLOUR)
        line3.Add(self.textOffset,0,wx.ALL, 0)
        
        box.Add(line3, 0, wx.LEFT, 20)
              
        # Offset slider
        self.offsetSlider = ControlSlider(self, minvalue=0, maxvalue=100, size=(222,15), init=0,
                                          outFunction=self.parent.onOffsetSlider, backColour=POPUP_BACK_COLOUR)
        self.offsetSlider.setSliderHeight(10)
        self.offsetSlider.setEnable(False)
        box.Add(self.offsetSlider, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        box.AddSpacer((200,10))

        self.close = CloseBox(panel, outFunction=self.close)
        box.Add(self.close, 0, wx.LEFT, 330)

        box.AddSpacer((200,7))

        panel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        self.title.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

        panel.SetSizerAndFit(box)
        self.Show(False)

    def OnLooseFocus(self, event):
        win = wx.FindWindowAtPointer()
        if win != None:
            if win.GetTopLevelParent() in [self, CeciliaLib.getVar("mainFrame")]:
                pass
            else:
                win = CeciliaLib.getVar("interface")
                win.Raise()

    def close(self):
        self.Hide()
        self.GetParent().toolbox.setOpen(False)

    def update(self, path, dur, type, bitDepth, chanNum, sampRate):
        self.path = path
        self.dur = dur
        self.type = type
        self.bitDepth = bitDepth
        self.chanNum = chanNum
        self.sampRate = sampRate
        soundInfoText = self.createHeader()
        self.title.setLabel(soundInfoText)
     
    def createHeader(self):
        if self.sampRate > 1000:
            self.sampRate = self.sampRate / 1000.
        header = '%s\n' % CeciliaLib.shortenName(self.path,48)
        header += '%0.2f sec - %s - %s - %d ch. - %2.1fkHz' % (self.dur, self.type, self.bitDepth, self.chanNum, self.sampRate)
        return header

    def liveInputHeader(self, yes=True):
        if yes:
            self.title.setLabel("Audio table will be filled with live input.")
        else:
            self.title.setLabel("")
    
    def SetRoundShape(self, event=None):
        self.SetShape(GetRoundShape(385, 143, 1))

class SamplerFrame(wx.Frame):
    def __init__(self, parent, name, pos=wx.DefaultPosition, size=(385, 290)):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT)
        wx.Frame.__init__(self, parent, title='', pos=pos, style=style)
        self.parent = parent
        self.size = size
        self.name = name
        
        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()
            
        self.loopList = ['Off', 'Forward', 'Backward', 'Back & Forth']
            
        panel = wx.Panel(self, -1)
        w, h = size
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)
        
        # Header
        self.title = FrameLabel(panel, '', size=(w-2, 50))
        box.Add(self.title, 0, wx.ALL, 1)

        # Static label for the offset slider
        line3 = wx.BoxSizer(wx.HORIZONTAL)
        textLabel2 = wx.StaticText(panel, -1, self.parent.label)
        textLabel2.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        textLabel2.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        textLabel2.SetBackgroundColour(BACKGROUND_COLOUR)
        line3.Add(textLabel2,0,wx.ALL, 0)
        
        self.textOffset = wx.StaticText(panel, -1, ' Offset :')
        self.textOffset.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        self.textOffset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        self.textOffset.SetBackgroundColour(BACKGROUND_COLOUR)
        line3.Add(self.textOffset,0,wx.ALL, 0)
        
        box.Add(line3, 0, wx.LEFT, 20)
        
        box.AddSpacer((200,2))
        
        # Offset slider
        offBox = wx.BoxSizer(wx.HORIZONTAL)
        self.offsetSlider = ControlSlider(panel, minvalue=0, maxvalue=100, size=(345,15), init=0,
                                          outFunction=self.parent.onOffsetSlider, backColour=POPUP_BACK_COLOUR)
        self.offsetSlider.SetToolTip(CECTooltip(TT_SAMPLER_OFFSET))                                  
        self.offsetSlider.setSliderHeight(10)
        self.offsetSlider.setEnable(False)
        offBox.Add(self.offsetSlider, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        box.Add(offBox)

        box.AddSpacer((200,10))
        
        #Loop type + toolbox
        loopBox = wx.FlexGridSizer(1,8,5,5)
        loopLabel = wx.StaticText(panel, -1, "Loop")
        loopLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        loopLabel.SetForegroundColour("#FFFFFF")
        loopBox.Add(loopLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 3)
        self.loopMenu = SamplerPopup(panel, self.loopList, self.loopList[1], self.name, outFunction=self.handleLoopMode)
        self.loopMenu.popup.SetToolTip(CECTooltip(TT_SAMPLER_LOOP))                                  
        loopBox.Add(self.loopMenu.popup, 0, wx.ALIGN_CENTER_VERTICAL)

        startLabel = wx.StaticText(panel, -1, "Start from loop")
        startLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        startLabel.SetForegroundColour("#FFFFFF")
        loopBox.Add(startLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.startToggle = SamplerToggle(panel, 0, self.name)
        self.startToggle.toggle.SetToolTip(CECTooltip(TT_SAMPLER_START))                                  
        loopBox.Add(self.startToggle.toggle, 0, wx.ALIGN_CENTER_VERTICAL)
        xfadeLabel = wx.StaticText(panel, -1, "Xfade")
        xfadeLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        xfadeLabel.SetForegroundColour("#FFFFFF")
        loopBox.Add(xfadeLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.xfadeSwitcher = XfadeSwitcher(panel, 0, outFunction=self.handleXfadeSwitch)
        loopBox.Add(self.xfadeSwitcher, 0, wx.ALIGN_CENTER_VERTICAL)
        tools = ToolBox(panel, size=(80,20), tools=['play', 'edit', 'time' ],
                        outFunction=[self.parent.listenSoundfile,
                                       self.parent.editSoundfile,
                                       self.parent.setTotalTime])
        loopBox.Add(tools, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        loopBox.AddGrowableCol(2)
        
        box.Add(loopBox, 0, wx.ALL, 10)
        
        # Sliders
        slidersBox = wx.FlexGridSizer(5, 4, 5, 5)

        self.loopInSlider = SamplerSlider(panel, self.name, "Loop In", "sec", 0, 1, 0, outFunction=self.handleLoopIn)
        self.loopInSlider.slider.SetToolTip(CECTooltip(TT_SAMPLER_LOOP_IN))                                  
        slidersBox.AddMany([(self.loopInSlider.labelText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT),
                            (self.loopInSlider.buttons, 0, wx.CENTER),
                            (self.loopInSlider.slider, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5),
                            (self.loopInSlider.unit, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)])
      

        self.loopOutSlider = SamplerSlider(panel, self.name, "Loop Time", "sec", 0, 1, 1, outFunction=self.handleLoopOut)
        self.loopOutSlider.slider.SetToolTip(CECTooltip(TT_SAMPLER_LOOP_DUR))                                  
        slidersBox.AddMany([(self.loopOutSlider.labelText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT),
                            (self.loopOutSlider.buttons, 0, wx.CENTER),
                            (self.loopOutSlider.slider, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5),
                            (self.loopOutSlider.unit, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)])

        self.loopXSlider = SamplerSlider(panel, self.name, "Loop X", "%", 0, 50, 1, outFunction=self.handleLoopX)
        self.loopXSlider.slider.SetToolTip(CECTooltip(TT_SAMPLER_CROSSFADE))                                  
        slidersBox.AddMany([(self.loopXSlider.labelText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT),
                            (self.loopXSlider.buttons, 0, wx.CENTER),
                            (self.loopXSlider.slider, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5),
                            (self.loopXSlider.unit, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)])

        self.gainSlider = SamplerSlider(panel, self.name, "Gain", "dB", -48, 18, 0, outFunction=self.handleGain)
        self.gainSlider.slider.SetToolTip(CECTooltip(TT_SAMPLER_GAIN))                                  
        slidersBox.AddMany([(self.gainSlider.labelText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT),
                            (self.gainSlider.buttons, 0, wx.CENTER),
                            (self.gainSlider.slider, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5),
                            (self.gainSlider.unit, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)])

        self.transpSlider = SamplerSlider(panel, self.name, "Transpo", "cents", -48, 48, 0, integer=False, outFunction=self.handleTransp)
        self.transpSlider.slider.SetToolTip(CECTooltip(TT_SAMPLER_TRANSPO))                                  
        slidersBox.AddMany([(self.transpSlider.labelText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT),
                            (self.transpSlider.buttons, 0, wx.CENTER),
                            (self.transpSlider.slider, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5),
                            (self.transpSlider.unit, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)])

        box.Add(slidersBox, 0, wx.EXPAND | wx.ALL, 6)

        self.close = CloseBox(panel, outFunction=self.close)
        box.Add(self.close, 0, wx.LEFT, 330)

        box.AddSpacer((200,7))

        self.sliderlist = [self.loopInSlider, self.loopOutSlider, self.loopXSlider, self.gainSlider, self.transpSlider]

        samplerSliders = CeciliaLib.getVar("samplerSliders")   
        CeciliaLib.setVar("samplerSliders", samplerSliders + self.sliderlist)
        userSliders = CeciliaLib.getVar("userSliders")
        CeciliaLib.setVar("userSliders", userSliders + self.sliderlist)  

        samplerTogPop = CeciliaLib.getVar("samplerTogglePopup")
        CeciliaLib.setVar("samplerTogglePopup", samplerTogPop + [self.loopMenu, self.startToggle])
      
        panel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        self.title.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

        panel.SetSizerAndFit(box)
        self.SetSize(panel.GetSize())
        self.Show(False)

    def OnLooseFocus(self, event):
        win = wx.FindWindowAtPointer()
        if win != None:
            if win.GetTopLevelParent() in [self, CeciliaLib.getVar("mainFrame")]:
                pass
            else:
                win = CeciliaLib.getVar("interface")
                win.Raise()

    def close(self):
        self.Hide()
        self.GetParent().toolbox.setOpen(False)

    def update(self, path, dur, type, bitDepth, chanNum, sampRate):
        self.path = path
        self.dur = dur
        self.type = type
        self.bitDepth = bitDepth
        self.chanNum = chanNum
        self.sampRate = sampRate
        soundInfoText = self.createHeader()
        self.title.setLabel(soundInfoText)
        self.loopInSlider.setRange(0, self.dur)
        self.loopInSlider.setValue(0)
        self.loopOutSlider.setRange(0, self.dur)
        self.loopOutSlider.setValue(self.dur)
     
    def createHeader(self):
        if self.sampRate > 1000:
            self.sampRate = self.sampRate / 1000.
        header = '%s\n' % CeciliaLib.shortenName(self.path,48)
        header += '%0.2f sec - %s - %s - %d ch. - %2.1fkHz' % (self.dur, self.type, self.bitDepth, self.chanNum, self.sampRate)
        return header

    def liveInputHeader(self, yes=True, mode=2):
        if yes:
            if mode == 2:
                self.title.setLabel("Audio table will be filled with live input.")
            else:
                self.title.setLabel("Audio table (double buffered) will be continuously filled with live input.")
        else:
            self.title.setLabel("")
            
    def SetRoundShape(self, event=None):
        w, h = self.size
        self.SetShape(GetRoundShape(w, h, 1))

    def handleXfadeSwitch(self, value):
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("currentModule")._samplers[self.name].setXfadeShape(value)

    def setXfadeShape(self, value):
        self.xfadeSwitcher.setValue(value)

    def getXfadeShape(self):
        return self.xfadeSwitcher.getValue()
        
    def handleLoopMode(self, value):
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("currentModule")._samplers[self.name].setLoopMode(value)
        
    def setLoopMode(self, index):
        self.loopMenu.popup.setByIndex(index)
        
    def getLoopMode(self):
        return self.loopMenu.getValue()

    def setStartFromLoop(self, value):
        self.startToggle.setValue(value)
        
    def getStartFromLoop(self):
        return self.startToggle.getValue()

    def handleLoopX(self, value):
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("currentModule")._samplers[self.name].setXfade(value)
         
    def setLoopX(self, values):
        self.loopXSlider.setValue(values[0])
        self.loopXSlider.setPlay(values[1])
        
    def getLoopX(self):
        return [self.loopXSlider.getValue(), self.loopXSlider.getPlay(), self.loopXSlider.getRec()] 

    def handleLoopIn(self, value):
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("currentModule")._samplers[self.name].setStart(value)
        
    def setLoopIn(self, values):
        self.loopInSlider.setValue(values[0])
        self.loopInSlider.setPlay(values[1])
        
    def getLoopIn(self):
        return [self.loopInSlider.getValue(), self.loopInSlider.getPlay(), self.loopInSlider.getRec()]

    def handleLoopOut(self, value):
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("currentModule")._samplers[self.name].setDur(value)
        
    def setLoopOut(self, values):
        self.loopOutSlider.setValue(values[0])
        self.loopOutSlider.setPlay(values[1])
        
    def getLoopOut(self):
        return [self.loopOutSlider.getValue(), self.loopOutSlider.getPlay(), self.loopOutSlider.getRec()]

    def handleGain(self, value):
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("currentModule")._samplers[self.name].setGain(value)
        
    def setGain(self, values):
        self.gainSlider.setValue(values[0])
        self.gainSlider.setPlay(values[1])
        
    def getGain(self):
        return [self.gainSlider.getValue(), self.gainSlider.getPlay(), self.gainSlider.getRec()]
        
    def handleTransp(self, value):
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("currentModule")._samplers[self.name].setPitch(value)

    def setTransp(self, values):
        self.transpSlider.setValue(values[0])
        self.transpSlider.setPlay(values[1])
        
    def getTransp(self):
        return [self.transpSlider.getValue(), self.transpSlider.getPlay(), self.transpSlider.getRec()]
    
class SamplerPlayRecButtons(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=(0,0), size=(40,20)):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.playColour = SLIDER_PLAY_COLOUR_HOT
        self.recColour = SLIDER_REC_COLOUR_HOT
        self.enterWithButtonDown = False
        self.playOver = False
        self.recOver = False
        self.playOverWait = True
        self.recOverWait = True
        self.play = False
        self.rec = False

    def setOverWait(self, which):
        if which == 0:
            self.playOverWait = False
        elif which == 1:
            self.recOverWait = False

    def checkForOverReady(self, pos):
        if not wx.Rect(2, 2, 17, 17).Contains(pos):
            self.playOverWait = True
        if not wx.Rect(21, 2, 38, 17).Contains(pos):
            self.recOverWait = True

    def setPlay(self, x):
        if x == 0: 
            self.play = False
            self.playColour = SLIDER_PLAY_COLOUR_HOT
        elif x == 1: 
            if self.rec:
                self.setRec(0)
            self.play = True
            self.playColour = SLIDER_PLAY_COLOUR_NO_BIND
        wx.CallAfter(self.Refresh)

    def setRec(self, x):
        if x == 0:
            self.rec = False
            self.recColour = SLIDER_REC_COLOUR_HOT
        else:
            if self.play:
                self.setPlay(0)
            self.rec = True
            self.recColour = SLIDER_REC_COLOUR_PRESSED
                        
    def MouseDown(self, evt):
        pos = evt.GetPosition()
        if wx.Rect(2, 2, 17, 17).Contains(pos):
            if self.play: 
                self.setPlay(0)
            else:
                self.setPlay(1)
            self.setOverWait(0)
        elif wx.Rect(21, 2, 38, 17).Contains(pos):
            if self.rec: 
                self.setRec(0)
            else: 
                self.setRec(1)
            self.setOverWait(1)
        self.playOver = False
        self.recOver = False
        wx.CallAfter(self.Refresh)
        evt.Skip()

    def OnEnter(self, evt):
        if evt.ButtonIsDown(wx.MOUSE_BTN_LEFT) and not CeciliaLib.getVar("audioServer").isAudioServerRunning():
            self.enterWithButtonDown = True
            pos = evt.GetPosition()
            if wx.Rect(0, 0, 20, 20).Contains(pos):
                if self.play: 
                    self.setPlay(0)
                else:
                    self.setPlay(1)
            elif wx.Rect(20, 0, 40, 20).Contains(pos):
                if self.rec: 
                    self.setRec(False)
                else: 
                    self.setRec(True)
            self.playOver = False
            self.recOver = False
            wx.CallAfter(self.Refresh)
            evt.Skip()

    def MouseUp(self, evt):
        self.enterWithButtonDown = False

    def OnMotion(self, evt):
        if not CeciliaLib.getVar("audioServer").isAudioServerRunning() and not self.enterWithButtonDown:
            pos = evt.GetPosition()
            if wx.Rect(2, 2, 17, 17).Contains(pos) and self.playOverWait:
                self.playOver = True
                self.recOver = False
            elif wx.Rect(21, 2, 38, 17).Contains(pos) and self.recOverWait:
                self.playOver = False
                self.recOver = True
            self.checkForOverReady(pos)
            wx.CallAfter(self.Refresh)
            evt.Skip()

    def OnLeave(self, evt):
        self.enterWithButtonDown = False
        self.playOver = False
        self.recOver = False
        self.playOverWait = True
        self.recOverWait = True
        wx.CallAfter(self.Refresh)
        evt.Skip()

    def OnPaint(self, evt):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        # Draw triangle
        if self.playOver: playColour = SLIDER_PLAY_COLOUR_OVER
        else: playColour = self.playColour
        dc.SetPen(wx.Pen(playColour, width=1, style=wx.SOLID))  
        dc.SetBrush(wx.Brush(playColour, wx.SOLID))
        dc.DrawPolygon([wx.Point(14,h/2), wx.Point(9,6), wx.Point(9,h-6)])

        dc.SetPen(wx.Pen('#333333', width=1, style=wx.SOLID))  
        dc.DrawLine(w/2,4,w/2,h-4)
        
        # Draw circle
        if self.recOver: recColour = SLIDER_REC_COLOUR_OVER
        else: recColour = self.recColour
        dc.SetPen(wx.Pen(recColour, width=1, style=wx.SOLID))  
        dc.SetBrush(wx.Brush(recColour, wx.SOLID))
        dc.DrawCircle(w/4+w/2, h/2, 4)

        evt.Skip()

    def getPlay(self):
        return self.play

    def getRec(self):
        return self.rec

class SamplerSlider:
    def __init__(self, parent, name, label, unit, mini, maxi, init, integer=False, outFunction=None):
        self.widget_type = "slider"
        self.name = name
        self.automationLength = None
        self.automationData = []
        self.outFunction = outFunction
        self.label = name + ' ' + label
        self.cname = {'Loop In': name+'start', 'Loop Time': name+'end', 
                      'Loop X': name+'xfade', 'Gain': name+'gain', 'Transpo': name+'trans'}[label]
        self.path = os.path.join(AUTOMATION_SAVE_PATH, self.cname)
        self.convertSliderValue = 200

        self.labelText = wx.StaticText(parent, -1, label)
        self.labelText.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        self.labelText.SetForegroundColour("#FFFFFF")
        self.buttons = SamplerPlayRecButtons(parent)
        self.slider = ControlSlider(parent, mini, maxi, init, size=(236, 15), integer=integer, outFunction=self.sendValue)
        self.slider.setSliderHeight(10) 
        self.unit = wx.StaticText(parent, -1, unit)
        self.unit.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        self.unit.SetForegroundColour("#FFFFFF")

    def setConvertSliderValue(self, x, end=None):
        self.convertSliderValue = x

    def getLog(self):
        return False

    def getMinValue(self):
        return self.slider.getMinValue()

    def getMaxValue(self):
        return self.slider.getMaxValue()

    def setAutomationLength(self, x):
        self.automationLength = x

    def getAutomationLength(self):
        return self.automationLength

    def sendValue(self, value):
        if self.getPlay() == False or self.getRec() == True:
            if self.outFunction != None:
                self.outFunction(value)

    def setRange(self, minval, maxval):
        self.slider.SetRange(minval, maxval)
        self.setValue(self.getValue())
        self.slider.OnPaint(wx.PaintEvent(-1))
        
    def setValue(self, val):
        self.slider.SetValue(val)
    
    def getValue(self):
        return self.slider.GetValue()

    def getLabel(self):
        return self.label

    def getCName(self):
        return self.cname

    def getName(self):
        return self.name

    def setPlay(self, x):
        self.buttons.setPlay(x)

    def getPlay(self):
        return self.buttons.getPlay()

    def setRec(self, x):
        self.buttons.setRec(x)

    def getRec(self):
        return self.buttons.getRec()

    def getValue(self):
        return self.slider.GetValue()

    def getPath(self):
        return self.path

    def setAutomationData(self, data):
        # convert values on scaling
        temp = []
        log = self.getLog()
        minval = self.getMinValue()
        maxval = self.getMaxValue()
        automationlength = self.getAutomationLength()
        frac = automationlength / CeciliaLib.getVar("totalTime")
        virtuallength = len(data) / frac
        data.extend([data[-1]] * int(((1 - frac) * virtuallength)))
        totallength = float(len(data))
        oldpos = 0
        oldval = data[0]
        if log:
            maxOnMin = maxval / minval
            torec = math.log10(oldval/minval) / math.log10(maxOnMin)
        else:
            maxMinusMin = maxval - minval
            torec = (oldval - minval) / maxMinusMin
        temp.append([0.0, torec])

        for i, val in enumerate(data):
            length = (i - oldpos) / totallength
            pos = oldpos / totallength + length
            if log:
                torec = math.log10(val/minval) / math.log10(maxOnMin)
            else:
                torec = (val - minval) / maxMinusMin 
            temp.append([pos, torec])
            oldval = val
            oldpos = i

        self.automationData = temp

    def getAutomationData(self):
        return [[x[0],x[1]] for x in self.automationData]

