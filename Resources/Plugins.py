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

import wx, math
from constants import *
import CeciliaLib
from Widgets import *

class PluginArrow(wx.Panel):
    def __init__(self, parent, dir="up", size=(8,10), outFunction=None, colour=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.outFunction = outFunction
        self.dir = dir
        self.hover = 0
        if colour:
            self.colour = colour
        else:
            self.colour = BACKGROUND_COLOUR
        if self.dir == "up":
            self.bitmaps = [ICON_PLUGINS_ARROW_UP.GetBitmap(), ICON_PLUGINS_ARROW_UP_HOVER.GetBitmap()]
        else:
            self.bitmaps = [ICON_PLUGINS_ARROW_DOWN.GetBitmap(), ICON_PLUGINS_ARROW_DOWN_HOVER.GetBitmap()]
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_ENTER_WINDOW, self.MouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.MouseLeave)

    def MouseEnter(self, evt):
        self.hover = 1
        wx.CallAfter(self.Refresh)
        
    def MouseLeave(self, evt):
        self.hover = 0
        wx.CallAfter(self.Refresh)

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        dc.DrawBitmap(self.bitmaps[self.hover], 0, 0, True)

    def MouseDown(self, event):
        if self.outFunction:
            self.outFunction(self.dir)
        #wx.CallAfter(self.Refresh)
        event.Skip()

class PluginKnob(ControlKnob):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0,0), size=(50,70), 
                log=False, outFunction=None, integer=False, backColour=None, label=''):
        ControlKnob.__init__(self, parent, minvalue, maxvalue, init, pos, size, 
                            log, outFunction, integer, backColour, label) 

        self.Bind(wx.EVT_RIGHT_DOWN, self.MouseRightDown)
        self.widget_type = "plugin_knob"
        self.name = ''
        self.longLabel = ''
        self.gliss = 0
        self.midictl = None
        self.midichan = 1
        self.midictlLabel = ''
        self.midiLearn = False
        self.automationLength = None
        self.automationData = []
        self.path = None
        self.play = False
        self.rec = False
        self.convertSliderValue = 200

    def getParentVPos(self):
        return self.GetParent().vpos

    def getKnobPos(self):
        names = self.GetParent().getKnobNames()
        return names.index(self.name)

    def setConvertSliderValue(self, x, end=None):
        self.convertSliderValue = x

    def getValue(self):
        return self.GetValue()

    def setValue(self, x):
        self.SetValue(x)

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
        self.path = os.path.join(AUTOMATION_SAVE_PATH, self.name)

    def setLongLabel(self, label):
        self.longLabel = label

    def getLongLabel(self):
        return self.longLabel
        
    def setPlay(self, x):
        if x:
            self.mode = 2
            data = CeciliaLib.getVar("grapher").plotter.data
            for line in data:
                if line.getName() == self.name:
                    line.setShow(1)
                    CeciliaLib.getVar("grapher").plotter.draw()
        else:
            self.mode = 0
        self.Refresh()

    def setRec(self, x):
        if x:
            self.mode = 1
        else:
            self.mode = 0
        self.Refresh()

    def getPlay(self):
        if self.mode == 2:
            return True
        else:
            return False

    def getPlayState(self):
        return self.mode
        
    def getRec(self):
        if self.mode == 1:
            return True
        else:
            return False

    def getPath(self):
        return self.path

    def getState(self):
        return [self.getValue(), self.getPlayState(), self.getMidiCtl(), self.getMidiChannel()]

    def setState(self, values):
        self.setValue(values[0])
        self.setPlay(values[1])
        self.setMidiCtl(values[2])
        if len(values) >= 4:
            self.setMidiChannel(values[3])

    def inMidiLearnMode(self):
        self.midiLearn = True
        self.Refresh()

    def setMidiCtl(self, ctl):
        if ctl == None:
            self.midictl = None
            self.midichan = 1
            self.midictlLabel = ''
            self.midiLearn = False
        else:    
            self.midictl = int(ctl)
            self.midictlLabel = str(self.midictl)
            self.midiLearn = False
        self.Refresh()

    def getMidiCtl(self):
        return self.midictl

    def setMidiChannel(self, chan):
        self.midichan = int(chan)
        
    def getMidiChannel(self):
        return self.midichan
            
    def getWithMidi(self):
        if self.getMidiCtl() != None and CeciliaLib.getVar("useMidi"):
            return True
        else:
            return False

    def setAutomationLength(self, x):
        self.automationLength = x

    def getAutomationLength(self):
        return self.automationLength

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

    def update(self, val):
        if not self.HasCapture() and self.getPlay() == 1 or self.getWithMidi():
            self.setValue(val)

    def MouseRightDown(self, evt):
        if self._enable:                
            rec = wx.Rect(5, 13, 45, 45)
            pos = evt.GetPosition()
            if rec.Contains(pos):
                if evt.ShiftDown():
                    self.setMidiCtl(None)
                else:
                    if CeciliaLib.getVar("useMidi"):
                        CeciliaLib.getVar("audioServer").midiLearn(self)
                        self.inMidiLearnMode()
                    else:
                        CeciliaLib.showErrorDialog("Midi not initialized!",
                            "There is no Midi interface connected!")
        evt.Skip()

