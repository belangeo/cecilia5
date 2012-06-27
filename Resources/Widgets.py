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

import wx, sys, math, os, random, time, copy, webbrowser
import wx.richtext as rt
from constants import *
import CeciliaLib as CeciliaLib
from types import ListType
from Drunk import *
import wx.lib.scrolledpanel as scrolled

def interpFloat(t, v1, v2):
    "interpolator for a single value; interprets t in [0-1] between v1 and v2"
    return (v2-v1)*t + v1

def tFromValue(value, v1, v2):
    "returns a t (in range 0-1) given a value in the range v1 to v2"
    return float(value-v1)/(v2-v1)

def clamp(v, minv, maxv):
    "clamps a value within a range"
    if v<minv: v=minv
    if v> maxv: v=maxv
    return v

def toLog(t, v1, v2):
    return math.log10(t/v1) / math.log10(v2/v1)

def toExp(t, v1, v2):
    return math.pow(10, t * (math.log10(v2) - math.log10(v1)) + math.log10(v1))

def GetRoundBitmap( w, h, r ):
    maskColor = wx.Colour(0,0,0)
    shownColor = wx.Colour(5,5,5)
    b = wx.EmptyBitmap(w,h)
    dc = wx.MemoryDC(b)
    dc.SetBrush(wx.Brush(maskColor))
    dc.DrawRectangle(0,0,w,h)
    dc.SetBrush(wx.Brush(shownColor))
    dc.SetPen(wx.Pen(shownColor))
    dc.DrawRoundedRectangle(0,0,w,h,r)
    dc.SelectObject(wx.NullBitmap)
    b.SetMaskColour(maskColor)
    return b

def GetRoundShape( w, h, r ):
    return wx.RegionFromBitmap( GetRoundBitmap(w,h,r) )

