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

import wx, math
import Resources.CeciliaLib as CeciliaLib
from .constants import *
from .Widgets import *

class PlayRecButtons(wx.Panel):
    def __init__(self, parent, cecslider, id=wx.ID_ANY, pos=(0, 0), size=(40, 20)):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.cecslider = cecslider
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.enterWithButtonDown = False
        self.playColour = SLIDER_PLAY_COLOUR_HOT
        self.recColour = SLIDER_REC_COLOUR_HOT
        self.playOver = False
        self.recOver = False
        self.playOverWait = True
        self.recOverWait = True
        self.play = 0
        self.rec = False

        if CeciliaLib.getVar("systemPlatform") == "win32":
            self.dcref = wx.BufferedPaintDC
        else:
            self.dcref = wx.PaintDC

    def cleanup(self):
        self.Unbind(wx.EVT_PAINT, handler=self.OnPaint)
        self.Unbind(wx.EVT_MOTION, handler=self.OnMotion)
        self.Unbind(wx.EVT_LEAVE_WINDOW, handler=self.OnLeave)
        self.Unbind(wx.EVT_ENTER_WINDOW, handler=self.OnEnter)
        self.Unbind(wx.EVT_LEFT_DOWN, handler=self.MouseDown)
        self.Unbind(wx.EVT_LEFT_UP, handler=self.MouseUp)
        self.cecslider = None

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

    def MouseDown(self, evt):
        if not CeciliaLib.getVar("audioServer").isAudioServerRunning():
            pos = evt.GetPosition()
            if wx.Rect(2, 2, 17, 17).Contains(pos):
                self.play = (self.play + 1) % 3
                self.setPlay(self.play)
                self.setOverWait(0)
            elif wx.Rect(21, 2, 38, 17).Contains(pos):
                if self.rec:
                    self.setRec(False)
                else:
                    self.setRec(True)
                self.setOverWait(1)
            self.playOver = False
            self.recOver = False
            wx.CallAfter(self.Refresh)
            evt.Skip()

    def OnEnter(self, evt):
        if evt.LeftIsDown() and not CeciliaLib.getVar("audioServer").isAudioServerRunning():
            self.enterWithButtonDown = True
            pos = evt.GetPosition()
            if wx.Rect(0, 0, 20, 20).Contains(pos):
                self.play = (self.play + 1) % 3
                self.setPlay(self.play)
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
        w, h = self.GetSize()
        dc = self.dcref(self)
        gc = wx.GraphicsContext_Create(dc)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        # Draw triangle
        if self.playOver: playColour = SLIDER_PLAY_COLOUR_OVER
        else: playColour = self.playColour
        gc.SetPen(wx.Pen(playColour, width=1, style=wx.SOLID))
        gc.SetBrush(wx.Brush(playColour, wx.SOLID))
        tri = [(14, h / 2), (9, 4), (9, h - 4), (14, h / 2)]
        gc.DrawLines(tri)

        dc.SetPen(wx.Pen('#333333', width=1, style=wx.SOLID))
        dc.DrawLine(w // 2, 4, w // 2, h - 4)

        # Draw circle
        if self.recOver: recColour = SLIDER_REC_COLOUR_OVER
        else: recColour = self.recColour
        gc.SetPen(wx.Pen(recColour, width=1, style=wx.SOLID))
        gc.SetBrush(wx.Brush(recColour, wx.SOLID))
        gc.DrawEllipse(w / 4 + w / 2 - 4, h / 2 - 4, 8, 8)

        evt.Skip()

    def setPlay(self, x):
        self.play = x
        if self.play == 0:
            self.playColour = SLIDER_PLAY_COLOUR_HOT
        elif self.play == 1:
            if self.rec:
                self.setRec(0)
            self.playColour = SLIDER_PLAY_COLOUR_PRESSED
        else:
            if self.rec:
                self.setRec(0)
            self.playColour = SLIDER_PLAY_COLOUR_NO_BIND
        wx.CallAfter(self.Refresh)

    def getPlay(self):
        return self.play

    def getRec(self):
        return self.rec

    def setRec(self, x):
        if x == 0:
            self.rec = False
            self.recColour = SLIDER_REC_COLOUR_HOT
        else:
            if self.play > 0:
                self.setPlay(0)
            self.rec = True
            self.recColour = SLIDER_REC_COLOUR_PRESSED

class Slider(wx.Panel):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0, 0), size=(200, 20),
                 valtype='float', log=False, function=None, cecslider=None):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, size=size, style=wx.BORDER_NONE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.SetMinSize(self.GetSize())
        self.outFunction = function
        self.cecslider = cecslider
        if valtype.startswith('i'): self.myType = int
        else: self.myType = float
        self.log = log
        self.SetRange(minvalue, maxvalue)
        self.borderWidth = 1
        self.fillcolor = SLIDER_BACK_COLOUR
        self.knobcolor = SLIDER_KNOB_COLOUR
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def cleanup(self):
        self.Unbind(wx.EVT_LEFT_DOWN, handler=self.MouseDown)
        self.Unbind(wx.EVT_LEFT_UP, handler=self.MouseUp)
        self.Unbind(wx.EVT_MOTION, handler=self.MouseMotion)
        self.Unbind(wx.EVT_PAINT, handler=self.OnPaint)
        self.Unbind(wx.EVT_SIZE, handler=self.OnResize)
        self.outFunction = None
        self.cecslider = None

    def createSliderBitmap(self):
        w, h = self.GetSize()
        b = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(b)
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=1))
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR))
        dc.DrawRectangle(0, 0, w, h)
        dc.SetBrush(wx.Brush("#777777"))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        h2 = self.sliderHeight // 4
        dc.DrawRoundedRectangle(0, h2, w, self.sliderHeight, 4)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour("#777777")
        self.sliderMask = b

    def createKnobMaskBitmap(self):
        w, h = self.knobSize, self.GetSize()[1]
        b = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(b)
        rec = wx.Rect(0, 0, int(w), h)
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=1))
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR))
        dc.DrawRectangle(rec)
        h2 = self.sliderHeight // 4
        rec = wx.Rect(0, h2, w, int(self.sliderHeight))
        dc.SetBrush(wx.Brush("#787878"))
        dc.SetPen(wx.Pen(KNOB_BORDER_COLOUR, width=1))
        dc.DrawRoundedRectangle(0, 0, w, h, 3)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour("#787878")
        self.knobMask = b

    def setFillColour(self, col1, col2):
        self.fillcolor = col1
        self.knobcolor = col2
        self.createBackgroundBitmap()
        self.createKnobBitmap()

    def SetRange(self, minvalue, maxvalue):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def scale(self):
        inter = CeciliaLib.tFromValue(self.pos, self.knobHalfSize, self.GetSize()[0] - self.knobHalfSize)
        return CeciliaLib.interpFloat(inter, self.minvalue, self.maxvalue)

    def MouseDown(self, evt):
        size = self.GetSize()
        self.pos = CeciliaLib.clamp(evt.GetPosition()[0], self.knobHalfSize, size[0] - self.knobHalfSize)
        self.value = self.scale()
        self.CaptureMouse()
        wx.CallAfter(self.Refresh)

    def MouseMotion(self, evt):
        size = self.GetSize()
        if evt.Dragging() and evt.LeftIsDown() and self.HasCapture():
            self.pos = CeciliaLib.clamp(evt.GetPosition()[0], self.knobHalfSize, size[0] - self.knobHalfSize)
            self.value = self.scale()
            wx.CallAfter(self.Refresh)

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        if self.cecslider.getUp() and CeciliaLib.getVar("currentModule") is not None:
            getattr(CeciliaLib.getVar("currentModule"), self.cecslider.name + "_up")(self.GetValue())

    def OnResize(self, evt):
        self.createSliderBitmap()
        self.createKnobMaskBitmap()
        self.createKnobBitmap()
        self.createBackgroundBitmap()
        self.clampPos()
        #wx.CallAfter(self.Refresh)
        self.Refresh()

    def clampPos(self):
        size = self.GetSize()
        self.pos = CeciliaLib.tFromValue(self.value, self.minvalue, self.maxvalue) * (size[0] - self.knobSize) + self.knobHalfSize
        self.pos = CeciliaLib.clamp(self.pos, self.knobHalfSize, size[0] - self.knobHalfSize)

