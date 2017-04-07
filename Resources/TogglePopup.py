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
from __future__ import division
import wx, random
from .Widgets import Label, CustomMenu, Toggle, Button, ListEntry
from .constants import *
import Resources.CeciliaLib as CeciliaLib

class CECPopup:
    def __init__(self, parent, label, values, init, rate, name, colour, tooltip=True, output=True):
        self.type = "popup"
        self.name = name
        self.output = output
        self.rate = rate
        self.label = Label(parent, label, colour=colour[0])
        self.popup = CustomMenu(parent, values, init, size=(100, 20), outFunction=self.onPopup, colour=colour[1])
        if tooltip:
            CeciliaLib.setToolTip(self.label, TT_POPUP)

    def getName(self):
        return self.name

    def getValue(self):
        return self.popup.getIndex()

    def getFullValue(self):
        return self.popup.getIndex(), self.popup.getLabel()

    def getLabel(self):
        return self.popup.getLabel()

    def setValue(self, value, out=False):
        self.popup.setByIndex(value, out)

    def onPopup(self, value, label):
        if CeciliaLib.getVar("currentModule") is not None and self.output and self.rate == "k":
            getattr(CeciliaLib.getVar("currentModule"), self.name)(value, label)

class CECToggle:
    def __init__(self, parent, label, init, rate, name, colour, tooltip, stack=False, output=True):
        self.type = "toggle"
        self.name = name
        self.rate = rate
        self.output = output
        if label != '':
            if stack:
                self.label = Label(parent, label, colour=colour[0], size=(210, 20))
            else:
                self.label = Label(parent, label, colour=colour[0], size=(100, 20))
            CeciliaLib.setToolTip(self.label, TT_TOGGLE)
        self.toggle = Toggle(parent, init, outFunction=self.onToggle, colour=colour[1])
        CeciliaLib.setToolTip(self.label, TT_TOGGLE)

    def getName(self):
        return self.name

    def getValue(self):
        return self.toggle.getValue()

    def setValue(self, state, dump=None):
        self.toggle.setValue(state)

    def onToggle(self, value):
        if CeciliaLib.getVar("currentModule") is not None and self.output:
            getattr(CeciliaLib.getVar("currentModule"), self.name)(value)

class CECButton:
    def __init__(self, parent, label, name, colour, tooltip):
        self.type = "button"
        self.name = name
        self.label = Label(parent, label, colour=colour[0])
        self.button = Button(parent, outFunction=self.onButton, colour=(colour[1], colour[0]))
        CeciliaLib.setToolTip(self.label, TT_BUTTON)

    def getValue(self):
        return 0

    def getName(self):
        return self.name

    def onButton(self, value):
        if CeciliaLib.getVar("currentModule") is not None:
            getattr(CeciliaLib.getVar("currentModule"), self.name)(value)


class CECGen:
    def __init__(self, parent, label, init, rate, name, popup, colour, tooltip):
        self.type = "gen"
        self.name = name
        self.rate = rate
        self.popup = popup
        self.label = Label(parent, label, colour=colour[0])
        self.entry = ListEntry(parent, ", ".join([str(x) for x in init]), colour=colour[1], outFunction=self.onEntry)
        CeciliaLib.setToolTip(self.label, TT_GEN)

    def getName(self):
        return self.name

    def convertToList(self, value):
        if ", " in value:
            value = value.split(', ')
        else:
            value = value.split(" ")
        value = [eval(val) for val in value if val.strip() != ""]
        return value

    def getValue(self):
        return self.convertToList(self.entry.getValue())

    def setValue(self, value, dump=None):
        self.entry.setValue(value)

    def onEntry(self, value):
        if type(value) != list:
            value = self.convertToList(value)
        if CeciliaLib.getVar("currentModule") is not None and self.rate == "k":
            getattr(CeciliaLib.getVar("currentModule"), self.name)(value)
        if self.popup is not None:
            self.popup[0].setValue(self.popup[1], True)

