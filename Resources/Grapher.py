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

import wx, time, random
import CeciliaPlot as plot
import math, copy
from constants import *
import CeciliaLib
from Widgets import *
from types import ListType, TupleType
from pyo import reducePoints

try:
    import numpy.oldnumeric as _Numeric
except:
    try:
        import numarray as _Numeric  #if numarray is used it is renamed Numeric
    except:
        try:
            import Numeric as _Numeric
        except:
            msg= """
            This module requires the Numeric/numarray or NumPy module,
            which could not be imported.  It probably is not installed
            (it's not part of the standard Python distribution). See the
            Numeric Python site (http://numpy.scipy.org) for information on
            downloading source or binaries."""
            raise ImportError, "Numeric,numarray or NumPy not found. \n" + msg

def mouseOver(dist1, dist2, pourcent=.0008):
    if dist1 > dist2 - (dist2 * pourcent) and dist1 < dist2 + (dist2 * pourcent):
        return True
    else:
        return False

def chooseColour(i, numlines):
    def clip(x):
        val = int(x*255)
        if val < 0: val = 0
        elif val > 255: val = 255
        else: val = val
        return val

    def colour(i, numlines, sat, bright):        
        hue = (i / float(numlines)) * 315
        segment = math.floor(hue / 60) % 6
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

    lineColour = colour(i, numlines, 1, 1)    
    midColour = colour(i, numlines, .5, .5)
    knobColour = colour(i, numlines, .8, .5)
    sliderColour = colour(i, numlines, .5, .75)

    return [lineColour, midColour, knobColour, sliderColour]

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

class Line:
    def __init__(self, data, yrange, colour, label='', log=False, name='', size=8192, slider=None, suffix=''):
        self.data = data
        self.yrange = yrange
        self.scale = yrange[1] - yrange[0]
        self.offset = yrange[0]
        self.label = label
        self.log = log
        self.name = name
        self.size = size
        self.slider = slider
        self.show = 1
        self.suffix = suffix
        self.colour = colour[0]
        self.midColour = colour[1]
        self.knobColour = colour[2]  
        self.sliderColour = colour[3]
        # curved variables
        self.curved = False
        self.lines = []
        self.initData = self.getLineState()

    def getLineState(self):
        dict = {'data': self.normalize(),
                'curved': self.getCurved()}
        return copy.deepcopy(dict)

    def setLineState(self, dict):
        dict = copy.deepcopy(dict)
        data = dict['data']
        self.data = self.denormalize(data)
        self.curved = dict.get('curved', False)
        self.checkIfCurved()

    def changeYrange(self, newrange):
        d = self.getLineState()
        self.yrange = newrange
        self.scale = self.yrange[1] - self.yrange[0]
        self.offset = self.yrange[0]
        self.setLineState(d)

    def getColour(self):
        return self.colour
    
    def getMidColour(self):
        return self.midColour

    def getSuffix(self):
        return self.suffix
        
    def getData(self):
        return self.data
        
    def setData(self, list):
        self.data = list
        self.checkIfCurved()

    def reset(self):
        self.setLineState(self.initData)
        self.initData = self.getLineState()

    def setPoint(self, point, value):
        self.data[point] = value
        self.checkIfCurved()

    def move(self, list, offset):
        self.data = [[l[0] - offset[0], l[1] - offset[1]] for l in list]
        self.checkIfCurved()

    def moveLog(self, list, offset):
        self.data = [[l[0] - offset[0], l[1] * offset[1]] for l in list]
        self.checkIfCurved()

    def insert(self, pos, value):
        self.data.insert(pos, value)
        self.checkIfCurved()

    def deletePoint(self, pos):
        del self.data[pos]
        self.checkIfCurved()

    def deletePointFromPoint(self, point):
        if point in self.data:
            self.data.remove(point)
            self.checkIfCurved()

    def setShow(self, state):
        self.show = state

    def getShow(self):
        return self.show

    def getYrange(self):
        return self.yrange

    def getScale(self):
        return self.scale

    def getOffset(self):
        return self.offset

    def getLabel(self):
        return self.label

    def getName(self):
        return self.name

    def getLog(self):
        return self.log

    def getLength(self):
        return len(self.data)

    def getSize(self):
        return self.size

    def getSlider(self):
        return self.slider

    def setCurved(self, state):
        self.curved = state

    def getCurved(self):
        return self.curved

    def getLines(self):
        return self.lines

    def normalize(self):
        data = [p for p in self.getData()]
        yrange = self.getYrange()
        totaltime = CeciliaLib.getVar("totalTime")
        templist = []
        if self.getLog():
            for l in data:
                l0 = l[0] / float(totaltime)
                l1 = math.log10(l[1]/yrange[0]) / math.log10(yrange[1]/yrange[0])
                templist.append([l0,l1])
        else:
            for l in data:
                l0 = l[0] / float(totaltime)
                l1 = (l[1] - yrange[0]) / (yrange[1] - yrange[0])
                templist.append([l0,l1])
        return templist

    def denormalize(self, data):
        yrange = self.getYrange()
        totaltime = CeciliaLib.getVar("totalTime")
        if self.getLog():
            for l in data:
                l[0] = l[0] * totaltime
                l[1] = math.pow(10, l[1] * (math.log10(yrange[1]) - math.log10(yrange[0])) + math.log10(yrange[0]))
        else:
            for l in data:
                l[0] = l[0] * totaltime
                l[1] = l[1] * (yrange[1] - yrange[0]) + yrange[0]
        return data

    def setCurvedLine(self):
        if self.curved:
            self.curved = False
            return
        else:
            self.curved = True

        data = self.normalize()

        num = 1024
        self.lines = []
   
        for k in range(len(data)-1):
            x1 = data[k][0]
            x2 = data[k][1]
            y1 = data[k+1][0]
            y2 = data[k+1][1]   
            steps = int((y1 - x1) * num)
            if steps <= 0:
                pass
            else:
                inc = 1.0 / num
                for i in range(steps):
                    mu = float(i) / steps
                    mu2 = (1.0 - math.cos(mu * math.pi)) * 0.5
                    x = x1 + inc * i
                    val = x2 * (1.0 - mu2) + y2 * mu2
                    self.lines.append([x, val])

        self.lines.append(data[-1])
        self.lines = self.denormalize(self.lines)

    def checkIfCurved(self):
        if self.getCurved():
            self.curved = False
            self.setCurvedLine()
     
