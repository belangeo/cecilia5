# -*- coding: utf-8 -*-
"""
Copyright 2009 iACT, universite de Montreal, Jean Piche, Olivier Belanger, Dominic Thibault

This file is part of Cecilia 4.

Cecilia 4 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Cecilia 4 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cecilia 4.  If not, see <http://www.gnu.org/licenses/>.
"""

import wx, math, random
from Widgets import Label, CustomMenu, Toggle, Button, CECTooltip, ControlSlider, ListEntry
from constants import *
import CeciliaLib

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

    labelColour = colour(name)
    objectColour = colour(name)

    return [labelColour, objectColour]

class CECPopup:
    def __init__(self, parent, label, values, init, name, colour, tooltip, output=True):
        self.name = name
        self.output = output
        self.label = Label(parent, label, colour=colour[0])
        self.popup = CustomMenu(parent, values, init, size=(100,20), outFunction=self.onPopup, colour=colour[1])
        if tooltip != '':
            self.popup.SetToolTip(CECTooltip(tooltip))
        
    def getName(self):
        return self.name

    def getValue(self):
        return self.popup.getIndex()
    
    def getFullValue(self):
        return self.popup.getIndex(), self.popup.getLabel()
        
    def setValue(self, value, out=False):
        self.popup.setByIndex(value, out)

    def onPopup(self, value, label):
        if CeciliaLib.getVar("currentModule") != None and self.output:
            getattr(CeciliaLib.getVar("currentModule"), self.name)(value, label)

class CECToggle:
    def __init__(self, parent, label, init, name, colour, tooltip, output=True):
        self.name = name
        self.output = output
        self.label = Label(parent, label, colour=colour[0])
        self.toggle = Toggle(parent, init, outFunction=self.onToggle, colour=colour[1])
        if tooltip != '':
            self.toggle.SetToolTip(CECTooltip(tooltip))

    def getName(self):
        return self.name

    def getValue(self):
        return self.toggle.getValue()
    
    def setValue(self, state, dump=None):
        self.toggle.setValue(state)

    def onToggle(self, value):
        if CeciliaLib.getVar("currentModule") != None and self.output:
            getattr(CeciliaLib.getVar("currentModule"), self.name)(value)

class CECButton:
    def __init__(self, parent, label, name, colour, tooltip):
        self.name = name
        self.label = Label(parent, label, colour=colour[0])
        self.button = Button(parent, outFunction=self.onButton, colour=(colour[1],colour[0]))
        if tooltip != '':
            self.button.SetToolTip(CECTooltip(tooltip))

    def getValue(self):
        return 0
        
    def getName(self):
        return self.name

    def onButton(self, value):
        if CeciliaLib.getVar("currentModule") != None:
            getattr(CeciliaLib.getVar("currentModule"), self.name)(value)
        

class CECGen:
    def __init__(self, parent, label, init, name, colour, tooltip):
        self.name = name
        self.oldLength = -1
        self.label = Label(parent, label, colour=colour[0])
        self.entry = ListEntry(parent, ", ".join([str(x) for x in init]), colour=colour[1], outFunction=self.onEntry)
        if tooltip != '':
            self.label.SetToolTip(CECTooltip(tooltip))
        
    def getName(self):
        return self.name

    def convertToList(self, value):
        value = value.split(',')
        value = [float(val) for val in value if val != ""]
        return value
        
    def getValue(self):
        return self.convertToList(self.entry.getValue())

    def setValue(self, value, dump=None):
        self.entry.setValue(value)
    
    def onEntry(self, value):
        value = self.convertToList(value)
        if CeciliaLib.getVar("currentModule") != None:
            getattr(CeciliaLib.getVar("currentModule"), self.name)(value)
        
class PolySlider(ControlSlider):
    def __init__(self, parent, name, label, mouseUpFunction, colour):
        ControlSlider.__init__(self, parent, 0.0001, 0.5, .001, log=True, size=(100, 15))
        self.name = name + 'spread'
        self.label = Label(parent, label, colour=colour[0])
        self.mouseUpFunction = mouseUpFunction

    def getValue(self):
        return self.GetValue()

    def setValue(self, state, dump=None):
        self.SetValue(state)
        
    def getName(self):
        return self.name

    def MouseUp(self, evt):
        if self.HasCapture():
            self.mouseUpFunction(self.GetValue())
            self.ReleaseMouse()