#---------------------------
# Popup menu
# outFunction return (index, value as string)
# --------------------------
class CustomMenu(wx.Panel):
    def __init__(self, parent, choice=[], init='', size=(100,20), outFunction=None, colour=None, maxChar=None, columns=1):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self._backgroundColour = BACKGROUND_COLOUR
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.closed = True
        self._enable = True
        self.maxChar = maxChar
        self.columns = columns
        self.outFunction = outFunction
        self.choice = choice
        self.choice = [str(choice) for choice in self.choice]
        if str(init) in self.choice:
            self.setLabel(str(init))
        elif len(self.choice) > 0:
            self.setLabel(self.choice[0])
        else:
            self.setLabel('')
        if colour:
            self.backColour = colour
        else:
            self.backColour = POPUP_BACK_COLOUR

    def setBackgroundColour(self, col):
        self._backgroundColour = col
        self.SetBackgroundColour(col)
        self.Refresh()

    def setBackColour(self, colour):
        self.backColour = colour
        self.Refresh()

    def setEnable(self, enable):
        self._enable = enable
        self.Refresh()

    def setChoice(self, choice, out=True):
        self.choice = choice
        self.setLabel(self.choice[0], out)
        self.Refresh()

    def getChoice(self):
        return self.choice
        
    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(self._backgroundColour, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(self._backgroundColour, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        rec = wx.Rect(0, 0, w, h)
        dc.SetBrush(wx.Brush(self.backColour))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        dc.DrawRoundedRectangleRect(rec, 3)

        font = wx.Font(MENU_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
        dc.SetFont(font)
        if self._enable:
            dc.SetBrush(wx.Brush(POPUP_LABEL_COLOUR, wx.SOLID))
            dc.SetPen(wx.Pen(POPUP_LABEL_COLOUR, width=1, style=wx.SOLID))  
            dc.SetTextForeground(POPUP_LABEL_COLOUR)
        else:    
            dc.SetBrush(wx.Brush(POPUP_DISABLE_LABEL_COLOUR, wx.SOLID))
            dc.SetPen(wx.Pen(POPUP_DISABLE_LABEL_COLOUR, width=1, style=wx.SOLID))  
            dc.SetTextForeground(POPUP_DISABLE_LABEL_COLOUR)
        if self.maxChar == None:
            dc.DrawLabel(self.label, wx.Rect(5, 0, w, h), wx.ALIGN_CENTER_VERTICAL)
        else:
            dc.DrawLabel(CeciliaLib.shortenName(self.label, self.maxChar), wx.Rect(5, 0, w, h), wx.ALIGN_CENTER_VERTICAL)
        if self.closed:
            dc.DrawPolygon([wx.Point(w-13,h/2), wx.Point(w-7,6), wx.Point(w-7,h-6)])
        else:
            dc.DrawPolygon([(w-13,6), (w-7,6), (w-10,h-6)])

    def MouseDown(self, event):
        if self._enable:
            off = wx.GetMousePosition()
            pos = (off[0]+10, off[1]+10)
            f = MenuFrame(self, pos, self.GetSize()[0], self.choice, self.columns)
            self.closed = False
            self.Refresh()

    def setLabel(self, label, out=False):
        self.label = label
        if self.outFunction and self.label != '' and out:
            self.outFunction(self.choice.index(self.label), self.label)
        self.Refresh()

    def setByIndex(self, ind, out=False):
        self.setLabel(self.choice[ind], out)

    def getLabel(self):
        return self.label

    def getIndex(self):
        return self.choice.index(self.label)

    def setClosed(self):
        self.closed = True
        self.Refresh()
    
    def setStringSelection(self, selection):
        if selection in self.choice:
            self.setLabel(selection)
        
class MenuFrame(wx.Frame):
    def __init__(self, parent, pos, xsize, choice, columns=1):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR |
                  wx.NO_BORDER | wx.FRAME_SHAPED | wx.FRAME_FLOAT_ON_PARENT)
        wx.Frame.__init__(self, parent, title='', pos=pos, style = style)
        self.parent = parent
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.closable = False
        self.choice = choice
        self.rects = []
        if columns == 1:
            self.xsize = xsize
            for i in range(len(self.choice)):
                self.rects.append(wx.Rect(2, i*20+2, xsize-4, 20))
            self.height = len(self.choice) * 20 + 10
        else:
            self.xsize = columns * 50
            rows = len(self.choice) / columns
            for j in range(columns):
                for i in range(rows):
                    self.rects.append(wx.Rect(2+(j*50), i*20+2, 46, 20))
            self.height = rows * 20 + 10
        dispSize = wx.GetDisplaySize()
        if pos[1] + self.height > dispSize[1]:
            self.SetPosition((pos[0], pos[1] - self.height))
        self.which = None

        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        if wx.Platform == '__WXGTK__':
            self.SetMinSize((self.xsize, self.height))
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()

        self.SetSize((self.xsize, self.height))
        self.closable = True
        t = wx.CallLater(1000, self.close)
        self.Show(True)

    def SetRoundShape(self, event=None):
        self.SetShape(GetRoundShape(self.xsize, self.height, 5))

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        w, h = self.GetSizeTuple()
        dc.SetPen( wx.Pen(POPUP_BORDER_COLOUR, width = 2))
        dc.SetBrush( wx.Brush(BACKGROUND_COLOUR))
        dc.DrawRoundedRectangle( 0,0,w,h,3)
        font = wx.Font(MENU_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
        dc.SetFont(font)
        for i in range(len(self.choice)):
            if self.which != None:
                if self.which == i:
                    dc.SetPen( wx.Pen(POPUP_HIGHLIGHT_COLOR))
                    dc.SetBrush( wx.Brush(POPUP_HIGHLIGHT_COLOR))
                    dc.DrawRoundedRectangleRect(self.rects[self.which], 3)
            dc.SetPen( wx.Pen(POPUP_TEXT_COLOUR, width = 1))
            dc.DrawText(self.choice[i], self.rects[i].GetLeft()+5, self.rects[i].GetTop()+4)

    def MouseDown(self, event):
        pos = event.GetPosition()
        for rec in self.rects:
            if rec.Contains(pos):
                self.which = self.rects.index(rec)
                break
        self.parent.setClosed()
        win = wx.FindWindowAtPointer()
        if win != None:
            win = win.GetTopLevelParent()
            if win in [CeciliaLib.getVar("mainFrame"), CeciliaLib.getVar("interface")]:
                win.Raise()
        try:
            self.parent.setLabel(self.choice[self.which], True)
            self.Close(force=True)
        except:
            pass

    def OnMotion(self, event):
        pos = event.GetPosition()
        for rec in self.rects:
            if rec.Contains(pos):
                self.which = self.rects.index(rec)
                break
        self.Refresh()
        event.Skip()

    def OnEnter(self, event):
        self.closable = False

    def OnLeave(self, event):
        toclose = False
        if self.which == None:
            toclose = True
        else:
            if self.choice[self.which] != 'Custom...':
                toclose = True

        if toclose:
            self.closable = True
            t = wx.CallLater(1000, self.close)

    def close(self):
        if self.closable:
            self.parent.setClosed()
            self.Close(force=True)

class MySoundfileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        if os.path.isfile(filenames[0]):
            self.window.parent.updateMenuFromPath(filenames[0])
        elif os.path.isdir(filenames[0]):
            self.window.parent.updateMenuFromPath(filenames[0])
        else:
            pass

class FolderPopup(wx.Panel):
    def __init__(self, parent, path=None, init='', outFunction=None, emptyFunction=None, backColour=None, tooltip=''):
        wx.Panel.__init__(self, parent, -1, size=(130,20))
        self.parent = parent
        drop = MySoundfileDropTarget(self)
        self.SetDropTarget(drop)
        self.SetMaxSize((130,20))
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.backColour = backColour
        self.closed = True
        self.outFunction = outFunction
        self.emptyFunction = emptyFunction
        self.tooltip = tooltip
        self.tip = wx.ToolTip(self.tooltip)
        self.SetToolTip(self.tip) 
        self.choice = []
        
        if init in self.choice:
            self.setLabel(init)
        elif len(self.choice) > 0:
            self.setLabel(self.choice[0])
        else:
            self.setLabel('')

    def reset(self):
        self.choice = []
        self.setLabel('')
        self.Refresh()
        
    def setChoice(self, choice):
        self.choice = choice
        
    def setLabel(self, label):
        try:
            self.label = label
            if self.outFunction and self.label != '':
                self.outFunction(self.choice.index(self.label), self.label)
        except:
            self.label = label
            if self.outFunction and self.label != '':
                self.outFunction(0, self.label)
        if CeciliaLib.getVar("useTooltips") and self.label != '':
            self.tip.SetTip(self.tooltip + '\n\nCurrent choice:\n' + self.label)
        elif CeciliaLib.getVar("useTooltips"):
            self.tip.SetTip(self.tooltip)
        else:
            self.tip.SetTip(self.label) 
        self.Refresh()
        
    def setByIndex(self, ind):
        self.label = self.choice[ind]
        self.Refresh()
        
    def setBackColour(self, colour):
        self.backColour = colour
        self.Refresh()
        
    def setClosed(self):
        self.closed = True
        self.Refresh()
        
    def MouseDown(self, event):
        off = self.GetScreenPosition()
        pos = (off[0]+10, off[1]+10)
        if self.choice != []:
            f = FolderMenuFrame(self, pos, self.choice, self.label)
            self.closed = False
            self.Refresh()
        else:
            if self.emptyFunction:
                self.emptyFunction()
        
    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        if self.backColour: backColour = self.backColour
        else: backColour = POPUP_BACK_COLOUR 

        rec = wx.Rect(0, 0, w, h)
        dc.SetBrush(wx.Brush(backColour))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        dc.DrawRoundedRectangleRect(rec, 3)

        font = wx.Font(MENU_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
        dc.SetFont(font)
        dc.SetBrush(wx.Brush(POPUP_LABEL_COLOUR, wx.SOLID))
        dc.SetPen(wx.Pen(POPUP_LABEL_COLOUR, width=1, style=wx.SOLID))  
        dc.SetTextForeground(POPUP_LABEL_COLOUR)
        dc.DrawLabel(CeciliaLib.shortenName(self.label,19), wx.Rect(5, 0, w, h), wx.ALIGN_CENTER_VERTICAL)
        if self.closed:
            dc.DrawPolygon([wx.Point(w-13,h/2), wx.Point(w-7,6), wx.Point(w-7,h-6)])
        else:
            dc.DrawPolygon([(w-13,6), (w-7,6), (w-10,h-6)])
   
class FolderMenuFrame(wx.Frame):
    def __init__(self, parent, pos, choice, label=''):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.NO_BORDER | wx.FRAME_SHAPED  )
        wx.Frame.__init__(self, parent, title='', pos=pos, style = style)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.maxCol = 3
        self.maxRow = 10
        self.colWidth = 200
        self.parent = parent
        self.choice = choice
        self.arrowOver = None
        
        # Create pages for the menu
        self.pages = []
        self.currPage = 0
        numPages = len(self.choice)/float((self.maxCol*self.maxRow))
        if len(self.choice)%float((self.maxCol*self.maxRow)) != 0:
            numPages += 1
        numPages = int(numPages)
        for i in range(numPages):
            inpage = self.choice[i*self.maxCol*self.maxRow:self.maxCol*self.maxRow*(i+1)]
            self.pages.append(inpage)
            if CeciliaLib.ensureNFD(label) in inpage:
                self.currPage = i
        
        self.defineSize()
        self.defineArrows() 
        self.showArrows()
        self.buildRects()
        self.which = None

        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()

        self.Show(True)
        
    def defineArrows(self):
        self.leftArrow = [(self.width-100, self.height-9),
                        (self.width-93, self.height-5),
                        (self.width-93, self.height-13)]

        self.rightArrow = [(self.width-17, self.height-13),
                          (self.width-10, self.height-9),
                          (self.width-17, self.height-5)]

    def showArrows(self):
        if self.currPage!=0:
            self.showLeftArrow = True
        else:
            self.showLeftArrow = False
        
        if self.currPage+1 < len(self.pages):
            self.showRightArrow = True
        else:
            self.showRightArrow =False
        
    def buildRects(self):
        self.rects = []
        for i in range(len(self.pages[self.currPage])):
            col = i/self.maxRow
            x = 2 + (self.colWidth*col)
            y = (i-(self.maxRow*col))*20+2
            self.rects.append(wx.Rect(x, y, self.colWidth-3, 20))

        self.arrows = []
        self.arrows.append(wx.Rect(self.leftArrow[1][0]-10,self.leftArrow[1][1]-10, 15, 15))
        self.arrows.append(wx.Rect(self.rightArrow[1][0]-10,self.rightArrow[1][1]-10, 15, 15))
    
    def defineSize(self):
        cols = len(self.pages[0])/self.maxRow
        if len(self.pages[0])%self.maxRow != 0:
            cols += 1
        self.width = cols*self.colWidth+cols*10
        
        if len(self.pages[0])>self.maxRow:
            self.height = self.maxRow * 20 + 25
        else:
            self.height = len(self.pages[0]) * 20 + 25
        self.SetMinSize((self.width, self.height))
        self.SetSize((self.width, self.height))

    def changePageUp(self):
        self.currPage += 1
        if self.currPage >= len(self.pages):
            self.currPage = len(self.pages)-1
            return
        self.defineSize()
        self.defineArrows()
        self.showArrows()
        self.buildRects()
        self.Refresh()
    
    def changePageDown(self):
        self.currPage -= 1
        if self.currPage<0:
            self.currPage = 0
            return
        self.defineSize()
        self.defineArrows()
        self.showArrows()
        self.buildRects()
        self.Refresh()

    def SetRoundShape(self, event=None):
        w, h = self.GetSizeTuple()
        self.SetShape(GetRoundShape(self.width, self.height, 5))

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        w, h = self.GetSizeTuple()
        dc.SetPen( wx.Pen(POPUP_BORDER_COLOUR, width = 2))
        dc.SetBrush( wx.Brush(BACKGROUND_COLOUR))
        dc.DrawRoundedRectangle( 0,0,w,h,3)
        font = wx.Font(FOLDER_MENU_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
        dc.SetFont(font)
        for i in range(len(self.pages[self.currPage])):
            col = i/self.maxRow
            if self.which != None:
                if self.which == i:
                    dc.SetPen( wx.Pen(POPUP_HIGHLIGHT_COLOR))
                    dc.SetBrush( wx.Brush(POPUP_HIGHLIGHT_COLOR))
                    dc.DrawRoundedRectangleRect(self.rects[self.which], 3)
            dc.SetPen( wx.Pen(POPUP_TEXT_COLOUR, width = 1))
            x = 5 + (self.colWidth*col)
            y = (i-(self.maxRow*col))*20+2
            dc.DrawText(CeciliaLib.shortenName(self.pages[self.currPage][i],35), x, y)
            
        dc.SetTextForeground(POPUP_PAGETEXT_COLOR)
        if len(self.pages)>1:
            if CeciliaLib.getVar("systemPlatform") == "win32":
                dc.DrawText('Page %d of %d' % (self.currPage+1,len(self.pages)), w-83, h-17)
            else:
                dc.DrawText('Page %d of %d' % (self.currPage+1,len(self.pages)), w-83, h-15)
        if self.showLeftArrow:
            if self.arrowOver==0:
                dc.SetPen( wx.Pen(POPUP_PAGEARROW_COLOR_OVER))
                dc.SetBrush( wx.Brush(POPUP_PAGEARROW_COLOR_OVER))
            else:
                dc.SetPen( wx.Pen(POPUP_PAGEARROW_COLOR))
                dc.SetBrush( wx.Brush(POPUP_PAGEARROW_COLOR))
            dc.DrawPolygon(self.leftArrow)
        if self.showRightArrow:
            if self.arrowOver==1:
                dc.SetPen( wx.Pen(POPUP_PAGEARROW_COLOR_OVER))
                dc.SetBrush( wx.Brush(POPUP_PAGEARROW_COLOR_OVER))
            else:
                dc.SetPen( wx.Pen(POPUP_PAGEARROW_COLOR))
                dc.SetBrush( wx.Brush(POPUP_PAGEARROW_COLOR))
            dc.DrawPolygon(self.rightArrow)

    def MouseDown(self, event):
        pos = event.GetPosition()
        isPageChange = False
        isLabelSelect = False
        for rec in self.rects:
            if rec.Contains(pos):
                self.which = self.rects.index(rec)
                isLabelSelect = True
                break
            
        for rec in self.arrows:
            if rec.Contains(pos):
                self.arrowOver = self.arrows.index(rec)
                isPageChange = True
                break
            
        if isLabelSelect:
            self.parent.setLabel(self.pages[self.currPage][self.which])
            self.parent.setClosed()
            self.Close(force=True)
            
        if isPageChange:
            if self.arrowOver==0:
                self.changePageDown()
            if self.arrowOver==1:
                self.changePageUp()

    def OnEnter(self, event):
        self.closable = False
    
    def OnLeave(self, event):
        self.closable = True
        t = wx.CallLater(1000, self.close)

    def close(self):
        if self.closable:
            self.parent.setClosed()
            self.Close(force=True)
 
    def OnMotion(self, event): #Mod
        pos = event.GetPosition()
        for rec in self.rects:
            if rec.Contains(pos):
                self.which = self.rects.index(rec)
                self.arrowOver = None
                break
            else:
                self.which = None
                self.arrowOver = None
        if not self.which:
            for rec in self.arrows:
                if rec.Contains(pos):
                    self.which = None
                    self.arrowOver = self.arrows.index(rec)
                    break
                else:
                    self.which = None
                    self.arrowOver = None
        
        self.Refresh()
        event.Skip()

#---------------------------
# Label (immutable)
# --------------------------
class MainLabel(wx.Panel):
    def __init__(self, parent, label, size=(100,20), font=None, colour=None, outFunction=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.label = label
        self.italic = False
        self.font = font
        if colour:
            self.colour = colour
        else:
            self.colour = LABEL_BACK_COLOUR
        self.outFunction = outFunction
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def setBackColour(self, colour):
        self.colour = colour
        self.Refresh()
    
    def setLabel(self, label):
        self.italic = False
        self.label = label
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.PaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        if self.font:
            dc.SetFont(self.font)
        else:
            if self.italic:
                font = wx.Font(LABEL_FONT, wx.NORMAL, wx.ITALIC, wx.LIGHT, face=FONT_FACE)
                dc.SetFont(font)
            else:
                font = wx.Font(LABEL_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
                dc.SetFont(font)

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        rec = wx.Rect(0, 0, w, h)
        dc.SetBrush(wx.Brush(self.colour))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        dc.DrawRoundedRectangleRect(rec, 3)
        dc.SetTextForeground(LABEL_LABEL_COLOUR)
        dc.DrawLabel(self.label, wx.Rect(0, 1, w-5, h-1), wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        
    def setItalicLabel(self, label):
        self.italic = True
        self.label = label
        self.Refresh()
        
    def getLabel(self):
        return self.label

class Label(MainLabel):
    def __init__(self, parent, label, size=(100,20), font=None, colour=None, outFunction=None):
        MainLabel.__init__(self, parent=parent, label=label, size=size, font=font, colour=colour, outFunction=outFunction)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        
    def OnLeftDown(self, event):
        xsize = self.GetSize()[0]
        xpos = event.GetPosition()[0]
        if xpos < (xsize/2):
            side = 'left'
        else:
            side = 'right'    
        if self.outFunction:
            if event.ShiftDown():
                self.outFunction(self.label, True, side=side)
            else:
                self.outFunction(self.label, side=side)

    def OnRightDown(self, event):
        xsize = self.GetSize()[0]
        xpos = event.GetPosition()[0]
        if xpos < (xsize/2):
            side = 'left'
        else:
            side = 'right'    
        if self.outFunction and not CeciliaLib.getVar("audioServer").isAudioServerRunning():
            if event.ShiftDown():        
                self.outFunction(self.label, True, True, side=side)                
            else:
                self.outFunction(self.label, alt=True, side=side)    

class OutputLabel(MainLabel):
    def __init__(self, parent, label, size=(100,20), font=None, colour=None, outFunction=None):
        MainLabel.__init__(self, parent=parent, label=label, size=size, font=font, colour=colour, outFunction=outFunction)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

    def OnLeftDown(self, event):
        if self.outFunction:
            self.outFunction()
        
class PeakLabel(MainLabel):
    def __init__(self, parent, label, size=(100,20), font=None, colour=None, gainSlider=None):
        MainLabel.__init__(self, parent=parent, label=label, size=size, font=font, colour=colour)
        self.gainSlider = gainSlider
        self.shiftDown = False
        self.canCmdClick = True        

        self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.onClick)
        
    def onDoubleClick(self, evt):
        self.setLabel('-90.00 dB')
        CeciliaLib.getControlPanel().resetVuMeter()
        
    def onClick(self, evt):
        if evt.CmdDown() and self.canCmdClick:
            try:
                mod = eval(self.getLabel().strip('+ dB'))*-1
                self.gainSlider.SetValue(self.gainSlider.GetValue()+mod)
                self.canCmdClick = False
            except:
                return
            
    def setLabel(self, label):
        self.italic = False
        self.label = label
        self.canCmdClick = True
        self.Refresh()

class FrameLabel(wx.Panel):
    def __init__(self, parent, label, size=(100,20), font=None, colour=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.label = label
        self.font = font
        if colour:
            self.colour = colour
        else:
            self.colour = TITLE_BACK_COLOUR
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
       
    def setBackColour(self, colour):
        self.colour = colour
        self.Refresh()
    
    def setLabel(self, label):
        self.label = label
        self.Refresh()

    def MouseDown(self, event):
        self.pos = event.GetPosition()
        self.CaptureMouse()
        event.Skip()

    def MouseUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        event.Skip()

    def OnMotion(self, event):
        if self.HasCapture():
            screenPos = wx.GetMousePosition()
            newPos = [screenPos[0]-self.pos[0], screenPos[1]-self.pos[1]]
            if newPos[0] < 0: newPos[0] = 0
            if newPos[1] < 0: newPos[1] = 0
            self.GetParent().GetParent().SetPosition(newPos)

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.PaintDC(self)

        dc.SetBrush(wx.Brush(TITLE_BACK_COLOUR, wx.SOLID))
        dc.Clear()

        if self.font:
            dc.SetFont(self.font)
        else:
            font = wx.Font(LABEL_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
            dc.SetFont(font)

        # Draw background
        dc.SetPen(wx.Pen(WHITE_COLOUR, width=1, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        rec = wx.Rect(0, 0, w-5, h)
        dc.SetTextForeground(LABEL_LABEL_COLOUR)
        if sys.platform == 'win32':
            dc.DrawLabel(self.label, rec, wx.ALIGN_CENTER)
        else:
            dc.DrawLabel(self.label, rec, wx.ALIGN_CENTER)

class AboutLabel(wx.Panel):
    def __init__(self, parent, version, copyright, size=(600,80), font=None, colour=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.version = version
        self.copyright = copyright
        self.font = font
        if colour:
            self.colour = colour
        else:
            self.colour = TITLE_BACK_COLOUR
        self.img_side = 70    
        self.bit = ICON_CECILIA_ABOUT_SMALL.GetBitmap()
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def setBackColour(self, colour):
        self.colour = colour
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.PaintDC(self)

        dc.SetBrush(wx.Brush(TITLE_BACK_COLOUR, wx.SOLID))
        dc.Clear()

        if self.font:
            dc.SetFont(self.font)
        else:
            font = wx.Font(LABEL_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
            dc.SetFont(font)

        # Draw background
        dc.SetPen(wx.Pen(WHITE_COLOUR, width=1, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        dc.DrawBitmap(self.bit, w/2-self.img_side/2, h/2-self.img_side/2)
        dc.SetBrush(wx.Brush(TITLE_BACK_COLOUR, wx.TRANSPARENT))
        dc.SetPen(wx.Pen(TITLE_BACK_COLOUR, width=3, style=wx.SOLID))
        dc.DrawCircle(w/2, h/2,self.img_side/2-1)
        
        dc.SetTextForeground(LABEL_LABEL_COLOUR)
        rec = wx.Rect(5, 68, 50, 10)
        dc.DrawLabel(self.copyright, rec, wx.ALIGN_CENTER)
        rec = wx.Rect(545, 68, 50, 10)
        dc.DrawLabel(self.version, rec, wx.ALIGN_CENTER)

#---------------------------
# Toggle (return 0 or 1)
# --------------------------
class Toggle(wx.Panel):
    def __init__(self, parent, state, size=(20,20), outFunction=None, colour=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.outFunction = outFunction
        self.state = state
        if colour:
            self.colour = colour
        else:
            self.colour = POPUP_BACK_COLOUR
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        dc.SetBrush(wx.Brush(self.colour, wx.SOLID))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1, style=wx.SOLID))  
        rec = wx.Rect(0, 0, w, h)
        dc.DrawRoundedRectangleRect(rec, 3)
        dc.SetTextForeground(TOGGLE_LABEL_COLOUR)
        if self.state: label = 'X'
        else: label = ''
        dc.DrawLabel(label, wx.Rect(0, 0, w, h), wx.ALIGN_CENTER)
        if self.outFunction:
            self.outFunction(self.state)

    def MouseDown(self, event):
        if self.state: self.state = 0
        else: self.state = 1
        self.Refresh()
        event.Skip()

    def getValue(self):
        return self.state
    
    def setValue(self, value):
        self.state = value
        self.Refresh()

#---------------------------
# Xfade switcher (return 0, 1 or 2)
# --------------------------
class XfadeSwitcher(wx.Panel):
    def __init__(self, parent, state, size=(20,20), outFunction=None, colour=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.outFunction = outFunction
        self.state = state
        if colour:
            self.colour = colour
        else:
            self.colour = POPUP_BACK_COLOUR

        self.bitmaps = [ICON_XFADE_LINEAR.GetBitmap(), ICON_XFADE_POWER.GetBitmap(), ICON_XFADE_SIGMOID.GetBitmap()]
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        dc.SetBrush(wx.Brush(self.colour, wx.SOLID))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1, style=wx.SOLID))  
        rec = wx.Rect(0, 0, w, h)
        dc.DrawRoundedRectangleRect(rec, 3)
        dc.SetPen(wx.Pen(TOGGLE_LABEL_COLOUR, width=1, style=wx.SOLID))  
        dc.DrawBitmap(self.bitmaps[self.state], 3, 3, True)
        if self.outFunction:
            self.outFunction(self.state)

    def MouseDown(self, event):
        self.state = (self.state+1) % 3
        self.Refresh()
        event.Skip()

    def getValue(self):
        return self.state

    def setValue(self, value):
        self.state = value
        self.Refresh()

#---------------------------
# Button (send a trigger)
# --------------------------
class Button(wx.Panel):
    def __init__(self, parent, size=(20,20), outFunction=None, colour=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.state = False
        self.outFunction = outFunction
        if colour:
            self.colour = colour[0]
            self.pushColour = '#222222' #colour[1]
        else:
            self.colour = POPUP_BACK_COLOUR
            self.pushColour = '#222222'
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        if not self.state:
            dc.SetBrush(wx.Brush(self.colour, wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(self.pushColour, wx.SOLID))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1, style=wx.SOLID))  
        rec = wx.Rect(0, 0, w, h)
        dc.DrawRoundedRectangleRect(rec, 9)

    def MouseDown(self, event):
        self.state = True
        if self.outFunction:
            self.outFunction(1)
        self.Refresh()
        event.Skip()

    def MouseUp(self, event):
        self.state = False
        if self.outFunction:
            self.outFunction(0)
        self.Refresh()
        event.Skip()

#---------------------------
# MinMaxToggle (return 0 or 1)
# --------------------------
class MinMaxToggle(wx.Panel):
    def __init__(self, parent, state, size=(20,20), outFunction=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(TITLE_BACK_COLOUR)
        self.outFunction = outFunction
        self.state = state
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.SetToolTip(CECTooltip(TT_EDITOR_SHOW))
        
    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(TITLE_BACK_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(TITLE_BACK_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        dc.SetPen(wx.Pen(WHITE_COLOUR, width=0, style=wx.SOLID))
        dc.SetBrush(wx.Brush(WHITE_COLOUR, style=wx.SOLID))

        if self.state: 
            dc.DrawPolygon([[5, 4], [5, h-6], [w-5, h/2-1]])
        else:
            dc.DrawPolygon([[5, 5], [w-5, 5], [w/2, h-6]])

    def MouseDown(self, event):
        if self.state: self.state = 0
        else: self.state = 1
        if self.outFunction:
            self.outFunction(self.state)
        self.Refresh()
        event.Skip()

    def SetValue(self, value):
        self.state = value
        self.Refresh()

    def GetValue(self):
        return self.state

#---------------------------
# Clocker (immutable)
# --------------------------
class Clocker(wx.Panel):
    def __init__(self, parent, size=(80,24), backgroundColour=None, borderColour=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetMaxSize(self.GetSize())
        if backgroundColour: self.backgroundColour = backgroundColour
        else: self.backgroundColour = TITLE_BACK_COLOUR
        self.SetBackgroundColour(self.backgroundColour)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        if borderColour: self.borderColour = borderColour
        else: self.borderColour = WIDGET_BORDER_COLOUR
        self.time = '00:00:00'
        self.font = wx.Font(CLOCKER_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE)
        self.colour = CONTROLSLIDER_BACK_COLOUR
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.createBackgroundBitmap()
        self.SetToolTip(CECTooltip(TT_CLOCK))

    def createBackgroundBitmap(self):
        w, h = self.GetSize()
        self.backgroundBitmap = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(self.backgroundBitmap)
        dc.SetBrush(wx.Brush(self.backgroundColour, wx.SOLID))

        # Draw background
        dc.SetPen(wx.Pen(self.backgroundColour, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        rec = wx.Rect(0, 0, w, h)
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        dc.SetBrush(wx.Brush(CONTROLLABEL_BACK_COLOUR))
        dc.DrawRoundedRectangleRect(rec, 4)
        dc.SelectObject(wx.NullBitmap)

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.Clear()
        dc.DrawBitmap(self.backgroundBitmap, 0, 0)

        dc.SetFont(self.font)
        dc.SetTextForeground(LABEL_LABEL_COLOUR)
        dc.DrawLabel(self.time, wx.Rect(0, 0, w, h), wx.ALIGN_CENTER)

    def setTime(self, m ,s, c):
        self.time = '%02d:%02d:%02d' % (m, s, c)
        self.Refresh()

#---------------------------
# EntryUnit
# --------------------------
class EntryUnit(wx.Panel):
    def __init__(self, parent, value=0, unit='', size=(130,20), valtype='float', outFunction=None, colour=None):
        wx.Panel.__init__(self, parent, -1, size=size, style=wx.WANTS_CHARS)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.value = value
        self.unit = unit
        self.valtype = valtype
        self.outFunction = outFunction
        self.selected = False
        self.clickPos = None
        self.oldValue = value
        self.increment = 0.001
        self.new = ''
        self.font = wx.Font(ENTRYUNIT_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
        self.unitFont = wx.Font(ENTRYUNIT_FONT, wx.ROMAN, wx.ITALIC, wx.LIGHT, face=FONT_FACE)
        self.entryRect = wx.Rect(45, 1, 52, self.GetSize()[1]-2)
        if CeciliaLib.getVar("systemPlatform") == 'win32':
            self.starttext = 65
        else:    
            self.starttext = 95
        if colour:
            self.backColour = colour
        else:
            self.backColour = ENTRYUNIT_BACK_COLOUR
        self.createBackgroundBitmap()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        self.Bind(wx.EVT_KILL_FOCUS, self.LooseFocus)

    def createBackgroundBitmap(self):
        w, h = self.GetSize()
        self.backgroundBitmap = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(self.backgroundBitmap)
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.SetTextForeground(LABEL_LABEL_COLOUR)

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        rec = wx.Rect(0, 0, w, h)
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        dc.SetBrush(wx.Brush(self.backColour))
        dc.DrawRoundedRectangleRect(rec, 3)

        # Draw triangle
        dc.SetPen(wx.Pen(LABEL_LABEL_COLOUR, width=1, style=wx.SOLID))  
        dc.SetBrush(wx.Brush(LABEL_LABEL_COLOUR, wx.SOLID))
        dc.DrawPolygon([wx.Point(12,h/2), wx.Point(7,5), wx.Point(7,h-5)])

        # Draw unit
        dc.SetFont(self.unitFont)
        dc.DrawLabel(self.unit, wx.Rect(105, 0, w-105, h), wx.ALIGN_CENTER_VERTICAL)
        dc.SelectObject(wx.NullBitmap)

    def setBackColour(self, colour):
        self.backColour = colour
        self.createBackgroundBitmap()
        self.Refresh()

    def LooseFocus(self, event):
        if self.new != '':
            self.value = eval(self.new)
        self.new = ''
        self.selected = False
        if self.outFunction:
            self.outFunction(self.value)
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        dc.SetTextForeground(LABEL_LABEL_COLOUR)
        dc.DrawBitmap(self.backgroundBitmap, 0, 0)

        # Draw value
        dc.SetFont(self.font)
        if self.selected:
            dc.SetPen(wx.Pen(ENTRYUNIT_HIGHLIGHT_COLOUR, width=1, style=wx.SOLID))  
            dc.SetBrush(wx.Brush(ENTRYUNIT_HIGHLIGHT_COLOUR, wx.SOLID))
            dc.DrawRoundedRectangleRect(self.entryRect, 3)
        dc.SetPen(wx.Pen(LABEL_LABEL_COLOUR, width=1, style=wx.SOLID))  
        dc.SetBrush(wx.Brush(LABEL_LABEL_COLOUR, wx.SOLID))
        if self.selected and self.new:
            val = self.new
        else:
            val = str(self.value)
        if CeciliaLib.getVar("systemPlatform") == 'linux2':
            width = len(val) * (dc.GetCharWidth() - 1)
        else:
            width = len(val) * dc.GetCharWidth()
        dc.DrawLabel(val, wx.Rect(self.starttext - width, 0, width, h), wx.ALIGN_CENTER_VERTICAL)

    def MouseDown(self, event):
        pos = event.GetPosition()
        if self.entryRect.Contains(pos):
            self.clickPos = wx.GetMousePosition()
            self.oldValue = self.value
            offset = self.starttext - pos[0]
            if offset <= 7:
                self.increment = 0.001
            elif offset <= 14:
                self.increment = 0.01    
            elif offset <= 21:
                self.increment = 0.1
            elif offset <= 28:
                self.increment = 1    
            else:
                self.increment = 10                    
            self.selected = True
            self.new = ''
            self.CaptureMouse()
        self.Refresh()
        event.Skip()

    def MouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown() and self.HasCapture():
            if self.clickPos != None:
                pos = wx.GetMousePosition()
                off = self.clickPos[1] - pos[1]
                if self.valtype == 'float':
                    off *= self.increment
                self.value = self.oldValue + off    
                if self.outFunction:
                    self.outFunction(self.value)
            self.Refresh()

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
            self.clickPos = None

    def keyDown(self, event):
        if self.selected:
            char = ''
            if event.GetKeyCode() in range(324, 334):
                char = str(event.GetKeyCode() - 324)
            elif event.GetKeyCode() == 390:
                char = '-'
            elif event.GetKeyCode() == 391:
                char = '.'
            elif event.GetKeyCode() == wx.WXK_BACK:
                if self.new != '':
                    self.new = self.new[0:-1]
            elif event.GetKeyCode() < 256:
                char = chr(event.GetKeyCode())
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.new += char
            elif char == '.' and not '.' in self.new:
                self.new += char
            elif char == '-' and len(self.new) == 0:
                self.new += char
            elif event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
                self.value = eval(self.new)
                self.new = ''
                self.selected = False
                if self.outFunction:
                    self.outFunction(self.value)
            self.Refresh()

    def setValue(self, val):
        self.value = val
        self.selected = False
        self.new = ''
        self.Refresh() # need by Windows
        self.OnPaint(wx.PaintEvent(wx.ID_ANY)) # need by OS X

class RangeEntryUnit(wx.Panel):
    def __init__(self, parent, value=[0,0], unit='', size=(130,20), valtype='float', outFunction=None, colour=None):
        wx.Panel.__init__(self, parent, -1, size=size, style=wx.WANTS_CHARS)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.value = value
        self.unit = unit
        self.valtype = valtype
        self.outFunction = outFunction
        self.selected = False
        self.clickPos = None
        self.oldValue = value
        self.increment = 0.001
        self.new = ''
        self.font = wx.Font(ENTRYUNIT_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
        self.unitFont = wx.Font(ENTRYUNIT_FONT, wx.ROMAN, wx.ITALIC, wx.LIGHT, face=FONT_FACE)
        self.entryRect = wx.Rect(20, 2, 80, self.GetSize()[1]-4)
        if CeciliaLib.getVar("systemPlatform") == 'win32':
            self.starttext = 65
        else:    
            self.starttext = 100
        if colour:
            self.backColour = colour
        else:
            self.backColour = ENTRYUNIT_BACK_COLOUR
        self.createBackgroundBitmap()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        self.Bind(wx.EVT_KILL_FOCUS, self.LooseFocus)

    def createBackgroundBitmap(self):
        w, h = self.GetSize()
        self.backgroundBitmap = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(self.backgroundBitmap)
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.SetTextForeground(LABEL_LABEL_COLOUR)

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        rec = wx.Rect(0, 0, w, h)
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        dc.SetBrush(wx.Brush(self.backColour))
        dc.DrawRoundedRectangleRect(rec, 3)

        # Draw triangle
        dc.SetPen(wx.Pen(LABEL_LABEL_COLOUR, width=1, style=wx.SOLID))  
        dc.SetBrush(wx.Brush(LABEL_LABEL_COLOUR, wx.SOLID))
        dc.DrawPolygon([wx.Point(12,h/2), wx.Point(7,5), wx.Point(7,h-5)])

        # Draw unit
        dc.SetFont(self.unitFont)
        dc.DrawLabel(self.unit, wx.Rect(105, 0, w-105, h), wx.ALIGN_CENTER_VERTICAL)
        dc.SelectObject(wx.NullBitmap)

    def setBackColour(self, colour):
        self.backColour = colour
        self.createBackgroundBitmap()
        self.Refresh()

    def LooseFocus(self, event):
        if self.new != '':
            self.value = eval(self.new)
        self.new = ''
        self.selected = False
        if self.outFunction:
            self.outFunction(self.value)
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        dc.SetTextForeground(LABEL_LABEL_COLOUR)
        dc.DrawBitmap(self.backgroundBitmap, 0, 0)

        # Draw value
        dc.SetFont(self.font)
        if self.selected:
            dc.SetPen(wx.Pen(ENTRYUNIT_HIGHLIGHT_COLOUR, width=1, style=wx.SOLID))  
            dc.SetBrush(wx.Brush(ENTRYUNIT_HIGHLIGHT_COLOUR, wx.SOLID))
            dc.DrawRoundedRectangleRect(self.entryRect, 3)
        dc.SetPen(wx.Pen(LABEL_LABEL_COLOUR, width=1, style=wx.SOLID))  
        dc.SetBrush(wx.Brush(LABEL_LABEL_COLOUR, wx.SOLID))
        if self.selected and self.new:
            val = self.new
        else:
            val = str(self.value[0]) + ', ' + str(self.value[1])
        if CeciliaLib.getVar("systemPlatform") == 'linux2':
            width = len(val) * (dc.GetCharWidth() - 3)
        else:
            width = len(val) * dc.GetCharWidth()
        dc.DrawLabel(val, wx.Rect(self.starttext - width, 0, width, h), wx.ALIGN_CENTER_VERTICAL)

    def MouseDown(self, event):
        pos = event.GetPosition()
        if self.entryRect.Contains(pos):
            if 0: # deactivate mouse scrolling for now
                self.clickPos = wx.GetMousePosition()
                self.oldValue = self.value
                offset = self.starttext - pos[0]
                if offset <= 7:
                    self.increment = 0.001
                elif offset <= 14:
                    self.increment = 0.01    
                elif offset <= 21:
                    self.increment = 0.1
                elif offset <= 28:
                    self.increment = 1    
                else:
                    self.increment = 10                    
                self.CaptureMouse()
            self.selected = True
            self.new = ''
        self.Refresh()
        event.Skip()

    def MouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown() and self.HasCapture():
            if self.clickPos != None:
                pos = wx.GetMousePosition()
                off = self.clickPos[1] - pos[1]
                if self.valtype == 'float':
                    off *= self.increment
                self.value = self.oldValue + off    
                if self.outFunction:
                    self.outFunction(self.value)
            self.Refresh()

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
            self.clickPos = None

    def keyDown(self, event):
        if self.selected:
            char = ''
            if event.GetKeyCode() in range(324, 334):
                char = str(event.GetKeyCode() - 324)
            elif event.GetKeyCode() == 390:
                char = '-'
            elif event.GetKeyCode() == 391:
                char = '.'
            elif event.GetKeyCode() == 44:
                char = ','
            elif event.GetKeyCode() == wx.WXK_BACK:
                if self.new != '':
                    self.new = self.new[0:-1]
            elif event.GetKeyCode() < 256:
                char = chr(event.GetKeyCode())
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.new += char
            elif char == '.' and self.new.count('.') <= 1:
                self.new += char
            elif char == ',' and not ',' in self.new:
                self.new += char
            elif char == '-' and len(self.new) == 0:
                self.new += char
            elif event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
                tmp = self.new.split(',')
                self.value = [eval(n.strip()) for n in tmp]
                self.value = [min(self.value),max(self.value)]
                self.new = ''
                self.selected = False
                if self.outFunction:
                    self.outFunction(self.value)
            self.Refresh()

    def setValue(self, val):
        self.value = val
        self.selected = False
        self.new = ''
        self.Refresh() # need by Windows
        self.OnPaint(wx.PaintEvent(wx.ID_ANY)) # need by OS X

class SplitterEntryUnit(wx.Panel):
    def __init__(self, parent, value=[0,0,0], unit='', size=(130,20), num=3, valtype='float', outFunction=None, colour=None):
        wx.Panel.__init__(self, parent, -1, size=size, style=wx.WANTS_CHARS)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.value = value
        self.unit = unit
        self.valtype = valtype
        self.outFunction = outFunction
        self.selected = False
        self.clickPos = None
        self.oldValue = value
        self.increment = 0.001
        self.new = ''
        self.font = wx.Font(ENTRYUNIT_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
        self.unitFont = wx.Font(ENTRYUNIT_FONT, wx.ROMAN, wx.ITALIC, wx.LIGHT, face=FONT_FACE)
        self.entryRect = wx.Rect(20, 2, 80, self.GetSize()[1]-4)
        if CeciliaLib.getVar("systemPlatform") == 'win32':
            self.starttext = 65
        else:    
            self.starttext = 100
        if colour:
            self.backColour = colour
        else:
            self.backColour = ENTRYUNIT_BACK_COLOUR
        self.createBackgroundBitmap()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        self.Bind(wx.EVT_KILL_FOCUS, self.LooseFocus)

    def createBackgroundBitmap(self):
        w, h = self.GetSize()
        self.backgroundBitmap = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(self.backgroundBitmap)
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.SetTextForeground(LABEL_LABEL_COLOUR)

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        rec = wx.Rect(0, 0, w, h)
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        dc.SetBrush(wx.Brush(self.backColour))
        dc.DrawRoundedRectangleRect(rec, 3)

        # Draw triangle
        # dc.SetPen(wx.Pen(LABEL_LABEL_COLOUR, width=1, style=wx.SOLID))  
        # dc.SetBrush(wx.Brush(LABEL_LABEL_COLOUR, wx.SOLID))
        # dc.DrawPolygon([wx.Point(12,h/2), wx.Point(7,5), wx.Point(7,h-5)])

        # Draw unit
        dc.SetFont(self.unitFont)
        dc.DrawLabel(self.unit, wx.Rect(105, 0, w-105, h), wx.ALIGN_CENTER_VERTICAL)
        dc.SelectObject(wx.NullBitmap)

    def setBackColour(self, colour):
        self.backColour = colour
        self.createBackgroundBitmap()
        self.Refresh()

    def LooseFocus(self, event):
        if self.new != '':
            self.value = eval(self.new)
        self.new = ''
        self.selected = False
        if self.outFunction:
            self.outFunction(self.value)
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        dc.SetTextForeground(LABEL_LABEL_COLOUR)
        dc.DrawBitmap(self.backgroundBitmap, 0, 0)

        # Draw value
        dc.SetFont(self.font)
        if self.selected:
            dc.SetPen(wx.Pen(ENTRYUNIT_HIGHLIGHT_COLOUR, width=1, style=wx.SOLID))  
            dc.SetBrush(wx.Brush(ENTRYUNIT_HIGHLIGHT_COLOUR, wx.SOLID))
            dc.DrawRoundedRectangleRect(self.entryRect, 3)
        dc.SetPen(wx.Pen(LABEL_LABEL_COLOUR, width=1, style=wx.SOLID))  
        dc.SetBrush(wx.Brush(LABEL_LABEL_COLOUR, wx.SOLID))
        if self.selected and self.new:
            val = self.new
        else:
            if self.valtype == "float":
                val = ["%.1f" % x for x in self.value]
                val = ",".join(val)
            else:
                val = ["%i" % x for x in self.value]
                val = ",".join(val)
            #val = str(self.value[0]) + ', ' + str(self.value[1])
        if CeciliaLib.getVar("systemPlatform") == 'linux2':
            width = len(val) * (dc.GetCharWidth() - 3)
        else:
            width = len(val) * dc.GetCharWidth()
        dc.DrawLabel(val, wx.Rect(self.starttext - width, 0, width, h), wx.ALIGN_CENTER_VERTICAL)

    def MouseDown(self, event):
        pos = event.GetPosition()
        if self.entryRect.Contains(pos):
            if 0: # deactivate mouse scrolling for now
                self.clickPos = wx.GetMousePosition()
                self.oldValue = self.value
                offset = self.starttext - pos[0]
                if offset <= 7:
                    self.increment = 0.001
                elif offset <= 14:
                    self.increment = 0.01    
                elif offset <= 21:
                    self.increment = 0.1
                elif offset <= 28:
                    self.increment = 1    
                else:
                    self.increment = 10                    
                self.CaptureMouse()
            self.selected = True
            self.new = ''
        self.Refresh()
        event.Skip()

    def MouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown() and self.HasCapture():
            if self.clickPos != None:
                pos = wx.GetMousePosition()
                off = self.clickPos[1] - pos[1]
                if self.valtype == 'float':
                    off *= self.increment
                self.value = self.oldValue + off    
                if self.outFunction:
                    self.outFunction(self.value)
            self.Refresh()

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
            self.clickPos = None

    def keyDown(self, event):
        if self.selected:
            char = ''
            if event.GetKeyCode() in range(324, 334):
                char = str(event.GetKeyCode() - 324)
            elif event.GetKeyCode() == 390:
                char = '-'
            elif event.GetKeyCode() == 391:
                char = '.'
            elif event.GetKeyCode() == 44:
                char = ','
            elif event.GetKeyCode() == wx.WXK_BACK:
                if self.new != '':
                    self.new = self.new[0:-1]
            elif event.GetKeyCode() < 256:
                char = chr(event.GetKeyCode())
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.new += char
            elif char == '.' and self.new.count('.') <= 1:
                self.new += char
            elif char == ',' and not ',' in self.new:
                self.new += char
            elif char == '-' and len(self.new) == 0:
                self.new += char
            elif event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
                tmp = self.new.split(',')
                self.value = [eval(n.strip()) for n in tmp]
                self.value = [min(self.value),max(self.value)]
                self.new = ''
                self.selected = False
                if self.outFunction:
                    self.outFunction(self.value)
            self.Refresh()

    def setValue(self, val):
        self.value = val
        self.selected = False
        self.new = ''
        self.Refresh() # need by Windows
        self.OnPaint(wx.PaintEvent(wx.ID_ANY)) # need by OS X

#---------------------------
# ListEntry
# --------------------------
class ListEntry(wx.Panel):
    def __init__(self, parent, value='1, .5, .25', size=(100,20), colour=None, outFunction=None):
        wx.Panel.__init__(self, parent, -1, size=size, style=wx.WANTS_CHARS)
        self.SetMaxSize(self.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.outFunction = outFunction
        self.value = value
        self.new = ''
        self.font = wx.Font(ENTRYUNIT_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
        if colour:
            self.backColour = colour
        else:
            self.backColour = ENTRYUNIT_BACK_COLOUR
        self.createBackgroundBitmap()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)

    def createBackgroundBitmap(self):
        w, h = self.GetSize()
        self.backgroundBitmap = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(self.backgroundBitmap)
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.SetTextForeground(LABEL_LABEL_COLOUR)

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        rec = wx.Rect(0, 0, w, h)
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        dc.SetBrush(wx.Brush(self.backColour))
        dc.DrawRoundedRectangleRect(rec, 3)

        dc.SelectObject(wx.NullBitmap)

    def setBackColour(self, colour):
        self.backColour = colour
        self.createBackgroundBitmap()
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        dc.SetTextForeground(LABEL_LABEL_COLOUR)
        dc.DrawBitmap(self.backgroundBitmap, 0, 0)

        if type(self.value) == ListType:
            self.value = ", ".join([str(x) for x in self.value])
        if not "," in self.value:
            self.value = ", ".join(self.value.split())
        val = CeciliaLib.shortenName(self.value, 19)
        # Draw value
        dc.SetFont(self.font)
        dc.SetPen(wx.Pen(LABEL_LABEL_COLOUR, width=1, style=wx.SOLID))
        dc.SetBrush(wx.Brush(LABEL_LABEL_COLOUR, wx.SOLID))
        dc.DrawLabel(val, wx.Rect(5, 0, w-10, h), wx.ALIGN_CENTER_VERTICAL)

    def MouseDown(self, event):
        pos = event.GetPosition()
        self.popup = ListEntryPopupFrame(self, self.value)
        self.popup.CenterOnScreen()
        self.popup.Show()

    def setValue(self, val):
        self.value = val
        if self.outFunction != None:
            self.outFunction(self.value)
        self.Refresh() # need by Windows
        self.OnPaint(wx.PaintEvent(wx.ID_ANY)) # need by OS X

    def getValue(self):
        return self.value

class ListEntryPopupFrame(wx.Frame):
    def __init__(self, parent, value):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT )
        wx.Frame.__init__(self, parent, title='', style = style)
        self.parent = parent
        self.value = value
        self.SetSize((320,100))

        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()

        self.font = wx.Font(LIST_ENTRY_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)

        panel = wx.Panel(self, -1)
        w, h = self.GetSize()
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)

        title = FrameLabel(panel, "ENTER LIST OF VALUES", size=(w-2, 24))
        box.Add(title, 0, wx.ALL, 1)

        self.entry = wx.TextCtrl(panel, -1, self.value, size=(300,15), style=wx.TE_PROCESS_ENTER|wx.NO_BORDER)
        self.entry.SetBackgroundColour(GRAPHER_BACK_COLOUR)
        self.entry.SetFont(self.font)       
        self.entry.Bind(wx.EVT_TEXT_ENTER, self.OnApply)
        box.Add(self.entry, 0, wx.ALL, 10)

        applyBox = wx.BoxSizer(wx.HORIZONTAL)
        apply = ApplyToolBox(panel, tools=['Cancel', 'Apply'], outFunction=[self.OnCancel, self.OnApply])
        applyBox.Add(apply, 0, wx.LEFT, 210)
        box.Add(applyBox)
        box.AddSpacer(10)
        panel.SetSizerAndFit(box)

    def SetRoundShape(self, event=None):
        self.SetShape(GetRoundShape(320, 90, 1))

    def OnApply(self, event=None):
        self.parent.setValue(self.entry.GetValue())
        self.Destroy()

    def OnCancel(self, event=None):
        self.Destroy()

class TextPopupFrame(wx.Frame):
    def __init__(self, parent, text, size=(600,400)):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT )
        wx.Frame.__init__(self, parent, title='', size=size, style = style)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.parent = parent
        self.text = text
        self.size = size
        w, h = self.size

        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()

        self.font = wx.Font(MENU_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)

        self.panel = wx.Panel(self, size=self.size)
        self.panel.SetBackgroundColour(BACKGROUND_COLOUR)
        panelBox = wx.BoxSizer(wx.VERTICAL)

        moduleName = os.path.split(CeciliaLib.getVar("currentCeciliaFile"))[1].split(".")[0]
        title = FrameLabel(self.panel, "MODULE DESCRIPTION\n%s" % moduleName, size=(w-2, 32))
        panelBox.Add(title, 0, wx.ALL, 1)

        self.entry = wx.TextCtrl(self.panel, size=(w-20,h-90), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.NO_BORDER)
        self.entry.SetBackgroundColour(BACKGROUND_COLOUR)
        self.entry.SetFont(self.font)
        self.entry.SetValue(self.text)
        panelBox.Add(self.entry, 0, wx.ALL, 10)

        closeBox = wx.BoxSizer(wx.HORIZONTAL)
        close = CloseBox(self.panel, outFunction=self.OnClose)
        closeBox.Add(close, 0, wx.LEFT, w/2-20)
        panelBox.Add(closeBox)
        self.panel.SetSizer(panelBox)
        panelBox.Fit(self.panel)
        panelBox.Layout()
        self.Show()

    def SetRoundShape(self, event=None):
        w, h = self.GetSizeTuple()
        self.SetShape(GetRoundShape(w, h, 1))

    def OnClose(self):
        self.Destroy()

class AboutPopupFrame(wx.Frame):
    def __init__(self, parent, y_pos):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT )
        wx.Frame.__init__(self, parent, title='', pos=(-1,y_pos), style = style)
        self.parent = parent

        if CeciliaLib.getVar("systemPlatform")  in ['win32', 'linux2']:
            self.SetSize((600,410))
            self.font = wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
        else:
            self.font = wx.Font(13, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE)
                
        if CeciliaLib.getVar("systemPlatform") == 'linux2':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()

        panel = wx.Panel(self, -1)
        w, h = self.GetSize()
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)

        title = AboutLabel(panel, APP_VERSION, APP_COPYRIGHT, size=(w-2, 80))
        box.Add(title, 0, wx.ALL, 1)

        self.rtc = rt.RichTextCtrl(panel, size=(w-40,270), style=wx.NO_BORDER)
        self.rtc.SetBackgroundColour(BACKGROUND_COLOUR)
        self.rtc.SetFont(self.font)    
        self.rtc.Freeze()
        self.rtc.BeginSuppressUndo()
        if CeciliaLib.getVar("systemPlatform")  in ['win32', 'linux2']:
            self.rtc.BeginParagraphSpacing(0, 20)
        else:    
            self.rtc.BeginParagraphSpacing(0, 40)
        self.rtc.BeginAlignment(rt.TEXT_ALIGNMENT_CENTRE)
        self.rtc.Newline()
        self.rtc.BeginTextColour((0, 0, 0))
        self.rtc.WriteText("Cecilia ")
        self.rtc.BeginTextColour((255, 255, 255))
        self.rtc.WriteText("is a tool to make ear-bending noises and music. It uses the pyo audio engine created for the Python programming language by ")
        self.rtc.BeginTextColour((0, 0, 0))
        self.rtc.WriteText("Olivier Bélanger ")
        self.rtc.BeginTextColour((255, 255, 255))
        self.rtc.WriteText("at Université de Montréal.")

        self.rtc.Newline()
        self.rtc.BeginTextColour((0, 0, 0))
        self.rtc.WriteText("Jean Piché ")
        self.rtc.BeginTextColour((255, 255, 255))
        self.rtc.WriteText("conceived, designed, and programmed Cecilia in 1995 to replace racks full of analog audio gear in a musique concrète studio.")

        self.rtc.Newline()
        self.rtc.BeginTextColour((0, 0, 0))
        self.rtc.WriteText("Olivier Bélanger ")
        self.rtc.BeginTextColour((255, 255, 255))
        self.rtc.WriteText("does all the programming and contributed heavily on design issues. He recoded Cecilia in Python from the ground up in 2008. Olivier is now the keeper of the program.")

        self.rtc.Newline()
        self.rtc.BeginTextColour((0, 0, 0))
        self.rtc.WriteText("Jean-Michel Dumas ")
        self.rtc.BeginTextColour((255, 255, 255))
        self.rtc.WriteText("translated almost every modules from Cecilia 4.2, created new ones and provided much needed moral support, patient testing and silly entertainment.")

        urlStyle = rt.TextAttrEx()
        urlStyle.SetTextColour(wx.BLUE)
        urlStyle.SetFontUnderlined(True)
    
        self.rtc.Newline()
        self.rtc.BeginStyle(urlStyle)
        self.rtc.BeginURL("http://code.google.com/p/cecilia5/")
        self.rtc.WriteText("The Cecilia5 Web Site on GoogleCode")
        self.rtc.EndURL();
        self.rtc.EndStyle();
        
        self.rtc.Newline()
        self.rtc.EndParagraphSpacing()
        self.rtc.EndSuppressUndo()
        self.rtc.Thaw()

        self.rtc.Bind(wx.EVT_TEXT_URL, self.OnURL)
           
        box.Add(self.rtc, 0, wx.ALL, 10)

        closeBox = wx.BoxSizer(wx.HORIZONTAL)
        close = CloseBox(panel, outFunction=self.OnClose)
        closeBox.Add(close, 0, wx.LEFT, w/2-25)
        box.Add(closeBox)
        box.AddSpacer(20)
        panel.SetSizerAndFit(box)
        self.Center(wx.CENTER_ON_SCREEN|wx.HORIZONTAL)
        if CeciliaLib.getVar("systemPlatform")  in ['win32', 'linux2']:
            self.Center(wx.CENTER_ON_SCREEN|wx.VERTICAL)
        self.Show()

    def OnURL(self, evt):
        webbrowser.open_new_tab("http://code.google.com/p/cecilia5/")
        
    def SetRoundShape(self, event=None):
        self.SetShape(GetRoundShape(600, 410, 1))

    def OnClose(self):
        self.Destroy()

#---------------------------
# ControlKnob
# --------------------------
class ControlKnob(wx.Panel):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0,0), size=(50,70), log=False, outFunction=None, integer=False, backColour=None, label=''):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, size=size, style=wx.NO_BORDER | wx.WANTS_CHARS)
        self.parent = parent
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.SetMinSize(self.GetSize())
        self.knobBitmap = ICON_PLUGINS_KNOB.GetBitmap()
        self.outFunction = outFunction
        self.integer = integer
        self.log = log
        self.label = label
        self.SetRange(minvalue, maxvalue)
        self.borderWidth = 1
        self.selected = False
        self._enable = True
        self.new = ''
        self.floatPrecision = '%.3f'
        self.mode = 0
        self.colours = {0: "#000000", 1: "#FF0000", 2: "#00FF00"}
        if backColour: self.backColour = backColour
        else: self.backColour = CONTROLSLIDER_BACK_COLOUR
        if init != None: 
            self.SetValue(init)
            self.init = init
        else: 
            self.SetValue(minvalue)
            self.init = minvalue
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.DoubleClick)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        self.Bind(wx.EVT_KILL_FOCUS, self.LooseFocus)

    def setFloatPrecision(self, x):
        self.floatPrecision = '%.' + '%df' % x
        self.Refresh()

    def getMinValue(self):
        return self.minvalue

    def getMaxValue(self):
        return self.maxvalue

    def setEnable(self, enable):
        self._enable = enable
        if self._enable:
            self.knobBitmap = ICON_PLUGINS_KNOB.GetBitmap()
        else:
            self.knobBitmap = ICON_PLUGINS_KNOB_DISABLE.GetBitmap()
        self.Refresh()

    def getInit(self):
        return self.init

    def getLabel(self):
        return self.label

    def getLog(self):
        return self.log
        
    def SetRange(self, minvalue, maxvalue):   
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def getRange(self):
        return [self.minvalue, self.maxvalue]

    def SetValue(self, value):
        value = clamp(value, self.minvalue, self.maxvalue)
        if self.log:
            t = toLog(value, self.minvalue, self.maxvalue)
            self.value = interpFloat(t, self.minvalue, self.maxvalue)
        else:
            t = tFromValue(value, self.minvalue, self.maxvalue)
            self.value = interpFloat(t, self.minvalue, self.maxvalue)
        if self.integer:
            self.value = int(self.value)
        self.selected = False
        self.Refresh()

    def GetValue(self):
        if self.log:
            t = tFromValue(self.value, self.minvalue, self.maxvalue)
            val = toExp(t, self.minvalue, self.maxvalue)
        else:
            val = self.value
        if self.integer:
            val = int(val)
        return val

    def LooseFocus(self, event):
        self.selected = False
        self.Refresh()

    def keyDown(self, event):
        if self.selected:
            char = ''
            if event.GetKeyCode() in range(324, 334):
                char = str(event.GetKeyCode() - 324)
            elif event.GetKeyCode() == 390:
                char = '-'
            elif event.GetKeyCode() == 391:
                char = '.'
            elif event.GetKeyCode() == wx.WXK_BACK:
                if self.new != '':
                    self.new = self.new[0:-1]
            elif event.GetKeyCode() < 256:
                char = chr(event.GetKeyCode())
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.new += char
            elif char == '.' and not '.' in self.new:
                self.new += char
            elif char == '-' and len(self.new) == 0:
                self.new += char
            elif event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
                if self.new != '':
                    self.SetValue(eval(self.new))
                    self.new = ''
                self.selected = False
            self.Refresh()

    def MouseDown(self, evt):
        if evt.ShiftDown():
            self.DoubleClick(evt)
            return
        if self._enable:
            rec = wx.Rect(5, 13, 45, 45)
            pos = evt.GetPosition()
            if rec.Contains(pos):
                self.clickPos = wx.GetMousePosition()
                self.oldValue = self.value
                self.CaptureMouse()
                self.selected = False
            self.Refresh()
        evt.Skip()

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def DoubleClick(self, event):
        if self._enable:
            w, h = self.GetSize()
            pos = event.GetPosition()
            reclab = wx.Rect(3, 60, w-3, 10)
            recpt = wx.Rect(self.knobPointPos[0]-3, self.knobPointPos[1]-3, 9, 9)
            if reclab.Contains(pos):
                self.selected = True
            elif recpt.Contains(pos):
                self.mode = (self.mode+1) % 3
            self.Refresh()
        event.Skip()

    def MouseMotion(self, evt):
        if self._enable:
            if evt.Dragging() and evt.LeftIsDown() and self.HasCapture():
                pos = wx.GetMousePosition()
                offY = self.clickPos[1] - pos[1]
                off = offY
                off *= 0.005 * (self.maxvalue - self.minvalue)
                self.value = clamp(self.oldValue + off, self.minvalue, self.maxvalue)    
                self.selected = False
                self.Refresh()

    def setbackColour(self, colour):
        self.backColour = colour

    def OnPaint(self, evt):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=self.borderWidth, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        dc.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        dc.SetTextForeground(CONTROLSLIDER_TEXT_COLOUR)

        # Draw text label
        reclab = wx.Rect(0, 1, w, 9)
        dc.DrawLabel(self.label, reclab, wx.ALIGN_CENTER_HORIZONTAL)

        recval = wx.Rect(0, 60, w, 10)

        if self.selected:
            dc.SetBrush(wx.Brush(CONTROLSLIDER_SELECTED_COLOUR, wx.SOLID))
            dc.SetPen(wx.Pen(CONTROLSLIDER_SELECTED_COLOUR, width=self.borderWidth, style=wx.SOLID))  
            dc.DrawRoundedRectangleRect(recval, 3)

        dc.DrawBitmap(self.knobBitmap, 2, 13, True)
        r = 0.17320508075688773 # math.sqrt(.03)
        val = tFromValue(self.value, self.minvalue, self.maxvalue) * 0.87
        ph = val * math.pi * 2 - (3 * math.pi / 2.2)
        X = int(round(r * math.cos(ph)*45))
        Y = int(round(r * math.sin(ph)*45))
        dc.SetPen(wx.Pen(self.colours[self.mode], width=1, style=wx.SOLID))
        dc.SetBrush(wx.Brush(self.colours[self.mode], wx.SOLID))
        self.knobPointPos = (X+22, Y+33)
        dc.DrawCircle(X+22, Y+33, 2)

        if not self.midiLearn:
            dc.SetFont(wx.Font(CONTROLSLIDER_FONT-1, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))    
            dc.DrawLabel(self.midictlLabel, wx.Rect(2, 12, 40, 40), wx.ALIGN_CENTER)
        else:
            dc.DrawLabel("?...", wx.Rect(2, 12, 40, 40), wx.ALIGN_CENTER)

        dc.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        # Draw text value
        if self.selected and self.new:
            val = self.new
        else:
            if self.integer:
                val = '%d' % self.GetValue()
            else:
                val = self.floatPrecision % self.GetValue()
        if CeciliaLib.getVar("systemPlatform") == 'linux2':
            width = len(val) * (dc.GetCharWidth() - 3)
        else:
            width = len(val) * dc.GetCharWidth()
        dc.SetTextForeground(CONTROLSLIDER_TEXT_COLOUR)
        dc.DrawLabel(val, recval, wx.ALIGN_CENTER)

        # Send value
        if self.outFunction:
            self.outFunction(self.GetValue())

        evt.Skip()
       
#---------------------------
# ControlSlider
# --------------------------
class ControlSlider(wx.Panel):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0,0), size=(200,20), log=False, outFunction=None, integer=False, backColour=None):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, size=size, style=wx.NO_BORDER | wx.WANTS_CHARS)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.SetMinSize(self.GetSize())
        self.knobSize = 40
        self.knobHalfSize = 20
        self.sliderHeight = 14
        self.outFunction = outFunction
        self.integer = integer
        self.log = log
        self.SetRange(minvalue, maxvalue)
        self.borderWidth = 1
        self.selected = False
        self._enable = True
        self.new = ''
        self.floatPrecision = '%.2f'
        if backColour: self.backColour = backColour
        else: self.backColour = CONTROLSLIDER_BACK_COLOUR
        if init != None: 
            self.SetValue(init)
            self.init = init
        else: 
            self.SetValue(minvalue)
            self.init = minvalue
        self.clampPos()
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_LEFT_DCLICK, self.DoubleClick)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.Bind(wx.EVT_KEY_DOWN, self.keyDown)
        self.Bind(wx.EVT_KILL_FOCUS, self.LooseFocus)
        self.createSliderBitmap()
        self.createKnobBitmap()

    def setFloatPrecision(self, x):
        self.floatPrecision = '%.' + '%df' % x
        self.Refresh()
        
    def getMinValue(self):
        return self.minvalue

    def getMaxValue(self):
        return self.maxvalue

    def setEnable(self, enable):
        self._enable = enable
        self.Refresh()

    def setSliderHeight(self, height):
        self.sliderHeight = height
        self.createSliderBitmap()
        self.createKnobBitmap()
        self.Refresh()

    def createSliderBitmap(self):
        w, h = self.GetSize()
        b = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(b)
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=1))
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR))
        dc.DrawRectangle(0,0,w,h)
        dc.SetBrush(wx.Brush("#777777"))
        dc.SetPen(wx.Pen(WIDGET_BORDER_COLOUR, width=1))
        h2 = self.sliderHeight / 4
        dc.DrawRoundedRectangle(0,h2,w,self.sliderHeight,2)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour("#777777")
        self.sliderMask = b

    def createKnobBitmap(self):
        w, h = self.knobSize, self.GetSize()[1]
        b = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(b)
        rec = wx.Rect(0, 0, w, h)
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=1))
        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR))
        dc.DrawRectangleRect(rec)
        h2 = self.sliderHeight / 4
        rec = wx.Rect(0, h2, w, self.sliderHeight)
        dc.GradientFillLinear(rec, GRADIENT_DARK_COLOUR, CONTROLSLIDER_BACK_COLOUR, wx.BOTTOM)
        dc.SetBrush(wx.Brush("#787878"))
        dc.SetPen(wx.Pen(KNOB_BORDER_COLOUR, width=1))
        dc.DrawRoundedRectangle(0,0,w,h,2)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour("#787878")
        self.knobMask = b

    def getInit(self):
        return self.init

    def SetRange(self, minvalue, maxvalue):   
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def getRange(self):
        return [self.minvalue, self.maxvalue]

    def scale(self):
        inter = tFromValue(self.pos, self.knobHalfSize, self.GetSize()[0]-self.knobHalfSize)
        if not self.integer:
            return interpFloat(inter, self.minvalue, self.maxvalue)
        else:
            return int(interpFloat(inter, self.minvalue, self.maxvalue))

    def SetValue(self, value):
        if self.HasCapture():
            self.ReleaseMouse()
        value = clamp(value, self.minvalue, self.maxvalue)
        if self.log:
            t = toLog(value, self.minvalue, self.maxvalue)
            self.value = interpFloat(t, self.minvalue, self.maxvalue)
        else:
            t = tFromValue(value, self.minvalue, self.maxvalue)
            self.value = interpFloat(t, self.minvalue, self.maxvalue)
        if self.integer:
            self.value = int(self.value)
        self.clampPos()
        self.selected = False
        self.Refresh()

    def GetValue(self):
        if self.log:
            t = tFromValue(self.value, self.minvalue, self.maxvalue)
            val = toExp(t, self.minvalue, self.maxvalue)
        else:
            val = self.value
        if self.integer:
            val = int(val)
        return val

    def LooseFocus(self, event):
        self.selected = False
        self.Refresh()

    def keyDown(self, event):
        if self.selected:
            char = ''
            if event.GetKeyCode() in range(324, 334):
                char = str(event.GetKeyCode() - 324)
            elif event.GetKeyCode() == 390:
                char = '-'
            elif event.GetKeyCode() == 391:
                char = '.'
            elif event.GetKeyCode() == wx.WXK_BACK:
                if self.new != '':
                    self.new = self.new[0:-1]
            elif event.GetKeyCode() < 256:
                char = chr(event.GetKeyCode())
            if char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                self.new += char
            elif char == '.' and not '.' in self.new:
                self.new += char
            elif char == '-' and len(self.new) == 0:
                self.new += char
            elif event.GetKeyCode() in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER]:
                self.SetValue(eval(self.new))
                self.new = ''
                self.selected = False
            self.Refresh()
 
    def MouseDown(self, evt):
        if evt.ShiftDown():
            self.DoubleClick(evt)
            return
        if self._enable:
            size = self.GetSize()
            self.pos = clamp(evt.GetPosition()[0], self.knobHalfSize, size[0]-self.knobHalfSize)
            self.value = self.scale()
            self.CaptureMouse()
            self.selected = False
            self.Refresh()
        evt.Skip()

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def DoubleClick(self, event):
        if self._enable:
            w, h = self.GetSize()
            pos = event.GetPosition()
            if wx.Rect(self.pos-self.knobHalfSize, 0, self.knobSize, h).Contains(pos):
                self.selected = True
            self.Refresh()
        event.Skip()
            
    def MouseMotion(self, evt):
        if self._enable:
            size = self.GetSize()
            if evt.Dragging() and evt.LeftIsDown():
                self.pos = clamp(evt.GetPosition()[0], self.knobHalfSize, size[0]-self.knobHalfSize)
                self.value = self.scale()
                self.selected = False
                self.Refresh()

    def OnResize(self, evt):
        self.createSliderBitmap()
        self.clampPos()    
        self.Refresh()

    def clampPos(self):
        size = self.GetSize()
        self.pos = tFromValue(self.value, self.minvalue, self.maxvalue) * (size[0] - self.knobSize) + self.knobHalfSize
        self.pos = clamp(self.pos, self.knobHalfSize, size[0]-self.knobHalfSize)
        
    def setbackColour(self, colour):
        self.backColour = colour

    def OnPaint(self, evt):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=self.borderWidth, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        # Draw inner part
        if self._enable: sliderColour = self.backColour
        else: sliderColour = CONTROLSLIDER_DISABLE_COLOUR
        h2 = self.sliderHeight / 4
        rec = wx.Rect(0, h2, w, self.sliderHeight)
        dc.GradientFillLinear(rec, GRADIENT_DARK_COLOUR, sliderColour, wx.BOTTOM)
        dc.DrawBitmap(self.sliderMask, 0, 0, True)

        # Draw knob
        if self._enable: knobColour = CONTROLSLIDER_KNOB_COLOUR
        else: knobColour = CONTROLSLIDER_DISABLE_COLOUR
        rec = wx.Rect(self.pos-self.knobHalfSize, 0, self.knobSize, h)  
        dc.GradientFillLinear(rec, GRADIENT_DARK_COLOUR, knobColour, wx.RIGHT)
        dc.DrawBitmap(self.knobMask, rec[0], rec[1], True)
        
        if self.selected:
            rec2 = wx.Rect(self.pos-self.knobHalfSize, 0, self.knobSize, h)  
            dc.SetBrush(wx.Brush(CONTROLSLIDER_SELECTED_COLOUR, wx.SOLID))
            dc.SetPen(wx.Pen(CONTROLSLIDER_SELECTED_COLOUR, width=self.borderWidth, style=wx.SOLID))  
            dc.DrawRoundedRectangleRect(rec2, 3)

        dc.SetFont(wx.Font(CONTROLSLIDER_FONT, wx.ROMAN, wx.NORMAL, wx.NORMAL, face=FONT_FACE))

        # Draw text
        if self.selected and self.new:
            val = self.new
        else:
            if self.integer:
                val = '%d' % self.GetValue()
            else:
                val = self.floatPrecision % self.GetValue()
        if sys.platform == 'linux2':
            width = len(val) * (dc.GetCharWidth() - 3)
        else:
            width = len(val) * dc.GetCharWidth()
        dc.SetTextForeground(CONTROLSLIDER_TEXT_COLOUR)
        dc.DrawLabel(val, rec, wx.ALIGN_CENTER)

        # Send value
        if self.outFunction:
            self.outFunction(self.GetValue())

        evt.Skip()