class Grapher(plot.PlotCanvas):
    def __init__(self, parent, style=wx.EXPAND):
        plot.PlotCanvas.__init__(self, parent, style=wx.EXPAND | wx.WANTS_CHARS)
        self.parent = parent
        self.menubarUndo = self.parent.parent.menubar.FindItemById(ID_UNDO)
        self.menubarRedo = self.parent.parent.menubar.FindItemById(ID_REDO)
        self._history = []
        self._historyPoint = 0
        self._clipboard = None
        self._tool = 0
        self._zoomed = False
        self.SetUseScientificNotation(False)
        self.SetEnableTitle(False)
        self.SetFontSizeAxis(GRAPHER_AXIS_FONT)
        self.SetFontSizeLegend(GRAPHER_LEGEND_FONT)
        self.SetBackColour(GRAPHER_BACK_COLOUR)
        self.SetGridColour(wx.Colour(170,170,170))
        self.SetEnableGrid(True)
        self.setLogScale((False, False))
        self.totaltime = 1
        self.curve = None # edited curve
        self.point = None # edited point
        self.selectedPoints = []
        self.markSelectionStart = None
        self.lineOver = None # mouse overed curve
        self.selected = 0 # selected curve
        self.data = []
        self._oldData = []
        self.visibleLines = []
        self._pencilData = []
        self._pencilDir = 0
        self._pencilOldPos = None
        self._background_bitmap = ICON_GRAPHER_BACKGROUND.GetBitmap()

        self.Bind(wx.EVT_CHAR, self.OnKeyDown)
        self.canvas.Bind(wx.EVT_CHAR, self.OnKeyDown)
        self.canvas.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

    def OnLooseFocus(self, event):
        win = wx.FindWindowAtPointer()
        if win != None:
            win = win.GetTopLevelParent()
            if win not in [CeciliaLib.getVar("mainFrame"), CeciliaLib.getVar("interface")]:
                win.Raise()
        event.Skip()
        
    def setTool(self, tool):
        self._tool = tool
        if self._tool < 2:
            self.SetToolCursor(tool)
            self.SetEnableZoom(False, tool)
            self.SetEnableDrag(False, tool)
        elif self._tool == 2:
            self.SetEnableZoom(True)
        else:
            self.SetEnableDrag(True)

    def setTotalTime(self, time):
        oldTotalTime = self.totaltime
        self.totaltime = time
        if self.data:
            for line in self.data:
                line.setData([[p[0]/oldTotalTime*self.totaltime, p[1]] for p in line.getData()])
            self.draw()

    def getTotalTime(self):
        return self.totaltime

    def getData(self):
        return self.data

    def setSelected(self, which):
        self.selectedPoints = []
        if self._zoomed:
            self.adjustZoomCorners(which)
        self.selected = which
        self.draw()

    def resetSelectedPoints(self):
        self.selectedPoints = []
        self.draw()
        
    def getSelected(self):
        return self.selected

    def sendSelected(self):
        self.parent.setSelected(self.selected)
        
    def getLine(self, which):
        return self.data[which]

    def removeLine(self, name):
        for line in self.data:
            if line.getName() == name:
                self.data.remove(line)
                break
        self.draw()

    def removeLines(self, names):
        for name in names:
            for line in self.data:
                if line.getName() == name:
                    self.data.remove(line)
                    break
        self.draw()
                
    def createLine(self, data, yrange, colour, label='', log=False, name='', size=8192, slider=None, suffix=''): 
        if data[0][0] != 0: data[0][0] = 0
        if data[-1][0] != self.totaltime: data[-1][0] = self.totaltime
        self.data.append(Line(data, yrange, colour, label, log, name, size, slider, suffix))
        self.draw()

    def onCopy(self):
        line = self.getLine(self.getSelected())
        self._clipboard = line.getLineState()

    def onPaste(self):
        if self._clipboard:
            line = self.getLine(self.getSelected())
            line.setLineState(self._clipboard)
            self.draw()
            self.onCopy()
            self.checkForHistory()
            if line.getSlider() != None:
                line.getSlider().setPlay(1)

    def checkForHistory(self, fromUndo=False):
        if self._oldData != self._currentData:
            self.addHistory(fromUndo)
            self._oldData = self._currentData

    def addHistory(self, fromUndo=False):
        data = {}
        for i, l in enumerate(self.data):
            data[i] = l.getLineState()
        if len(self._history) > 100:
            del self._history[-1]
        if len(self._history):
            if data != self._history[0]:
                self._history.insert(0, data)
        else:
            self._history.insert(0, data)
        if not fromUndo:
            self._historyPoint = 0

    def undoRedo(self, dir):
        if dir == 1 and self._historyPoint < (len(self._history) - 1):
            self._historyPoint += dir
            for i, l in enumerate(self.data):
                l.setLineState(self._history[self._historyPoint][i])
            self.draw()
        elif dir == -1 and self._historyPoint > 0:
            self._historyPoint += dir
            for i, l in enumerate(self.data):
                l.setLineState(self._history[self._historyPoint][i])
            self.draw()
 
        if len(self._history) > 0 :
            if self._historyPoint >= (len(self._history) - 1):
                self.menubarUndo.Enable(False)
            else:     
                self.menubarUndo.Enable(True)
            if self._historyPoint <= 0:
                self.menubarRedo.Enable(False)
            else:     
                self.menubarRedo.Enable(True)
        else:
            self.menubarUndo.Enable(False)
            self.menubarRedo.Enable(False)
         
    def zoom(self):
        if self._zoomed:
            minX, minY= _Numeric.minimum( self._zoomCorner1, self._zoomCorner2)
            maxX, maxY= _Numeric.maximum( self._zoomCorner1, self._zoomCorner2)
            if self.last_draw != None:
                self._Draw(self.last_draw[0], xAxis = (minX,maxX), yAxis = (minY,maxY), dc = None)
   
    def rescaleLinLin(self, data, scale, currentScale, offset, currentOffset):
        scaling = float(currentScale) / scale
        return [[p[0], (p[1]-offset) * scaling + currentOffset] for p in data]

    def rescaleLogLog(self, data, yrange, currentYrange):
        list = []
        totalRange = math.log10(yrange[1] / yrange[0])
        currentTotalRange = math.log10(currentYrange[1]/currentYrange[0])
        currentMin = math.log10(currentYrange[0])
        for p in data:
            ratio = math.log10(p[1] / yrange[0]) / totalRange
            list.append([p[0], math.pow(10, ratio * currentTotalRange + currentMin)])
        return list

    def rescaleLinLog(self, data, yrange, currentYrange):
        list = []
        if yrange[0] == 0: yoffrange = .00001
        else: yoffrange = yrange[0] 
        totalRange = yrange[1] - yoffrange
        currentTotalRange = math.log10(currentYrange[1]/currentYrange[0])
        currentMin = math.log10(currentYrange[0])
        for p in data:
            if p[1] == 0: p1 = .00001
            else: p1 = p[1]
            ratio = (p1 - yoffrange) / totalRange
            list.append([p[0], math.pow(10, ratio * currentTotalRange + currentMin)])
        return list

    def rescaleLogLin(self, data, yrange, currentYrange):
        list = []
        totalRange = math.log10(yrange[1] / yrange[0])
        currentTotalRange = currentYrange[1] - currentYrange[0]
        currentMin = currentYrange[0]
        for p in data:
            ratio = math.log10(p[1] / yrange[0]) / totalRange
            list.append([p[0], ratio * currentTotalRange + currentMin])
        return list

    def adjustZoomCorners(self, new):
        currentLine = self.getLine(self.getSelected())
        newLine = self.getLine(new)
        if currentLine.getLog() and newLine.getLog():
            _zoomCorner1 = _Numeric.array([self._zoomCorner1[0], _Numeric.power(10, self._zoomCorner1[1])])
            _zoomCorner2 = _Numeric.array([self._zoomCorner2[0], _Numeric.power(10, self._zoomCorner2[1])])
            self._zoomCorner1 = _Numeric.array(self.rescaleLogLog([_zoomCorner1], currentLine.getYrange(), newLine.getYrange()))[0]
            self._zoomCorner2 = _Numeric.array(self.rescaleLogLog([_zoomCorner2], currentLine.getYrange(), newLine.getYrange()))[0]
            self._zoomCorner1[1] = _Numeric.log10(self._zoomCorner1[1])
            self._zoomCorner2[1] = _Numeric.log10(self._zoomCorner2[1])
        elif currentLine.getLog() and not newLine.getLog():
            _zoomCorner1 = _Numeric.array([self._zoomCorner1[0], _Numeric.power(10, self._zoomCorner1[1])])
            _zoomCorner2 = _Numeric.array([self._zoomCorner2[0], _Numeric.power(10, self._zoomCorner2[1])])
            self._zoomCorner1 = _Numeric.array(self.rescaleLogLin([_zoomCorner1], currentLine.getYrange(), newLine.getYrange()))[0]
            self._zoomCorner2 = _Numeric.array(self.rescaleLogLin([_zoomCorner2], currentLine.getYrange(), newLine.getYrange()))[0]
        elif not currentLine.getLog() and not newLine.getLog():
            self._zoomCorner1 = _Numeric.array(self.rescaleLinLin([self._zoomCorner1], currentLine.getScale(), newLine.getScale(),
                                                                                       currentLine.getOffset(), newLine.getOffset()))[0]
            self._zoomCorner2 = _Numeric.array(self.rescaleLinLin([self._zoomCorner2], currentLine.getScale(), newLine.getScale(),
                                                                                       currentLine.getOffset(), newLine.getOffset()))[0]
        elif not currentLine.getLog() and newLine.getLog():
            self._zoomCorner1 = _Numeric.array(self.rescaleLinLog([self._zoomCorner1], currentLine.getYrange(), newLine.getYrange()))[0]
            self._zoomCorner2 = _Numeric.array(self.rescaleLinLog([self._zoomCorner2], currentLine.getYrange(), newLine.getYrange()))[0]
            self._zoomCorner1[1] = _Numeric.log10(self._zoomCorner1[1])
            self._zoomCorner2[1] = _Numeric.log10(self._zoomCorner2[1])

    def getRawData(self):
        data = []
        for l in self.data:
            data.append([p for p in l.getData()])
            data.append(l.getCurved())
        return data

    def draw(self):
        lines = []
        markers = []
        self.visibleLines = []
        currentScale = self.data[self.selected].getScale()
        currentOffset = self.data[self.selected].getOffset()
        currentYrange = self.data[self.selected].getYrange()
        tmpData = self.tmpDataOrderSelEnd()
        for l in tmpData:
            index = self.data.index(l)
            if index == self.lineOver: 
                col = 'black'
            else: 
                col = l.getColour()
            if l.getShow():
                if l.getCurved():
                    data = l.getLines()
                else:
                    data = l.getData()
                if index == self.selected: 
                    width = 2
                    mark = 'circle'
                    line = plot.PolyLine(data, colour=col, width=width, legend=l.getLabel())
                    marker = plot.PolyMarker(l.getData(), size=1.1, marker=mark, fillcolour='black')
                    if CeciliaLib.getVar("currentModule") != None:
                        try:
                            CeciliaLib.getVar("currentModule")._graphs[l.name].setValue(data)
                        except:
                            try:
                                if CeciliaLib.getVar("currentModule")._sliders[l.name].type == "slider":
                                    CeciliaLib.getVar("currentModule")._sliders[l.name].setGraph(data)
                                else:
                                    if l.getLabel().endswith("min"):
                                        which = 0
                                    else:
                                        which = 1
                                    CeciliaLib.getVar("currentModule")._sliders[l.name].setGraph(which, data)
                            except:
                                try:
                                    CeciliaLib.getVar("currentModule")._samplers[l.name].setGraph(l.name, data)
                                except:
                                    pass
                else: 
                    width = 1
                    mark = 'dot'
                    if self.data[self.selected].getLog():
                        if l.getLog():
                            dataToDraw = self.rescaleLogLog(data, l.getYrange(), currentYrange)
                        else:
                            dataToDraw = self.rescaleLinLog(data, l.getYrange(), currentYrange)
                    else:
                        if l.getLog():
                            dataToDraw = self.rescaleLogLin(data, l.getYrange(), currentYrange)
                        else:
                            dataToDraw = self.rescaleLinLin(data, l.getScale(), currentScale, l.getOffset(), currentOffset)
                    line = plot.PolyLine(dataToDraw, colour=col, width=width, legend=l.getLabel())
                    marker = plot.PolyMarker([dataToDraw[0], dataToDraw[-1]], size=1, marker=mark)
                if l.getLog():
                    line.setLogScale((False, True))
                    marker.setLogScale((False, True))
                if self.data[self.selected].getLog():
                    self.setLogScale((False, True))
                else:
                    self.setLogScale((False, False))
                lines.append(line)
                markers.append(marker)
                if self.selectedPoints and index == self.selected:
                    selmarker = plot.PolyMarker([l.getData()[selp] for selp in self.selectedPoints], size=1.5, marker=mark, fillcolour='white')
                    markers.append(selmarker)
                self.visibleLines.append(l)
        lines.extend(markers)    

        gc = plot.PlotGraphics(lines, 'Title', '', '')
        self.Draw(gc, xAxis = (0,self.totaltime), yAxis = self.data[self.selected].getYrange())
        self._currentData = self.getRawData()
        self.zoom()

    def OnLeave(self, event):
        self.curve = None
        self.point = None
        self.lineOver = None
        self.draw()
        
    def OnMouseDoubleClick(self, event):
        if self.lineOver != None and self.lineOver == self.selected:
            line = self.data[self.lineOver]
            line.setCurvedLine()
            if line.getSlider() != None:
                line.getSlider().setPlay(1)
        else:
            pos = list(self.GetXY(event))
            line = self.data[self.selected]
            points = [p[0] for p in line.getData()]
            for i in range(len(points)-1):
                if pos[0] > points[i] and pos[0] < points[i+1]:
                    line.insert(i+1, pos)
                    self.point = i+1
            if pos[0] > points[-1]:
                    line.insert(len(points), pos)
                    self.point = len(points)
            elif pos[0] < points[0]:
                    line.insert(0, pos)
                    self.point = 0
            if line.getSlider() != None:
                line.getSlider().setPlay(1)
            self.curve = self.selected
            self.setValuesToDraw(self._getXY(event), pos[0], pos[1])
        self.draw()

    def OnMouseRightDown(self, event):
        pos = self._getXY(event)
        ldata = self.GetClosestPoint(pos, pointScaled=True)
        # test the distance of the closest point
        if ldata[5] < 5:
            self._historyAddFlag = True
            l = self.data.index(self.visibleLines[ldata[0]])
            line = self.data[l]
            if line.getCurved():
                if ldata[2] == 0 or ldata[2] == (len(line.getLines())-1):
                    return
                if line.getLines()[ldata[2]] in line.getData():
                    line.deletePoint(line.getData().index(line.getLines()[ldata[2]]))
            else:
                if ldata[2] == 0 or ldata[2] == (len(line.getData())-1):
                    return
                line.deletePoint(ldata[2])
            self.draw()
        self.checkForHistory()

    def pointsNear(self, p1, p2):
        if (p2[0] - .5) < p1[0] < (p2[0] + .5) and (p2[1] - .5) < p1[1] < (p2[1] + .5):
            return True
        else:
            return False
                
    def OnMouseLeftDown(self, event):
        tmp_selectedPoints = [p for p in self.selectedPoints]
        if self._tool > 1:
            self._zoomCorner1[0], self._zoomCorner1[1]= self._getXY(event)
            self._screenCoordinates = _Numeric.array(event.GetPosition())
            if self._dragEnabled:
                self.SetCursor(self.GrabHandCursor)
                self.canvas.CaptureMouse()

        pos = self._getXY(event)
        ldata = self.GetClosestPoint(pos, pointScaled=True)
        ldata2 = self.GetClosestPoints(pos, pointScaled=True)
        for res in ldata2:
            if res[5] < 5:
                if self.data.index(self.visibleLines[res[0]]) == self.selected:
                    ldata = res
                    break
        if ldata:
            # grab a point and select the line
            if ldata[5] < 5:
                l = self.data.index(self.visibleLines[ldata[0]])
                p = ldata[2]
                line = self.data[l]
                if line.getCurved():
                    pt = p
                    for point in line.getData():
                        if self.pointsNear(line.getLines()[pt], point):
                            p = line.getData().index(point)
                            break
                        else:
                            p = None
                if p != None and line.getShow():
                    self.curve = l
                    self.point = p
                    if self._tool == 0:
                        if p not in tmp_selectedPoints:
                            self.selectedPoints = [p]
                            if event.ShiftDown() and tmp_selectedPoints:
                                self.selectedPoints.extend([pt for pt in tmp_selectedPoints if pt not in self.selectedPoints])
                            self.selectedPoints.sort()    
                        self.templist = [[l[0], l[1]] for i,l in enumerate(self.data[self.selected].getData()) if i in self.selectedPoints]
                        self.startpos = self.lastpos = self.GetXY(event)
                    self.selected = self.curve
                    self.mouseOver = None
                    self.sendSelected()
                    self.setValuesToDraw(self._getXY(event), pos[0], pos[1])
                    self.draw()
                    event.Skip()
                    return
                    
        self.selectedPoints = []

        if self._tool == 1:
            pos = list(self.GetXY(event))
            self._pencilData = []
            self.startpos = pos
            self._pencilOldPos = pos
            line = self.data[self.selected]
            points = [p[0] for p in line.getData()]
            for i in range(len(points)-1):
                if pos[0] > points[i] and pos[0] < points[i+1]:
                    line.insert(i+1, pos)
            if pos[0] > points[-1]:
                    line.insert(len(points), pos)
            elif pos[0] < points[0]:
                    line.insert(0, pos)
            if line.getSlider() != None:
                line.getSlider().setPlay(1)
            self.curve = self.selected
            self.point = None
            self.setValuesToDraw(self._getXY(event), pos[0], pos[1])
            self.draw()

        else:
            pos = self.GetXY(event)
            # move the line if already selected
            if self.lineOver != None and self.lineOver == self.selected:
                self.startpos = pos
                self.curve = self.lineOver
                # set extreme Xs and Ys for clipping
                self.templist = [[l[0], l[1]] for l in self.data[self.curve].getData()]
                Xs = [p[0] for p in self.templist]
                self.extremeXs = (min(Xs), max(Xs))
                Ys = [p[1] for p in self.templist]
                self.extremeYs = (min(Ys), max(Ys)) 
                self.draw()

            # removed selecting a line from the graph
            # select the line if not already selected
            #elif self.lineOver != None and self.data[self.lineOver].getShow():
            #    if self._zoomed: # rescale _zoomCorners if zoomed
            #        self.adjustZoomCorners(self.lineOver)
            #    self.selected = self.lineOver
            #    self.sendSelected()
            #    self.draw() 
            else:
                if self._tool == 0:
                    self.markSelectionStart = self.GetXY(event)
                    self._markSelectionStart = self._getXY(event)
        
        if tmp_selectedPoints != []:
            tmp_selectedPoints = []
            self.draw()               
        event.Skip()

    def OnMouseLeftUp(self, event):
        if self._zoomEnabled:
            if self._hasDragged == True:                
                self._drawRubberBand(self._zoomCorner1, self._zoomCorner2) # remove old
                self._zoomCorner2[0], self._zoomCorner2[1] = self._getXY(event)
                
                tmp_Y = self._zoomCorner1[1]-self._zoomCorner2[1]
                tmp_X = self._zoomCorner2[0]-self._zoomCorner1[0]
                # maximum percentage of zooming
                if tmp_Y >= 0.01 and (tmp_X / self.getTotalTime()) >= 0.01:                   
                    minX, minY = _Numeric.minimum( self._zoomCorner1, self._zoomCorner2)
                    maxX, maxY = _Numeric.maximum( self._zoomCorner1, self._zoomCorner2)
                    self._hasDragged = False  # reset flag
                    self.last_PointLabel = None        #reset pointLabel
                    self._zoomed = True    
                    if self.last_draw != None:
                        self._Draw(self.last_draw[0], xAxis = (minX,maxX), yAxis = (minY,maxY), dc = None)
                else:
                    self._hasDragged = False  # reset flag
                    self.last_PointLabel = None        #reset pointLabel
                    if self.last_draw != None:
                        self._Draw(self.last_draw[0], xAxis = self.last_draw[1], yAxis = self.last_draw[2], dc = None)
                            
        if self._dragEnabled:
            self.SetCursor(self.HandCursor)
            if self.canvas.HasCapture():
                self.canvas.ReleaseMouse()

        if self.markSelectionStart != None:
            self.selectedPoints = []
            markSelectionEnd = self.GetXY(event)
            X = min(markSelectionEnd[0], self.markSelectionStart[0])
            Y = min(markSelectionEnd[1], self.markSelectionStart[1])
            W = max(markSelectionEnd[0], self.markSelectionStart[0]) - X
            H = max(markSelectionEnd[1], self.markSelectionStart[1]) - Y
            rect = wx.Rect2D(X, Y, W, H)
            data = self.getLine(self.getSelected()).getData()
            for p in data:
                if rect.Contains(p):
                    self.selectedPoints.append(data.index(p))
            self.markSelectionStart = None
            self.drawSelectionRect(None, None)
            self.draw()        
            
        self.checkForHistory()
        self.curve = None
        self.point = None
        self.setValuesToDraw(self._getXY(event))
    
    def OnMotion(self,event):
        if self._zoomEnabled and event.LeftIsDown() and self._tool > 1 and self.curve == None:
            if self._hasDragged:
                self._drawRubberBand(self._zoomCorner1, self._zoomCorner2) # remove old
            else:
                self._hasDragged= True
            self._zoomCorner2[0], self._zoomCorner2[1] = self._getXY(event)
            self._drawRubberBand(self._zoomCorner1, self._zoomCorner2) # add new
        elif self._dragEnabled and event.LeftIsDown() and self._zoomed and self._tool > 1 and self.curve == None:
            coordinates = event.GetPosition()
            newpos, oldpos = map(_Numeric.array, map(self.PositionScreenToUser, [coordinates, self._screenCoordinates]))
            dist = newpos-oldpos
            self._screenCoordinates = coordinates

            yRange = self.getLine(self.getSelected()).getYrange()
            if self.last_draw is not None:
                graphics, xAxis, yAxis= self.last_draw
                yAxis -= dist[1]
                xAxis -= dist[0]

                if xAxis[0] < 0:
                    xAxis[1] = xAxis[1] - xAxis[0]
                    xAxis[0] = 0
                elif xAxis[1] > self.getTotalTime():
                    xAxis[0] = self.getTotalTime() - (xAxis[1] - xAxis[0])
                    xAxis[1] = self.getTotalTime()
                if self.getLine(self.getSelected()).getLog():
                    if _Numeric.power(10,yAxis[0]) < yRange[0]:
                        yAxis[1] = _Numeric.log10(yRange[0]) + yAxis[1] - yAxis[0]
                        yAxis[0] = _Numeric.log10(yRange[0])
                    elif _Numeric.power(10,yAxis[1]) > yRange[1]:
                        yAxis[0] = _Numeric.log10(yRange[1]) - (yAxis[1] - yAxis[0])
                        yAxis[1] = _Numeric.log10(yRange[1])
                else:
                    if yAxis[0] < yRange[0]:
                        yAxis[1] = yRange[0] + yAxis[1] - yAxis[0]
                        yAxis[0] = yRange[0]
                    elif yAxis[1] > yRange[1]:
                        yAxis[0] = yRange[1] - (yAxis[1] - yAxis[0])
                        yAxis[1] = yRange[1]

                self._zoomCorner1[0] = xAxis[0]
                self._zoomCorner2[0] = xAxis[1]
                self._zoomCorner1[1] = yAxis[0]
                self._zoomCorner2[1] = yAxis[1]
                
                self._Draw(graphics,xAxis,yAxis)

        if self._tool == 0:
            pos = self.GetXY(event)
            # Moves point
            if self.point != None:
                if not self.selectedPoints:
                    if self.point == 0: minboundary = self.GetXCurrentRange()[0]
                    else: minboundary = self.data[self.curve].getData()[self.point-1][0]
                    if self.point == (len(self.data[self.curve].getData()) - 1): maxboundary = self.GetXCurrentRange()[1]
                    else: maxboundary = self.data[self.curve].getData()[self.point+1][0]
    
                    if pos[0] < minboundary: X = minboundary
                    elif pos[0] > maxboundary: X = maxboundary
                    else: X = pos[0]
                    
                    if pos[1] < self.GetYCurrentRange()[0]: Y = self.GetYCurrentRange()[0] 
                    elif pos[1] > self.GetYCurrentRange()[1]: Y = self.GetYCurrentRange()[1]
                    else: Y = pos[1]
    
                    if self.point == 0: X = 0
                    if self.point == (self.data[self.curve].getLength() - 1): X = self.totaltime            
                    self.data[self.curve].setPoint(self.point, [X,Y])
                else:
                    currentYrange = self.data[self.selected].getYrange()
                    selectedPoints = [p for p in self.selectedPoints]
                    if pos[0] > self.lastpos[0]:
                        selectedPoints.reverse()
                    for p in selectedPoints:
                        if p == 0: minboundary = self.GetXCurrentRange()[0]
                        else: minboundary = self.data[self.curve].getData()[p-1][0]
                        if p == (len(self.data[self.curve].getData()) - 1): maxboundary = self.GetXCurrentRange()[1]
                        else: maxboundary = self.data[self.curve].getData()[p+1][0]

                        if self.data[self.selected].getLog():
                            offset = (self.startpos[0] - pos[0], pos[1] / self.startpos[1])
                        else:
                            offset = (self.startpos[0] - pos[0], self.startpos[1] - pos[1])
                            
                        newxpos =  self.templist[self.selectedPoints.index(p)][0] - offset[0]     
                        if newxpos < minboundary: X = minboundary
                        elif newxpos > maxboundary: X = maxboundary
                        else: X = newxpos

                        if self.data[self.selected].getLog():
                            newypos =  self.templist[self.selectedPoints.index(p)][1] * offset[1]   
                        else:      
                            newypos =  self.templist[self.selectedPoints.index(p)][1] - offset[1]   
                        if newypos < self.GetYCurrentRange()[0]: Y = self.GetYCurrentRange()[0] 
                        elif newypos > self.GetYCurrentRange()[1]: Y = self.GetYCurrentRange()[1]
                        else: Y = newypos

                        if p == 0: X = 0
                        if p == (self.data[self.curve].getLength() - 1): X = self.totaltime            
                        self.data[self.curve].setPoint(p, [X,Y])
                    self.lastpos = pos
                self.setValuesToDraw(self._getXY(event), pos[0], pos[1])
                self.draw()
    
            # Move line    
            elif self.curve != None:
                if self.data[self.selected].getLog():
                    offset = (self.startpos[0] - pos[0], pos[1] / self.startpos[1])
                    clipedOffset = self.clipLog(offset, self.extremeXs, self.extremeYs)
                    self.data[self.curve].moveLog(self.templist, clipedOffset)
                else:
                    offset = (self.startpos[0] - pos[0], self.startpos[1] - pos[1])
                    clipedOffset = self.clip(offset, self.extremeXs, self.extremeYs)
                    self.data[self.curve].move(self.templist, clipedOffset)
                self.draw()
            
            # draw selection marquee
            elif self.markSelectionStart != None:
                corner1 = self._markSelectionStart
                corner2 = self._getXY(event)
                self.drawSelectionRect(corner1, corner2)
                self.draw()
                
            # Check for mouse over            
            else:
                currentScale = float(self.data[self.selected].getScale())
                currentOffset = float(self.data[self.selected].getOffset())
                currentYrange = self.data[self.selected].getYrange()
                tmpData = self.tmpDataOrderSelBegin()
                for curve in tmpData:
                    if self.data.index(curve) != self.selected:
                        continue # removed mouse over for non-selected lines
                        if self.data[self.selected].getLog():
                            if curve.getLog():
                                ratio = math.log10(pos[1]/currentYrange[0]) / math.log10(currentYrange[1]/currentYrange[0])
                                pos1 = math.pow(10, ratio * math.log10(curve.getYrange()[1]/curve.getYrange()[0]) + math.log10(curve.getOffset()))
                                checkPos = (pos[0], pos1)
                            else:
                                ratio = math.log10(pos[1]/currentYrange[0]) / math.log10(currentYrange[1]/currentYrange[0])
                                checkPos = (pos[0], ratio * curve.getScale() + curve.getOffset())
                        else:
                            if curve.getLog():
                                ratio = (pos[1] - currentOffset) / (currentYrange[1] - currentYrange[0])
                                pos1 = math.pow(10, ratio * math.log10(curve.getYrange()[1]/curve.getYrange()[0]) + math.log10(curve.getOffset()))
                                checkPos = (pos[0], pos1)
                            else:
                                scl = curve.getScale() / currentScale
                                checkPos = (pos[0], (pos[1] - currentOffset) * scl + curve.getOffset())
                    else:
                        checkPos = (pos[0], pos[1])
                    if curve.getCurved():
                        curvePosCheck = self._getXY(event)
                        ldata = self.GetClosestPoint(curvePosCheck, pointScaled=True)
                        ldata2 = self.GetClosestPoints(curvePosCheck, pointScaled=True)
                        for res in ldata2:
                            if res[5] < 5:
                                if self.data.index(self.visibleLines[res[0]]) == self.selected:
                                    ldata = res
                                    break
                        if ldata[5] < 10:
                            l = self.data.index(self.visibleLines[ldata[0]])
                            if self.data.index(curve) == l:
                                self.lineOver = self.data.index(curve)
                                self.draw()
                                return
                        else:
                            self.lineOver = None
                            self.draw()
                    else:
                        curveData = curve.getData()
                        pourcent = 0.0007
                    if curve.getLog() and not curve.getCurved():
                        for i in range(len(curveData)-1):
                            if mouseOver(self.distanceLog(checkPos, curveData[i], curve.getYrange()) + 
                                         self.distanceLog(checkPos, curveData[i+1], curve.getYrange()), 
                                         self.distanceLog(curveData[i], curveData[i+1], curve.getYrange()), pourcent):
                                self.lineOver = self.data.index(curve)
                                self.draw()
                                return
                            else:
                                if self.lineOver != None:
                                    self.lineOver = None
                                    self.draw()
                    elif not curve.getLog() and not curve.getCurved():
                        for i in range(len(curveData)-1):
                            if mouseOver(self.distance(checkPos, curveData[i], curve.getScale()) + 
                                         self.distance(checkPos, curveData[i+1], curve.getScale()), 
                                         self.distance(curveData[i], curveData[i+1], curve.getScale()), pourcent):
                                self.lineOver = self.data.index(curve)
                                self.draw()
                                return
                            else:
                                if self.lineOver != None:
                                    self.lineOver = None
                                    self.draw()
        elif self._tool == 1 and event.LeftIsDown():
            pos = self.GetXY(event)
            line = self.data[self.selected]
            if pos[0] < 0.0: pos = [0.0, pos[1]]
            elif pos[0] > CeciliaLib.getVar("totalTime"): pos = [CeciliaLib.getVar("totalTime"), pos[1]]
            minY, maxY = line.getYrange()[0], line.getYrange()[1] 
            if pos[1] < minY: pos = [pos[0], minY]
            elif pos[1] > maxY: pos = [pos[0], maxY]
            if line.getLog():
                distance = self.distanceLog(pos, self._pencilOldPos, line.getYrange())
            else:
                distance = self.distance(pos, self._pencilOldPos, line.getScale())    
            if distance > 0.001:
                if self._pencilOldPos[0] < pos[0]:
                    _pencilDir = 0
                else:
                    _pencilDir = 1    
                if _pencilDir != self._pencilDir:
                    self._pencilDir = _pencilDir
                    self._pencilData = []
                    self.startpos = pos
                minpos = min(self.startpos[0], pos[0])        
                maxpos = max(self.startpos[0], pos[0])        
                for p in line.getData():
                    if p[0] >= minpos and p[0] <= maxpos and p not in self._pencilData:
                        line.deletePointFromPoint(p)
                points = [p[0] for p in line.getData()]  
                for i in range(len(points)-1):
                    if pos[0] > points[i] and pos[0] < points[i+1]:
                        line.insert(i+1, pos)
                        self._pencilData.append(pos)
                if pos[0] >= points[-1]:
                    line.deletePoint(-1)              
                    line.data.append([CeciliaLib.getVar("totalTime"), pos[1]])
                    self._pencilData.append(pos)
                elif pos[0] <= points[0]:
                    line.deletePoint(0)              
                    line.data.insert(0, [0.0, pos[1]])
                    self._pencilData.append(pos)
                if line.getSlider() != None:
                    line.getSlider().setPlay(1)
                self.setValuesToDraw(self._getXY(event), pos[0], pos[1])
                self._pencilOldPos = pos
                self.point = None
                self.draw()

        event.Skip()
        
    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key == 118:
            self.parent.toolbar.radiotoolbox.setTool('pointer')
        elif key == 112:
            self.parent.toolbar.radiotoolbox.setTool('pencil')
        elif key == 122 and not event.CmdDown():
            self.parent.toolbar.radiotoolbox.setTool('zoom')
        elif key == 104:
            self.parent.toolbar.radiotoolbox.setTool('hand')
        elif key in [wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE, wx.WXK_BACK]:
            if self.selectedPoints:
                points = [self.data[self.selected].getData()[p] for p in self.selectedPoints]
                for p in points:
                    if not p[0] in [0.0, CeciliaLib.getVar("totalTime")]:
                        self.data[self.selected].deletePointFromPoint(p)
                self.selectedPoints = []    
                self.draw()
                self.checkForHistory()
            
        if self._zoomed and key == wx.WXK_ESCAPE:
            self._zoomed = False
            self.draw()
        event.Skip()

    def tmpDataOrderSelBegin(self):
        tmpData = [self.data[self.selected]]
        tmpData += [curve for curve in self.data if curve != self.data[self.selected]]
        return tmpData

    def tmpDataOrderSelEnd(self):
        tmpData = [curve for curve in self.data if curve != self.data[self.selected]]
        tmpData.reverse()
        tmpData += [self.data[self.selected]]
        return tmpData
        
    def clip(self, off, exXs, exYs):
        x,y = off
        minX, maxX = 0, self.getTotalTime()
        minY, maxY = self.getLine(self.getSelected()).getYrange()[0], self.getLine(self.getSelected()).getYrange()[1] 
        if exXs[0] - x >= minX and exXs[1] - x <= maxX:
            x = x
        elif exXs[1] - x >= maxX:
            x = exXs[1] - maxX
        else:
            x = exXs[0]
        if exYs[0] - y >= minY and exYs[1] - y <= maxY:
            y = y
        elif exYs[1] - y >= maxY:
            y = exYs[1] - maxY
        else:
            y = exYs[0] - minY
        return (x,y)

    def clipLog(self, off, exXs, exYs):
        x,y = off
        minX, maxX = 0, self.getTotalTime()
        minY, maxY = self.getLine(self.getSelected()).getYrange()[0], self.getLine(self.getSelected()).getYrange()[1] 
        if exXs[0] - x >= minX and exXs[1] - x <= maxX:
            x = x
        elif exXs[1] - x >= maxX:
            x = exXs[1] - maxX
        else:
            x = exXs[0]
        if exYs[0] * y >= minY and exYs[1] * y <= maxY:
            y = y
        elif exYs[1] * y >= maxY:
            y = maxY / exYs[1]
        else:
            y = minY / exYs[0]
        return (x,y)

    def distance(self, p1, p2, yscale):
        "Length of line between two points"
        xscl = 1./self.totaltime
        yscl = 1./yscale
        return math.sqrt(pow((p2[0]-p1[0])*xscl, 2) + pow((p2[1]-p1[1])*yscl, 2))
    
    def distanceLog(self, p1, p2, yrange):
        "Length of line between two points (based on X scale and Y ratio)"
        xscl = 1./self.totaltime
        Y = math.log10(p2[1]/p1[1]) / math.log10(yrange[1] / yrange[0])
        return math.sqrt(pow((p2[0]-p1[0])*xscl, 2) + pow(Y, 2))