class CECPoly:
    def __init__(self, parent, label, name, values, init, colour, tooltip):
        self.name = name
        self.up = 1
        popupLabel = '# of ' + label
        self.popup = CECPopup(parent, popupLabel, values, init, self.name + 'num', colour, tooltip, output=False)
        self.popup.label.SetToolTip(CECTooltip(TT_POLY_LABEL))
        sliderLabel = label.capitalize() + ' spread'
        self.slider = PolySlider(parent, self.name, sliderLabel, self.onSlider, colour)
        self.slider.label.SetToolTip(CECTooltip(TT_POLY_SPREAD))
        self.slider.setSliderHeight(10)
        self.slider.setFloatPrecision(4)
        self.slider.setbackColour(colour[1])
        if tooltip != '':
            self.popup.popup.SetToolTip(CECTooltip(tooltip))

    def getValue(self):
        return self.popup.getValue()

    def getUp(self):
        return self.up
   
    def onSlider(self, value):
        pass
        
class SamplerPopup:
    def __init__(self, parent, values, init, name, outFunction=None):
        self.name = name+'loopi'
        self.outFunction = outFunction
        self.value = values.index(init)
        self.popup = CustomMenu(parent, values, init, size=(100,20), outFunction=self.onPopup)

    def onPopup(self, ind, label):
        self.value = ind
        if self.outFunction != None:
            self.outFunction(self.value)

    def getName(self):
        return self.name

    def getValue(self):
        return self.value        

class SamplerToggle:
    def __init__(self, parent, init, name):
        self.name = name+'startpoint'
        self.value = init
        self.toggle = Toggle(parent, init, outFunction=self.onToggle)

    def onToggle(self,val):
        self.value = val

    def getName(self):
        return self.name

    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
        self.toggle.setValue(self.value)