class HSlider(Slider):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0, 0), size=(200, 15),
                 valtype='float', log=False, function=None, cecslider=None):
        Slider.__init__(self, parent, minvalue, maxvalue, init, pos, size, valtype, log, function, cecslider)
        self.SetMinSize((50, 15))
        if self.cecslider:
            if self.cecslider.half:
                self.knobSize = 22
                self.knobHalfSize = 11
            else:
                self.knobSize = 28
                self.knobHalfSize = 14
        else:
            self.knobSize = 28
            self.knobHalfSize = 14
        self.sliderHeight = 14
        self.createKnobMaskBitmap()
        self.createSliderBitmap()
        self.createKnobBitmap()
        self.createBackgroundBitmap()
        self.value = 0
        if init is not None: self._setValue(init)
        else: self._setValue(minvalue)
        self.clampPos()
        self.midictl = ''
        self.midiLearn = False
        self.openSndCtrl = ''
        self.font = wx.Font(LABEL_FONT - 2, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT)

        self.mario = 0
        self.useMario = False
        self.marios = [CeciliaLib.getVar("ICON_MARIO1"), CeciliaLib.getVar("ICON_MARIO2"), CeciliaLib.getVar("ICON_MARIO3"),
                       CeciliaLib.getVar("ICON_MARIO4"), CeciliaLib.getVar("ICON_MARIO5"), CeciliaLib.getVar("ICON_MARIO6")]

    def setSliderHeight(self, height):
        self.sliderHeight = height
        self.createSliderBitmap()
        self.createKnobMaskBitmap()
        self.createBackgroundBitmap()
        self.createKnobBitmap()
        wx.CallAfter(self.Refresh)

    def createBackgroundBitmap(self):
        w, h = self.GetSize()
        self.backgroundBitmap = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(self.backgroundBitmap)
        gc = wx.GraphicsContext_Create(dc)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=self.borderWidth, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        # Draw inner part
        h2 = self.sliderHeight // 4
        rec = wx.Rect(0, h2, w-1, int(self.sliderHeight))
        gc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        brush = gc.CreateLinearGradientBrush(0, h2, 0, h2 + self.sliderHeight, GRADIENT_DARK_COLOUR, self.fillcolor)
        gc.SetBrush(brush)
        gc.DrawRoundedRectangle(rec[0], rec[1], rec[2], rec[3], 4)
        dc.SelectObject(wx.NullBitmap)

    def createKnobBitmap(self):
        w, h = self.GetSize()
        self.knobBitmap = wx.EmptyBitmap(self.knobSize, h)
        dc = wx.MemoryDC(self.knobBitmap)
        gc = wx.GraphicsContext_Create(dc)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        rec = wx.Rect(0, 0, int(self.knobSize), h)

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=self.borderWidth, style=wx.SOLID))
        dc.DrawRectangle(rec)

        brush = gc.CreateLinearGradientBrush(0, 0, self.knobSize, 0, GRADIENT_DARK_COLOUR, self.knobcolor)
        gc.SetPen(wx.Pen(KNOB_BORDER_COLOUR, width=1))
        gc.SetBrush(brush)
        gc.DrawRoundedRectangle(rec[0], rec[1], rec[2]-1, rec[3]-1, 2)
        dc.SelectObject(wx.NullBitmap)

    def setMidiCtl(self, str):
        self.midictl = str
        self.midiLearn = False

    def inMidiLearnMode(self):
        self.midiLearn = True
        wx.CallAfter(self.Refresh)

    def setOpenSndCtrl(self, str):
        self.openSndCtrl = str
        wx.CallAfter(self.Refresh)

    def _setValue(self, value):
        self.lastvalue = self.value
        value = CeciliaLib.clamp(value, self.minvalue, self.maxvalue)
        if self.log:
            t = CeciliaLib.toLog(value, self.minvalue, self.maxvalue)
            self.value = CeciliaLib.interpFloat(t, self.minvalue, self.maxvalue)
        else:
            t = CeciliaLib.tFromValue(value, self.minvalue, self.maxvalue)
            self.value = CeciliaLib.interpFloat(t, self.minvalue, self.maxvalue)
        if self.myType == int:
            self.value = int(self.value)
        self.clampPos()

    def SetValue(self, value):
        self._setValue(value)
        wx.CallAfter(self.Refresh)

    def GetValue(self):
        if self.log:
            t = CeciliaLib.tFromValue(self.value, self.minvalue, self.maxvalue)
            val = CeciliaLib.toExp(t, self.minvalue, self.maxvalue)
        else:
            val = self.value
        if self.myType == int:
            return int(val)
        return val

    def OnPaint(self, evt):
        w, h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetFont(self.font)
        dc.SetTextForeground(LABEL_LABEL_COLOUR)
        pos = self.pos - self.knobHalfSize

        dc.DrawBitmap(self.backgroundBitmap, 0, 0)

        # Draw knob
        if not self.useMario:
            dc.DrawBitmap(self.knobBitmap, pos, 0)
        else:
            if self.lastvalue < self.value: marioff = 0
            else: marioff = 3
            bitmario = self.marios[(self.mario % 3) + marioff]
            dc.DrawBitmap(bitmario, self.pos - 8, 0, True)
            self.mario += 1

        if CeciliaLib.getVar("systemPlatform") == "win32":
            dc.SetFont(wx.Font(LABEL_FONT - 1, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        else:
            dc.SetFont(wx.Font(LABEL_FONT - 1, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT))

        if self.midiLearn:
            dc.DrawLabel("Move a MIDI controller...", wx.Rect(5, 0, 50, h), wx.ALIGN_CENTER_VERTICAL)
        elif self.openSndCtrl:
            dc.DrawLabel(self.openSndCtrl, wx.Rect(5, 0, w, h), wx.ALIGN_CENTER_VERTICAL)
        else:
            dc.DrawLabel(self.midictl, wx.Rect(5, 0, w, h), wx.ALIGN_CENTER_VERTICAL)

        # Send value
        if self.outFunction:
            self.outFunction(self.GetValue())

class CECSlider:
    def __init__(self, parent, minvalue, maxvalue, init=None, label='slider', unit='', valtype='float',
                 log=False, name='', gliss=.025, midictl=None, tooltip='', up=False, half=False):
        self.widget_type = "slider"
        self.parent = parent
        self.valtype = valtype
        self.name = name
        self.half = half
        self.gliss = gliss
        self.automationLength = None
        self.automationData = []
        self.path = None
        self.openSndCtrl = None
        self.OSCOut = None
        self.midictl = None
        self.midichan = 1
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.log = log
        self.up = up
        self.convertSliderValue = 200
        self.path = os.path.join(AUTOMATION_SAVE_PATH, self.name)

        pos = (0, 0)
        size = (200, 16)
        self.slider = HSlider(parent, minvalue, maxvalue, init, pos, size, valtype, log, self.writeToEntry, self)
        self.slider.setSliderHeight(11)

        self.setMidiCtl(midictl)

        self.label = Label(parent, label, size=(100, 16), outFunction=self.onLabelClick, dclickFunction=self.onLabelDClick)
        CeciliaLib.setToolTip(self.label, TT_SLIDER_LABEL)
        if self.half:
            unitX = 100
        else:
            unitX = 120
        self.entryUnit = EntryUnit(parent, self.slider.GetValue(), unit, size=(unitX, 16),
                                   valtype=valtype, outFunction=self.entryReturn)
        CeciliaLib.setToolTip(self.entryUnit, TT_SLIDER_DISPLAY)
        self.buttons = PlayRecButtons(parent, self, size=(40, 16))
        CeciliaLib.setToolTip(self.buttons, TT_SLIDER_AUTO)

    def cleanup(self):
        self.entryUnit.cleanup()
        self.slider.cleanup()
        self.label.cleanup()
        self.buttons.cleanup()

    def refresh(self):
        wx.CallAfter(self.slider.Refresh)
        wx.CallAfter(self.label.Refresh)
        wx.CallAfter(self.entryUnit.Refresh)

    def setFillColour(self, col1, col2, col3):
        self.slider.setFillColour(col1, col2)
        self.label.setBackColour(col1)
        self.entryUnit.setBackColour(col1)

    def onLabelClick(self, label, shift=False, alt=False, side='left'):
        if not self.up:
            # alt is now the right click
            if alt and shift:
                self.setMidiCtl(None)
            elif shift:
                CeciliaLib.getVar("grapher").setShowLineSolo(label)
                CeciliaLib.getVar("grapher").toolbar.menu.setLabel(label, True)
            elif alt:
                if CeciliaLib.getVar("useMidi"):
                    CeciliaLib.getVar("grapher").toolbar.menu.setLabel(label, True)
                    CeciliaLib.getVar("audioServer").midiLearn(self)
                    self.slider.inMidiLearnMode()
                else:
                    CeciliaLib.showErrorDialog("Midi not initialized!",
                        "There is no Midi interface connected!")
            else:
                CeciliaLib.getVar("grapher").resetShow()
                CeciliaLib.getVar("grapher").toolbar.menu.setLabel(label, True)

    def onLabelDClick(self, side='left'):
        f = OSCPopupFrame(CeciliaLib.getVar('interface'), self)
        f.CenterOnParent()
        f.Show()

    def setOSCInput(self, value):
        self.setOpenSndCtrl(value)

    def setOSCOutput(self, value):
        self.setOSCOut(value)

    def setConvertSliderValue(self, x, end=None):
        self.convertSliderValue = x

    def setAutomationLength(self, x):
        self.automationLength = x

    def getAutomationLength(self):
        return self.automationLength

    def sendValue(self, value):
        if self.getPlay() in [0, 1] or self.getRec() == 1:
            if CeciliaLib.getVar("currentModule") is not None:
                CeciliaLib.getVar("currentModule")._sliders[self.name].setValue(value)

    def entryReturn(self, value):
        self.slider.SetValue(value)
        self.sendValue(value)

    def writeToEntry(self, value):
        if self.slider.myType == float:
            if value >= 10000:
                self.entryUnit.setValue(float('%5.2f' % value))
            elif value >= 1000:
                self.entryUnit.setValue(float('%5.3f' % value))
            elif value >= 10:
                self.entryUnit.setValue(float('%5.5f' % value))
            elif value >= 0:
                self.entryUnit.setValue(float('%5.5f' % value))
            elif value >= -100:
                self.entryUnit.setValue(float('%5.5f' % value))
            elif value >= -1000:
                self.entryUnit.setValue(float('%5.4f' % value))
            elif value >= -10000:
                self.entryUnit.setValue(float('%5.3f' % value))
            else:
                self.entryUnit.setValue(float('%5.2f' % value))
        else:
            self.entryUnit.setValue(value)
        self.sendValue(value)

    def getUp(self):
        return self.up

    def setValue(self, value):
        self.slider.SetValue(value)

    def getValue(self):
        return self.slider.GetValue()

    def getLog(self):
        return self.log

    def getMinValue(self):
        return self.minvalue

    def getMaxValue(self):
        return self.maxvalue

    def getName(self):
        return self.name

    def setPlay(self, x):
        self.buttons.setPlay(x)

    def setRec(self, x):
        self.buttons.setRec(x)

    def getPlay(self):
        return self.buttons.getPlay()

    def getRec(self):
        return self.buttons.getRec()

    def getState(self):
        return [self.getValue(), self.getPlay(), self.getMidiCtl(), self.getMidiChannel(), self.getOpenSndCtrl(), self.getOSCOut()]

    def setState(self, values):
        self.setValue(values[0])
        self.setPlay(values[1])
        if len(values) >= 4:
            self.setMidiChannel(values[3])
        self.setMidiCtl(values[2])
        if len(values) >= 5:
            self.setOpenSndCtrl(values[4])
        if len(values) >= 6:
            self.setOSCOut(values[5])

    def getPath(self):
        return self.path

    def setMidiCtl(self, ctl):
        if ctl is None:
            self.midictl = None
            self.midichan = 1
            self.slider.setMidiCtl('')
        else:
            self.midictl = int(ctl)
            self.slider.setMidiCtl("%d:%d" % (self.midictl, self.midichan))
            self.openSndCtrl = None
            self.slider.setOpenSndCtrl('')
        wx.CallAfter(self.slider.Refresh)

    def getMidiCtl(self):
        return self.midictl

    def setMidiChannel(self, chan):
        self.midichan = int(chan)

    def getMidiChannel(self):
        return self.midichan

    def getWithMidi(self):
        if self.getMidiCtl() is not None and CeciliaLib.getVar("useMidi"):
            return True
        else:
            return False

    def setOpenSndCtrl(self, value):
        if value is None or value == "":
            self.openSndCtrl = None
            self.slider.setOpenSndCtrl("")
        else:
            if type(value) == tuple:
                msg = "%s:%s" % (value[0], value[1])
            else:
                msg = value
            sep = msg.split(":")
            port = int(sep[0].strip())
            address = str(sep[1].strip())
            self.openSndCtrl = (port, address)
            self.slider.setOpenSndCtrl("%d:%s" % (port, address))
            self.setMidiCtl(None)

    def setOSCOut(self, value):
        if value is None or value == "":
            self.OSCOut = None
        else:
            if type(value) == tuple:
                msg = "%s:%d:%s" % (value[0], value[1], value[2])
            else:
                msg = value
            sep = msg.split(":")
            host = str(sep[0].strip())
            port = int(sep[1].strip())
            address = str(sep[2].strip())
            self.OSCOut = (host, port, address)

    def getOpenSndCtrl(self):
        return self.openSndCtrl

    def getOSCOut(self):
        return self.OSCOut

    def getWithOSC(self):
        if self.openSndCtrl is not None:
            return True
        else:
            return False

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
            torec = math.log10(oldval / minval) / math.log10(maxOnMin)
        else:
            maxMinusMin = maxval - minval
            torec = (oldval - minval) / maxMinusMin
        temp.append([0.0, torec])

        for i, val in enumerate(data):
            length = (i - oldpos) / totallength
            pos = oldpos / totallength + length
            if val == 0:
                val = oldval
            if log:
                torec = math.log10(val / minval) / math.log10(maxOnMin)
            else:
                torec = (val - minval) / maxMinusMin
            temp.append([pos, torec])
            oldval = val
            oldpos = i

        self.automationData = temp

    def getAutomationData(self):
        return [[x[0], x[1]] for x in self.automationData]

    def update(self, val):
        if not self.slider.HasCapture() and self.getPlay() == 1 or self.getWithMidi():
            self.setValue(val)

class RangeSlider(wx.Panel):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0, 0), size=(200, 20),
                 valtype='float', log=False, function=None, cecslider=None):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, size=size, style=wx.BORDER_NONE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.SetMinSize(self.GetSize())
        self.sliderHeight = 14
        self.borderWidth = 1
        self.action = None
        self.fillcolor = SLIDER_BACK_COLOUR
        self.knobcolor = SLIDER_KNOB_COLOUR
        self.handlecolor = wx.Colour(int(self.knobcolor[1:3]) - 10, int(self.knobcolor[3:5]) - 10, int(self.knobcolor[5:7]) - 10)
        self.outFunction = function
        self.cecslider = cecslider
        if valtype.startswith('i'): self.myType = int
        else: self.myType = float
        self.log = log
        self.SetRange(minvalue, maxvalue)
        self.handles = [minvalue, maxvalue]
        if init is not None:
            if type(init) in [list, tuple]:
                if len(init) == 1:
                    self.SetValue([init[0], init[0]])
                else:
                    self.SetValue([init[0], init[1]])
            else:
                self.SetValue([minvalue, maxvalue])
        else:
            self.SetValue([minvalue, maxvalue])
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.MouseRightDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_RIGHT_UP, self.MouseUp)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def cleanup(self):
        self.Unbind(wx.EVT_LEFT_DOWN, handler=self.MouseDown)
        self.Unbind(wx.EVT_RIGHT_DOWN, handler=self.MouseRightDown)
        self.Unbind(wx.EVT_LEFT_UP, handler=self.MouseUp)
        self.Unbind(wx.EVT_RIGHT_UP, handler=self.MouseUp)
        self.Unbind(wx.EVT_MOTION, handler=self.MouseMotion)
        self.Unbind(wx.EVT_PAINT, handler=self.OnPaint)
        self.Unbind(wx.EVT_SIZE, handler=self.OnResize)
        self.outFunction = None
        self.cecslider = None

    def createSliderBitmap(self):
        w, h = self.GetSize()
        b = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(b)
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=1))
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR))
        dc.DrawRectangle(0, 0, w, h)
        dc.SetBrush(wx.Brush("#777777"))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        h2 = self.sliderHeight // 4
        dc.DrawRoundedRectangle(0, h2, w, self.sliderHeight, 4)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour("#777777")
        self.sliderMask = b

    def setFillColour(self, col1, col2):
        self.fillcolor = col1
        self.knobcolor = col2
        self.handlecolor = wx.Colour(self.knobcolor[0] * 0.35, self.knobcolor[1] * 0.35, self.knobcolor[2] * 0.35)
        self.createBackgroundBitmap()

    def SetRange(self, minvalue, maxvalue):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def scale(self, pos):
        tmp = []
        for p in pos:
            inter = CeciliaLib.tFromValue(p, 1, self.GetSize()[0] - 1)
            inter2 = CeciliaLib.interpFloat(inter, self.minvalue, self.maxvalue)
            tmp.append(inter2)
        return tmp

    def MouseRightDown(self, evt):
        xpos = evt.GetPosition()[0]
        if xpos > (self.handlePos[0] - 5) and xpos < (self.handlePos[1] + 5):
            self.lastpos = xpos
            self.length = self.handlePos[1] - self.handlePos[0]
            self.action = 'drag'
            self.handles = self.scale(self.handlePos)
            self.CaptureMouse()
            wx.CallAfter(self.Refresh)

    def MouseDown(self, evt):
        size = self.GetSize()
        xpos = evt.GetPosition()[0]
        self.middle = (self.handlePos[1] - self.handlePos[0]) // 2 + self.handlePos[0]
        midrec = wx.Rect(int(self.middle) - 7, 4, 15, size[1] - 9)
        if midrec.Contains(evt.GetPosition()):
            self.lastpos = xpos
            self.length = self.handlePos[1] - self.handlePos[0]
            self.action = 'drag'
        elif xpos < self.middle:
            self.handlePos[0] = CeciliaLib.clamp(xpos, 1, self.handlePos[1])
            self.action = 'left'
        elif xpos > self.middle:
            self.handlePos[1] = CeciliaLib.clamp(xpos, self.handlePos[0], size[0] - 1)
            self.action = 'right'
        self.handles = self.scale(self.handlePos)
        self.CaptureMouse()
        wx.CallAfter(self.Refresh)

    def MouseMotion(self, evt):
        size = self.GetSize()
        if evt.Dragging() and self.HasCapture() and evt.LeftIsDown() or evt.RightIsDown():
            xpos = evt.GetPosition()[0]
            if self.action == 'drag':
                off = xpos - self.lastpos
                self.lastpos = xpos
                self.handlePos[0] = CeciliaLib.clamp(self.handlePos[0] + off, 1, size[0] - self.length)
                self.handlePos[1] = CeciliaLib.clamp(self.handlePos[1] + off, self.length, size[0] - 1)
            if self.action == 'left':
                self.handlePos[0] = CeciliaLib.clamp(xpos, 1, self.handlePos[1] - 4)
            elif self.action == 'right':
                self.handlePos[1] = CeciliaLib.clamp(xpos, self.handlePos[0] + 4, size[0] - 1)
            self.handles = self.scale(self.handlePos)
            wx.CallAfter(self.Refresh)

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        if self.cecslider.getUp() and CeciliaLib.getVar("currentModule") is not None:
            getattr(CeciliaLib.getVar("currentModule"), self.cecslider.name + "_up")(self.GetValue())

    def OnResize(self, evt):
        self.createSliderBitmap()
        self.createBackgroundBitmap()
        self.clampHandlePos()
        wx.CallAfter(self.Refresh)

    def clampHandlePos(self):
        size = self.GetSize()
        tmp = []
        for handle in [min(self.handles), max(self.handles)]:
            pos = CeciliaLib.tFromValue(handle, self.minvalue, self.maxvalue) * size[0]
            pos = CeciliaLib.clamp(pos, 1, size[0] - 1)
            tmp.append(pos)
        self.handlePos = tmp