class ToolBar(wx.Panel):
    def __init__(self, parent, size=(-1,25), tools=[], toolFunctions=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetBackgroundColour(TITLE_BACK_COLOUR)
        self.box = wx.FlexGridSizer(1, 7, 5, 0)
        self.parent = parent
        ffakePanel = wx.Panel(self, -1, size=(5, self.GetSize()[1]))
        ffakePanel.SetBackgroundColour(TITLE_BACK_COLOUR)
        self.menu = CustomMenu(self, choice=[], size=(130,20), init=None, outFunction=self.parent.onPopupMenu)               
        self.menu.setBackgroundColour(TITLE_BACK_COLOUR)
        self.menu.SetToolTip(CECTooltip(TT_GRAPH_POPUP))
        self.toolbox = ToolBox(self, tools=tools, outFunction=toolFunctions)
        self.toolbox.setBackColour(TITLE_BACK_COLOUR)
        self.convertSlider = ConvertSlider(self, self.GetParent())
        self.convertSlider.setBackColour(TITLE_BACK_COLOUR)
        self.convertSlider.SetToolTip(CECTooltip(TT_RES_SLIDER))

        fakePanel = wx.Panel(self, -1, size=(10, self.GetSize()[1]))
        fakePanel.SetBackgroundColour(TITLE_BACK_COLOUR)

        if CeciliaLib.getVar("moduleDescription") != '':
            helpButton = CloseBox(fakePanel, size=(18,18), pos=(25,2), outFunction=self.onShowModuleDescription, label=CeciliaLib.getVar("currentCeciliaFile", unicode=True))
            helpButton.setBackgroundColour(TITLE_BACK_COLOUR)
            helpButton.setInsideColour(CONTROLLABEL_BACK_COLOUR)
            helpButton.setTextMagnify(2)
        
        self.radiotoolbox = RadioToolBox(self, outFunction=[self.toolPointer, self.toolPencil, self.toolZoom, self.toolHand])
        self.palettetoolbox = PaletteToolBox(self)

        self.box.Add(ffakePanel, 0)
        self.box.Add(self.menu, 0, wx.BOTTOM | wx.LEFT, 5)
        self.box.Add(self.toolbox, 0, wx.BOTTOM | wx.LEFT, 5)
        self.box.Add(self.convertSlider, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 6)
        self.box.Add(fakePanel, 0, wx.EXPAND | wx.RIGHT, 20)
        self.box.Add(self.radiotoolbox, 0, wx.RIGHT, 20)
        self.box.Add(self.palettetoolbox, 0, wx.RIGHT, 20)

        self.Bind(wx.EVT_CHAR, self.OnKeyDown)

        self.box.AddGrowableCol(3)
        self.SetSizerAndFit(self.box)

        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        fakePanel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

    def onShowModuleDescription(self):
        pos = wx.GetMousePosition()
        pop = TextPopupFrame(self, CeciliaLib.getVar("moduleDescription"), pos=(pos[0]-100,pos[1]+20))
        
    def OnLooseFocus(self, event):
        win = wx.FindWindowAtPointer()
        if win != None:
            win = win.GetTopLevelParent()
            if win not in [CeciliaLib.getVar("mainFrame"), CeciliaLib.getVar("interface")]:
                win.Raise()
        event.Skip()

    def setPopupChoice(self, choice):
        self.menu.setChoice(choice)

    def getPopupChoice(self):
        return self.menu.getChoice()

    def toolPointer(self):
        self.GetParent().plotter.setTool(0)

    def toolPencil(self):
        self.GetParent().plotter.setTool(1)

    def toolZoom(self):
        self.GetParent().plotter.setTool(2)

    def toolHand(self):
        self.GetParent().plotter.setTool(3)

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key == 118:
            self.radiotoolbox.setTool('pointer')
        elif key == 112:
            self.radiotoolbox.setTool('pencil')
        elif key == 122:
            self.radiotoolbox.setTool('zoom')
        elif key == 104:
            self.radiotoolbox.setTool('hand')
        self.parent.plotter.OnKeyDown(event)    

class CursorPanel(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=(20,20), size=(410, 10)):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size)
        self.parent = parent
        self.SetMinSize((100,10))
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.time = 0
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

    def OnLooseFocus(self, event):
        win = wx.FindWindowAtPointer()
        if win != None:
            win = win.GetTopLevelParent()
            if win not in [CeciliaLib.getVar("mainFrame"), CeciliaLib.getVar("interface")]:
                win.Raise()
        event.Skip()

    def OnPaint(self, evt):
        gap = int(self.parent.plotter.PositionUserToScreen((0,0))[0])
        totalTime = CeciliaLib.getVar("totalTime")
        w, h = self.GetSize()
        time = int(self.time / totalTime * (w - gap * 2)) + gap + 4
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetPen(wx.Pen(GRAPHER_BACK_COLOUR))
        dc.SetBrush(wx.Brush(GRAPHER_BACK_COLOUR))
        dc.DrawRectangle(0, 0, w, h)
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR))
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR))
        dc.DrawPolygon([(time, h-1), (time-4, h-7), (time+4, h-7)])
    
    def setTime(self, time):
        self.time = time
        wx.CallAfter(self.Refresh)