def buildTogglePopupBox(parent, list):
    mainBox = wx.BoxSizer(wx.VERTICAL)
    box = wx.FlexGridSizer(10,2,2,10)
    objects = []

    widgetlist = [widget for widget in list if widget['type'] in ['cpopup', 'ctoggle', 'cbutton']]
    widgetpoly = [widget for widget in list if widget['type'] == 'cpoly']
    widgetCecList = [widget for widget in list if widget['type'] == 'cgen']
    
    for i, widget in enumerate(widgetlist):
        if widget['type'] == 'cpopup':
            tooltip = widget.get('help', '')
            name = widget['name']
            if name.startswith('-'):
                CeciliaLib.showErrorDialog('Error when building interface!', "Missing name. First argument of cpopup can't be %s." % widget['name'])
            label = widget.get('label', '')
            if label == '':
                CeciliaLib.showErrorDialog('Error when building interface!', "cpopup %s has no -label option." % name)
            values = widget.get('value')
            init = widget.get('init', values[0])
            col = widget.get('col', '')
            if col == '':
                col = random.choice(COLOUR_CLASSES.keys())
            elif col not in COLOUR_CLASSES.keys():
                CeciliaLib.showErrorDialog('Wrong colour!', '"%s"\n\nAvailable colours for -col flag are:\n\n%s.' % (col, ', '.join(COLOUR_CLASSES.keys())))
                col = random.choice(COLOUR_CLASSES.keys())
            colour = chooseColourFromName(col) 
            cpopup = CECPopup(parent, label, values, init, name, colour, tooltip)

            box.AddMany([(cpopup.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (cpopup.popup, 0, wx.TOP | wx.ALIGN_LEFT, 2)]) 
            objects.append(cpopup)
        if widget['type'] == 'ctoggle':
            tooltip = widget.get('help', '')
            name = widget['name']
            if name.startswith('-'):
                CeciliaLib.showErrorDialog('Error when building interface!', "Missing name. First argument of ctoggle can't be %s." % widget['name'])
            label = widget.get('label', '')
            if label == '':
                CeciliaLib.showErrorDialog('Error when building interface!', "ctoggle %s has no -label option." % name)
            init = widget.get('init', 0)
            col = widget.get('col', '')
            if col == '':
                col = random.choice(COLOUR_CLASSES.keys())
            elif col not in COLOUR_CLASSES.keys():
                CeciliaLib.showErrorDialog('Wrong colour!', '"%s"\n\nAvailable colours for -col flag are:\n\n%s.' % (col, ', '.join(COLOUR_CLASSES.keys())))
                col = random.choice(COLOUR_CLASSES.keys())
            colour = chooseColourFromName(col) 
            ctoggle = CECToggle(parent, label, init, name, colour, tooltip)

            box.AddMany([(ctoggle.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (ctoggle.toggle, 0, wx.TOP | wx.ALIGN_LEFT, 2)]) 
            objects.append(ctoggle)
        if widget['type'] == 'cbutton':
            tooltip = widget.get('help', '')
            name = widget['name']
            if name.startswith('-'):
                CeciliaLib.showErrorDialog('Error when building interface!', "Missing name. First argument of cbutton can't be %s." % widget['name'])
            label = widget.get('label', '')
            col = widget.get('col', '')
            if col == '':
                col = random.choice(COLOUR_CLASSES.keys())
            elif col not in COLOUR_CLASSES.keys():
                CeciliaLib.showErrorDialog('Wrong colour!', '"%s"\n\nAvailable colours for -col flag are:\n\n%s.' % (col, ', '.join(COLOUR_CLASSES.keys())))
                col = random.choice(COLOUR_CLASSES.keys())
            colour = chooseColourFromName(col) 
            if label == '':
                CeciliaLib.showErrorDialog('Error when building interface!', "cbutton %s has no -label option." % name)
            cbutton = CECButton(parent, label, name, colour, tooltip)

            box.AddMany([(cbutton.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (cbutton.button, 0, wx.TOP | wx.ALIGN_LEFT, 2)]) 
            objects.append(cbutton)
    for i, widget in enumerate(widgetpoly):
        tooltip = widget.get('help', '')
        name = widget['name']
        if name.startswith('-'):
            CeciliaLib.showErrorDialog('Error when building interface!', "Missing name. First argument of cpoly can't be %s." % widget['name'])
        minvoices = widget.get('min', 1)
        maxvoices = widget.get('max', 10)
        values = [str(voice) for voice in range(minvoices, maxvoices+1)]
        init = widget.get('init', values[0])
        label = widget.get('label', '')
        if label == '':
            CeciliaLib.showErrorDialog('Error when building interface!', "cpoly %s has no -label option." % name)
        colour = [CPOLY_COLOUR, CPOLY_COLOUR]
        cpoly = CECPoly(parent, label, name, values, init, colour, tooltip)
        box.AddMany([(cpoly.popup.label, 0, wx.ALIGN_RIGHT), (cpoly.popup.popup, 0, wx.ALIGN_LEFT),
                    (cpoly.slider.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (cpoly.slider, 0, wx.ALIGN_LEFT | wx.TOP, 6)]) 
        objects.append(cpoly.popup)
        objects.append(cpoly.slider)
    for i, widget in enumerate(widgetCecList):
        tooltip = widget.get('help', '')
        name = widget['name']
        if name.startswith('-'):
            CeciliaLib.showErrorDialog('Error when building interface!', "Missing name. First argument of cpoly can't be %s." % widget['name'])
        init = widget.get('init', '1')
        label = widget.get('label', '')
        if label == '':
            CeciliaLib.showErrorDialog('Error when building interface!', "cpoly %s has no -label option." % name)
        gen = widget.get('gen', -2)
        size = widget.get('size', 8192)
        if gen == -2:
            size = None    
        col = widget.get('col', '')
        if col == '':
            col = random.choice(COLOUR_CLASSES.keys())
        elif col not in COLOUR_CLASSES.keys():
            CeciliaLib.showErrorDialog('Wrong colour!', '"%s"\n\nAvailable colours for -col flag are:\n\n%s.' % (col, ', '.join(COLOUR_CLASSES.keys())))
            col = random.choice(COLOUR_CLASSES.keys())
        colour = chooseColourFromName(col) 
        clist = CECGen(parent, label, init, name, colour, tooltip)
        box.AddMany([(clist.label, 0, wx.ALIGN_RIGHT), (clist.entry, 0, wx.ALIGN_LEFT)]) 
        objects.append(clist)
    mainBox.Add(box, 0, wx.ALL, 8)
    return mainBox, objects