class HRangeSlider(RangeSlider):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0, 0), size=(200, 15),
                 valtype='float', log=False, function=None, cecslider=None):
        RangeSlider.__init__(self, parent, minvalue, maxvalue, init, pos, size, valtype, log, function, cecslider)
        self.SetMinSize((50, 15))
        self.createSliderBitmap()
        self.createBackgroundBitmap()
        self.clampHandlePos()
        self.midictl1 = ''
        self.midictl2 = ''
        self.openSndCtrl1 = ''
        self.openSndCtrl2 = ''
        self.midiLearn = False
        self.font = wx.Font(LABEL_FONT - 2, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT)

    def setSliderHeight(self, height):
        self.sliderHeight = height
        self.createSliderBitmap()
        self.createBackgroundBitmap()
        wx.CallAfter(self.Refresh)

    def createBackgroundBitmap(self):
        w, h = self.GetSize()
        self.backgroundBitmap = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(self.backgroundBitmap)
        gc = wx.GraphicsContext_Create(dc)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=self.borderWidth, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        # Draw inner part
        h2 = self.sliderHeight // 4
        rec = wx.Rect(0, h2, w-1, int(self.sliderHeight))
        gc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        brush = gc.CreateLinearGradientBrush(0, h2, 0, h2 + self.sliderHeight, GRADIENT_DARK_COLOUR, self.fillcolor)
        gc.SetBrush(brush)
        gc.DrawRoundedRectangle(rec[0], rec[1], rec[2], rec[3], 4)
        dc.SelectObject(wx.NullBitmap)

    def setMidiCtl(self, str1, str2):
        self.midictl1 = str1
        self.midictl2 = str2
        self.midiLearn = False

    def inMidiLearnMode(self):
        self.midiLearn = True
        wx.CallAfter(self.Refresh)

    def setOpenSndCtrl(self, str, side):
        if side == 'left':
            self.openSndCtrl1 = str
        else:
            self.openSndCtrl2 = str
        self.OnResize(None)

    def SetOneValue(self, value, which):
        value = CeciliaLib.clamp(value, self.minvalue, self.maxvalue)
        if self.log:
            t = CeciliaLib.toLog(value, self.minvalue, self.maxvalue)
            value = CeciliaLib.interpFloat(t, self.minvalue, self.maxvalue)
        else:
            t = CeciliaLib.tFromValue(value, self.minvalue, self.maxvalue)
            value = CeciliaLib.interpFloat(t, self.minvalue, self.maxvalue)
        if self.myType == int:
            value = int(value)
        self.handles[which] = value
        self.OnResize(None)

    def SetValue(self, values):
        tmp = []
        for val in values:
            value = CeciliaLib.clamp(val, self.minvalue, self.maxvalue)
            if self.log:
                t = CeciliaLib.toLog(value, self.minvalue, self.maxvalue)
                value = CeciliaLib.interpFloat(t, self.minvalue, self.maxvalue)
            else:
                t = CeciliaLib.tFromValue(value, self.minvalue, self.maxvalue)
                value = CeciliaLib.interpFloat(t, self.minvalue, self.maxvalue)
            if self.myType == int:
                value = int(value)
            tmp.append(value)
        self.handles = tmp
        self.OnResize(None)

    def GetValue(self):
        tmp = []
        for value in self.handles:
            if self.log:
                t = CeciliaLib.tFromValue(value, self.minvalue, self.maxvalue)
                val = CeciliaLib.toExp(t, self.minvalue, self.maxvalue)
            else:
                val = value
            if self.myType == int:
                val = int(val)
            tmp.append(val)
        tmp = [min(tmp), max(tmp)]
        return tmp

    def OnPaint(self, evt):
        w, h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetFont(self.font)
        dc.SetTextForeground(LABEL_LABEL_COLOUR)

        dc.DrawBitmap(self.backgroundBitmap, 0, 0)

        # Draw handles
        dc.SetPen(wx.Pen(self.handlecolor, width=1, style=wx.SOLID))
        dc.SetBrush(wx.Brush(self.handlecolor))

        if self.handlePos[1] - self.handlePos[0] > 4:
            rec = wx.Rect(int(self.handlePos[0]), 3, int(self.handlePos[1] - self.handlePos[0]), h - 7)
            dc.DrawRoundedRectangle(rec, 4)
            dc.SetPen(wx.Pen(self.fillcolor, width=1, style=wx.SOLID))
            dc.SetBrush(wx.Brush(self.fillcolor))
            mid = (self.handlePos[1] - self.handlePos[0]) // 2 + self.handlePos[0]
            rec = wx.Rect(int(mid) - 4, 4, 8, h - 9)
            dc.DrawRoundedRectangle(rec, 3)
        else:
            mid = (self.handlePos[1] - self.handlePos[0]) // 2 + self.handlePos[0]
            rec = wx.Rect(int(mid) - 4, 4, 8, h - 9)
            dc.DrawRoundedRectangle(rec, 3)

        if self.midiLearn:
            dc.SetFont(wx.Font(LABEL_FONT - 1, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT))
            dc.DrawLabel("Move 2 MIDI controllers...", wx.Rect(5, 0, 50, h), wx.ALIGN_CENTER_VERTICAL)
        elif self.openSndCtrl1 or self.openSndCtrl2:
            if self.openSndCtrl1:
                dc.DrawLabel(self.openSndCtrl1, wx.Rect(5, 0, w, h), wx.ALIGN_CENTER_VERTICAL)
            if self.openSndCtrl2:
                textwidth = dc.GetTextExtent(self.openSndCtrl2)[0] + 5
                dc.DrawLabel(self.openSndCtrl2, wx.Rect(w - textwidth, 0, textwidth, h), wx.ALIGN_CENTER_VERTICAL)
        else:
            textwidth = dc.GetTextExtent(self.midictl2)[0] + 5
            dc.DrawLabel(self.midictl1, wx.Rect(5, 0, 30, h), wx.ALIGN_CENTER_VERTICAL)
            dc.DrawLabel(self.midictl2, wx.Rect(w - textwidth, 0, textwidth, h), wx.ALIGN_CENTER_VERTICAL)

        # Send value
        if self.outFunction:
            self.outFunction(self.GetValue())