class Plugin(wx.Panel):
    def __init__(self, parent, choiceFunc, order):
        wx.Panel.__init__(self, parent, pos=wx.DefaultPosition)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.choiceFunc = choiceFunc
        self.order = order
        self.vpos = order

    def setKnobLabels(self):
        if self.pluginName != 'None':
            for i, knob in enumerate(self.getKnobs()):
                knob.setLongLabel("PP%d %s %s" % (self.vpos+1, self.pluginName, knob.getLabel()))

    def setKnobNames(self):
        if self.pluginName != 'None':
            for i, knob in enumerate(self.getKnobs()):
                knob.setName(self.knobNameTemplates[i] % self.vpos)
        
    def replacePlugin(self, i, new):
        self.choiceFunc(self.vpos, new)

    def getName(self):
        return self.pluginName

    def getKnobs(self):
        return [self.knob1, self.knob2, self.knob3]

    def getKnobNames(self):
        return [knob.getName() for knob in self.getKnobs()]

    def getKnobLongLabels(self):
        return [knob.getLongLabel() for knob in self.getKnobs()]

    def getParams(self):
        return [self.knob1.GetValue(),self.knob2.GetValue(),self.knob3.GetValue(),self.preset.getIndex()]

    def getStates(self):
        return [self.knob1.getState(),self.knob2.getState(),self.knob3.getState()]

    def setStates(self, states):
        self.knob1.setState(states[0])
        self.knob2.setState(states[1])
        self.knob3.setState(states[2])

    def setParams(self, params):
        self.knob1.SetValue(params[0])
        self.knob2.SetValue(params[1])
        self.knob3.SetValue(params[2])
        self.preset.setByIndex(params[3])

    def initAudioServerChannels(self):
        self.onChangeKnob1(self.knob1.GetValue())
        self.onChangeKnob2(self.knob2.GetValue())
        self.onChangeKnob3(self.knob3.GetValue())
        self.onChangePreset(self.preset.getIndex())

    def onChangeKnob1(self, x):
        if self.knob1.getState()[1] in [0,1]:
            if CeciliaLib.getVar("currentModule") != None:
                CeciliaLib.getVar("audioServer").setPluginValue(self.vpos, 0, x)

    def onChangeKnob2(self, x):
        if self.knob2.getState()[1] in [0,1]:
            if CeciliaLib.getVar("currentModule") != None:
                CeciliaLib.getVar("audioServer").setPluginValue(self.vpos, 1, x)

    def onChangeKnob3(self, x):
        if self.knob3.getState()[1] in [0,1]:
            if CeciliaLib.getVar("currentModule") != None:
                CeciliaLib.getVar("audioServer").setPluginValue(self.vpos, 2, x)

    def onChangePreset(self, x, label=None):
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("audioServer").setPluginPreset(self.vpos, x, label)

    def createHeadBox(self):
        self.headBox = wx.BoxSizer(wx.HORIZONTAL)
        plugChoiceText = wx.StaticText(self, -1, 'Effects:')
        plugChoiceText.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoiceText.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        self.headBox.Add(plugChoiceText, 0)
        self.tw,th = plugChoiceText.GetTextExtent('Effects:')
        self.headBox.AddSpacer((75 - self.tw, -1))
        self.arrowUp = PluginArrow(self, "up", outFunction=self.arrowLeftDown)
        self.headBox.Add(self.arrowUp, 0)
        self.arrowDown = PluginArrow(self, "down", outFunction=self.arrowLeftDown)
        self.headBox.Add(self.arrowDown, 0)
        if self.vpos == 0:
            self.headBox.GetChildren()[1].SetSpacer((83 - self.tw, -1))
            self.arrowUp.Hide()
        if self.vpos == (NUM_OF_PLUGINS - 1):
            self.arrowDown.Hide()

    def checkArrows(self):
        if self.vpos == 0:
            self.headBox.GetChildren()[1].SetSpacer((83 - self.tw, -1))
            self.arrowUp.Hide()
            self.arrowDown.Show()
            self.headBox.Layout()
        elif self.vpos == (NUM_OF_PLUGINS - 1):
            self.headBox.GetChildren()[1].SetSpacer((75 - self.tw, -1))
            self.arrowUp.Show()
            self.arrowDown.Hide()
            self.headBox.Layout()
        else:
            self.headBox.GetChildren()[1].SetSpacer((75 - self.tw, -1))
            self.arrowUp.Show()
            self.arrowDown.Show()
            self.headBox.Layout()

    def arrowLeftDown(self, dir):
        if dir == "up":
            CeciliaLib.getControlPanel().movePlugin(self.vpos, -1)
        else:
            CeciliaLib.getControlPanel().movePlugin(self.vpos, 1)

class NonePlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'None'
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0, 1, 0, size=(43,70), label='None')
        self.knob1.setEnable(False)    
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0, 1, 0, size=(43,70), label='None')
        self.knob2.setEnable(False)    
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, 1, 0, size=(43,70), label='None')
        self.knob3.setEnable(False)    
        self.sizer.Add(self.knob3)
        
        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='None', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)
        
        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['None'], init='None', size=(93,18), colour=CONTROLLABEL_BACK_COLOUR)
        self.preset.setEnable(False)
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)
        
        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class ReverbPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Reverb'
        self.knobNameTemplates = ['plugin_%d_reverb_mix', 'plugin_%d_reverb_time', 'plugin_%d_reverb_damp']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0, 1, 0.25, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Mix')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0.01, 10, 1, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Time')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, 1, 0.5, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Damp')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()
        
        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Reverb', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)
        
        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_reverb_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class WGReverbPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'WGVerb'
        self.knobNameTemplates = ['plugin_%d_wgreverb_mix', 'plugin_%d_wgreverb_feed', 'plugin_%d_wgreverb_lp']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0, 1, 0.25, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Mix')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0., 1, 0.7, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Feed')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 100, 15000, 5000, size=(43,70), log=True, outFunction=self.onChangeKnob3, label='Cutoff')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)
        self.knob3.setFloatPrecision(2)   
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='WGVerb', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_wgreverb_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class FilterPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Filter'
        self.knobNameTemplates = ['plugin_%d_filter_level', 'plugin_%d_filter_freq', 'plugin_%d_filter_q']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0, 2, 1, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Level')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 20, 18000, 1000, size=(43,70), log=True, outFunction=self.onChangeKnob2, label='Freq')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.knob2.setFloatPrecision(0)     
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0.5, 10, 1, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Q')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Filter', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Lowpass', 'Highpass', 'Bandpass', 'Bandreject'], init='Lowpass', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_filter_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class EQPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Para EQ'
        self.knobNameTemplates = ['plugin_%d_eq_freq', 'plugin_%d_eq_q', 'plugin_%d_eq_gain']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 20, 18000, 1000, size=(43,70), log=True, outFunction=self.onChangeKnob1, label='Freq')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.knob1.setFloatPrecision(0)     
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, .5, 10, 1, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Q')
        self.knob2.setName(self.knobNameTemplates[1] % self.order)
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, -48, 18, -3, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Gain')
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Para EQ', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Peak/Notch', 'Lowshelf', 'Highshelf'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_eq_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class EQ3BPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = '3 Bands EQ'
        self.knobNameTemplates = ['plugin_%d_eq3b_low', 'plugin_%d_eq3b_mid', 'plugin_%d_eq3b_high']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, -60, 18, 0, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Low')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.knob1.setFloatPrecision(2)
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, -60, 18, 0, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Mid')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.knob2.setFloatPrecision(2)
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, -60, 18, 0, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='High')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.knob3.setFloatPrecision(2)
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='3 Bands EQ', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_eq3b_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class ChorusPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Chorus'
        self.knobNameTemplates = ['plugin_%d_chorus_mix', 'plugin_%d_chorus_depth', 'plugin_%d_chorus_feed']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0, 1, 0.5, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Mix')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0.001, 5., 0.2, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Depth')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, 1, .5, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Feed')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Chorus', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Flange', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_chorus_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class CompressPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Compress'
        self.knobNameTemplates = ['plugin_%d_comp_thresh', 'plugin_%d_comp_ratio', 'plugin_%d_comp_gain']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, -80, 0, -20, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Thresh')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.knob1.setFloatPrecision(1)     
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0.125, 20, 3, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Ratio')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.knob2.setFloatPrecision(3)
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, -36, 36, 0, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Gain')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Compress', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_comp_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class GatePlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Gate'
        self.knobNameTemplates = ['plugin_%d_gate_thresh', 'plugin_%d_gate_rise', 'plugin_%d_gate_fall']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, -120, 0, -70, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Thresh')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0.0005, .5, 0.005, size=(43,70), log=True, outFunction=self.onChangeKnob2, label='Rise')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0.0005, .5, .01, size=(43,70), log=True, outFunction=self.onChangeKnob3, label='Fall')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Gate', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_gate_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class DistoPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Disto'
        self.knobNameTemplates = ['plugin_%d_disto_drive', 'plugin_%d_disto_slope', 'plugin_%d_disto_gain']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0, 1, .7, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Drive')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0, 1, .7, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Slope')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, -60, 0, -12, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Gain')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Disto', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_disto_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class AmpModPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'AmpMod'
        self.knobNameTemplates = ['plugin_%d_ampmod_freq', 'plugin_%d_ampmod_amp', 'plugin_%d_ampmod_stereo']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0.01, 1000, 8, size=(43,70), log=True, outFunction=self.onChangeKnob1, label='Freq')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0, 1, 1, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Amp')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, 0.5, 0, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Stereo')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='AmpMod', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Amplitude', 'RingMod'], init='Amplitude', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_ampmod_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class PhaserPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Phaser'
        self.knobNameTemplates = ['plugin_%d_phaser_freq', 'plugin_%d_phaser_q', 'plugin_%d_phaser_spread']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 20, 1000, 100, size=(43,70), log=True, outFunction=self.onChangeKnob1, label='Freq')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.knob1.setFloatPrecision(2)     
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 1, 20, 5, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Q')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, .5, 2, 1.1, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Spread')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Phaser', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_phaser_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class DelayPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Delay'
        self.knobNameTemplates = ['plugin_%d_delay_delay', 'plugin_%d_delay_feed', 'plugin_%d_delay_mix']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0.01, 1, .1, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Delay')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0, .999, 0, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Feed')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, 1, 0.5, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Mix')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Delay', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_delay_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class FlangePlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Flange'
        self.knobNameTemplates = ['plugin_%d_flange_depth', 'plugin_%d_flange_freq', 'plugin_%d_flange_feed']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0.001, .99, .5, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Depth')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0.005, 20, 1, size=(43,70), log=True, outFunction=self.onChangeKnob2, label='Freq')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, .999, 0.5, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Feed')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Flange', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_flange_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class HarmonizerPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Harmonizer'
        self.knobNameTemplates = ['plugin_%d_harmonizer_transpo', 'plugin_%d_harmonizer_feed', 'plugin_%d_harmonizer_mix']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, -24, 24, -7, size=(43,70), log=False, outFunction=self.onChangeKnob1, label='Transpo')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0, .999, 0, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Feed')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, 1, 0.5, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Mix')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Harmonizer', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_harmonizer_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)


class ResonatorsPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'Resonators'
        self.knobNameTemplates = ['plugin_%d_resonators_freq', 'plugin_%d_resonators_spread', 'plugin_%d_resonators_mix']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 20, 1000, 80, size=(43,70), log=True, outFunction=self.onChangeKnob1, label='Freq')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.knob1.setFloatPrecision(2)     
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, .25, 4, 2.01, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Spread')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, 1, 0.33, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Mix')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='Resonators', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_resonators_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class DeadResonPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'DeadReson'
        self.knobNameTemplates = ['plugin_%d_deadresonators_freq', 'plugin_%d_deadresonators_detune', 'plugin_%d_deadresonators_mix']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 20, 1000, 80, size=(43,70), log=True, outFunction=self.onChangeKnob1, label='Freq')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.knob1.setFloatPrecision(2)     
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0, 1, 0.5, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Detune')        
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, 1, 0.33, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Mix')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='DeadReson', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Active'], init='Active', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_deadresonators_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)

class ChaosModPlugin(Plugin):
    def __init__(self, parent, choiceFunc, order):
        Plugin.__init__(self, parent, choiceFunc, order)
        self.pluginName = 'ChaosMod'
        self.knobNameTemplates = ['plugin_%d_chaosmod_freq', 'plugin_%d_chaosmod_amp', 'plugin_%d_chaosmod_amp']
        self.sizer = wx.FlexGridSizer(1,4,0,0)
        revMenuBox = wx.BoxSizer(wx.VERTICAL)

        self.knob1 = PluginKnob(self, 0.001, 1, 0.025, size=(43,70), log=True, outFunction=self.onChangeKnob1, label='Speed')
        self.knob1.setName(self.knobNameTemplates[0] % self.order)       
        self.sizer.Add(self.knob1)

        self.knob2 = PluginKnob(self, 0, 1, 0.5, size=(43,70), log=False, outFunction=self.onChangeKnob2, label='Chaos')    
        self.knob2.setName(self.knobNameTemplates[1] % self.order)       
        self.sizer.Add(self.knob2)

        self.knob3 = PluginKnob(self, 0, 1, 1, size=(43,70), log=False, outFunction=self.onChangeKnob3, label='Amp')        
        self.knob3.setName(self.knobNameTemplates[2] % self.order)       
        self.sizer.Add(self.knob3)

        self.setKnobLabels()

        self.createHeadBox()
        revMenuBox.Add(self.headBox, 0, wx.TOP, 0)
        self.choice = CustomMenu(self, choice=PLUGINS_CHOICE, init='ChaosMod', size=(93,18), colour=PLUGINPOPUP_BACK_COLOUR, outFunction=self.replacePlugin)
        self.choice.SetToolTip(CECTooltip(TT_POST_ITEMS))
        revMenuBox.Add(self.choice, 0, wx.TOP, 2)

        plugChoicePreset = wx.StaticText(self, -1, 'Type:')
        plugChoicePreset.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        plugChoicePreset.SetForegroundColour(TEXT_LABELFORWIDGET_COLOUR)
        revMenuBox.Add(plugChoicePreset, 0, wx.TOP, 6)
        self.preset = CustomMenu(self, choice=['Bypass', 'Lorenz', 'Rossler'], init='Rossler', size=(93,18), 
                                colour=CONTROLLABEL_BACK_COLOUR, outFunction=self.onChangePreset)
        self.presetName = 'plugin_%d_chaosmod_preset' % self.order                     
        revMenuBox.Add(self.preset, 0, wx.TOP, 2)

        self.sizer.Add(revMenuBox, 0, wx.LEFT, 5)
        self.SetSizer(self.sizer)