class CECPoly:
    def __init__(self, parent, label, name, values, init, colour, tooltip):
        self.name = name
        self.up = 1
        popupLabel = label.capitalize() + ' Voices'
        self.popup = CECPopup(parent, popupLabel, values, init, "i", self.name + 'num', colour, tooltip=False, output=False)
        chordLabel = label.capitalize() + ' Chords'
        self.chord = CECPopup(parent, chordLabel, sorted(POLY_CHORDS.keys()), '00 - None', "i", self.name, colour, tooltip=False, output=False)
        CeciliaLib.setToolTip(self.popup.label, TT_POLY_LABEL)
        CeciliaLib.setToolTip(self.chord.label, TT_POLY_CHORD)

    def getValue(self):
        return self.popup.getValue()

    def getChordValue(self):
        return self.chord.getValue()

    def getUp(self):
        return self.up

class SamplerPopup:
    def __init__(self, parent, values, init, name, outFunction=None):
        self.name = name + 'loopi'
        self.outFunction = outFunction
        self.value = values.index(init)
        self.popup = CustomMenu(parent, values, init, size=(100, 20), outFunction=self.onPopup)

    def onPopup(self, ind, label):
        self.value = ind
        if self.outFunction is not None:
            self.outFunction(self.value)

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

class SamplerToggle:
    def __init__(self, parent, init, name):
        self.name = name + 'startpoint'
        self.value = init
        self.toggle = Toggle(parent, init, outFunction=self.onToggle)

    def onToggle(self, val):
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
    outBox = wx.BoxSizer(wx.VERTICAL)
    objects = []

    widgetlist = [widget for widget in list if widget['type'] in ['cpopup', 'ctoggle', 'cbutton']]
    widgetCecList = [widget for widget in list if widget['type'] == 'cgen']
    widgetpoly = [widget for widget in list if widget['type'] == 'cpoly']

    for i, widget in enumerate(widgetlist):
        if widget['type'] == 'cpopup':
            tooltip = widget.get('help', '')
            name = widget['name']
            label = widget.get('label', '')
            values = widget.get('value')
            init = widget.get('init', values[0])
            rate = widget.get('rate', 'k')
            if rate == 'k':
                col = widget.get('col', '')
                if col == '':
                    col = random.choice(list(COLOUR_CLASSES.keys()))
                elif col not in COLOUR_CLASSES.keys():
                    CeciliaLib.showErrorDialog('Wrong colour!', '"%s"\n\nAvailable colours for -col flag are:\n\n%s.' % (col, ', '.join(COLOUR_CLASSES.keys())))
                    col = random.choice(list(COLOUR_CLASSES.keys()))
                colour = CeciliaLib.chooseColourFromName(col)
            else:
                colour = CeciliaLib.chooseColourFromName("grey")
            cpopup = CECPopup(parent, label, values, init, rate, name, colour)
            box = wx.FlexGridSizer(1, 2, 2, 10)
            box.AddMany([(cpopup.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (cpopup.popup, 0, wx.TOP | wx.ALIGN_LEFT, 2)])
            mainBox.Add(box, 0, wx.TOP | wx.BOTTOM, 1)
            objects.append(cpopup)

        elif widget['type'] == 'ctoggle':
            tooltip = widget.get('help', '')
            name = widget['name']
            label = widget.get('label', '')
            stack = widget.get('stack', False)
            init = widget.get('init', 0)
            rate = widget.get('rate', 'k')
            if rate == 'k':
                col = widget.get('col', '')
                if col == '':
                    col = random.choice(list(COLOUR_CLASSES.keys()))
                elif col not in COLOUR_CLASSES.keys():
                    CeciliaLib.showErrorDialog('Wrong colour!', '"%s"\n\nAvailable colours for -col flag are:\n\n%s.' % (col, ', '.join(COLOUR_CLASSES.keys())))
                    col = random.choice(list(COLOUR_CLASSES.keys()))
                colour = CeciliaLib.chooseColourFromName(col)
            else:
                colour = CeciliaLib.chooseColourFromName("grey")
            ctoggle = CECToggle(parent, label, init, rate, name, colour, tooltip, stack)
            if stack and label != '':
                labelBox = wx.FlexGridSizer(1, 1, 2, 10)
                labelBox.Add(ctoggle.label, 0, wx.EXPAND | wx.TOP, 2)
                mainBox.Add(labelBox, 0, wx.TOP | wx.BOTTOM, 1)
                stackBox = wx.FlexGridSizer(1, 8, 2, 7)
                stackBox.Add(ctoggle.toggle, 0, wx.TOP, 2)
                mainBox.Add(stackBox, 0, wx.TOP | wx.BOTTOM, 1)
            elif stack:
                stackBox.Add(ctoggle.toggle, 0, wx.TOP | wx.ALIGN_LEFT, 2)
            else:
                box = wx.FlexGridSizer(1, 2, 2, 10)
                box.AddMany([(ctoggle.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (ctoggle.toggle, 0, wx.TOP | wx.ALIGN_LEFT, 2)])
                mainBox.Add(box, 0, wx.TOP | wx.BOTTOM, 1)
            objects.append(ctoggle)

        elif widget['type'] == 'cbutton':
            tooltip = widget.get('help', '')
            name = widget['name']
            label = widget.get('label', '')
            col = widget.get('col', '')
            if col == '':
                col = random.choice(list(COLOUR_CLASSES.keys()))
            elif col not in COLOUR_CLASSES.keys():
                CeciliaLib.showErrorDialog('Wrong colour!', '"%s"\n\nAvailable colours for -col flag are:\n\n%s.' % (col, ', '.join(COLOUR_CLASSES.keys())))
                col = random.choice(list(COLOUR_CLASSES.keys()))
            colour = CeciliaLib.chooseColourFromName(col)
            cbutton = CECButton(parent, label, name, colour, tooltip)
            box = wx.FlexGridSizer(1, 2, 2, 10)
            box.AddMany([(cbutton.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (cbutton.button, 0, wx.TOP | wx.ALIGN_LEFT, 2)])
            mainBox.Add(box, 0, wx.TOP | wx.BOTTOM, 1)
            objects.append(cbutton)

    for i, widget in enumerate(widgetCecList):
        tooltip = widget.get('help', '')
        name = widget['name']
        init = widget.get('init', '1')
        label = widget.get('label', '')
        rate = widget.get('rate', 'k')
        if rate == 'k':
            col = widget.get('col', '')
            if col == '':
                col = random.choice(list(COLOUR_CLASSES.keys()))
            elif col not in COLOUR_CLASSES.keys():
                CeciliaLib.showErrorDialog('Wrong colour!', '"%s"\n\nAvailable colours for -col flag are:\n\n%s.' % (col, ', '.join(COLOUR_CLASSES.keys())))
                col = random.choice(list(COLOUR_CLASSES.keys()))
            colour = CeciliaLib.chooseColourFromName(col)
        else:
            colour = CeciliaLib.chooseColourFromName("grey")
        popup = widget.get("popup", None)
        ok = False
        if popup is not None:
            for obj in objects:
                if obj.name == popup[0]:
                    popup = (obj, popup[1])
                    ok = True
                    break
        if not ok: popup = None
        clist = CECGen(parent, label, init, rate, name, popup, colour, tooltip)
        box = wx.FlexGridSizer(1, 2, 2, 10)
        box.AddMany([(clist.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (clist.entry, 0, wx.ALIGN_LEFT | wx.TOP, 2)])
        mainBox.Add(box, 0, wx.TOP | wx.BOTTOM, 1)
        objects.append(clist)

    for i, widget in enumerate(widgetpoly):
        tooltip = widget.get('help', '')
        name = widget['name']
        minvoices = widget.get('min', 1)
        maxvoices = widget.get('max', 10)
        values = [str(voice) for voice in range(minvoices, maxvoices + 1)]
        init = widget.get('init', values[0])
        label = widget.get('label', '')
        colour = [CPOLY_COLOUR, CPOLY_COLOUR]
        cpoly = CECPoly(parent, label, name, values, init, colour, tooltip)
        box = wx.FlexGridSizer(0, 2, 2, 10)
        box.AddMany([(cpoly.popup.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (cpoly.popup.popup, 0, wx.ALIGN_LEFT | wx.TOP, 2),
                    (cpoly.chord.label, 0, wx.TOP | wx.ALIGN_RIGHT, 2), (cpoly.chord.popup, 0, wx.ALIGN_LEFT | wx.TOP, 2)])
        mainBox.Add(box, 0, wx.TOP | wx.BOTTOM, 1)
        objects.append(cpoly.popup)
        objects.append(cpoly.chord)

    outBox.Add(mainBox, 0, wx.ALL, 5)
    return outBox, objects