class CECRange:
    def __init__(self, parent, minvalue, maxvalue, init=None, label='range', unit='', valtype='float',
                 log=False, name='', gliss=.025, midictl=None, tooltip='', up=False):
        self.widget_type = "range"
        self.parent = parent
        self.valtype = valtype
        self.name = name
        self.gliss = gliss
        self.automationLength = None
        self.automationData = []
        self.path = os.path.join(AUTOMATION_SAVE_PATH, self.name)
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.log = log
        self.up = up
        self.convertSliderValue = {'min': 200, 'max': 200}
        self.midictl = None
        self.midichan = [1, 1]
        self.openSndCtrl = None
        self.OSCOut = None

        pos = (0, 0)
        size = (200, 16)
        self.slider = HRangeSlider(parent, minvalue, maxvalue, init, pos, size, valtype, log, self.writeToEntry, self)
        self.slider.setSliderHeight(11)

        self.setMidiCtl(midictl)

        self.label = Label(parent, label, size=(100, 16), outFunction=self.onLabelClick, dclickFunction=self.onLabelDClick)
        CeciliaLib.setToolTip(self.label, TT_RANGE_LABEL)
        self.entryUnit = RangeEntryUnit(parent, self.slider.GetValue(), unit, size=(120, 16), valtype=valtype, outFunction=self.entryReturn)
        CeciliaLib.setToolTip(self.entryUnit, TT_RANGE_DISPLAY)
        self.buttons = PlayRecButtons(parent, self, size=(40, 16))
        CeciliaLib.setToolTip(self.buttons, TT_SLIDER_AUTO)

    def cleanup(self):
        self.entryUnit.cleanup()
        self.slider.cleanup()
        self.label.cleanup()
        self.buttons.cleanup()

    def refresh(self):
        wx.CallAfter(self.slider.Refresh)
        wx.CallAfter(self.label.Refresh)
        wx.CallAfter(self.entryUnit.Refresh)

    def setFillColour(self, col1, col2, col3):
        self.slider.setFillColour(col3, col2)
        self.label.setBackColour(col1)
        self.entryUnit.setBackColour(col1)

    def onLabelClick(self, label, shift=False, alt=False, side='left'):
        if not self.up:
            # alt is now the right click
            rightclick = alt
            if side == 'left':
                label = label + ' min'
            else:
                label = label + ' max'
            if rightclick and shift:
                self.setMidiCtl(None)
            elif shift:
                CeciliaLib.getVar("grapher").setShowLineSolo(label)
                CeciliaLib.getVar("grapher").toolbar.menu.setLabel(label, True)
            elif rightclick:
                if CeciliaLib.getVar("useMidi"):
                    CeciliaLib.getVar("grapher").toolbar.menu.setLabel(label, True)
                    CeciliaLib.getVar("audioServer").midiLearn(self, True)
                    self.slider.inMidiLearnMode()
                else:
                    CeciliaLib.showErrorDialog("Midi not initialized!",
                        "There is no Midi interface connected!")
            else:
                CeciliaLib.getVar("grapher").resetShow()
                CeciliaLib.getVar("grapher").toolbar.menu.setLabel(label, True)

    def onLabelDClick(self, side='left'):
        f = OSCPopupFrame(CeciliaLib.getVar('interface'), self, side=side)
        f.CenterOnParent()
        f.Show()

    def setOSCInput(self, value, side):
        self.setOpenSndCtrl(value, side)

    def setOSCOutput(self, value, side):
        self.setOSCOut(value, side)

    def setConvertSliderValue(self, x, end='min'):
        self.convertSliderValue[end] = x

    def setAutomationLength(self, x):
        self.automationLength = x

    def getAutomationLength(self):
        return self.automationLength

    def sendValue(self, value):
        if self.getPlay() in [0, 1] or self.getRec() == 1:
            if CeciliaLib.getVar("currentModule") is not None:
                CeciliaLib.getVar("currentModule")._sliders[self.name].setValue(value)

    def entryReturn(self, value):
        self.slider.SetValue(value)
        self.sendValue(value)

    def writeToEntry(self, values):
        tmp = []
        if self.slider.myType == float:
            for value in values:
                if value >= 10000:
                    val = int(value)
                elif value >= 1000:
                    val = int(value)
                elif value >= 100:
                    val = float('%5.1f' % value)
                elif value >= 10:
                    val = float('%5.1f' % value)
                elif value >= -10:
                    val = float('%5.2f' % value)
                elif value >= -100:
                    val = float('%5.1f' % value)
                elif value >= -1000:
                    val = float('%5.1f' % value)
                elif value >= -10000:
                    val = float('%5.1f' % value)
                else:
                    val = float('%5.0f' % value)
                tmp.append(val)
        else:
            tmp = [i for i in values]
        self.entryUnit.setValue(tmp)
        self.sendValue(values)

    def getUp(self):
        return self.up

    def setOneValue(self, value, which):
        self.slider.SetOneValue(value, which)

    def setValue(self, value):
        self.slider.SetValue(value)

    def getValue(self):
        return self.slider.GetValue()

    def getLog(self):
        return self.log

    def getMinValue(self):
        return self.minvalue

    def getMaxValue(self):
        return self.maxvalue

    def getName(self):
        return self.name

    def setPlay(self, x):
        self.buttons.setPlay(x)

    def setRec(self, x):
        self.buttons.setRec(x)

    def getPlay(self):
        return self.buttons.getPlay()

    def getRec(self):
        return self.buttons.getRec()

    def getState(self):
        return [self.getValue(), self.getPlay(), self.getMidiCtl(), self.getMidiChannel(), self.getOpenSndCtrl(), self.getOSCOut()]

    def setState(self, values):
        self.setValue(values[0])
        self.setPlay(values[1])
        if len(values) >= 4:
            self.setMidiChannel(values[3])
        self.setMidiCtl(values[2])
        if len(values) >= 5:
            if values[4] is not None:
                for i, tup in enumerate(values[4]):
                    if tup != ():
                        if i == 0:
                            self.setOpenSndCtrl("%d:%s" % (tup[0], tup[1]), 'left')
                        else:
                            self.setOpenSndCtrl("%d:%s" % (tup[0], tup[1]), 'right')
            else:
                self.setOpenSndCtrl("", 'left')
                self.setOpenSndCtrl("", 'right')
        if len(values) >= 6:
            if values[5] is not None:
                for i, tup in enumerate(values[5]):
                    if tup != ():
                        if i == 0:
                            self.setOSCOut("%s:%d:%s" % (tup[0], tup[1], tup[2]), 'left')
                        else:
                            self.setOSCOut("%s:%d:%s" % (tup[0], tup[1], tup[2]), 'right')
            else:
                self.setOSCOut("", 'left')
                self.setOSCOut("", 'right')

    def getPath(self):
        return self.path

    def setMidiCtl(self, ctls):
        if ctls is None:
            self.midictl = None
            self.midichan = [1, 1]
            self.slider.setMidiCtl('', '')
        else:
            self.midictl = ctls
            self.slider.setMidiCtl("%d:%d" % (self.midictl[0], self.midichan[0]), "%d:%d" % (self.midictl[1], self.midichan[1]))
            self.openSndCtrl = None
            self.slider.setOpenSndCtrl('', "left")
            self.slider.setOpenSndCtrl('', "right")
        wx.CallAfter(self.slider.Refresh)

    def getMidiCtl(self):
        return self.midictl

    def setMidiChannel(self, chan):
        self.midichan = chan

    def getMidiChannel(self):
        return self.midichan

    def getWithMidi(self):
        if self.getMidiCtl() is not None and CeciliaLib.getVar("useMidi"):
            return True
        else:
            return False

    def setOpenSndCtrl(self, value, side='left'):
        if value is None or value == "":
            self.slider.setOpenSndCtrl("", side)
            if self.openSndCtrl is not None:
                if side == 'left':
                    self.openSndCtrl = ((), self.openSndCtrl[1])
                else:
                    self.openSndCtrl = (self.openSndCtrl[0], ())
                if self.openSndCtrl == ((), ()):
                    self.openSndCtrl = None
        else:
            if type(value) == tuple:
                msg = "%s:%s" % (value[0], value[1])
            else:
                msg = value
            sep = msg.split(":")
            port = int(sep[0].strip())
            address = str(sep[1].strip())
            if self.openSndCtrl is None:
                if side == 'left':
                    self.openSndCtrl = ((port, address), ())
                else:
                    self.openSndCtrl = ((), (port, address))
            else:
                if side == 'left':
                    self.openSndCtrl = ((port, address), self.openSndCtrl[1])
                else:
                    self.openSndCtrl = (self.openSndCtrl[0], (port, address))
            self.slider.setOpenSndCtrl("%d:%s" % (port, address), side)
            self.setMidiCtl(None)

    def setOSCOut(self, value, side='left'):
        if value is not None:
            if value == "":
                if self.OSCOut is not None:
                    if side == 'left':
                        self.OSCOut = ((), self.OSCOut[1])
                    else:
                        self.OSCOut = (self.OSCOut[0], ())
                    if self.OSCOut == ((), ()):
                        self.OSCOut = None
            else:
                sep = value.split(":")
                host = str(sep[0].strip())
                port = int(sep[1].strip())
                address = str(sep[2].strip())
                if self.OSCOut is None:
                    if side == 'left':
                        self.OSCOut = ((host, port, address), ())
                    else:
                        self.OSCOut = ((), (host, port, address))
                else:
                    if side == 'left':
                        self.OSCOut = ((host, port, address), self.OSCOut[1])
                    else:
                        self.OSCOut = (self.OSCOut[0], (host, port, address))

    def getOpenSndCtrl(self):
        return self.openSndCtrl

    def getOSCOut(self):
        return self.OSCOut

    def getWithOSC(self):
        if self.openSndCtrl is not None:
            return True
        else:
            return False

    def setAutomationData(self, data, which=0):
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
            torec = math.log10(oldval / minval) / math.log10(maxOnMin)
        else:
            maxMinusMin = maxval - minval
            torec = (oldval - minval) / maxMinusMin
        temp.append([0.0, torec])

        for i, val in enumerate(data):
            length = (i - oldpos) / totallength
            pos = oldpos / totallength + length
            if log:
                torec = math.log10(val / minval) / math.log10(maxOnMin)
            else:
                torec = (val - minval) / maxMinusMin
            temp.append([pos, torec])
            oldval = val
            oldpos = i

        if len(self.automationData) < 2:
            self.automationData.append(temp)
        else:
            self.automationData[which] = temp

    def getAutomationData(self, which=0):
        return [[x[0], x[1]] for x in self.automationData[which]]

    def update(self, val):
        if not self.slider.HasCapture() and self.getPlay() == 1 or self.getWithMidi():
            self.setValue(val)