#---------------------------
# PlainSlider
# --------------------------
class PlainSlider(wx.Panel):
    def __init__(self, parent, minvalue, maxvalue, init=None, pos=(0,0), size=(80,10), log=False, outFunction=None):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, pos=pos, size=size, style=wx.NO_BORDER)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)  
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self._backColour = BACKGROUND_COLOUR
        self.SetMinSize(self.GetSize())
        self.knobSize = 12
        self.knobHalfSize = 6
        self.sliderHeight = 6.
        self.outFunction = outFunction
        self.log = log
        self.SetRange(minvalue, maxvalue)
        self.borderWidth = 1
        if init != None: self.SetValue(init)
        else: self.SetValue(minvalue)
        self.clampPos()
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        self.Bind(wx.EVT_MOTION, self.MouseMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)
        self.show = True
        self.createSliderBitmap()
        self.createKnobBitmap()

    def createSliderBitmap(self):
        w, h = self.GetSize()
        b = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(b)
        dc.SetPen(wx.Pen(self._backColour, width=1))
        dc.SetBrush(wx.Brush(self._backColour))
        dc.DrawRectangle(0,0,w,h)
        dc.SetBrush(wx.Brush("#777777"))
        dc.SetPen(wx.Pen(self._backColour, width=0))
        h2 = round(self.sliderHeight / 4)
        dc.DrawRoundedRectangle(0,h2,w,self.sliderHeight,3)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour("#777777")
        self.sliderMask = b

    def createKnobBitmap(self):
        w, h = self.knobSize, self.GetSize()[1]
        b = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC(b)
        rec = wx.Rect(0, 0, w, h)
        dc.SetPen(wx.Pen(self._backColour, width=1))
        dc.SetBrush(wx.Brush(self._backColour))
        dc.DrawRectangleRect(rec)
        h2 = round(self.sliderHeight / 4)
        rec = wx.Rect(0, h2, w, self.sliderHeight)
        dc.GradientFillLinear(rec, GRADIENT_DARK_COLOUR, CONTROLSLIDER_BACK_COLOUR, wx.BOTTOM)
        dc.SetBrush(wx.Brush("#787878"))
        dc.DrawRoundedRectangle(0,0,w,h,2)
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour("#787878")
        self.knobMask = b

    def setBackColour(self, col):
        self._backColour = col
        self.SetBackgroundColour(col)
        self.createSliderBitmap()
        self.createKnobBitmap()
        self.Refresh()

    def Show(self):
        self.show = True
        self.Refresh()

    def Hide(self):
        self.show = False
        self.Refresh()
    
    def SetRange(self, minvalue, maxvalue):   
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def scale(self):
        inter = tFromValue(self.pos, self.knobHalfSize, self.GetSize()[0]-self.knobHalfSize)
        return interpFloat(inter, self.minvalue, self.maxvalue)

    def SetValue(self, value):
        if self.HasCapture():
            self.ReleaseMouse()
        value = clamp(value, self.minvalue, self.maxvalue)
        t = tFromValue(value, self.minvalue, self.maxvalue)
        if self.log:
            self.value = interpFloat(math.sqrt(t), self.minvalue, self.maxvalue)
        else:
            self.value = interpFloat(t, self.minvalue, self.maxvalue)
        self.clampPos()
        self.Refresh()

    def GetValue(self):
        if self.log:
            t = tFromValue(self.value, self.minvalue, self.maxvalue)
            val = interpFloat(t*t, self.minvalue, self.maxvalue)
        else:
            val = self.value
        return val
 
    def MouseDown(self, evt):
        size = self.GetSize()
        self.pos = clamp(evt.GetPosition()[0], self.knobHalfSize, size[0]-self.knobHalfSize)
        self.value = self.scale()
        self.CaptureMouse()
        self.Refresh()

    def MouseUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
            
    def MouseMotion(self, evt):
        size = self.GetSize()
        if evt.Dragging() and evt.LeftIsDown():
            self.pos = clamp(evt.GetPosition()[0], self.knobHalfSize, size[0]-self.knobHalfSize)
            self.value = self.scale()
            self.Refresh()

    def OnResize(self, evt):
        self.createSliderBitmap()
        self.clampPos()    
        self.Refresh()

    def clampPos(self):
        size = self.GetSize()
        self.pos = tFromValue(self.value, self.minvalue, self.maxvalue) * (size[0] - self.knobHalfSize) + self.knobHalfSize
        self.pos = clamp(self.pos, self.knobHalfSize, size[0]-self.knobHalfSize)

    def OnPaint(self, evt):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(self._backColour, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(self._backColour, width=self.borderWidth, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        if self.show:
            # Draw inner part
            h2 = round(self.sliderHeight / 4)
            rec = wx.Rect(0, h2, w, self.sliderHeight)
            dc.GradientFillLinear(rec, GRADIENT_DARK_COLOUR, CONTROLSLIDER_BACK_COLOUR, wx.BOTTOM)
            dc.DrawBitmap(self.sliderMask, 0, 0, True)
    
            # Draw knob
            rec = wx.Rect(self.pos-self.knobHalfSize, 0, self.knobSize, h)  
            dc.GradientFillLinear(rec, GRADIENT_DARK_COLOUR, CONTROLSLIDER_KNOB_COLOUR, wx.RIGHT)
            dc.DrawBitmap(self.knobMask, rec[0], rec[1], True)
           
            # Send value
            if self.outFunction:
                self.outFunction(self.GetValue())

        evt.Skip()

#---------------------------
# ToolBox (need a list of outFunctions axxociated with tools)
# --------------------------
class ToolBox(wx.Panel):
    def __init__(self, parent, size=(80,20), tools=[], outFunction=None, openSampler=False):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self._backColour = BACKGROUND_COLOUR
        self.parent = parent
        toolsLength = len(tools)
        if len(tools) == 0:
            raise('ToolBox must have at least a list of one tool!')
        self.num = len(tools)
        self.SetSize((20*self.num, 20))
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        self.tools = tools
        self.maps = {'save': self.onSave, 'load': self.onLoad, 'reset': self.onReset, 'show': self.onShow,
                     'open': self.onOpen, 'edit': self.onEdit, 'recycle': self.onRecycle, 'play': self.onPlay,
                     'time': self.onTime, 'delete': self.onDelete}
        self.tooltips = {'save': [TT_SAVE_GRAPH,TT_PRESET_SAVE], 'load': [TT_LOAD_SOUND,TT_SET_OUTPUT,TT_LOAD_GRAPH], 
                        'reset': TT_REINIT_GRAPH, 'show': TT_SHOW_GRAPH,
                        'open': TT_OPEN_SAMPLER, 'edit': TT_EDIT_SOUND, 'recycle': TT_USE_OUTPUT, 'play': TT_PLAY_SOUND,
                        'time': TT_SET_DUR, 'delete': TT_PRESET_DELETE}             

        self.graphics = {'save': [ICON_TB_SAVE.GetBitmap(), ICON_TB_SAVE_OVER.GetBitmap()], 
                 'load': [ICON_TB_LOAD.GetBitmap(), ICON_TB_LOAD_OVER.GetBitmap()], 
                 'reset': [ICON_TB_RESET.GetBitmap(), ICON_TB_RESET_OVER.GetBitmap()],
                 'delete': [ICON_TB_DELETE.GetBitmap(), ICON_TB_DELETE_OVER.GetBitmap()],
                 'play': [ICON_TB_PLAY.GetBitmap(), ICON_TB_PLAY_OVER.GetBitmap()],
                 'recycle': [ICON_TB_RECYCLE.GetBitmap(), ICON_TB_RECYCLE_OVER.GetBitmap()],
                 'edit': [ICON_TB_EDIT.GetBitmap(), ICON_TB_EDIT_OVER.GetBitmap()],
                 'open': [ICON_TB_OPEN.GetBitmap(), ICON_TB_OPEN_OVER.GetBitmap(),
                          ICON_TB_CLOSE.GetBitmap(), ICON_TB_CLOSE_OVER.GetBitmap()], 
                 'time': [ICON_TB_TIME.GetBitmap(), ICON_TB_TIME_OVER.GetBitmap()], 
                 'show': [ICON_TB_SHOW.GetBitmap(), ICON_TB_SHOW_OVER.GetBitmap(),
                          ICON_TB_HIDE.GetBitmap(), ICON_TB_HIDE_OVER.GetBitmap()]}

        self.rectList = []
        for i in range(self.num):
            self.rectList.append(wx.Rect(i*20, 0, 20, self.GetSize()[1]))
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.show = True
        self.open = False
        self.openSampler = openSampler
        self.samplerFrame = None
        self.outFunction = outFunction

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

        tooltip = ''
        for tool in self.tools:
            if tool == 'save':
                if 'delete' in tools:
                    tooltip += self.tooltips[tool][1] + '\n\n'
                else:    
                    tooltip += self.tooltips[tool][0] + '\n\n'
            elif tool == 'load':
                if 'open' in tools:
                    tooltip += self.tooltips[tool][0] + '\n\n'
                elif 'recycle' in tools:
                    tooltip += self.tooltips[tool][1] + '\n\n'
                else:
                    tooltip += self.tooltips[tool][2] + '\n\n'
            else:        
                tooltip += self.tooltips[tool] + '\n\n'
        self.SetToolTip(CECTooltip(tooltip))
        
    def setBackColour(self, col):
        self._backColour = col
        self.SetBackgroundColour(col)
        self.Refresh()

    def setOverWait(self, which):
        self.oversWait[which] = False

    def checkForOverReady(self, pos):
        for i, rec in enumerate(self.rectList):
            if not rec.Contains(pos):
                self.oversWait[i] = True
                        
    def OnMotion(self, event):
        pos = event.GetPosition()
        self.overs = [False] * self.num
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos) and self.oversWait[i]:
                self.overs[i] = True
        self.checkForOverReady(pos)
        self.Refresh()
        event.Skip()

    def OnLeave(self, event):
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(self._backColour, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(self._backColour, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        for i, tool in enumerate(self.tools):
            if not self.overs[i]:
                if tool == 'show':
                    if self.show: icon = self.graphics[tool][0]
                    else: icon = self.graphics[tool][2]
                elif tool == 'open':
                    if self.open: icon = self.graphics[tool][2]
                    else: icon = self.graphics[tool][0]
                else:
                    icon = self.graphics[tool][0]
            else:
                if tool == 'show':
                    if self.show: icon = self.graphics[tool][1]
                    else: icon = self.graphics[tool][3]
                elif tool == 'open':
                    if self.open: icon = self.graphics[tool][3]
                    else: icon = self.graphics[tool][1]
                else:
                    icon = self.graphics[tool][1]
            dc.DrawBitmap(icon, self.rectList[i][0]+2, self.rectList[i][1]+1, True)
        dc.SetPen(wx.Pen(WHITE_COLOUR, width=1, style=wx.SOLID))  
        for i in range((self.num-1)):
            dc.DrawLine((i+1)*20, 2, (i+1)*20, h-2)

    def MouseDown(self, event):
        pos = event.GetPosition()
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos):
                tool = self.tools[i]
                self.setOverWait(i)
                break
        if self.outFunction:
            self.maps[tool]()
        self.Refresh()

    def onSave(self):
        self.outFunction[self.tools.index('save')]()

    def onLoad(self):
        self.outFunction[self.tools.index('load')]()

    def onReset(self):
        self.outFunction[self.tools.index('reset')]()

    def onPlay(self):
        self.outFunction[self.tools.index('play')]()

    def onEdit(self):
        self.outFunction[self.tools.index('edit')]()

    def onRecycle(self):
        self.outFunction[self.tools.index('recycle')]()

    def onDelete(self):
        self.outFunction[self.tools.index('delete')]()

    def onOpen(self):
        self.outFunction[self.tools.index('open')]()
        if self.open:
            self.open = False
        else:
            self.open = True
        self.Refresh()

    def onTime(self):
        self.outFunction[self.tools.index('time')]()

    def onShow(self):
        if self.show: self.show = False
        else: self.show = True
        self.outFunction[self.tools.index('show')](self.show)

    def setShow(self, state):
        self.show = state
        self.Refresh()
    
    def setOpen(self, state):
        self.open = state
        self.Refresh()
        
#---------------------------
# RadioToolBox (need a list of outFunctions axxociated with tools)
# --------------------------
class RadioToolBox(wx.Panel):
    def __init__(self, parent, size=(75,20), tools=['pointer', 'pencil', 'zoom', 'hand'], outFunction=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(TITLE_BACK_COLOUR)
        toolsLength = len(tools)
        if len(tools) == 0:
            raise('ToolBox must have at least a list of one tool!')
        self.num = len(tools)
        self.SetSize((25*self.num, 20))
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        self.tools = tools
        self.maps = {'pointer': self.onPointer, 'pencil': self.onPencil, 'zoom': self.onZoom, 'hand': self.onHand}
        self.graphics = {'pointer': [ICON_RTB_POINTER.GetBitmap(), ICON_RTB_POINTER_OVER.GetBitmap(), ICON_RTB_POINTER_CLICK.GetBitmap()],
                         'pencil': [ICON_RTB_PENCIL.GetBitmap(), ICON_RTB_PENCIL_OVER.GetBitmap(), ICON_RTB_PENCIL_CLICK.GetBitmap()],
                         'zoom': [ICON_RTB_ZOOM.GetBitmap(), ICON_RTB_ZOOM_OVER.GetBitmap(), ICON_RTB_ZOOM_CLICK.GetBitmap()],
                         'hand': [ICON_RTB_HAND.GetBitmap(), ICON_RTB_HAND_OVER.GetBitmap(), ICON_RTB_HAND_CLICK.GetBitmap()]}
        self.tooltips = {'pointer': TT_POINTER, 'pencil': TT_PENCIL, 'zoom': TT_ZOOM, 'hand': TT_HAND}
        self.rectList = []
        for i in range(self.num):
            self.rectList.append(wx.Rect(i*25, 0, 25, self.GetSize()[1]))
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.selected = 0
        self.outFunction = outFunction
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

        tooltip = ''
        for tool in self.tools:
            tooltip += self.tooltips[tool] + '\n\n'
        self.SetToolTip(CECTooltip(tooltip))

    def setOverWait(self, which):
        self.oversWait[which] = False

    def checkForOverReady(self, pos):
        for i, rec in enumerate(self.rectList):
            if not rec.Contains(pos):
                self.oversWait[i] = True
                        
    def OnMotion(self, event):
        pos = event.GetPosition()
        self.overs = [False] * self.num
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos) and self.oversWait[i]:
                self.overs[i] = True
        self.checkForOverReady(pos)
        self.Refresh()
        event.Skip()

    def OnLeave(self, event):
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(TITLE_BACK_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(TITLE_BACK_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        for i, tool in enumerate(self.tools):
            if not self.overs[i]:
                if i == self.selected:
                    icon = self.graphics[tool][2]
                else:
                    icon = self.graphics[tool][0]
            else:
                icon = self.graphics[tool][1]
            dc.DrawBitmap(icon, self.rectList[i][0]+2, self.rectList[i][1]+1, True)
        dc.SetPen(wx.Pen(WHITE_COLOUR, width=1, style=wx.SOLID))  
        for i in range((self.num-1)):
            dc.DrawLine((i+1)*25, 2, (i+1)*25, h-2)

    def setTool(self, tool):
        self.selected = self.tools.index(tool)
        if self.outFunction:
            self.maps[tool]()
        self.Refresh()

    def MouseDown(self, event):
        pos = event.GetPosition()
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos):
                tool = self.tools[i]
                self.selected = i
                self.setOverWait(i)
                break
        if self.outFunction:
            self.maps[tool]()
        self.Refresh()
        event.Skip()

    def onPointer(self):
        self.outFunction[self.tools.index('pointer')]()

    def onPencil(self):
        self.outFunction[self.tools.index('pencil')]()

    def onZoom(self):
        self.outFunction[self.tools.index('zoom')]()

    def onHand(self):
        self.outFunction[self.tools.index('hand')]()

class PreferencesRadioToolBox(wx.Panel):
    def __init__(self, parent, size=(200,30), tools=['path', 'audio', 'midi', 'filer', 'cecilia'], outFunction=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(TITLE_BACK_COLOUR)
        toolsLength = len(tools)
        if len(tools) == 0:
            raise('ToolBox must have at least a list of one tool!')
        self.num = len(tools)
        self.SetSize((40*self.num, 30))
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        self.tools = tools
        self.graphics = {'path': [ICON_PREF_PATH.GetBitmap(), ICON_PREF_PATH_OVER.GetBitmap(), ICON_PREF_PATH_CLICK.GetBitmap()],
                         'audio': [ICON_PREF_AUDIO.GetBitmap(), ICON_PREF_AUDIO_OVER.GetBitmap(), ICON_PREF_AUDIO_CLICK.GetBitmap()],
                         'midi': [ICON_PREF_MIDI.GetBitmap(), ICON_PREF_MIDI_OVER.GetBitmap(), ICON_PREF_MIDI_CLICK.GetBitmap()],
                         'filer': [ICON_PREF_FILER.GetBitmap(), ICON_PREF_FILER_OVER.GetBitmap(), ICON_PREF_FILER_CLICK.GetBitmap()],
                         'cecilia': [ICON_PREF_CECILIA.GetBitmap(), ICON_PREF_CECILIA_OVER.GetBitmap(), ICON_PREF_CECILIA_CLICK.GetBitmap()],
                         }
        #self.tooltips = {'pointer': TT_POINTER, 'pencil': TT_PENCIL, 'zoom': TT_ZOOM, 'hand': TT_HAND}
        self.rectList = []
        for i in range(self.num):
            self.rectList.append(wx.Rect(i*40, 0, 40, self.GetSize()[1]))
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.selected = 0
        self.outFunction = outFunction

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

        #tooltip = ''
        #for tool in self.tools:
        #    tooltip += self.tooltips[tool] + '\n\n'
        #self.SetToolTip(CECTooltip(tooltip))

    def setOverWait(self, which):
        self.oversWait[which] = False

    def checkForOverReady(self, pos):
        for i, rec in enumerate(self.rectList):
            if not rec.Contains(pos):
                self.oversWait[i] = True

    def OnMotion(self, event):
        pos = event.GetPosition()
        self.overs = [False] * self.num
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos) and self.oversWait[i]:
                self.overs[i] = True
        self.checkForOverReady(pos)
        self.Refresh()
        event.Skip()

    def OnLeave(self, event):
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(TITLE_BACK_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(TITLE_BACK_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        for i, tool in enumerate(self.tools):
            if not self.overs[i]:
                if i == self.selected:
                    icon = self.graphics[tool][2]
                else:
                    icon = self.graphics[tool][0]
            else:
                icon = self.graphics[tool][1]
            dc.DrawBitmap(icon, self.rectList[i][0]+2, self.rectList[i][1]+1, True)
        dc.SetPen(wx.Pen(WHITE_COLOUR, width=1, style=wx.SOLID))  
        for i in range((self.num-1)):
            dc.DrawLine((i+1)*40, 2, (i+1)*40, h-2)

    def setTool(self, tool):
        self.selected = self.tools.index(tool)
        if self.outFunction:
            self.maps[tool]()
        self.Refresh()

    def MouseDown(self, event):
        pos = event.GetPosition()
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos):
                tool = self.tools[i]
                self.selected = i
                self.setOverWait(i)
                break
        if self.outFunction:
            self.outFunction(self.selected)
        self.Refresh()
        event.Skip()

#---------------------------
# ApplyToolBox (need a list of outFunctions axxociated with tools)
# --------------------------
class ApplyToolBox(wx.Panel):
    def __init__(self, parent, size=(100,20), tools=['Close', 'Apply'], outFunction=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        toolsLength = len(tools)
        if len(tools) == 0:
            raise('ToolBox must have at least a list of one tool!')
        self.num = len(tools)
        self.SetSize((50*self.num, 20))
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        self.tools = tools
        self.maps = {'Apply': self.onApply, 'Close': self.onClose, 'Cancel': self.onCancel}

        self.rectList = []
        for i in range(self.num):
            self.rectList.append(wx.Rect(i*50, 0, 50, self.GetSize()[1]))
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.outFunction = outFunction

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

    def setOverWait(self, which):
        self.oversWait[which] = False

    def checkForOverReady(self, pos):
        for i, rec in enumerate(self.rectList):
            if not rec.Contains(pos):
                self.oversWait[i] = True
                        
    def OnMotion(self, event):
        pos = event.GetPosition()
        self.overs = [False] * self.num
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos) and self.oversWait[i]:
                self.overs[i] = True
        self.checkForOverReady(pos)
        self.Refresh()
        event.Skip()

    def OnLeave(self, event):
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(BACKGROUND_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(BACKGROUND_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        for i, tool in enumerate(self.tools):
            if not self.overs[i]:
                textColour = "#FFFFFF"
            else:
                textColour = "#000000"
            dc.SetBrush(wx.Brush('#8896BB'))
            dc.SetPen(wx.Pen("#FFFFFF", width=1))
            rec = self.rectList[i]
            dc.DrawRoundedRectangle(rec[0]+2, rec[1], rec[2]-4, rec[3], 3)
            dc.SetFont(wx.Font(LABEL_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
            dc.SetTextForeground(textColour)
            dc.DrawLabel(self.tools[i], self.rectList[i], wx.ALIGN_CENTER)

    def MouseDown(self, event):
        pos = event.GetPosition()
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos):
                tool = self.tools[i]
                self.setOverWait(i)
                break
        if self.outFunction:
            self.maps[tool]()
        self.Refresh()
        event.Skip()

    def onApply(self):
        self.outFunction[self.tools.index('Apply')]()

    def onClose(self):
        self.outFunction[self.tools.index('Close')]()

    def onCancel(self):
        self.outFunction[self.tools.index('Cancel')]()

class CloseBox(wx.Panel):
    def __init__(self, parent, size=(50,20), pos=wx.DefaultPosition, outFunction=None, label='Close'):
        wx.Panel.__init__(self, parent, -1, size=size, pos=pos)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.setBackgroundColour(BACKGROUND_COLOUR)
        self.setInsideColour(CLOSEBOX_INSIDE_COLOUR)
        self.SetSize(size)
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        self.textMagnify = 0
        self.label = label
        self.over = False
        self.overWait = True
        self.outFunction = outFunction
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

    def setTextMagnify(self, point):
        self.textMagnify = point
        self.Refresh()
        
    def setBackgroundColour(self, colour):
        self._backColour = colour
        self.SetBackgroundColour(colour)
        self.Refresh()

    def setInsideColour(self, colour):
        self._insideColour = colour
        self.Refresh()
        
    def setOverWait(self):
        self.overWait = False
                        
    def OnMotion(self, event):
        pos = event.GetPosition()
        self.over = True
        self.Refresh()
        event.Skip()

    def OnLeave(self, event):
        self.over = False
        self.overWait = True
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(self._backColour, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(self._backColour, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        if not self.over:
            textColour = "#FFFFFF"
        else:
            textColour = "#000000"
        dc.SetBrush(wx.Brush(self._insideColour))
        dc.SetPen(wx.Pen("#FFFFFF", width=1))
        dc.DrawRoundedRectangle(2, 0, w-4, h, 3)
        dc.SetFont(wx.Font(LABEL_FONT+self.textMagnify, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        dc.SetTextForeground(textColour)
        dc.DrawLabel(self.label, wx.Rect(2, 0, w-4, h), wx.ALIGN_CENTER)

    def MouseDown(self, event):
        pos = event.GetPosition()
        if self.outFunction:
            self.outFunction()
        self.Refresh()
        event.Skip()

#---------------------------
# PaletteToolBox (need a list of outFunctions axxociated with tools)
# --------------------------
class PaletteToolBox(wx.Panel):
    def __init__(self, parent, size=(90,20), tools=['random', 'waves', 'process'], outFunction=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour(TITLE_BACK_COLOUR)
        self.randomFrame = RandomFrame(self)
        self.wavesFrame = WavesFrame(self)
        self.processFrame = ProcessFrame(self)
        toolsLength = len(tools)
        if len(tools) == 0:
            raise('ToolBox must have at least a list of one tool!')
        self.num = len(tools)
        self.SetSize((30*self.num, 20))
        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())
        self.tools = tools
        self.maps = {'random': self.onRandom, 'waves': self.onWaves, 'process': self.onProcess}
        self.graphics = {'random': [ICON_PTB_RANDOM.GetBitmap(), ICON_PTB_RANDOM_OVER.GetBitmap()], 
                         'waves': [ICON_PTB_WAVES.GetBitmap(), ICON_PTB_WAVES_OVER.GetBitmap()],
                         'process': [ICON_PTB_PROCESS.GetBitmap(), ICON_PTB_PROCESS_OVER.GetBitmap()]}
        self.tooltips = {'random': TT_STOCHASTIC, 'waves': TT_WAVEFORM, 'process': TT_PROCESSOR}
        self.rectList = []
        for i in range(self.num):
            self.rectList.append(wx.Rect(i*30, 0, 30, self.GetSize()[1]))
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.selected = 0
        self.outFunction = outFunction
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

        tooltip = ''
        for tool in self.tools:
            tooltip += self.tooltips[tool] + '\n\n'
        self.SetToolTip(CECTooltip(tooltip))

    def setOverWait(self, which):
        self.oversWait[which] = False

    def checkForOverReady(self, pos):
        for i, rec in enumerate(self.rectList):
            if not rec.Contains(pos):
                self.oversWait[i] = True
                        
    def OnMotion(self, event):
        pos = event.GetPosition()
        self.overs = [False] * self.num
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos) and self.oversWait[i]:
                self.overs[i] = True
        self.checkForOverReady(pos)
        self.Refresh()
        event.Skip()

    def OnLeave(self, event):
        self.overs = [False] * self.num
        self.oversWait = [True] * self.num
        self.Refresh()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(TITLE_BACK_COLOUR, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(TITLE_BACK_COLOUR, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        for i, tool in enumerate(self.tools):
            if not self.overs[i]:
                icon = self.graphics[tool][0]
            else:
                icon = self.graphics[tool][1]
            dc.DrawBitmap(icon, self.rectList[i][0]+2, self.rectList[i][1]+1, True)
        dc.SetPen(wx.Pen(WHITE_COLOUR, width=1, style=wx.SOLID))  
        for i in range((self.num-1)):
            dc.DrawLine((i+1)*30, 2, (i+1)*30, h-2)

    def MouseDown(self, event):
        pos = event.GetPosition()
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos):
                tool = self.tools[i]
                self.selected = i
                self.setOverWait(i)
                break
        self.maps[tool]()
        self.Refresh()

    def checkForOpenFrame(self, index):
        if index != 0:
            self.randomFrame.Hide()
        if index != 1:
            self.wavesFrame.Hide()
        if index != 2:
            self.processFrame.Hide()

    def onRandom(self):
        self.checkForOpenFrame(0)
        off = self.GetScreenPosition()
        pos = (off[0]-200, off[1]+20)
        self.randomFrame.SetPosition(pos)
        self.randomFrame.Show()

    def onWaves(self):
        self.checkForOpenFrame(1)
        off = self.GetScreenPosition()
        pos = (off[0]-200, off[1]+20)
        self.wavesFrame.SetPosition(pos)
        self.wavesFrame.Show()

    def onProcess(self):
        self.checkForOpenFrame(2)
        off = self.GetScreenPosition()
        pos = (off[0]-200, off[1]+20)
        self.processFrame.SetPosition(pos)
        self.processFrame.Show()

    def checkForSelection(self, selected):
        if len(selected) >= 2:
            grapher = CeciliaLib.getVar("grapher")
            line = grapher.plotter.getLine(grapher.plotter.getSelected())
            minx = line.getData()[selected[0]][0] / CeciliaLib.getVar("totalTime")
            maxx = line.getData()[selected[-1]][0] / CeciliaLib.getVar("totalTime")
            addPointsBefore = [pt for i, pt in enumerate(line.normalize()) if i < selected[0]]
            addPointsAfter = [pt for i, pt in enumerate(line.normalize()) if i > selected[-1]]
        else:
            minx = 0
            maxx = 1 
            addPointsBefore = [] 
            addPointsAfter = []
        return minx, maxx, addPointsBefore, addPointsAfter

#---------------------------
# Grapher Palette frames (### classe parent ###)
# --------------------------
class RandomFrame(wx.Frame):
    def __init__(self, parent):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT )
        wx.Frame.__init__(self, parent, title='', style = style)
        self.parent = parent
        self.SetSize((300,233))
        if CeciliaLib.getVar("systemPlatform") == 'linux2':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()
        
        self.distList = ['Uniform', 'Gaussian', 'Weibull', 'Beta', 'Drunk', 'Loopseg', 'Repeater', 'DroneAndJump'] 
        self.interpList = ['Linear', 'Sample hold']
  
        panel = wx.Panel(self, -1)
        w, h = self.GetSize()
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)

        title = FrameLabel(panel, "STOCHASTIC GENERATOR", size=(w-2, 24))
        box.Add(title, 0, wx.ALL, 1)

        interpBox = wx.BoxSizer(wx.HORIZONTAL)
        interpLabel = wx.StaticText(panel, -1, "Interpolation")
        interpLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        interpLabel.SetForegroundColour(WHITE_COLOUR)
        interpBox.Add(interpLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 114)
        self.interpMenu = CustomMenu(panel, self.interpList, self.interpList[0])
        self.interpMenu.SetToolTip(CECTooltip(TT_STOCH_INTERP))
        interpBox.Add(self.interpMenu, 0, wx.LEFT | wx.RIGHT, 5)

        slidersBox = wx.FlexGridSizer(5, 2, 5, 5)

        ptsLabel = wx.StaticText(panel, -1, "Points")
        ptsLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        ptsLabel.SetForegroundColour(WHITE_COLOUR)
        self.ptsSlider = ControlSlider(panel, 5, 1000, 50, size=(236, 15), integer=True)
        self.ptsSlider.setSliderHeight(10)
        self.ptsSlider.SetToolTip(CECTooltip(TT_STOCH_POINTS))
        slidersBox.AddMany([(ptsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.ptsSlider, 0, wx.RIGHT, 5)])

        minLabel = wx.StaticText(panel, -1, "Min")
        minLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        minLabel.SetForegroundColour(WHITE_COLOUR)
        self.minSlider = ControlSlider(panel, 0, 1, 0, size=(236, 15))
        self.minSlider.setSliderHeight(10)
        self.minSlider.SetToolTip(CECTooltip(TT_STOCH_MIN))
        slidersBox.AddMany([(minLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.minSlider, 0, wx.RIGHT, 5)])

        maxLabel = wx.StaticText(panel, -1, "Max")
        maxLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        maxLabel.SetForegroundColour(WHITE_COLOUR)
        self.maxSlider = ControlSlider(panel, 0, 1, 1, size=(236, 15))
        self.maxSlider.setSliderHeight(10)
        self.maxSlider.SetToolTip(CECTooltip(TT_STOCH_MAX))
        slidersBox.AddMany([(maxLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.maxSlider, 0, wx.RIGHT, 5)])

        x1Label = wx.StaticText(panel, -1, "x1")
        x1Label.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        x1Label.SetForegroundColour(WHITE_COLOUR)
        self.x1Slider = ControlSlider(panel, 0, 1, .5, size=(236, 15))
        self.x1Slider.setSliderHeight(10)
        self.x1Slider.SetToolTip(CECTooltip(TT_STOCH_X1))
        slidersBox.AddMany([(x1Label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.x1Slider, 0, wx.RIGHT, 5)])

        x2Label = wx.StaticText(panel, -1, "x2")
        x2Label.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        x2Label.SetForegroundColour(WHITE_COLOUR)
        self.x2Slider = ControlSlider(panel, 0, 1, .5, size=(236, 15))
        self.x2Slider.setSliderHeight(10)
        self.x2Slider.SetToolTip(CECTooltip(TT_STOCH_X2))
        slidersBox.AddMany([(x2Label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.x2Slider, 0, wx.RIGHT, 5)])
        slidersBox.AddGrowableCol(1)

        distBox = wx.BoxSizer(wx.HORIZONTAL)
        distLabel = wx.StaticText(panel, -1, "Distribution")
        distLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        distLabel.SetForegroundColour(WHITE_COLOUR)
        distBox.Add(distLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 120)
        self.distMenu = CustomMenu(panel, self.distList, self.distList[0], outFunction=self.onDistribution)
        self.distMenu.SetToolTip(CECTooltip(TT_STOCH_TYPE))
        self.distMenu.setLabel(self.distMenu.getLabel(), True)
        distBox.Add(self.distMenu, 0, wx.LEFT | wx.RIGHT, 5)

        applyBox = wx.BoxSizer(wx.HORIZONTAL)
        applyer = ApplyToolBox(panel, outFunction=[self.OnClose, self.OnApply])
        applyBox.Add(applyer, 0, wx.LEFT, 195)

        box.Add(distBox, 0, wx.ALL, 5)
        box.Add(interpBox, 0, wx.ALL, 5)
        box.Add(slidersBox, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(applyBox, 0, wx.TOP, 15)
        box.AddSpacer(10)

        panel.SetSizerAndFit(box)

        panel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        title.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

    def OnLooseFocus(self, event):
        win = wx.FindWindowAtPointer()
        if win != None:
            if win.GetTopLevelParent() == self:
                pass
            else:
                win = CeciliaLib.getVar("interface")
                win.Raise()

    def SetRoundShape(self, event=None):
        self.SetShape(GetRoundShape(300, 233, 1))
     
    def OnClose(self):
        self.Hide()

    def onDistribution(self, ind, label):
        if label == 'Uniform':
            self.x1Slider.setEnable(False)
            self.x2Slider.setEnable(False)
        else:
            self.x1Slider.setEnable(True)
            self.x2Slider.setEnable(True)

    def OnApply(self):
        dist = self.distMenu.getLabel()
        interp = self.interpMenu.getLabel()
        points = self.ptsSlider.GetValue()
        mini = self.minSlider.GetValue()
        maxi = self.maxSlider.GetValue()
        x1 = self.x1Slider.GetValue()
        x2 = self.x2Slider.GetValue()
        if dist == 'Uniform':
            dict = self.uniformGenerate(interp, points, mini, maxi)
        elif dist == 'Gaussian':
            dict = self.gaussGenerate(interp, points, mini, maxi, x1, x2)
        elif dist == 'Weibull':
            dict = self.weibullGenerate(interp, points, mini, maxi, x1, x2)
        elif dist == 'Beta':
            dict = self.betaGenerate(interp, points, mini, maxi, x1, x2)
        elif dist in ['Drunk', 'Loopseg']:
            dict = self.drunkGenerate(interp, points, mini, maxi, x1, x2, dist)
        elif dist in ['Repeater', 'DroneAndJump']:
            dict = self.repeatGenerate(interp, points, mini, maxi, x1, x2, dist)
        line = CeciliaLib.getVar("grapher").plotter.getLine(CeciliaLib.getVar("grapher").plotter.getSelected())
        line.setLineState(dict)
        line.setShow(1)
        CeciliaLib.getVar("grapher").toolbar.toolbox.setShow(1)
        if line.getSlider() != None:
            line.getSlider().setPlay(1)
        CeciliaLib.getVar("grapher").plotter.draw()
    
    def uniformGenerate(self, interp, points, mini, maxi):
        templist = []
        step = 1. / (points - 1)
        if interp == 'Linear':
            for i in range(points):
                x = i * step
                y = random.uniform(mini, maxi)
                templist.append([x, y])
        elif interp == 'Sample hold':
            for i in range(points):
                x = i * step
                y = random.uniform(mini, maxi)
                templist.append([x, y])
                if i != points-1:
                    xx = (i+1) * step
                    templist.append([xx,y])
        return {'data': templist}

    def gaussGenerate(self, interp, points, mini, maxi, x1, x2):
        templist = []
        step = 1. / (points - 1)
        x1 = x1 * .5
        if interp == 'Linear':
            for i in range(points):
                x = i * step
                y = random.gauss(x2, x1)
                if y < mini: y = mini
                elif y > maxi: y = maxi
                templist.append([x, y])
        if interp == 'Sample hold':
            for i in range(points):
                x = i * step
                y = random.gauss(x2, x1)
                if y < mini: y = mini
                elif y > maxi: y = maxi
                templist.append([x, y])
                if i != points-1:
                    xx = (i+1) * step
                    templist.append([xx,y])
        return {'data': templist}

    def weibullGenerate(self, interp, points, mini, maxi, x1, x2):
        templist = []
        step = 1. / (points - 1)
        x1 = x1 * 10
        if interp == 'Linear':
            for i in range(points):
                x = i * step
                y = random.weibullvariate(x2, x1)
                if y < mini: y = mini
                elif y > maxi: y = maxi
                templist.append([x, y])
        if interp == 'Sample hold':
            for i in range(points):
                x = i * step
                y = random.weibullvariate(x2, x1)
                if y < mini: y = mini
                elif y > maxi: y = maxi
                templist.append([x, y])
                if i != points-1:
                    xx = (i+1) * step
                    templist.append([xx,y])
        return {'data': templist}
    
    def betaGenerate(self, interp, points, mini, maxi, x1, x2):
        templist = []
        step = 1. / (points - 1)
        x1 = x1 * 10 + .001
        x2 = x2 * 10 + .001
        if interp == 'Linear':
            for i in range(points):
                x = i * step
                y = random.betavariate(x2, x1)
                if y < mini: y = mini
                elif y > maxi: y = maxi
                templist.append([x, y])
        if interp == 'Sample hold':
            for i in range(points):
                x = i * step
                y = random.betavariate(x2, x1)
                if y < mini: y = mini
                elif y > maxi: y = maxi
                templist.append([x, y])
                if i != points-1:
                    xx = (i+1) * step
                    templist.append([xx,y])
        return {'data': templist}

    def drunkGenerate(self, interp, points, mini, maxi, x1, x2, dist):
        templist = []
        step = 1. / (points - 1)
        minimum = int(mini * 1000)
        maximum = int(maxi * 1000)
        if maximum < minimum:
            tmp = minimum
            minimum = maximum
            maximum = tmp
        if dist == 'Drunk':    
            drunk = Drunk(minimum, maximum)
        elif dist == 'Loopseg':
            drunk = Loopseg(minimum, maximum)    
        drunk.setLastValue(int(x1*(maximum-minimum)+minimum))
        stepsize = -int((x2*0.5*(maximum-minimum)))    
        if interp == 'Linear':
            templist.append([0, (x1*(maximum-minimum)+minimum)*0.001])
            for i in range(1, points):
                x = i * step
                y = drunk.next(stepsize) * 0.001
                if y < mini: y = mini
                elif y > maxi: y = maxi
                templist.append([x, y])
        if interp == 'Sample hold':
            templist.append([0, (x1*(maximum-minimum)+minimum)*0.001])
            templist.append([step, (x1*(maximum-minimum)+minimum)*0.001])
            for i in range(1, points):
                x = i * step
                y = drunk.next(stepsize) * 0.001
                if y < mini: y = mini
                elif y > maxi: y = maxi
                templist.append([x, y])
                if i != points-1:
                    xx = (i+1) * step
                    templist.append([xx,y])
        return {'data': templist}

    def repeatGenerate(self, interp, points, mini, maxi, x1, x2, dist):
        templist = []
        step = 1. / (points - 1)
        minimum = int(mini * 1000)
        maximum = int(maxi * 1000)
        if maximum < minimum:
            tmp = minimum
            minimum = maximum
            maximum = tmp
        if dist == 'Repeater':    
            drunk = Repeater(minimum, maximum)
        elif dist == 'DroneAndJump':
            drunk = DroneAndJump(minimum, maximum)    
        drunk.setLastValue(int(x1*(maximum-minimum)+minimum))
        stepsize = -int((x2*0.5*(maximum-minimum))) 
        last_y = (x1*(maximum-minimum)+minimum)*0.001    
        if interp == 'Linear':
            templist.append([0.0, last_y])
            for i in range(1, points):
                x = i * step
                y = drunk.next(stepsize) * 0.001
                if y < mini: y = mini
                elif y > maxi: y = maxi
                if y == templist[-1][1]:
                    continue
                templist.append([x, y])
        if interp == 'Sample hold':
            templist.append([0, last_y])
            for i in range(1, points):
                x = i * step
                y = drunk.next(stepsize) * 0.001
                if y < mini: y = mini
                elif y > maxi: y = maxi
                if y == last_y:
                    continue
                if i != points-1 and i != 0:
                    templist.append([x,last_y])
                templist.append([x, y])
                last_y = y
        if templist[-1][0] != 1.0:
            templist.append([1.0, last_y])        
        return {'data': templist}

class WavesFrame(wx.Frame):
    def __init__(self, parent):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT )
        wx.Frame.__init__(self, parent, title='', style = style)
        self.parent = parent
        self.SetSize((300,205))
        if CeciliaLib.getVar("systemPlatform") == 'linux2':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()

        self.distList = ['Sine', 'Square', 'Sawtooth'] 
  
        panel = wx.Panel(self, -1)
        w, h = self.GetSize()
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)

        title = FrameLabel(panel, "WAVEFORM GENERATOR", size=(w-2, 24))
        box.Add(title, 0, wx.ALL, 1)

        slidersBox = wx.FlexGridSizer(5, 2, 5, 5)

        ptsLabel = wx.StaticText(panel, -1, "Points")
        ptsLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        ptsLabel.SetForegroundColour(WHITE_COLOUR)
        self.ptsSlider = ControlSlider(panel, 5, 1000, 50, size=(227, 15), integer=True)
        self.ptsSlider.setSliderHeight(10)
        self.ptsSlider.SetToolTip(CECTooltip(TT_WAVE_POINTS))
        slidersBox.AddMany([(ptsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.ptsSlider, 0, wx.RIGHT, 5)])

        ampLabel = wx.StaticText(panel, -1, "Amp")
        ampLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        ampLabel.SetForegroundColour(WHITE_COLOUR)
        self.ampSlider = ControlSlider(panel, 0, 1, 1, size=(227, 15))
        self.ampSlider.setSliderHeight(10)
        self.ampSlider.SetToolTip(CECTooltip(TT_WAVE_AMP))
        slidersBox.AddMany([(ampLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.ampSlider, 0, wx.RIGHT, 5)])

        freqLabel = wx.StaticText(panel, -1, "Freq")
        freqLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        freqLabel.SetForegroundColour(WHITE_COLOUR)
        self.freqSlider = ControlSlider(panel, 0, 100, 1, size=(227, 15))
        self.freqSlider.setSliderHeight(10)
        self.freqSlider.SetToolTip(CECTooltip(TT_WAVE_FREQ))
        slidersBox.AddMany([(freqLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.freqSlider, 0, wx.RIGHT, 5)])

        phaseLabel = wx.StaticText(panel, -1, "Phase")
        phaseLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        phaseLabel.SetForegroundColour(WHITE_COLOUR)
        self.phaseSlider = ControlSlider(panel, 0, 1, 0, size=(227, 15))
        self.phaseSlider.setSliderHeight(10)
        self.phaseSlider.SetToolTip(CECTooltip(TT_WAVE_PHASE))
        slidersBox.AddMany([(phaseLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.phaseSlider, 0, wx.RIGHT, 5)])

        widthLabel = wx.StaticText(panel, -1, "Width")
        widthLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        widthLabel.SetForegroundColour(WHITE_COLOUR)
        self.widthSlider = ControlSlider(panel, 0, 1, .5, size=(227, 15))
        self.widthSlider.setSliderHeight(10)
        self.widthSlider.SetToolTip(CECTooltip(TT_WAVE_WIDTH))
        slidersBox.AddMany([(widthLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.widthSlider, 0, wx.RIGHT, 5)])
        slidersBox.AddGrowableCol(1)

        distBox = wx.BoxSizer(wx.HORIZONTAL)
        distLabel = wx.StaticText(panel, -1, "Shape")
        distLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        distLabel.SetForegroundColour(WHITE_COLOUR)
        distBox.Add(distLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 137)
        self.distMenu = CustomMenu(panel, self.distList, self.distList[0], outFunction=self.onDistribution)
        self.distMenu.setLabel(self.distMenu.getLabel(), True)
        self.distMenu.SetToolTip(CECTooltip(TT_WAVE_SHAPE))
        distBox.Add(self.distMenu, 0, wx.LEFT | wx.RIGHT, 5)

        applyBox = wx.BoxSizer(wx.HORIZONTAL)
        apply = ApplyToolBox(panel, outFunction=[self.OnClose, self.OnApply])
        applyBox.Add(apply, 0, wx.LEFT, 195)

        box.Add(distBox, 0, wx.ALL, 5)
        box.Add(slidersBox, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(applyBox, 0, wx.TOP, 15)
        box.AddSpacer(10)

        panel.SetSizerAndFit(box)

        panel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        title.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

    def OnLooseFocus(self, event):
        win = wx.FindWindowAtPointer()
        if win != None:
            if win.GetTopLevelParent() == self:
                pass
            else:
                win = CeciliaLib.getVar("interface")
                win.Raise()

    def SetRoundShape(self, event=None):
        self.SetShape(GetRoundShape(300, 205, 1))

    def OnClose(self):
        self.Hide()

    def onDistribution(self, ind, label):
        if label == 'Sine':
            self.ptsSlider.setEnable(True)
            self.widthSlider.setEnable(False)
        elif label == 'Sawtooth':
            self.ptsSlider.setEnable(False)
            self.widthSlider.setEnable(False)
        elif label == 'Square':
            self.ptsSlider.setEnable(False)
            self.widthSlider.setEnable(True)

    def OnApply(self):
        dist = self.distMenu.getLabel()
        points = self.ptsSlider.GetValue()
        amp = self.ampSlider.GetValue()
        freq = self.freqSlider.GetValue()
        phase = self.phaseSlider.GetValue()
        width = self.widthSlider.GetValue()
        if dist == 'Sine':
            dict = self.sineGenerate(points, amp, freq, phase)
        elif dist == 'Square':
            dict = self.squareGenerate(points, amp, freq, phase, width)
        elif dist == 'Sawtooth':
            dict = self.sawtoothGenerate(points, amp, freq, phase)
        line = CeciliaLib.getVar("grapher").plotter.getLine(CeciliaLib.getVar("grapher").plotter.getSelected())
        line.setLineState(dict)
        line.setShow(1)
        CeciliaLib.getVar("grapher").toolbar.toolbox.setShow(1)
        if line.getSlider() != None:
            line.getSlider().setPlay(1)
        CeciliaLib.getVar("grapher").plotter.draw()
 
    def sineGenerate(self, points, amp, freq, phase):
        selected = CeciliaLib.getVar("grapher").plotter.selectedPoints
        minx, maxx, addPointsBefore, addPointsAfter = self.parent.checkForSelection(selected)
             
        templist = []
        step = 1. / (points - 1)
        A = amp * .5
        w = 2 * math.pi * freq
        ph = phase * 2 * math.pi
        
        if addPointsBefore:
            templist.extend(addPointsBefore)
            
        for i in range(points):
            inc = i * step
            x = inc * (maxx-minx) + minx
            y = A * math.sin(w * inc + ph) + .5
            templist.append([x, y])

        if addPointsAfter:
            templist.extend(addPointsAfter)

        CeciliaLib.getVar("grapher").plotter.resetSelectedPoints()
        return {'data': templist}

    def squareGenerate(self, points, amp, freq, phase, width):
        selected = CeciliaLib.getVar("grapher").plotter.selectedPoints
        minx, maxx, addPointsBefore, addPointsAfter = self.parent.checkForSelection(selected)

        templist = []
        step = 1. / (freq)
        A = amp * .5   
        if int(freq) == freq: length = int(freq)
        else: length = int(freq) + 1 

        if phase >= .5: A = -A

        if addPointsBefore:
            templist.extend(addPointsBefore)

        for i in range(length):
            inc = i * step
            x = inc * (maxx-minx) + minx
            y = .5 + A
            templist.append([x, y])
            x = inc * (maxx-minx) + minx + (step * (maxx-minx) * width)
            if x > 1: 
                x = 1
                templist.append([x, y])
                break
            else:
                templist.append([x, y])
            x = inc * (maxx-minx) + minx + (step * (maxx-minx) * width)
            y = .5 - A
            templist.append([x, y])
            x = (i+1) * step * (maxx-minx) + minx
            if x > 1:
                x = 1
                templist.append([x, y])
                break
            else:
                templist.append([x, y])

        if addPointsAfter:
            templist.extend(addPointsAfter)

        CeciliaLib.getVar("grapher").plotter.resetSelectedPoints()
        return {'data': templist}

    def sawtoothGenerate(self, points, amp, freq, phase):
        selected = CeciliaLib.getVar("grapher").plotter.selectedPoints
        minx, maxx, addPointsBefore, addPointsAfter = self.parent.checkForSelection(selected)

        templist = []
        step = 1. / (freq)
        A = amp * .5   
        if int(freq) == freq: length = int(freq)
        else: length = int(freq) + 1 

        if phase >= .5: A = -A

        if addPointsBefore:
            templist.extend(addPointsBefore)

        for i in range(length):
            inc = i * step
            x = inc * (maxx-minx) + minx
            y = .5 + A
            templist.append([x, y])
            x = (i+1) * step * (maxx-minx) + minx
            y = .5 - A
            if x > 1:
                gap = step - (x - 1)
                if A >= 0:
                    y = y + gap
                else:
                    y = y - (y * gap)
                x = 1
                templist.append([x, y])
                break
            else:
                templist.append([x, y])

        if addPointsAfter:
            templist.extend(addPointsAfter)

        CeciliaLib.getVar("grapher").plotter.resetSelectedPoints()
        return {'data': templist}

class ProcessFrame(wx.Frame):
    def __init__(self, parent):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.NO_BORDER | wx.FRAME_FLOAT_ON_PARENT )
        wx.Frame.__init__(self, parent, title='', style = style)
        self.parent = parent
        self.SetSize((300,235))
        if CeciliaLib.getVar("systemPlatform") == 'linux2':
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetRoundShape)
        else:
            self.SetRoundShape()

        self.distList = ['Scatter', 'Jitter', 'Comp/Expand']
        self.interpList = ['Linear', 'Sample hold'] 
        self._oldState = None
        self._oldSelected = None

        panel = wx.Panel(self, -1)
        w, h = self.GetSize()
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box = wx.BoxSizer(wx.VERTICAL)

        title = FrameLabel(panel, "FUNCTION PROCESSOR", size=(w-2, 24))
        box.Add(title, 0, wx.ALL, 1)

        slidersBox = wx.FlexGridSizer(5, 2, 5, 5)

        interpBox = wx.BoxSizer(wx.HORIZONTAL)
        interpLabel = wx.StaticText(panel, -1, "Interpolation")
        interpLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        interpLabel.SetForegroundColour(WHITE_COLOUR)
        interpBox.Add(interpLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 103)
        self.interpMenu = CustomMenu(panel, self.interpList, self.interpList[0])
        interpBox.Add(self.interpMenu, 0, wx.LEFT | wx.RIGHT, 5)

        ptsLabel = wx.StaticText(panel, -1, "Points")
        ptsLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        ptsLabel.SetForegroundColour(WHITE_COLOUR)
        self.ptsSlider = ControlSlider(panel, 5, 1000, 50, size=(215, 15), integer=True)
        self.ptsSlider.setSliderHeight(10)
        slidersBox.AddMany([(ptsLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.ptsSlider, 0, wx.RIGHT, 5)])

        self.scatXLabel = wx.StaticText(panel, -1, "Scatt X")
        self.scatXLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        self.scatXLabel.SetForegroundColour(WHITE_COLOUR)
        self.scatXSlider = ControlSlider(panel, 0, 0.5, 0.005, size=(215, 15))
        self.scatXSlider.setFloatPrecision(3)
        self.scatXSlider.setSliderHeight(10)
        slidersBox.AddMany([(self.scatXLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.scatXSlider, 0, wx.RIGHT, 5)])

        self.scatYLabel = wx.StaticText(panel, -1, "Scatt Y")
        self.scatYLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        self.scatYLabel.SetForegroundColour(WHITE_COLOUR)
        self.scatYSlider = ControlSlider(panel, 0, 0.5, 0.05, size=(215, 15))
        self.scatYSlider.setFloatPrecision(3)
        self.scatYSlider.setSliderHeight(10)
        slidersBox.AddMany([(self.scatYLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.scatYSlider, 0, wx.RIGHT, 5)])

        offXLabel = wx.StaticText(panel, -1, "Offset X")
        offXLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        offXLabel.SetForegroundColour("#FFFFFF")
        self.offXSlider = ControlSlider(panel, -0.5, 0.5, 0, size=(215, 15))
        self.offXSlider.setFloatPrecision(3)
        self.offXSlider.setSliderHeight(10)
        slidersBox.AddMany([(offXLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.offXSlider, 0, wx.RIGHT, 5)])

        offYLabel = wx.StaticText(panel, -1, "Offset Y")
        offYLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        offYLabel.SetForegroundColour("#FFFFFF")
        self.offYSlider = ControlSlider(panel, -0.5, 0.5, 0, size=(215, 15))
        self.offYSlider.setFloatPrecision(3)
        self.offYSlider.setSliderHeight(10)
        slidersBox.AddMany([(offYLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.RIGHT | wx.LEFT, 5),
                            (self.offYSlider, 0, wx.RIGHT, 5)])

        distBox = wx.BoxSizer(wx.HORIZONTAL)
        distLabel = wx.StaticText(panel, -1, "Processor")
        distLabel.SetFont(wx.Font(TEXT_LABELFORWIDGET_FONT, wx.NORMAL, wx.NORMAL, wx.NORMAL, face=FONT_FACE))
        distLabel.SetForegroundColour(WHITE_COLOUR)
        distBox.Add(distLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 119)
        self.distMenu = CustomMenu(panel, self.distList, self.distList[0], outFunction=self.onDistribution)
        self.distMenu.SetToolTip(CECTooltip(TT_STOCH_TYPE))
        self.distMenu.setLabel(self.distMenu.getLabel(), True)
        distBox.Add(self.distMenu, 0, wx.LEFT | wx.RIGHT, 5)

        applyBox = wx.BoxSizer(wx.HORIZONTAL)
        apply = ApplyToolBox(panel, outFunction=[self.OnClose, self.OnApply])
        applyBox.Add(apply, 0, wx.LEFT, 195)

        box.Add(distBox, 0, wx.ALL, 5)
        box.Add(interpBox, 0, wx.ALL, 5)
        box.Add(slidersBox, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(applyBox, 0, wx.TOP, 15)
        box.AddSpacer(10)

        panel.SetSizerAndFit(box)

        panel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)
        title.Bind(wx.EVT_LEAVE_WINDOW, self.OnLooseFocus)

    def OnLooseFocus(self, event):
        win = wx.FindWindowAtPointer()
        if win != None:
            if win.GetTopLevelParent() == self:
                pass
            else:
                win = CeciliaLib.getVar("interface")
                win.Raise()

    def SetRoundShape(self, event=None):
        self.SetShape(GetRoundShape(300, 235, 1))

    def OnClose(self):
        self._oldState = None
        self.Hide()

    def onDistribution(self, ind, label):
        if label == 'Scatter':
            self.ptsSlider.setEnable(False)
            self.offXSlider.setEnable(False)
            self.offYSlider.setEnable(False)
            self.scatXLabel.SetLabel('Scatt X')
            self.scatYLabel.SetLabel('Scatt Y')
            self.scatXSlider.SetRange(0, 0.5)
            self.scatXSlider.SetValue(0.005)
            self.scatYSlider.SetRange(0, 0.5)
            self.scatYSlider.SetValue(0.05)
        elif label == 'Jitter':
            self.ptsSlider.setEnable(True)
            self.offXSlider.setEnable(False)
            self.offYSlider.setEnable(False)
            self.scatXLabel.SetLabel('Jitte X')
            self.scatYLabel.SetLabel('Jitte Y')
            self.scatXSlider.SetRange(0, 0.5)
            self.scatXSlider.SetValue(0.005)
            self.scatYSlider.SetRange(0, 0.5)
            self.scatYSlider.SetValue(0.05)
        elif label == 'Comp/Expand':
            self.ptsSlider.setEnable(False)
            self.offXSlider.setEnable(True)
            self.offYSlider.setEnable(True)
            self.scatXLabel.SetLabel('Comp X')
            self.scatYLabel.SetLabel('Comp Y')
            self.scatXSlider.SetRange(0., 2.)
            self.scatXSlider.SetValue(1.)
            self.scatYSlider.SetRange(0., 2.)
            self.scatYSlider.SetValue(1.)
        self._oldState = None    
            
    def OnApply(self):
        line = CeciliaLib.getVar("grapher").plotter.getSelected()
        if self._oldSelected != line or self._oldState == None:
            self.data = CeciliaLib.getVar("grapher").plotter.getLine(CeciliaLib.getVar("grapher").plotter.getSelected()).getLineState()['data']
            self._oldSelected = line
            self._oldState = self.data
        elif self._oldSelected == line and self._oldState != None:
            self.data = self._oldState
        dist = self.distMenu.getLabel()
        interp = self.interpMenu.getLabel()
        points = self.ptsSlider.GetValue()
        scatX = self.scatXSlider.GetValue()
        scatY = self.scatYSlider.GetValue()
        offX = self.offXSlider.GetValue()
        offY = self.offYSlider.GetValue()
        if dist == 'Scatter':
            dict = self.processScattering(interp, scatX, scatY)
        elif dist == 'Jitter':
            dict = self.processJittering(interp, points, scatX, scatY)
        elif dist == 'Comp/Expand':    
            dict = self.processCompExpand(dist, points, scatX, scatY, offX, offY)
        line = CeciliaLib.getVar("grapher").plotter.getLine(CeciliaLib.getVar("grapher").plotter.getSelected())
        line.setLineState(dict)
        line.setShow(1)
        CeciliaLib.getVar("grapher").toolbar.toolbox.setShow(1)
        if line.getSlider() != None:
            line.getSlider().setPlay(1)
        CeciliaLib.getVar("grapher").plotter.draw()

    def processScattering(self, interp, scatX, scatY):
        selected = CeciliaLib.getVar("grapher").plotter.selectedPoints
        minx, maxx, addPointsBefore, addPointsAfter = self.parent.checkForSelection(selected)

        data = copy.deepcopy(self.data)
        dataLen = len(data)
        step = 1. / dataLen
        templist = []

        if addPointsBefore or addPointsAfter:
            templist.extend(addPointsBefore)
            istart, istop = selected[0], selected[-1]
        else:
            istart, istop = 0, dataLen-1    

        for i in range(istart, istop):
            x = data[i][0]
            y = data[i][1]
            lastY = y
            if i == 0:
                newX = x
            else:    
                newX = x + (random.uniform(-scatX, scatX) * step) 
            if newX < 0: newX = 0
            elif newX > 1: newX = 1
            try:
                if newX < templist[-1][0]: newX = templist[-1][0]
            except:
                pass
            newY = y + random.uniform(-scatY, scatY)
            if newY < 0: newY = 0
            elif newY > 1: newY = 1
            if interp == 'Sample hold':
                if i != 0:
                    templist.append([newX, templist[-1][1]])
                else:    
                    templist.append([newX,lastY])
            lastY = newY 
            templist.append([newX, newY])                    

        if addPointsAfter:
            if interp == 'Sample hold':
                templist.append([addPointsAfter[0][0], lastY])
            templist.extend(addPointsAfter)
        else:
            if interp == 'Sample hold':
                templist.append([data[-1][0], lastY])
            else:    
                templist.append(data[-1])
            
        CeciliaLib.getVar("grapher").plotter.resetSelectedPoints()
        return {'data': templist}
    
    def processJittering(self, interp, points, scatX, scatY):
        selected = CeciliaLib.getVar("grapher").plotter.selectedPoints
        minx, maxx, addPointsBefore, addPointsAfter = self.parent.checkForSelection(selected)

        data = copy.deepcopy(self.data)
        dataLen = len(data)
        templist = []

        if addPointsBefore or addPointsAfter:
            templist.extend(addPointsBefore)
            istart, istop = selected[0], selected[-1]
            totalLen = data[istop][0] - data[istart][0]
        else:
            istart, istop = 0, dataLen-1 
            totalLen = 1   

        for i in range(istart, istop):
            x = data[i][0]
            y = data[i][1]
            lastY = y
            x2 = data[i+1][0]
            y2 = data[i+1][1]
            distance = x2 - x
            numStep = int(points * distance / totalLen)
            step = distance / numStep
            for j in range(numStep):
                if j == 0 and i == 0:
                    newX = x
                else:    
                    newX = x + ((step * j) + (random.uniform(-scatX, scatX) * step))
                if newX < 0: newX = 0
                elif newX > 1: newX = 1
                try:
                    if newX < templist[-1][0]: newX = templist[-1][0]
                except:
                    pass
                ydiff = y2-y
                if ydiff == 0:
                    newY = y + random.uniform(-scatY, scatY)
                else:
                    newY = (y + ((y2-y) / numStep * j)) + random.uniform(-scatY, scatY)
                if newY < 0: newY = 0
                elif newY > 1: newY = 1
                if interp == 'Sample hold':
                    if j == 0 and i != 0:
                        templist.append([newX, templist[-1][1]])
                    else:    
                        templist.append([newX,lastY])
                lastY = newY 
                templist.append([newX, newY])                    

        if addPointsAfter:
            if interp == 'Sample hold':
                templist.append([addPointsAfter[0][0], lastY])
            templist.extend(addPointsAfter)
        else:
            if interp == 'Sample hold':
                templist.append([data[-1][0], lastY])
            else:    
                templist.append(data[-1])

        CeciliaLib.getVar("grapher").plotter.resetSelectedPoints()
        return {'data': templist}

    def processCompExpand(self, dist, points, scatX, scatY, offX, offY):
        selected = CeciliaLib.getVar("grapher").plotter.selectedPoints
        minx, maxx, addPointsBefore, addPointsAfter = self.parent.checkForSelection(selected)

        data = copy.deepcopy(self.data)
        dataLen = len(data)
        templist = []

        if addPointsBefore or addPointsAfter:
            templist.extend(addPointsBefore)
            istart, istop = selected[0], selected[-1]
        else:
            istart, istop = 0, dataLen

        ylist = [d[1] for d in data][istart: istop]
        minY = min(ylist)
        maxY = max(ylist)
        midY = (maxY-minY) * 0.5 + minY
        if addPointsBefore:
            if scatX != 1.0 or offX != 0.0:
                templist.append(data[selected[0]])
        else:    
            if scatX != 1.0 or offX != 0.0:
                templist.append(data[0])
        for i in range(istart, istop):
            x = data[i][0]
            y = data[i][1]
            newX = 0.5 + (x - 0.5) * scatX + offX
            if newX < 0: newX = 0.
            elif newX > 1: newX = 1.
            try:
                if newX < templist[-1][0]: newX = templist[-1][0]
            except:
                pass
                  
            newY = midY + (y - midY) * scatY + offY
            if newY < 0: newY = 0.
            elif newY > 1: newY = 1.
            templist.append([newX, newY])
            
        if addPointsAfter:
            if scatX != 1.0 or offX != 0.0:
                templist.append([addPointsAfter[0][0], templist[-1][1]])
            templist.extend(addPointsAfter)
        else:    
            if scatX != 1.0 or offX != 0.0:
                templist[0] = [0.0, templist[1][1]]
                templist.append([1.0, templist[-1][1]])
            
        CeciliaLib.getVar("grapher").plotter.resetSelectedPoints()
        return {'data': templist}

#---------------------------
# Transport
# --------------------------
class Transport(wx.Panel):
    def __init__(self, parent, size=(90,30), outPlayFunction=None, 
                 outRecordFunction=None, backgroundColour=None, borderColour=None):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        if backgroundColour: self.backgroundColour = backgroundColour
        else: self.backgroundColour = BACKGROUND_COLOUR
        self.SetBackgroundColour(self.backgroundColour)
        if borderColour: self.borderColour = borderColour
        else: self.borderColour = BACKGROUND_COLOUR
        self.SetMaxSize(self.GetSize())
        self.rectList = []
        for i in range(2):
            self.rectList.append(wx.Rect(i*45, 0, 40, self.GetSize()[1]))

        self.outPlayFunction = outPlayFunction
        self.outRecordFunction = outRecordFunction
        self.playOver = False
        self.recordOver = False
        self.playOverWait = True
        self.recordOverWait = True

        self.playColour = TR_PLAY_NORMAL_COLOUR
        self.recordColour = TR_RECORD_OFF_COLOUR
        self.playing = False
        self.recording = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.MouseUp)

        self.SetToolTip(CECTooltip(TT_PLAY + '\n\n' + TT_RECORD))
        
    def setPlay(self, play):
        self.playing = play
        self.Refresh()

    def getPlay(self):
        return self.playing

    def onPlay(self):
        if not self.playing:
            if self.getRecord():
                self.setRecord(False)

    def setRecord(self, record):
        self.recording = record
        if not self.recording:
            self.recordColour = TR_RECORD_OFF_COLOUR
        else:
            self.recordColour = TR_RECORD_ON_COLOUR
        self.Refresh()
    
    def getRecord(self):
        return self.recording

    def onRecord(self):
        if self.recording:
            if not self.getPlay():
                self.setPlay(True)
        else:
            if self.getPlay():
                self.setPlay(False)

    def OnMotion(self, event):
        pos = event.GetPosition()
        if self.rectList[0].Contains(pos) and self.playOverWait:
            self.rewindOver = False
            self.playOver = True
            self.recordOver = False
        elif self.rectList[1].Contains(pos) and self.recordOverWait:
            self.rewindOver = False
            self.playOver = False
            self.recordOver = True
        self.checkForOverReady(pos)
        self.Refresh()
        event.Skip()

    def setOverWait(self, which):
        if which == 0:
            self.playOverWait = False
        elif which == 1:
            self.recordOverWait = False

    def checkForOverReady(self, pos):
        if not self.rectList[0].Contains(pos):
            self.playOverWait = True
        if not self.rectList[1].Contains(pos):
            self.recordOverWait = True
                        
    def MouseDown(self, event):
        pos = event.GetPosition()
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos):
                if i == 0:
                    self.playColour = TR_PLAY_CLICK_COLOUR
                    self.playOver = False
                elif i == 1 and not self.playing:
                    if not self.recording:
                        self.recording = True
                        self.recordColour = TR_RECORD_ON_COLOUR
                    else:
                        self.recording = False
                        self.recordColour = TR_RECORD_OFF_COLOUR
                    self.recordOver = False
                    self.onRecord()
                    if self.outRecordFunction:
                        self.outRecordFunction(self.recording)
                self.setOverWait(i)
                break
        self.Refresh()
        event.Skip()

    def MouseUp(self, event):
        pos = event.GetPosition()
        for i, rec in enumerate(self.rectList):
            if rec.Contains(pos):
                if i == 0:
                    if not self.playing:
                        self.playing = True
                    else:
                        self.playing = False
                    self.playColour = TR_PLAY_NORMAL_COLOUR
                    self.playOver = False
                    self.onPlay()
                    if self.outPlayFunction:
                        self.outPlayFunction(self.playing)
                break
        self.Refresh()

    def OnLeave(self, event):
        self.playOver = False
        self.recordOver = False
        self.playOverWait = True
        self.recordOverWait = True
        self.Refresh()
        event.Skip()

    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)

        dc.SetBrush(wx.Brush(self.backgroundColour, wx.SOLID))
        dc.Clear()

        # Draw background
        dc.SetPen(wx.Pen(self.backgroundColour, width=0, style=wx.SOLID))
        dc.DrawRectangle(0, 0, w, h)

        # Draw play/stop
        if self.playOver:
            penWidth = 2
            offStopX = 13
            offStopY = 8
            offPlayX = 13
            offPlayY = 7
        else:
            penWidth = 1
            offStopX = 14
            offStopY = 9
            offPlayX = 14
            offPlayY = 9
        x, y, w1, h1 = self.rectList[0].Get()
        rec = wx.Rect(x+1, y+1, w1-2, h1-2)
        dc.SetPen(wx.Pen(TR_BORDER_COLOUR, 1))
        dc.SetBrush(wx.Brush(TR_BACK_COLOUR))
        dc.DrawRoundedRectangleRect(rec, 4)

        dc.SetBrush(wx.Brush(self.playColour, wx.SOLID))
        if not self.playing:
            dc.DrawPolygon([(x+offPlayX,y+offPlayY), (x+offPlayX,h1-offPlayY), (x+w1-offPlayX,h1/2)])
        else:
            dc.DrawRoundedRectangle(x+offStopX, y+offStopY, w1-(offStopX*2), h1-(offStopY*2), 3)

        # Draw record
        if self.recordOver and not self.playing:
            penWidth = 2
            radius = 7
        else:
            penWidth = 1
            radius = 6
        x, y, w1, h1 = self.rectList[1].Get()
        rec = wx.Rect(x+1, y+1, w1-2, h1-2)
        dc.SetPen(wx.Pen(TR_BORDER_COLOUR, 1))
        dc.SetBrush(wx.Brush(TR_BACK_COLOUR))
        dc.DrawRoundedRectangleRect(rec, 4)

        dc.SetBrush(wx.Brush(self.recordColour, wx.SOLID))
        dc.DrawCircle(x+(w1/2), h1/2, radius)

#---------------------------
# VuMeter
# --------------------------
class VuMeter(wx.Panel):
    def __init__(self, parent, size=(218,11)):
        wx.Panel.__init__(self, parent, -1, size=size)
        self.parent = parent
        self.SetMinSize((218,6))
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.SetBackgroundColour("#000000")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.nchnls = CeciliaLib.getVar("nchnls")
        self.SetSize((218, 5*self.nchnls+1))
        self.SetMaxSize((218, 5*self.nchnls+1))
        self.bitmap = ICON_VUMETER.GetBitmap()
        self.backBitmap = ICON_VUMETER_DARK.GetBitmap()
        self.amplitude = [0] * self.nchnls
        self.oldChnls = 1
        self.peak = 0
 
    def updateNchnls(self):
        self.nchnls = CeciliaLib.getVar("nchnls")
        self.amplitude = [0] * self.nchnls
        gap = (self.nchnls - self.oldChnls) * 5
        self.oldChnls = self.nchnls
        parentSize = self.parent.GetSize()
        if CeciliaLib.getVar("systemPlatform")  == 'win32':
            self.SetSize((218, 5*self.nchnls+1))
            self.SetMaxSize((218, 5*self.nchnls+1))
        else:
            self.SetSize((218, 5*self.nchnls+1))
            self.SetMaxSize((218, 5*self.nchnls+1))
            self.parent.SetSize((parentSize[0], parentSize[1]+gap))
        self.Refresh()
        CeciliaLib.getVar("interface").OnSize(wx.SizeEvent())

    def setRms(self, *args):
        if args[0] < 0: 
            return
        if not args:
            self.amplitude = [0 for i in range(self.nchnls)]                
        else:
            self.amplitude = args
        self.amplitude = [math.log10(amp+0.00001) * 0.2 + 1. for amp in self.amplitude]
        if self.seekPeak():
            CeciliaLib.getControlPanel().updatePeak(self.peak)
        wx.CallAfter(self.Refresh)
        
    def OnPaint(self, event):
        w,h = self.GetSize()
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBrush(wx.Brush("#000000"))
        dc.Clear()
        dc.DrawRectangle(0,0,w,h)
        for i in range(self.nchnls):
            try:
                width = int(self.amplitude[i]*w)
            except:
                width = 0
            dc.DrawBitmap(self.backBitmap, 0, i*5)
            dc.SetClippingRegion(0, i*5, width, 5)
            dc.DrawBitmap(self.bitmap, 0, i*5)
            dc.DestroyClippingRegion()

    def reset(self):
        self.amplitude = [0 for i in range(self.nchnls)]
        self.Refresh()

    def seekPeak(self):
        newPeak = False
        if max(self.amplitude) > self.peak:
            self.peak = max(self.amplitude)
            newPeak = True                
        return newPeak
                        
    def getPeak(self):
        return self.peak
    
    def resetMax(self):
        self.peak = 0

class CECTooltip(wx.ToolTip):            
    def __init__(self, tip):
        if CeciliaLib.getVar("useTooltips"):
            wx.ToolTip.__init__(self, tip)
        else:    
            wx.ToolTip.__init__(self, '')
                
class Separator(wx.Panel):
    def __init__(self, parent, size=(200,1), style=wx.NO_BORDER, colour=BORDER_COLOUR):
        wx.Panel.__init__(self, parent, size=size, style=style)
        self.SetBackgroundColour(colour)