class CECGrapher(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, pos=(20,20), size=(100, 100)):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size)
        self.parent = parent
        self.SetMinSize((100,100))
        self.SetBackgroundColour(BACKGROUND_COLOUR)

        self.showLineState = {}

        mainBox = wx.FlexGridSizer(4, 1, 0, 0)

        self.toolbar = ToolBar(self, tools=['save', 'load', 'reset', 'show'],
                               toolFunctions=[self.OnSave, self.OnLoad, self.onReset, self.onShow])
        mainBox.Add(self.toolbar, 0, wx.EXPAND)
        
        sepLine = Separator(self, size=(200,2), colour=BORDER_COLOUR)
        mainBox.Add(sepLine, 0, wx.EXPAND)

        self.cursorPanel = CursorPanel(self, size=(-1, 10))
        mainBox.Add(self.cursorPanel, 0, wx.EXPAND)

        self.plotter = Grapher(self)
        self.plotter.SetMinSize((100,100))  
        mainBox.Add(self.plotter, 1, wx.EXPAND | wx.ALL)

        mainBox.AddGrowableCol(0)
        mainBox.AddGrowableRow(3)
        self.SetSizerAndFit(mainBox)
        self.SetSize(self.GetBestSize())
        
    def getPlotter(self):
        return self.plotter

    def setShowLineState(self):
        if self.showLineState == {}:
            for line in self.plotter.getData():
                self.showLineState[line.getLabel()] = line.getShow()

    def setShowLineSolo(self, label):
        self.setShowLineState()
        for line in self.plotter.getData():
            if line.getLabel() == label:
                line.setShow(True)
            else:
                line.setShow(False)
        self.plotter.draw()

    def resetShow(self):
        if self.showLineState != {}:
            for line in self.plotter.getData():
                line.setShow(self.showLineState[line.getLabel()])
            self.showLineState = {}
            self.plotter.draw()
        
    def setTotalTime(self, time):
        self.plotter.setTotalTime(time)

    def createLines(self, list):
        for l in list:
            self.createLine(l[0], l[1], l[2], l[3], l[4], l[5], l[6])

    def createLine(self, points, yrange, colour, label, log, name, size):
        self.plotter.createLine(points, yrange, colour, label, log, name, size)

    def createSliderLines(self, list):
        for l in list:
            self.createSliderLine(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8])

    def createSliderLine(self, points, yrange, colour, label, log, name, size, sl, suffix):
        self.plotter.createLine(points, yrange, colour, label, log, name, size, sl, suffix)

    def OnSave(self):
        line = self.plotter.getLine(self.plotter.getSelected())
        dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), 
                            defaultFile="", style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            f = open(path, 'w')
            f.write(str(line.getLineState()))
            f.close()
        dlg.Destroy()

    def OnLoad(self):
        line = self.plotter.getLine(self.plotter.getSelected())
        dlg = wx.FileDialog(self, message="Choose a file", defaultDir=os.getcwd(), 
            defaultFile="", style=wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            f = open(path, 'r')
            state = eval(f.read())
            f.close()
            line.setLineState(state)
            self.plotter.draw()
            self.plotter.checkForHistory()
            if line.getSlider() != None:
                line.getSlider().setPlay(1)
        dlg.Destroy()

    def onReset(self):
        self.getSelected().reset()
        self.plotter.draw()

    def onShow(self, state):
        self.getSelected().setShow(state)
        self.plotter.draw()
    
    def onPopupMenu(self, ind, val):
        self.plotter.setSelected(ind)
        colour = self.getSelected().getMidColour()
        self.toolbar.menu.setBackColour(colour)
        self.getSelected().setShow(1)
        self.toolbar.toolbox.setShow(True)
        self.plotter.draw()
        self.checkForConvertSlider()

    def checkForConvertSlider(self):
        if self.getSelected().getSlider():
            if self.getSelected().getSlider().automationData != []:
                self.toolbar.convertSlider.Show()
            else:
                self.toolbar.convertSlider.Hide()
        else:
            self.toolbar.convertSlider.Hide()

    def setSelected(self, which):
        self.toolbar.menu.setByIndex(which)
        colour = self.plotter.getLine(which).getMidColour()
        self.toolbar.menu.setBackColour(colour)
        self.checkForConvertSlider()

    def getSelected(self):
        return self.plotter.getLine(self.plotter.getSelected())

    def checkForAutomation(self):
        threshold = .002

        sl = None
        if CeciliaLib.getVar("samplerSliders"):
            for slider in CeciliaLib.getVar("samplerSliders"):
                if slider.getRec():
                    sl = slider
                    slider.setAutomationLength(CeciliaLib.getControlPanel().getTime())
                    path = slider.getPath()
                    data = convert(path+"_000", slider, threshold, which=None)
                    for line in self.plotter.getData():
                        if line.getName() == slider.getCName():
                            self.setLineData(line, data)
                            line.setShow(1)
                            ind = self.plotter.getData().index(line)
                            self.plotter.setSelected(ind)
                            self.setSelected(ind)
                            slider.setRec(0)
                            slider.setPlay(1)
        if CeciliaLib.getVar("userSliders"):
            for slider in CeciliaLib.getVar("userSliders"):
                if slider.getRec():
                    slider.setAutomationLength(CeciliaLib.getControlPanel().getTime())
                    path = slider.getPath()
                    if type(slider.getValue()) not in [ListType, TupleType]:
                        data = convert(path+"_000", slider, threshold, which=None)
                        for line in self.plotter.getData():
                            if line.getName() == slider.getName():
                                self.setLineData(line, data)
                                ind = self.plotter.getData().index(line)
                                self.plotter.setSelected(ind)
                                self.setSelected(ind)
                                slider.setRec(0)
                                slider.setPlay(1)
                    else:
                        for i in range(2):
                            ends = ['min', 'max']
                            data = convert(path+"_00%d" % i, slider, threshold, which=i)
                            for line in self.plotter.getData():
                                if line.getName() == slider.getName() and line.getLabel().endswith(ends[i]):
                                    self.setLineData(line, data)
                                    ind = self.plotter.getData().index(line)
                                    self.plotter.setSelected(ind)
                                    self.setSelected(ind)
                                    slider.setRec(0)
                                    slider.setPlay(1)
        plugins = CeciliaLib.getVar("plugins")
        for plugin in plugins:
            if plugin != None:
                knobs = plugin.getKnobs()
                for slider in knobs:
                    if slider.getPath() and slider.getRec():
                        sl = slider
                        slider.setAutomationLength(CeciliaLib.getControlPanel().getTime())
                        path = slider.getPath()
                        data = convert(path+"_000", slider, threshold)
                        for line in self.plotter.getData():
                            if line.getName() == slider.getName():
                                self.setLineData(line, data)
                                line.setShow(1)
                                ind = self.plotter.getData().index(line)
                                self.plotter.setSelected(ind)
                                self.setSelected(ind)
                                slider.setRec(0)
                                slider.setPlay(1)
                                        
        
    def setLineData(self, line, data):
        yrange = line.getYrange()
        totaltime = self.plotter.getTotalTime()
        if line.getLog():
            for l in data:
                l[0] = l[0] * totaltime
                l[1] = math.pow(10, l[1] * (math.log10(yrange[1]) - math.log10(yrange[0])) + math.log10(yrange[0]))
        else:
            for l in data:
                l[0] = l[0] * totaltime
                l[1] = l[1] * (yrange[1] - yrange[0]) + yrange[0]
        line.setData(data)
        self.plotter.draw()
        self.plotter.checkForHistory()  

class ConvertSlider(PlainSlider):
    def __init__(self, parent, cecGrapher):
        PlainSlider.__init__(self, parent, 50, 2500, 200, log=True, outFunction=self.onSlider1)
        self.cecGrapher = cecGrapher
        self.threshold = .01
        
    def rescale(self):
        ends = ['min', 'max']
        if self.HasCapture():
            line = self.cecGrapher.getSelected()
            slider = line.getSlider()
            path = slider.getPath()
            if type(slider.getValue()) in [ListType, TupleType]:
                for i in range(2):
                    if line.getLabel().endswith(ends[i]):
                        path = path+"_00%d" % i
                        break
                data = convert(path, slider, self.thresh, True, which=i)
            else:
                data = convert(path, slider, self.thresh, True)                    
            self.cecGrapher.setLineData(line, data)

    def onSlider1(self, value):
        val = value * .001
        self.thresh = self.threshold * val
        self.rescale()   

def checkFunctionValidity(func, totaltime):
    for i, p in enumerate(func):
        func[i] = (p[0]*totaltime, p[1])
    if func[0][0] != 0: 
        func[0] = (0, func[0][1])
    if func[-1][0] != totaltime: 
        func[-1] = (totaltime, func[-1][1])
    oldX = -1
    for f in func:
        if f[0] < oldX:
            CeciliaLib.showErrorDialog("Error in graph function.", "Time values must be in increasing order!")
        else:
            oldX = f[0]
    return func

def checkColourValidity(col):
    if col not in COLOUR_CLASSES.keys():
        CeciliaLib.showErrorDialog('Wrong colour!', '"%s"\n\nAvailable colours for -col flag are:\n\n%s.' % (col, ', '.join(COLOUR_CLASSES.keys())))
        col = random.choice(COLOUR_CLASSES.keys())
    return col

def checkLogValidity(linlog, mini, maxi, verbose=False):
    if linlog not in ['lin', 'log']:
        if verbose:
            CeciliaLib.showErrorDialog('Error when building interface!', "'rel' argument choices are 'lin' or 'log'. Reset to 'lin'.")
        linlog = 'lin'
    log = {'lin': False, 'log': True}[linlog]
    if log and mini == 0 or log and maxi == 0:
        if verbose:
            CeciliaLib.showErrorDialog('Error when building interface!', "'min' or 'max' arguments can't be 0 for a logarithmic cgraph. Reset to 'lin'.")
        log = False
    return log
    
def buildGrapher(parent, list, totaltime):
    grapher = CECGrapher(parent, -1)
    grapher.setTotalTime(totaltime)

    widgetlist = []
    widgetlist2 = []
    widgetlist2range = []
    widgetlist2splitter = []
    widgetlist3 = []

    labelList = []

    for widget in list:
        if widget['type'] == 'cgraph':
            widgetlist.append(copy.deepcopy(widget))
        elif widget['type'] == 'cslider':
            if widget['up'] == False:
                widgetlist2.append(copy.deepcopy(widget))
        elif widget['type'] == 'crange':
            if widget['up'] == False:
                widgetlist2range.append(copy.deepcopy(widget))

    for widget in CeciliaLib.getVar("samplerSliders"):
        widgetlist3.append(widget)

    linelist = []
    for i, widget in enumerate(widgetlist):
        name = widget['name']
        label = widget['label']
        size = widget['size']
        mini = widget['min']
        maxi = widget['max']
        unit = widget['unit']
        func = widget['func']
        func = checkFunctionValidity(func, totaltime)
        linlog = widget['rel']
        log = checkLogValidity(linlog, mini, maxi, True)
        col = widget['col']
        col = checkColourValidity(col)
        colour = chooseColourFromName(col)
        labelList.append(label)
        linelist.append([func, (mini, maxi), colour, label, log, name, size])
    if linelist:
        grapher.createLines(linelist)

    linelist = []
    for i, widget in enumerate(widgetlist2):
        name = widget['name']
        mini = widget['min']
        maxi = widget['max']
        init = widget['init']
        label = widget['label']
        unit = widget['unit']
        up = widget.get('up', False)
        func = widget['func']
        if func == None:
            func = [(0, init), (1, init)]
            init_play = False
        else:
            init_play = True
        func = checkFunctionValidity(func, totaltime)
        col = widget['col']
        col = checkColourValidity(col)
        colour = chooseColourFromName(col)
        linlog = widget['rel']
        log = checkLogValidity(linlog, mini, maxi)
        for slider in CeciliaLib.getVar("userSliders"):
            if slider.getName() == name:
                slider.setFillColour(colour[1], colour[2], colour[3])
                sl = slider
                if init_play:
                    slider.setPlay(1)
                break
        labelList.append(label)
        linelist.append([func, (mini, maxi), colour, label, log, name, 8192, sl, ''])
    if linelist:
        grapher.createSliderLines(linelist)

    linelist = []
    ends = ['min', 'max']
    for i, widget in enumerate(widgetlist2range):
        for j in range(2):
            name = widget['name']
            mini = widget['min']
            maxi = widget['max']
            init = widget['init'][j]
            label = widget['label'] + ' %s' % ends[j]
            unit = widget['unit']
            func = copy.deepcopy(widget['func'][j])
            if func == None:
                func = [(0, init), (1, init)]
                init_play = False
            else:
                init_play = True
            func = checkFunctionValidity(func, totaltime)
            up = widget.get('up', False)
            col = widget.get('col', '')
            col = checkColourValidity(col)
            if up:
                colour = chooseColourFromName("grey")
            else:
                colour = chooseColourFromName(col) 
            linlog = widget['rel']
            log = checkLogValidity(linlog, mini, maxi)
            for slider in CeciliaLib.getVar("userSliders"):
                if slider.getName() == name:
                    slider.setFillColour(colour[1], colour[2], colour[3])
                    sl = slider
                    if init_play:
                        slider.setPlay(1)
                    break
            labelList.append(label)
            linelist.append([func, (mini, maxi), colour, label, log, name, 8192, sl, ends[j]])
    if linelist:
        grapher.createSliderLines(linelist)

    linelist = []
    for i, widget in enumerate(widgetlist2splitter):
        num = widget.get('num_knobs', 3)
        for j in range(num):
            name = widget['name']
            mini = widget['min']
            maxi = widget['max']
            init = widget['init'][j]
            label = widget['label'] + ' %d' % j
            unit = widget['unit']
            func = copy.deepcopy(widget['func'][j])
            if func == None:
                func = [(0, init), (1, init)]
                init_play = False
            else:
                init_play = True
            func = checkFunctionValidity(func, totaltime)
            up = widget.get('up', False)
            col = widget.get('col', '')
            col = checkColourValidity(col)
            if up:
                colour = chooseColourFromName("grey")
            else:
                colour = chooseColourFromName(col) 
            linlog = widget['rel']
            log = checkLogValidity(linlog, mini, maxi)
            for slider in CeciliaLib.getVar("userSliders"):
                if slider.getName() == name:
                    slider.setFillColour(colour[1], colour[2], colour[3])
                    sl = slider
                    if init_play:
                        slider.setPlay(1)
                    break
            labelList.append(label)
            linelist.append([func, (mini, maxi), colour, label, log, name, 8192, sl, "_%d" % j])
    if linelist:
        grapher.createSliderLines(linelist)

    linelist = []
    samplerSliderNames = []
    for i, widget in enumerate(widgetlist3):
        colour = chooseColour(5, 5)
        mini = widget.slider.getRange()[0]
        maxi = widget.slider.getRange()[1]
        init = widget.slider.getInit()
        func = [(0, init), (1, init)]
        func = checkFunctionValidity(func, totaltime)
        label = widget.getLabel()
        unit = ''
        log = False
        name = widget.getCName()
        for slider in CeciliaLib.getVar("samplerSliders"):
            samplerSliderNames.append(slider.getCName())
            if slider.getCName() == name:
                sl = slider
                break
        labelList.append(label)
        linelist.append([func, (mini, maxi), colour, label, log, name, 8192, sl, ''])
    if linelist:
        grapher.createSliderLines(linelist)

    if len(grapher.plotter.getData()) == 0:
        grapher.createLine([[0, 0], [totaltime, 0]], (0, 1), "#FFFFFF", 'unused', False, 'unused', 8192)
        labelList.append('unused')
        
    for line in grapher.plotter.getData():
        if line.getName() in samplerSliderNames:
            line.setShow(0)

    checkLineShow = [line.getShow() for line in grapher.plotter.getData()]
    if 1 not in checkLineShow:
        grapher.plotter.getData()[0].setShow(1)

    grapher.toolbar.setPopupChoice(labelList)
    grapher.plotter.drawCursor(0)
    return grapher

def convert(path, slider, threshold, fromSlider=False, which=None):
    if not fromSlider:
        f = open(path, 'r')
        data = f.read().split('\n')
        data = [x.split()[1] for x in data if x != '']
        data = [float(x) for x in data if x != '']
        f.close()
        if which != None:
            slider.setAutomationData(data, which)
        else:
            slider.setAutomationData(data)

    if which != None:
        temp = slider.getAutomationData(which)
    else:    
        temp = slider.getAutomationData()

    maxval = slider.getMaxValue()
    points = reducePoints(temp, threshold)
    return points