class SplitterSlider(wx.Panel):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0, 0), size=(200, 20), num_knobs=3,
                 valtype='float', log=False, function=None, cecslider=None):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, size=size, style=wx.BORDER_NONE)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.SetMinSize(self.GetSize())
        self.sliderHeight = 14
        self.knobSize = 11
        self.borderWidth = 1
        self.selectedHandle = None
        self.handleWidth = 10
        self.fillcolor = SLIDER_BACK_COLOUR
        self.knobcolor = SLIDER_KNOB_COLOUR
        self.handlecolor = wx.Colour(int(self.knobcolor[1:3]) - 10, int(self.knobcolor[3:5]) - 10, int(self.knobcolor[5:7]) - 10)
        self.outFunction = function
        self.cecslider = cecslider
        self.num_knobs = num_knobs
        if valtype.startswith('i'): self.myType = int
        else: self.myType = float
        self.log = log
        self.SetRange(minvalue, maxvalue)
        self.handles = [0 for i in range(self.num_knobs)]
        if init is not None:
            if type(init) in [list, tuple]:
                if len(init) != self.num_knobs:
                    vals = [float(i) / self.num_knobs * (self.maxvalue - self.minvalue) + self.minvalue for i in range(self.num_knobs)]
                    self.SetValue(vals)
                else:
                    self.SetValue([v for v in init])
            else:
                vals = [float(i) / self.num_knobs * (self.maxvalue - self.minvalue) + self.minvalue for i in range(self.num_knobs)]
                self.SetValue(vals)
        else:
            vals = [float(i) / self.num_knobs * (self.maxvalue - self.minvalue) + self.minvalue for i in range(self.num_knobs)]
            self.SetValue(vals)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_RIGHT_UP, self.MouseUp)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def cleanup(self):
        self.Unbind(wx.EVT_LEFT_DOWN, handler=self.MouseDown)
        self.Unbind(wx.EVT_LEFT_UP, handler=self.MouseUp)
        self.Unbind(wx.EVT_RIGHT_UP, handler=self.MouseUp)
        self.Unbind(wx.EVT_MOTION, handler=self.MouseMotion)
        self.Unbind(wx.EVT_PAINT, handler=self.OnPaint)
        self.Unbind(wx.EVT_SIZE, handler=self.OnResize)
        self.outFunction = None
        self.cecslider = None

    def createSliderBitmap(self):
        w, h = self.GetSize()
        b = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(b)
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=1))
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR))
        dc.DrawRectangle(0, 0, w, h)
        dc.SetBrush(wx.Brush("#777777"))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        h2 = self.sliderHeight // 4
        dc.DrawRoundedRectangle(0, h2, w, self.sliderHeight, 4)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour("#777777")
        self.sliderMask = b

    def createKnobMaskBitmap(self):
        w, h = self.knobSize, self.GetSize()[1]
        b = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(b)
        rec = wx.Rect(0, 0, int(w), h)
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=1))
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR))
        dc.DrawRectangle(rec)
        h2 = self.sliderHeight // 4
        rec = wx.Rect(0, h2, w, int(self.sliderHeight))
        dc.GradientFillLinear(rec, GRADIENT_DARK_COLOUR, self.fillcolor, wx.BOTTOM)
        dc.SetBrush(wx.Brush("#787878"))
        dc.SetPen(wx.Pen(KNOB_BORDER_COLOUR, width=1))
        dc.DrawRoundedRectangle(0, 0, w, h, 2)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour("#787878")
        self.knobMask = b

    def setFillColour(self, col1, col2):
        self.fillcolor = col1
        self.knobcolor = col2
        self.handlecolor = wx.Colour(self.knobcolor[0] * 0.25, self.knobcolor[1] * 0.25, self.knobcolor[2] * 0.25)
        self.createSliderBitmap()

    def SetRange(self, minvalue, maxvalue):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def scale(self, pos):
        tmp = []
        for p in pos:
            inter = CeciliaLib.tFromValue(p, 1, self.GetSize()[0] - 1)
            inter2 = CeciliaLib.interpFloat(inter, self.minvalue, self.maxvalue)
            tmp.append(inter2)
        return tmp

    def setHandlePosition(self, xpos):
        size = self.GetSize()
        halfSize = self.handleWidth // 2 + 1
        if self.selectedHandle == 0:
            self.handlePos[self.selectedHandle] = CeciliaLib.clamp(xpos, halfSize, self.handlePos[self.selectedHandle + 1] - self.handleWidth)
        elif self.selectedHandle == (self.num_knobs - 1):
            self.handlePos[self.selectedHandle] = CeciliaLib.clamp(xpos, self.handlePos[self.selectedHandle - 1] + self.handleWidth, size[0] - halfSize)
        else:
            self.handlePos[self.selectedHandle] = CeciliaLib.clamp(xpos, self.handlePos[self.selectedHandle - 1] + self.handleWidth, self.handlePos[self.selectedHandle + 1] - self.handleWidth)
        self.handles = self.scale(self.handlePos)

    def MouseDown(self, evt):
        w, h = self.GetSize()
        pos = evt.GetPosition()
        xpos = pos[0]
        self.selectedHandle = None
        for i, handle in enumerate(self.handlePos):
            rec = wx.Rect(int(handle) - 5, 3, 10, h - 7)
            if rec.Contains(pos):
                self.selectedHandle = i
                break
        if self.selectedHandle is None:
            return
        self.setHandlePosition(xpos)
        self.CaptureMouse()
        wx.CallAfter(self.Refresh)

    def MouseMotion(self, evt):
        if evt.Dragging() and self.HasCapture() and evt.LeftIsDown():
            self.setHandlePosition(evt.GetPosition()[0])
            wx.CallAfter(self.Refresh)

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        if self.cecslider.getUp() and CeciliaLib.getVar("currentModule") is not None:
            getattr(CeciliaLib.getVar("currentModule"), self.cecslider.name + "_up")(self.GetValue())

    def OnResize(self, evt):
        self.createSliderBitmap()
        self.createBackgroundBitmap()
        self.clampHandlePos()
        wx.CallAfter(self.Refresh)

    def clampHandlePos(self):
        size = self.GetSize()
        tmp = []
        for handle in self.handles:
            pos = CeciliaLib.tFromValue(handle, self.minvalue, self.maxvalue) * (size[0])
            pos = CeciliaLib.clamp(pos, 1, size[0] - 1)
            tmp.append(pos)
        self.handlePos = tmp

class HSplitterSlider(SplitterSlider):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0, 0), size=(200, 15), num_knobs=3,
                 valtype='float', log=False, function=None, cecslider=None):
        SplitterSlider.__init__(self, parent, minvalue, maxvalue, init, pos, size, num_knobs, valtype, log, function, cecslider)
        self.SetMinSize((50, 15))
        self.createSliderBitmap()
        self.createBackgroundBitmap()
        self.createKnobMaskBitmap()
        self.createKnobBitmap()
        self.clampHandlePos()
        self.midictl1 = ''
        self.midictl2 = ''
        self.midiLearn = False
        self.font = wx.Font(SPLITTER_FONT, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT)

    def setSliderHeight(self, height):
        self.sliderHeight = height
        self.createSliderBitmap()
        self.createBackgroundBitmap()
        wx.CallAfter(self.Refresh)

    def createBackgroundBitmap(self):
        w, h = self.GetSize()
        self.backgroundBitmap = wx.EmptyBitmap(w, h)
        dc = wx.MemoryDC(self.backgroundBitmap)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=self.borderWidth, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        # Draw inner part
        h2 = self.sliderHeight // 4
        rec = wx.Rect(0, h2, w, int(self.sliderHeight))
        dc.GradientFillLinear(rec, GRADIENT_DARK_COLOUR, self.fillcolor, wx.BOTTOM)
        dc.DrawBitmap(self.sliderMask, 0, 0, True)
        dc.SelectObject(wx.NullBitmap)

    def createKnobBitmap(self):
        w, h = self.GetSize()
        self.knobBitmap = wx.EmptyBitmap(self.knobSize, h)
        dc = wx.MemoryDC(self.knobBitmap)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        rec = wx.Rect(0, 0, int(self.knobSize), h)
        dc.GradientFillLinear(rec, GRADIENT_DARK_COLOUR, self.handlecolor, wx.RIGHT)
        dc.DrawBitmap(self.knobMask, rec[0], rec[1], True)
        dc.SelectObject(wx.NullBitmap)

    def setMidiCtl(self, str1, str2):
        self.midictl1 = str1
        self.midictl2 = str2
        self.midiLearn = False

    def inMidiLearnMode(self):
        self.midiLearn = True
        wx.CallAfter(self.Refresh)

    def SetValue(self, values):
        tmp = []
        for val in values:
            value = CeciliaLib.clamp(val, self.minvalue, self.maxvalue)
            if self.log:
                t = CeciliaLib.toLog(value, self.minvalue, self.maxvalue)
                value = CeciliaLib.interpFloat(t, self.minvalue, self.maxvalue)
            else:
                t = CeciliaLib.tFromValue(value, self.minvalue, self.maxvalue)
                value = CeciliaLib.interpFloat(t, self.minvalue, self.maxvalue)
            if self.myType == int:
                value = int(value)
            tmp.append(value)
        self.handles = tmp
        self.OnResize(None)

    def GetValue(self):
        tmp = []
        for value in self.handles:
            if self.log:
                t = CeciliaLib.tFromValue(value, self.minvalue, self.maxvalue)
                val = CeciliaLib.toExp(t, self.minvalue, self.maxvalue)
            else:
                val = value
            if self.myType == int:
                val = int(val)
            tmp.append(val)
        return tmp

    def OnPaint(self, evt):
        w, h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetFont(self.font)
        dc.SetTextForeground(LABEL_LABEL_COLOUR)

        dc.DrawBitmap(self.backgroundBitmap, 0, 0)

        # Draw handles
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1, style=wx.SOLID))
        dc.SetBrush(wx.Brush(self.handlecolor))
        for i, handle in enumerate(self.handlePos):
            dc.DrawBitmap(self.knobBitmap, handle - 5, 0)
            rec = wx.Rect(int(handle) - 4, 1, 10, h - 2)
            dc.DrawLabel(str(i + 1), rec, wx.ALIGN_CENTER)

        if not self.midiLearn:
            dc.DrawLabel(self.midictl1, wx.Rect(10, 0, 30, h), wx.ALIGN_CENTER_VERTICAL)
            dc.DrawLabel(self.midictl2, wx.Rect(w - 20, 0, 20, h), wx.ALIGN_CENTER_VERTICAL)
        else:
            dc.SetFont(wx.Font(LABEL_FONT - 1, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_LIGHT))
            dc.DrawLabel("Move 2 MIDI controllers...", wx.Rect(5, 0, 50, h), wx.ALIGN_CENTER_VERTICAL)

        # Send value
        if self.outFunction:
            self.outFunction(self.GetValue())

class CECSplitter:
    def __init__(self, parent, minvalue, maxvalue, init=None, label='splitter', unit='', valtype='float', num_knobs=3,
                 log=False, name='', gliss=.025, midictl=None, tooltip='', up=False):
        self.widget_type = "splitter"
        self.parent = parent
        self.valtype = valtype
        self.num_knobs = num_knobs
        self.name = name
        self.gliss = gliss
        self.automationLength = None
        self.automationData = []
        self.path = os.path.join(AUTOMATION_SAVE_PATH, self.name)
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.log = log
        self.up = up
        self.midictl = None
        self.midichan = [1 for i in range(num_knobs)]

        pos = (0, 0)
        size = (200, 16)
        self.slider = HSplitterSlider(parent, minvalue, maxvalue, init, pos, size,
                                      num_knobs, valtype, log, self.writeToEntry, self)
        self.slider.setSliderHeight(11)

        self.setMidiCtl(midictl)

        self.label = Label(parent, label, size=(100, 16))
        CeciliaLib.setToolTip(self.label, TT_SPLITTER_LABEL)
        self.entryUnit = SplitterEntryUnit(parent, self.slider.GetValue(), unit,
                                           size=(120, 16), num=num_knobs, 
                                           valtype=valtype, outFunction=self.entryReturn)
        CeciliaLib.setToolTip(self.entryUnit, TT_SPLITTER_DISPLAY)
        # Buttons are always hidden for csplitter.
        self.buttons = PlayRecButtons(parent, self, size=(40, 16))

    def cleanup(self):
        self.entryUnit.cleanup()
        self.slider.cleanup()
        self.label.cleanup()
        self.buttons.cleanup()

    def refresh(self):
        wx.CallAfter(self.slider.Refresh)
        wx.CallAfter(self.label.Refresh)
        wx.CallAfter(self.entryUnit.Refresh)

    def setFillColour(self, col1, col2, col3):
        self.slider.setFillColour(col3, col2)
        self.label.setBackColour(col1)
        self.entryUnit.setBackColour(col1)

    def setAutomationLength(self, x):
        self.automationLength = x

    def getAutomationLength(self):
        return self.automationLength

    def sendValue(self, value):
        if self.getPlay() in [0, 1] or self.getRec() == 1:
            if CeciliaLib.getVar("currentModule") is not None:
                CeciliaLib.getVar("currentModule")._sliders[self.name].setValue(value)

    def entryReturn(self, value):
        self.slider.SetValue(value)
        self.sendValue(value)

    def writeToEntry(self, values):
        tmp = []
        if self.slider.myType == float:
            for value in values:
                if value >= 10000:
                    val = float('%5.0f' % value)
                elif value >= 1000:
                    val = float('%5.1f' % value)
                elif value >= 100:
                    val = float('%5.2f' % value)
                elif value >= 10:
                    val = float('%5.3f' % value)
                elif value >= -100:
                    val = float('%5.3f' % value)
                elif value >= -1000:
                    val = float('%5.2f' % value)
                elif value >= -10000:
                    val = float('%5.1f' % value)
                else:
                    val = float('%5.2f' % value)
                tmp.append(val)
        else:
            tmp = [i for i in values]
        self.entryUnit.setValue(tmp)
        self.sendValue(values)

    def getUp(self):
        return self.up

    def setValue(self, value):
        self.slider.SetValue(value)

    def getValue(self):
        return self.slider.GetValue()

    def getLog(self):
        return self.log

    def getMinValue(self):
        return self.minvalue

    def getMaxValue(self):
        return self.maxvalue

    def getName(self):
        return self.name

    def setPlay(self, x):
        self.buttons.setPlay(x)

    def setRec(self, x):
        self.buttons.setRec(x)

    def getPlay(self):
        return self.buttons.getPlay()

    def getRec(self):
        return self.buttons.getRec()

    def getState(self):
        return [self.getValue(), self.getPlay(), self.getMidiCtl(), self.getMidiChannel()]

    def setState(self, values):
        self.setValue(values[0])
        self.setPlay(values[1])
        self.setMidiCtl(values[2])
        if len(values) >= 4:
            self.setMidiChannel(values[3])

    def getPath(self):
        return self.path

    def setMidiCtl(self, ctls):
        if ctls is None:
            self.midictl = None
            self.midichan = [1, 1]
            self.slider.setMidiCtl('', '')
        else:
            self.midictl = ctls
            self.slider.setMidiCtl(str(self.midictl[0]), str(self.midictl[1]))
        self.slider.Refresh()

    def getMidiCtl(self):
        return self.midictl

    def setMidiChannel(self, chan):
        self.midichan = chan

    def getMidiChannel(self):
        return self.midichan

    def getWithMidi(self):
        if self.getMidiCtl() is not None and CeciliaLib.getVar("useMidi"):
            return True
        else:
            return False

    def setAutomationData(self, data, which=0):
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
            torec = math.log10(oldval / minval) / math.log10(maxOnMin)
        else:
            maxMinusMin = maxval - minval
            torec = (oldval - minval) / maxMinusMin
        temp.append([0.0, torec])

        for i, val in enumerate(data):
            length = (i - oldpos) / totallength
            pos = oldpos / totallength + length
            if log:
                torec = math.log10(val / minval) / math.log10(maxOnMin)
            else:
                torec = (val - minval) / maxMinusMin
            temp.append([pos, torec])
            oldval = val
            oldpos = i

        if len(self.automationData) < 2:
            self.automationData.append(temp)
        else:
            self.automationData[which] = temp

    def getAutomationData(self, which=0):
        return [[x[0], x[1]] for x in self.automationData[which]]

    def update(self, val):
        if not self.slider.HasCapture() and self.getPlay() == 1 or self.getWithMidi():
            self.setValue(val)

def buildHorizontalSlidersBox(parent, list):
    mainBox = wx.BoxSizer(wx.VERTICAL)
    outBox = wx.BoxSizer(wx.VERTICAL)
    sliders = []
    halfcount = 0
    for widget in list:
        if widget['type'] in ['cslider', 'crange', 'csplitter']:
            name = widget['name']
            label = widget['label']
            tooltip = widget['help']
            mini = widget['min']
            maxi = widget['max']
            unit = widget['unit']
            init = widget['init']
            up = widget['up']
            midictl = widget['midictl']
            half = widget['half']
            if midictl is not None and midictl <= -1:
                midictl = None
            valtype = widget['res']
            if valtype not in ['int', 'float']:
                CeciliaLib.showErrorDialog('Error when building interface!', "'res' argument choices are 'int' or 'float'. Reset to 'float'.")
                valtype = 'float'
            gliss = widget['gliss']
            if gliss < 0.0 or up:
                gliss = 0.0
            linlog = widget['rel']
            if linlog not in ['lin', 'log']:
                CeciliaLib.showErrorDialog('Error when building interface!', "'rel' argument choices are 'lin' or 'log'. Reset to 'lin'.")
                linlog = 'lin'
            log = {'lin': False, 'log': True}[linlog]
            if log and mini == 0 or log and maxi == 0:
                CeciliaLib.showErrorDialog('Error when building interface!', "'min' or 'max' arguments can't be 0 for a logarithmic slider. Reset to 'lin'.")
                log = False
            if widget['type'] == 'cslider':
                sl = CECSlider(parent, mini, maxi, init, label, unit, valtype, log, name, gliss, midictl, tooltip, up, half)
            elif widget['type'] == 'crange':
                sl = CECRange(parent, mini, maxi, init, label, unit, valtype, log, name, gliss, midictl, tooltip, up)
            else:
                num_knobs = widget['num_knobs']
                sl = CECSplitter(parent, mini, maxi, init, label, unit, valtype, num_knobs, log, name, gliss, midictl, tooltip, up)
            if up or widget['type'] == "csplitter":
                sl.buttons.Hide()
            if not half:
                box = wx.FlexGridSizer(1, 4, 2, 5)
                box.AddGrowableCol(2)
                box.AddMany([(sl.label, 0, wx.LEFT, 5), (sl.buttons, 0, wx.LEFT, 0),
                             (sl.slider, 0, wx.EXPAND), (sl.entryUnit, 0, wx.LEFT | wx.RIGHT, 5)])
                mainBox.Add(box, 1, wx.EXPAND | wx.TOP | wx.BOTTOM, 2)
            else:
                if halfcount % 2 == 0:
                    lowerBox = wx.BoxSizer(wx.HORIZONTAL)
                    leftbox, rightbox = wx.FlexGridSizer(1, 4, 2, 5), wx.FlexGridSizer(1, 4, 2, 5)
                    leftbox.AddGrowableCol(2)
                    rightbox.AddGrowableCol(2)
                    leftbox.AddMany([(sl.label, 0, wx.LEFT, 5), (sl.buttons, 0, wx.LEFT, 0),
                                 (sl.slider, 0, wx.EXPAND), (sl.entryUnit, 0, wx.LEFT | wx.RIGHT, 5)])
                    lowerBox.Add(leftbox, 1, wx.TOP | wx.BOTTOM, 0)
                    mainBox.Add(lowerBox, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 2)
                else:
                    rightbox.AddMany([(sl.label, 0, wx.LEFT, 5), (sl.buttons, 0, wx.LEFT, 0),
                                 (sl.slider, 0, wx.EXPAND), (sl.entryUnit, 0, wx.LEFT | wx.RIGHT, 5)])
                    lowerBox.Add(rightbox, 1, wx.TOP | wx.BOTTOM, 0)
                halfcount += 1
            sliders.append(sl)

    outBox.Add(mainBox, 0, wx.ALL | wx.EXPAND, 3)
    return outBox, sliders