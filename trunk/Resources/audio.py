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

import wx
import sys, os, math, copy, time
import CeciliaLib
from constants import *

if CeciliaLib.getVar("samplePrecision") == '64 bit':
    from pyo64 import *
else:
    from pyo import *
from API_interface import *

class CeciliaFilein:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        userInputs = CeciliaLib.getVar("userInputs")
        chnls = CeciliaLib.getVar("nchnls")
        info = userInputs[name]
        snd_chnls = info['nchnls'+self.name]
        if snd_chnls == 1:
            self.table = SndTable([info['path'] for i in range(chnls)], start=info["off"+self.name])
        else:
            self.table = SndTable(info['path'], start=info["off"+self.name])

    def sig(self):
        return self.table

class CeciliaSampler:
    def __init__(self, parent, name, user_pitch, user_amp):
        self.parent = parent
        self.name = name
        self.user_pitch = user_pitch
        self.user_amp = user_amp
        userInputs = CeciliaLib.getVar("userInputs")
        info = userInputs[name]
        totalTime = CeciliaLib.getVar("totalTime")
        chnls = CeciliaLib.getVar("nchnls")
        samplerList = CeciliaLib.getVar("userSamplers")
        for sampler in samplerList:
            if sampler.name == name:
                sinfo = sampler.getSamplerInfo()
                break
            
        graph_lines = {}
        for line in CeciliaLib.getVar("grapher").plotter.getData():
            if line.name.startswith(self.name):
                graph_lines[line.name] = line

        if 0:
            print info
            print sinfo
            print graph_lines
        
        paths = [slider.getPath() for slider in sampler.getSamplerSliders()]
        
        start_init, self.start_play, self.start_rec = sinfo['loopIn'][0], sinfo['loopIn'][1], sinfo['loopIn'][2]
        line = graph_lines[self.name+'start']
        curved = line.getCurved()
        if curved:
            self.start_table = CosTable()
        else:
            self.start_table = LinTable()
        if not self.start_play:
            self.start = SigTo(value=start_init, time=0.025, init=start_init)
        if self.start_rec:
            self.start_record = ControlRec(self.start, filename=paths[0], rate=1000, dur=totalTime).play()
        if self.start_play:
            data = line.getData()
            data = [tuple(x) for x in data]
            self.setGraph('start', data)
            self.start = TableRead(self.start_table, freq=1.0/totalTime).play()
        
        dur_init, self.dur_play, self.dur_rec = sinfo['loopOut'][0], sinfo['loopOut'][1], sinfo['loopOut'][2]
        line = graph_lines[self.name+'end']
        curved = line.getCurved()
        if curved:
            self.dur_table = CosTable()
        else:
            self.dur_table = LinTable()
        if not self.dur_play:
            self.dur = SigTo(value=dur_init, time=0.025, init=dur_init)
        if self.dur_rec:
            self.dur_record = ControlRec(self.dur, filename=paths[1], rate=1000, dur=totalTime).play()
        if self.dur_play:
            data = line.getData()
            data = [tuple(x) for x in data]
            self.setGraph('end', data)
            self.dur = TableRead(self.dur_table, freq=1.0/totalTime).play()
        
        xfade_init, self.xfade_play, self.xfade_rec = sinfo['loopX'][0], sinfo['loopX'][1], sinfo['loopX'][2]
        line = graph_lines[self.name+'xfade']
        curved = line.getCurved()
        if curved:
            self.xfade_table = CosTable()
        else:
            self.xfade_table = LinTable()
        if not self.xfade_play:
            self.xfade = SigTo(value=xfade_init, time=0.025, init=xfade_init)
        if self.xfade_rec:
            self.xfade_record = ControlRec(self.xfade, filename=paths[2], rate=1000, dur=totalTime).play()
        if self.xfade_play:
            data = line.getData()
            data = [tuple(x) for x in data]
            self.setGraph('xfade', data)
            self.xfade = TableRead(self.xfade_table, freq=1.0/totalTime).play()
       
        gain_init, self.gain_play, self.gain_rec = sinfo['gain'][0], sinfo['gain'][1], sinfo['gain'][2]
        line = graph_lines[self.name+'gain']
        curved = line.getCurved()
        if curved:
            self.gain_table = CosTable()
        else:
            self.gain_table = LinTable()
        if not self.gain_play:
            self.gain_in = SigTo(value=gain_init, time=0.025, init=gain_init)
        if self.gain_rec:
            self.gain_record = ControlRec(self.gain_in, filename=paths[3], rate=1000, dur=totalTime).play()
        if self.gain_play:
            data = line.getData()
            data = [tuple(x) for x in data]
            self.setGraph('gain', data)
            self.gain_in = TableRead(self.gain_table, freq=1.0/totalTime).play()
        self.gain = Pow(10, self.gain_in * 0.05, mul=self.user_amp)
        
        pitch_init, self.pitch_play, self.pitch_rec = sinfo['transp'][0], sinfo['transp'][1], sinfo['transp'][2]
        line = graph_lines[self.name+'trans']
        curved = line.getCurved()
        if curved:
            self.pitch_table = CosTable()
        else:
            self.pitch_table = LinTable()
        if not self.pitch_play:
            self.pitch_in = SigTo(value=pitch_init, time=0.025, init=pitch_init)
        if self.pitch_rec:
            self.pitch_record = ControlRec(self.pitch_in, filename=paths[4], rate=1000, dur=totalTime).play()
        if self.pitch_play:
            data = line.getData()
            data = [tuple(x) for x in data]
            self.setGraph('trans', data)
            self.pitch_in = TableRead(self.pitch_table, freq=1.0/totalTime).play()
        self.pitch = Pow(1.0594630943593, self.pitch_in, self.user_pitch)
    
        self.table = SndTable(info['path'], start=info["off"+self.name])
        if self.parent.number_of_voices > 1:
            sp_freq = [random.uniform(.2,1) for i in range(self.parent.number_of_voices*len(self.table))]
            sp_phase = [random.random() for i in range(self.parent.number_of_voices*len(self.table))]
            self.pitch_rnd = Sine(sp_freq, sp_phase, mul=self.parent.polyphony_spread, add=1)
        else:
            self.pitch_rnd = 1.0
        self.looper = Looper( table=self.table,
                                    pitch=self.pitch*self.pitch_rnd,
                                    start=self.start,
                                    dur=self.dur,
                                    xfade=self.xfade,
                                    mode=sinfo['loopMode'],
                                    xfadeshape=sinfo['xfadeshape'],
                                    startfromloop=sinfo['startFromLoop'],
                                    interp=4,
                                    autosmooth=True,
                                    mul=self.gain)
        self.mix = Mix(self.looper, voices=chnls)

    def setGraph(self, which, func):
        totalTime = CeciliaLib.getVar("totalTime")
        func = [(int(x/float(totalTime)*8192), y) for x, y in func]
        if which.endswith('start'):
            self.start_table.replace(func)
        elif which.endswith('end'):
            self.dur_table.replace(func)
        elif which.endswith('xfade'):
            self.xfade_table.replace(func)
        elif which.endswith('gain'):
            self.gain_table.replace(func)
        elif which.endswith('trans'):
            self.pitch_table.replace(func)
    
    def checkForAutomation(self):
        if self.start_rec:
            self.start_record.write()
        if self.dur_rec:
            self.dur_record.write()
        if self.xfade_rec:
            self.xfade_record.write()
        if self.gain_rec:
            self.gain_record.write()
        if self.pitch_rec:
            self.pitch_record.write()

    def sig(self):
        return self.mix
    
    def setSound(self, snd):
        self.table.setSound(snd)
    
    def setStart(self, x):
        if not self.start_play:
            self.start.value = x
    
    def setDur(self, x):
        if not self.dur_play:
            self.dur.value = x
    
    def setXfade(self, x):
        if not self.xfade_play:
            self.xfade.value = x
    
    def setGain(self, x):
        if not self.gain_play:
            self.gain_in.value = x
    
    def setPitch(self, x):
        if not self.pitch_play:
            self.pitch_in.value = x

    def setLoopMode(self, x):
        self.looper.mode = x
    
    def setXfadeShape(self, x):
        self.looper.xfadeshape = x

class CeciliaSlider:
    def __init__(self, dic, baseModule):
        self.type = "slider"
        self.name = dic["name"]
        gliss = dic["gliss"]
        up = dic["up"]
        totalTime = CeciliaLib.getVar("totalTime")
        self.baseModule = baseModule

        if not up:
            for line in CeciliaLib.getVar("grapher").plotter.getData():
                if line.name == self.name:
                    break
        
            self.widget = line.slider
            self.play = self.widget.getPlay()
            self.rec = self.widget.getRec()
            self.midi = self.widget.getWithMidi()
            self.openSndCtrl = self.widget.getWithOSC()
        
            curved = line.getCurved()
            if curved:
                self.table = CosTable()
            else:
                self.table = LinTable()
        else:
            self.play = self.rec = self.midi = 0
            for slider in CeciliaLib.getVar("userSliders"):
                if slider.name == self.name:
                    self.widget = slider
                    break
            
        init = self.widget.getValue()    
        mini = self.widget.getMinValue()
        maxi = self.widget.getMaxValue()
        self.log = self.widget.getLog()
        self.slider = SigTo(init, time=gliss, init=init)
        if self.rec:
            self.record = ControlRec(self.slider, filename=self.widget.getPath(), rate=1000, dur=totalTime).play()
        if self.play > 0:
            data = line.getData()
            data = [tuple(x) for x in data]
            self.setGraph(data)
            self.reader = TableRead(self.table, freq=1.0/totalTime).play()
        elif self.midi:
            if self.log:
                init = math.sqrt((init - mini) / (maxi - mini)) * (maxi - mini) + mini
                exp = 2
            else: 
                exp = 1
            self.ctlin = Midictl(self.widget.getMidiCtl(), mini, maxi, init, self.widget.getMidiChannel())
            self.ctlin.setInterpolation(False)
            self.reader = Scale(self.ctlin, inmin=mini, inmax=maxi, outmin=mini, outmax=maxi, exp=exp)
        elif self.openSndCtrl:
            port, address = self.widget.getOpenSndCtrl()
            self.baseModule._addOpenSndCtrlWidget(port, address, self)

    def sig(self):
        if self.play == 0:
            return self.slider
        else:
            return self.reader

    def setValue(self, x):
        self.slider.value = x

    def setGraph(self, func):
        totalTime = CeciliaLib.getVar("totalTime")
        func = [(int(x/float(totalTime)*8192), y) for x, y in func]
        self.table.replace(func)

    def updateWidget(self):
        val = self.reader.get()
        wx.CallAfter(self.widget.setValue, val)

    def setValueFromOSC(self, val):
        wx.CallAfter(self.widget.setValue, val)
        
class CeciliaRange:
    def __init__(self, dic):
        self.type = "range"
        self.name = dic["name"]
        gliss = dic["gliss"]
        up = dic["up"]
        totalTime = CeciliaLib.getVar("totalTime")

        if not up:
            self.graph_lines = [None, None]
            for line in CeciliaLib.getVar("grapher").plotter.getData():
                if self.name in line.name:
                    if line.suffix == "min":
                        self.graph_lines[0] = line
                    elif line.suffix == "max":
                        self.graph_lines[1] = line

            self.widget = self.graph_lines[0].slider
            self.play = self.widget.getPlay()
            self.rec = self.widget.getRec()
            self.midi = self.widget.getWithMidi()

            curved = [line.getCurved() for line in self.graph_lines]
            if curved[0]:
                self.table_min = CosTable()
            else:
                self.table_min = LinTable()
            if curved[1]:
                self.table_max = CosTable()
            else:
                self.table_max = LinTable()
        else:
            self.play = self.rec = self.midi = 0
            for slider in CeciliaLib.getVar("userSliders"):
                if slider.name == self.name:
                    self.widget = slider
                    break

        init = self.widget.getValue()
        mini = self.widget.getMinValue()
        maxi = self.widget.getMaxValue()
        log = self.widget.getLog()

        self.slider = SigTo(init, time=gliss, init=init)
        if self.rec:
            self.record = ControlRec(self.slider, filename=self.widget.getPath(), rate=1000, dur=totalTime).play()
        if self.play > 0:
            data = self.graph_lines[0].getData()
            data = [tuple(x) for x in data]
            self.setGraph(0, data)
            self.reader_min = TableRead(self.table_min, freq=1.0/totalTime).play()
            data = self.graph_lines[1].getData()
            data = [tuple(x) for x in data]
            self.setGraph(1, data)
            self.reader_max = TableRead(self.table_max, freq=1.0/totalTime).play()
            self.reader = Mix([self.reader_min, self.reader_max], voices=2)
        elif self.midi:
            if log:
                init = [math.sqrt((x - mini) / (maxi - mini)) * (maxi - mini) + mini for x in init]
                exp = 2
            else: 
                exp = 1
            self.ctlin = Midictl(self.widget.getMidiCtl(), mini, maxi, init, self.widget.getMidiChannel())
            self.ctlin.setInterpolation(False)
            self.reader = Scale(self.ctlin, inmin=mini, inmax=maxi, outmin=mini, outmax=maxi, exp=exp)

    def sig(self):
        if self.play == 0:
            return self.slider
        else:
            return self.reader

    def setValue(self, x):
        self.slider.value = x

    def setGraph(self, which, func):
        totalTime = CeciliaLib.getVar("totalTime")
        func = [(int(x/float(totalTime)*8192), y) for x, y in func]
        if which == 0:
            self.table_min.replace(func)
        else:
            self.table_max.replace(func)

    def updateWidget(self):
        val = self.reader.get(all=True)
        #print val
        wx.CallAfter(self.widget.setValue, val)

class CeciliaSplitter:
    def __init__(self, dic):
        self.type = "splitter"
        self.name = dic["name"]
        gliss = dic["gliss"]
        up = dic["up"]
        self.num_knobs = dic["num_knobs"]
        totalTime = CeciliaLib.getVar("totalTime")

        if 0: #if not up:
            self.graph_lines = [None for i in range(self.num_knobs)]
            for line in CeciliaLib.getVar("grapher").plotter.getData():
                if self.name in line.name:
                    which = int(line.suffix[1:])
                    self.graph_lines[which] = line

            self.widget = self.graph_lines[0].slider
            self.play = self.widget.getPlay()
            self.rec = self.widget.getRec()

            self.tables = []
            for curved in [line.getCurved() for line in self.graph_lines]:
                if curved:
                    self.tables.append(CosTable())
                else:
                    self.tables.append(LinTable())
        else:
            self.play = self.rec = self.midi = 0
            for slider in CeciliaLib.getVar("userSliders"):
                if slider.name == self.name:
                    self.widget = slider
                    break

        init = self.widget.getValue()
        self.slider = SigTo(init, time=gliss, init=init)

        if self.rec:
            self.record = ControlRec(self.slider, filename=self.widget.getPath(), rate=1000, dur=totalTime).play()
        if self.play > 0:
            self.readers = []
            for i in range(self.num_knobs):
                data = self.graph_lines[i].getData()
                data = [tuple(x) for x in data]
                self.setGraph(i, data)
                self.readers.append(TableRead(self.tables[i], freq=1.0/totalTime).play())
            self.reader = Mix(self.readers, voices=self.num_knobs)

    def sig(self):
        if self.play == 0:
            return self.slider
        else:
            return self.reader

    def setValue(self, x):
        self.slider.value = x

    def setGraph(self, which, func):
        totalTime = CeciliaLib.getVar("totalTime")
        func = [(int(x/float(totalTime)*8192), y) for x, y in func]
        self.tables[which].replace(func)

    def updateWidget(self):
        val = self.reader.get(all=True)
        wx.CallAfter(self.widget.setValue, val)

class CeciliaGraph:
    def __init__(self, dic):
        self.name = dic["name"]
        self.isTable = dic["table"]
        self.size = dic["size"]
        totalTime = CeciliaLib.getVar("totalTime")
        for line in CeciliaLib.getVar("grapher").plotter.getData():
            if line.name == self.name:
                break

        func = [(int(x/float(totalTime)*(self.size-1)), y) for x, y in line.getData()]
        curved = line.getCurved()
        if curved:
            self.table = CosTable(func, size=self.size)
        else:
            self.table = LinTable(func, size=self.size)
        if not self.isTable:
            self.reader = TableRead(self.table, freq=1.0/totalTime).play()

    def sig(self):
        if self.isTable:
            return self.table
        else:
            return self.reader

    def setValue(self, func):
        totalTime = CeciliaLib.getVar("totalTime")
        func = [(int(x/float(totalTime)*(self.size-1)), y) for x, y in func]
        self.table.replace(func)

class BaseModule:
    def __init__(self):
        self._fileins = {}
        self._samplers = {}
        self._sliders = {}
        self._toggles = {}
        self._popups = {}
        self._buttons = {}
        self._gens = {}
        self._graphs = {}
        self._polyphony = None
        self._openSndCtrlDict = {}
        self._openSndCtrlSliderDict = {}

        ###### Public attributes ######
        self.sr = CeciliaLib.getVar("sr")
        self.nchnls = CeciliaLib.getVar("nchnls")
        self.totalTime = CeciliaLib.getVar("totalTime")
        self.number_of_voices = 1
        self.polyphony_spread = 0.0
        ###############################

        interfaceWidgets = copy.deepcopy(CeciliaLib.getVar("interfaceWidgets"))
        for widget in interfaceWidgets:
            if widget['type'] in ["cslider", "crange", "csplitter"]:
                self._addSlider(widget, widget["type"])
            elif widget['type'] == "cgraph":
                self._addGraph(widget)
            elif widget['type'] == "ctoggle":
                if widget['rate'] == "k":
                    self._toggles[widget["name"]] = widget
            elif widget['type'] == "cpopup":
                if widget['rate'] == "k":
                    self._popups[widget["name"]] = widget
            elif widget['type'] == "cbutton":
                self._buttons[widget["name"]] = widget
            elif widget['type'] == "cgen":
                if widget['rate'] == "k":
                    self._gens[widget["name"]] = widget
            elif widget['type'] == "cpoly" and self._polyphony == None:
                self._polyphony = widget

        userTogglePopups = CeciliaLib.getVar("userTogglePopups")
        polyname = "noPolyphonyWidget"
        if self._polyphony != None:
            polyname = self._polyphony["name"]
        for togPop in userTogglePopups:
            if togPop.name.startswith(polyname):
                if togPop.name.endswith("num"):
                    self.number_of_voices = togPop.getValue() + 1
                else:
                    self.polyphony_spread = togPop.getValue()
            if togPop.type == "popup":
                name = togPop.name
                setattr(self, name + "_index", togPop.getValue())
                setattr(self, name + "_value", togPop.getLabel())
            elif togPop.type == "toggle":
                name = togPop.name
                setattr(self, name + "_value", togPop.getValue())
            elif togPop.type == "gen":
                name = togPop.name
                setattr(self, name + "_value", togPop.getValue())

        self._metro = Metro(.06).play(dur=self.totalTime)
        self._updater = TrigFunc(self._metro, self._updateWidgets).play(dur=self.totalTime)

    ###### Public methods ######
    def addFilein(self, name):
        self._fileins[name] = CeciliaFilein(self, name)
        return self._fileins[name].sig()

    def addSampler(self, name, pitch=1, amp=1):
        self._samplers[name] = CeciliaSampler(self, name, pitch, amp)
        return self._samplers[name].sig()

    def duplicate(self, seq, num):
        tmp = [x for x in seq for i in range(num)]
        return tmp

    def setGlobalSeed(self, x):
        CeciliaLib.getVar("audioServer").server.globalseed = x

    ############################

    ###### Private methods ######
    def _createOpenSndCtrlReceivers(self):
        if self._openSndCtrlDict:
            self.oscReceivers = {}
            self.oscScalers = []
            for key in self._openSndCtrlDict.keys():
                self.oscReceivers[key] = OscReceive(key, self._openSndCtrlDict[key])

    def _addOpenSndCtrlWidget(self, port, address, slider):
        if self._openSndCtrlDict.has_key(port):
            self._openSndCtrlDict[port].append(address)
            self._openSndCtrlSliderDict[port].append(slider)
        else:
            self._openSndCtrlDict[port] = [address]
            self._openSndCtrlSliderDict[port] = [slider]

    def _checkForAutomation(self):
        for sampler in self._samplers.values():
            sampler.checkForAutomation()
        for slider in self._sliders.values():
            if slider.rec:
                slider.record.write()

    def _updateWidgets(self):
        for slider in self._sliders.values():
            if slider.play == 1 or slider.midi:
                slider.updateWidget()
            if self._openSndCtrlDict:
                for key in self._openSndCtrlDict.keys():
                    values = self.oscReceivers[key].get(all=True)
                    for i, val in enumerate(values):
                        self._openSndCtrlSliderDict[key][i].setValueFromOSC(val)
        CeciliaLib.getVar("audioServer").updatePluginWidgets()

    def _setWidgetValues(self):
        # graph lines
        for line in CeciliaLib.getVar("grapher").plotter.getData():
            name = line.getName()
            if name in self._graphs.keys():
                data = line.getData()
                self._graphs[name].setValue(data)
        # sliders
        for slider in CeciliaLib.getVar("userSliders"):
            name = slider.getName()
            self._sliders[name].setValue(slider.getValue())
        # toggles and popups
        for togPop in CeciliaLib.getVar("userTogglePopups"):
            name = togPop.getName()
            if name in self._toggles:
                getattr(self, name)(togPop.getValue())
            elif name in self._popups:
                index, label = togPop.getFullValue()
                getattr(self, name)(index, label)
            elif name in self._gens:
                getattr(self, name)(togPop.getValue())

    def _addSlider(self, dic, typ):
        if typ == "cslider":
            self._sliders[dic["name"]] = CeciliaSlider(dic, self)
        elif typ == "crange":
            self._sliders[dic["name"]] = CeciliaRange(dic)
        elif typ == "csplitter":
            self._sliders[dic["name"]] = CeciliaSplitter(dic)
        setattr(self, dic["name"], self._sliders[dic["name"]].sig())

    def _addGraph(self, dic):
        self._graphs[dic["name"]] = CeciliaGraph(dic)
        setattr(self, dic["name"], self._graphs[dic["name"]].sig())

    def __del__(self):
        for key in self.__dict__.keys():
            del self.__dict__[key]

class CeciliaPlugin:
    def __init__(self, input, params=None, knobs=None):
        self.input = Sig(input)
        gliss = 0.05
        totalTime = CeciliaLib.getVar("totalTime")
        if params == None:
            self._p1 = SigTo(0, time=0.025)
            self._p2 = SigTo(0, time=0.025)
            self._p3 = SigTo(0, time=0.025)
        else:
            self.widget_p1 = knobs[0]
            name = self.widget_p1.getName()
            for line in CeciliaLib.getVar("grapher").plotter.getData():
                if line.name == name:
                    break
            self.play_p1 = self.widget_p1.getPlay()
            self.rec_p1 = self.widget_p1.getRec()
            curved = line.getCurved()
            if curved:
                self.table_p1 = CosTable()
            else:
                self.table_p1 = LinTable()
            self._p1 = SigTo(params[0], time=gliss, init=params[0])
            if self.rec_p1:
                self.record_p1 = ControlRec(self._p1, filename=self.widget_p1.getPath(), 
                                        rate=1000, dur=totalTime).play()
            if self.play_p1 > 0:
                data = line.getData()
                data = [tuple(x) for x in data]
                self.setGraph(0, data)
                self.reader_p1 = TableRead(self.table_p1, freq=1.0/totalTime).play()
            
            self.widget_p2 = knobs[1]
            name = self.widget_p2.getName()
            for line in CeciliaLib.getVar("grapher").plotter.getData():
                if line.name == name:
                    break
            self.play_p2 = self.widget_p2.getPlay()
            self.rec_p2 = self.widget_p2.getRec()
            curved = line.getCurved()
            if curved:
                self.table_p2 = CosTable()
            else:
                self.table_p2 = LinTable()
            self._p2 = SigTo(params[1], time=gliss, init=params[1])
            if self.rec_p2:
                self.record_p2 = ControlRec(self._p2, filename=self.widget_p2.getPath(), 
                                        rate=1000, dur=totalTime).play()
            if self.play_p2 > 0:
                data = line.getData()
                data = [tuple(x) for x in data]
                self.setGraph(1, data)
                self.reader_p2 = TableRead(self.table_p2, freq=1.0/totalTime).play()
            
            self.widget_p3 = knobs[2]
            name = self.widget_p3.getName()
            for line in CeciliaLib.getVar("grapher").plotter.getData():
                if line.name == name:
                    break
            self.play_p3 = self.widget_p3.getPlay()
            self.rec_p3 = self.widget_p3.getRec()
            curved = line.getCurved()
            if curved:
                self.table_p3 = CosTable()
            else:
                self.table_p3 = LinTable()
            self._p3 = SigTo(params[2], time=gliss, init=params[2])
            if self.rec_p3:
                self.record_p3 = ControlRec(self._p3, filename=self.widget_p3.getPath(), 
                                        rate=1000, dur=totalTime).play()
            if self.play_p3 > 0:
                data = line.getData()
                data = [tuple(x) for x in data]
                self.setGraph(2, data)
                self.reader_p3 = TableRead(self.table_p3, freq=1.0/totalTime).play()

            self.preset = params[3]

    def setPreset(self, x, label):
        self.preset = x
        if self.preset == 0:
            self.out.interp = 0
        else:
            self.out.interp = 1

    def setInput(self, input):
        self.input.value = input

    def setGraph(self, which, func):
        totalTime = CeciliaLib.getVar("totalTime")
        func = [(int(x/float(totalTime)*8192), y) for x, y in func]
        if which == 0:
            self.table_p1.replace(func)
        elif which == 1:
            self.table_p2.replace(func)
        elif which == 2:
            self.table_p3.replace(func)

    def stopControls(self):
        self._p1.stop()
        self._p2.stop()
        self._p3.stop()

    def startControls(self):
        self._p1.play()
        self._p2.play()
        self._p3.play()

    def setValue(self, which, x):
        if which == 0:
            self._p1.value = x
        elif which == 1:
            self._p2.value = x
        elif which == 2:
            self._p3.value = x

    def checkForAutomation(self):
        if self.rec_p1:
            self.record_p1.write()
        if self.rec_p2:
            self.record_p2.write()
        if self.rec_p3:
            self.record_p3.write()
            
    def updateWidget(self):
        if self.play_p1:
            val = self.reader_p1.get()
            wx.CallAfter(self.widget_p1.setValue, val)
        if self.play_p2:
            val = self.reader_p2.get()
            wx.CallAfter(self.widget_p2.setValue, val)
        if self.play_p3:
            val = self.reader_p3.get()
            wx.CallAfter(self.widget_p3.setValue, val)

class CeciliaNonePlugin(CeciliaPlugin):
    def __init__(self, input):
        CeciliaPlugin.__init__(self, input)
        self.out = self.input
        self.stopControls()

class CeciliaReverbPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        self.out = Freeverb(self.input, size=self._p2 * 0.1, damp=self._p3, bal=self._p1 * self.preset)

    def setPreset(self, x, label):
        self.preset = x
        self.out.bal = self._p1 * self.preset

class CeciliaFilterPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
            typ = 0
        else:
            inter = 1
            typ = self.preset - 1
        self.filter = Biquad(self.input, freq=self._p2, q=self._p3, type=typ, mul=self._p1)
        self.out = Interp(self.input, self.filter, inter)

    def setPreset(self, x, label):
        self.preset = x
        if self.preset == 0:
            self.out.interp = 0
        else:
            self.filter.type = self.preset - 1
            self.out.interp = 1

class CeciliaEQPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
            typ = 0
        else:
            inter = 1
            typ = self.preset - 1
        self.filter = EQ(self.input, freq=self._p1, q=self._p2, boost=self._p3, type=typ)
        self.out = Interp(self.input, self.filter, inter)

    def setPreset(self, x, label):
        self.preset = x
        if self.preset == 0:
            self.out.interp = 0
        else:
            self.filter.type = self.preset - 1
            self.out.interp = 1

class CeciliaChorusPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        self.out = Chorus(self.input, depth=self._p2, feedback=self._p3, bal=self._p1*self.preset)

    def setPreset(self, x, label):
        self.preset = x
        self.out.bal = self._p1 * self.preset

class CeciliaEQ3BPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.low = EQ(self.input, freq=250, q=0.707, boost=self._p1, type=1)
        self.mid = EQ(self.low, freq=1500, q=0.707, boost=self._p2, type=0)
        self.high = EQ(self.mid, freq=2500, q=0.707, boost=self._p3, type=2)
        self.out = Interp(self.input, self.high, inter)

class CeciliaCompressPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.dbtoamp = DBToA(self._p3)
        self.comp = Compress(self.input, thresh=self._p1, ratio=self._p2, lookahead=4, knee=.5, mul=self.dbtoamp)
        self.out = Interp(self.input, self.comp, inter)

class CeciliaGatePlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.gate = Gate(self.input, thresh=self._p1, risetime=self._p2, falltime=self._p3, lookahead=4)
        self.out = Interp(self.input, self.gate, inter)

class CeciliaDistoPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.gain = DBToA(self._p3)
        self.disto = Disto(self.input, drive=self._p1, slope=self._p2, mul=self.gain)
        self.out = Interp(self.input, self.disto, inter)

class CeciliaAmpModPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            mode = self.preset - 1
            inter = 1
        
        self.zero = Sig(0)
        if len(self.input) < 2:
            self.lfoamp = Sine(freq=self._p1, mul=.5, add=.5)
            self.iamp = 1.0 - self._p2
            self.modamp = self.input * (self.lfoamp * self._p2 + self.iamp)
            self.lforing = Sine(freq=self._p1, mul=self._p2)
            self.modring = self.input * self.lforing
        else:
            self.lfoamp = Sine(freq=self._p1, phase=[self.zero, self._p3], mul=.5, add=.5)
            self.iamp = 1.0 - self._p2
            self.modamp = self.input * (self.lfoamp * self._p2 + self.iamp)
            self.lforing = Sine(freq=self._p1, phase=[self.zero, self._p3], mul=self._p2)
            self.modring = self.input * self.lforing
            
        if mode == 0:
            self.out = Interp(self.input, self.modamp, inter)
        else:
            self.out = Interp(self.input, self.modring, inter)

    def setPreset(self, x, label):
        self.preset = x
        if self.preset == 0:
            self.out.interp = 0
        else:
            if self.preset == 1:
                self.out.input2 = self.modamp
            else:
                self.out.input2 = self.modring
            self.out.interp = 1

class CeciliaPhaserPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.phaser = Phaser(self.input, freq=self._p1, spread=self._p3, q=self._p2, feedback=0.8, num=8, mul=.5)
        self.out = Interp(self.input, self.phaser, inter)

class CeciliaDelayPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.gain = DBToA(self._p3)
        self.delaytime = SigTo(self._p1, time=.1, init=.1)
        self.delay = Delay(self.input, delay=self.delaytime, feedback=self._p2)
        self.delaymix = Interp(self.input, self.delay, self._p3)
        self.out = Interp(self.input, self.delaymix, inter)

class CeciliaFlangePlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.lfo = Sine(freq=self._p2, mul=self._p1*0.005, add=0.005)
        self.delay = Delay(self.input, delay=self.lfo, feedback=self._p3)
        self.delaymix = self.delay + self.input
        self.out = Interp(self.input, self.delaymix, inter)

class CeciliaHarmonizerPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.harmo = Harmonizer(self.input, transpo=self._p1, feedback=self._p2)
        self.mix = Interp(self.input, self.harmo, self._p3)
        self.out = Interp(self.input, self.mix, inter)

class CeciliaResonatorsPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.wg1 = Waveguide(self.input, freq=self._p1, dur=30, mul=.05)
        self.f2 = self._p1 * self._p2
        self.wg2 = Waveguide(self.input, freq=self.f2, dur=30, mul=.05)
        self.f3 = self._p1 * self._p2 * self._p2
        self.wg3 = Waveguide(self.input, freq=self.f3, dur=30, mul=.05)
        self.f4 = self._p1 * self._p2 * self._p2 * self._p2
        self.wg4 = Waveguide(self.input, freq=self.f4, dur=30, mul=.05)
        self.total = self.wg1 + self.wg2 + self.wg3 + self.wg4
        self.mix = Interp(self.input, self.total, self._p3)
        self.out = Interp(self.input, self.mix, inter)

class CeciliaDeadResonPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.wg1 = AllpassWG(self.input, freq=self._p1, feed=.995, detune=self._p2, mul=.1)
        self.wg2 = AllpassWG(self.input, freq=self._p1*0.993, feed=.995, detune=self._p2, mul=.1)
        self.total = self.wg1 + self.wg2
        self.mix = Interp(self.input, self.total, self._p3)
        self.out = Interp(self.input, self.mix, inter)

class AudioServer():
    def __init__(self):
        self.amp = 1.0
        sr, bufsize, nchnls, duplex, host, outdev, indev = self.getPrefs()
        if CeciliaLib.getVar("DEBUG"):
            print "AUDIO CONFIG:\nsr: %s, buffer size: %s, num of channels: %s, duplex: %s, host: %s, output device: %s, input device: %s" % (sr, bufsize, nchnls, duplex, host, outdev, indev)
        self.server = Server(sr=sr, buffersize=bufsize, nchnls=nchnls, duplex=duplex, audio=host)
        if CeciliaLib.getVar("DEBUG"):
            self.server.verbosity = 15
        #self.boot()
        self.setTimeCallable()
        self.timeOpened = True
        self.plugins = [None, None, None]
        self.out = self.plugin1 = self.plugin2 = self.plugin3 = None
        self.pluginDict = {"Reverb": CeciliaReverbPlugin, "Filter": CeciliaFilterPlugin, "Para EQ": CeciliaEQPlugin, "Chorus": CeciliaChorusPlugin,
                           "3 Bands EQ": CeciliaEQ3BPlugin, "Compress": CeciliaCompressPlugin, "Gate": CeciliaGatePlugin, "Disto": CeciliaDistoPlugin,
                           "AmpMod": CeciliaAmpModPlugin, "Phaser": CeciliaPhaserPlugin, "Delay": CeciliaDelayPlugin, "Flange": CeciliaFlangePlugin,
                           "Harmonizer": CeciliaHarmonizerPlugin, "Resonators": CeciliaResonatorsPlugin, "DeadReson": CeciliaDeadResonPlugin}

    def getPrefs(self):
        sr = CeciliaLib.getVar("sr")
        bufsize = int(CeciliaLib.getVar("bufferSize"))
        nchnls = CeciliaLib.getVar("nchnls")
        duplex = CeciliaLib.getVar("enableAudioInput")
        host = CeciliaLib.getVar("audioHostAPI")
        outdev = CeciliaLib.getVar("audioOutput")
        indev = CeciliaLib.getVar("audioInput")
        return sr, bufsize, nchnls, duplex, host, outdev, indev

    def start(self, timer=True, rec=False):
        self.timeOpened = True
        fade = CeciliaLib.getVar("globalFade")
        self.globalamp = Fader(fadein=fade, fadeout=fade, dur=CeciliaLib.getVar("totalTime")).play()
        self.out.mul = self.globalamp
        if rec:
            fileformat = {"wav": 0, "aiff": 1}[CeciliaLib.getVar("audioFileType")]
            sampletype = CeciliaLib.getVar("sampSize")
            self.recamp = SigTo(self.amp, time=0.05, init=self.amp)
            self.recorder = Record(self.plugin3.out * self.recamp, CeciliaLib.getVar("outputFile"), CeciliaLib.getVar("nchnls"),
                                   fileformat=fileformat, sampletype=sampletype, buffering=8)
        if CeciliaLib.getVar("startOffset") > 0.0:
            self.server.startoffset = CeciliaLib.getVar("startOffset")
        if timer:
            self.endcall = CallAfter(function=CeciliaLib.stopCeciliaSound, time=CeciliaLib.getVar("totalTime")+0.2)
            self.server.start()
        else:
            self.server.start()
            CeciliaLib.resetControls()

    def stop(self):
        self.server.stop()
        if getattr(self, "recorder", None) != None:
            self.recorder.stop()
        self.timeOpened = False
        if CeciliaLib.getVar("grapher") != None:
            CeciliaLib.getVar("grapher").cursorPanel.setTime(CeciliaLib.getVar("startOffset"))
        time.sleep(.1)

    def shutdown(self):
        self.server.shutdown()

    def boot(self):
        sr, bufsize, nchnls, duplex, host, outdev, indev = self.getPrefs()
        if CeciliaLib.getVar("DEBUG"):
            print "AUDIO CONFIG:\nsr: %s, buffer size: %s, num of channels: %s, duplex: %s, host: %s, output device: %s, input device: %s" % (sr, bufsize, nchnls, duplex, host, outdev, indev)
        outdevs = pa_get_output_devices()
        outdev = outdevs[1][outdev]
        indevs = pa_get_input_devices()
        indev = indevs[1][indev]
        self.server.setSamplingRate(sr)
        self.server.setBufferSize(bufsize)
        self.server.setNchnls(nchnls)
        self.server.setDuplex(duplex)
        self.server.setOutputDevice(outdev)
        if CeciliaLib.getVar("enableAudioInput"):
            self.server.setInputDevice(indev)
        if CeciliaLib.getVar("useMidi"):
            self.server.setMidiInputDevice(CeciliaLib.getVar("midiDeviceIn"))
        self.server.boot()

    def reinit(self):
        if CeciliaLib.getVar("toDac"):
            sr, bufsize, nchnls, duplex, host, outdev, indev = self.getPrefs()
            self.server.reinit(audio=host)
        else:
            self.server.reinit(audio="offline_nb")
            dur = CeciliaLib.getVar("totalTime")
            filename = CeciliaLib.getVar("outputFile")
            fileformat = {"wav": 0, "aiff": 1}[CeciliaLib.getVar("audioFileType")]
            sampletype = CeciliaLib.getVar("sampSize")
            self.server.recordOptions(dur=dur, filename=filename, fileformat=fileformat, sampletype=sampletype)

    def setAmpCallable(self, callable):
        self.server._server.setAmpCallable(callable)

    def setTimeCallable(self):
        self.server._server.setTimeCallable(self)

    def setTime(self, *args):
        if len(args) >= 4 and self.timeOpened:
            time = args[1]*60 + args[2] + args[3]*0.001
            CeciliaLib.getVar("grapher").cursorPanel.setTime(time)
            CeciliaLib.getVar("interface").controlPanel.setTime(time, args[1], args[2], args[3]/10)
            if time >= (CeciliaLib.getVar("totalTime") - 0.5):
                wx.CallLater(250, CeciliaLib.getControlPanel().closeBounceToDiskDialog)
        else:
            CeciliaLib.getVar("grapher").cursorPanel.setTime(CeciliaLib.getVar("startOffset"))
            CeciliaLib.getVar("interface").controlPanel.setTime(0, 0, 0, 0)

    def recstart(self):
        self.server.recstart()

    def recstop(self):
        self.server.recstop()

    def setAmp(self, x):
        self.amp = math.pow(10.0, x * 0.05)
        self.server.amp = self.amp
        if getattr(self, "recamp", None) != None:
            self.recamp.value = self.amp

    def setInOutDevice(self, device):
        self.server.setInOutDevice(device)

    def setMidiInputDevice(self, device):
        self.server.setMidiInputDevice(device)

    def setSamplingRate(self, sr):
        self.server.setSamplingRate(sr)

    def recordOptions(self, dur, filename, fileformat, sampletype):
        self.server.recordOptions(dur=dur, filename=filename, fileformat=fileformat, sampletype=sampletype)
    
    def isAudioServerRunning(self):
        if self.server.getIsStarted():
            return True
        else:
            return False

    def openCecFile(self, filepath):
        CeciliaLib.setVar("currentModule", None)
        CeciliaLib.setVar("currentModuleRef", None)
        CeciliaLib.setVar("interfaceWidgets", [])
        CeciliaLib.setVar("startOffset", 0.0)
        try:
            global Module, Interface
            del Module, Interface
        except:
            pass
        try:
            global CECILIA_PRESETS
            del CECILIA_PRESETS
        except:
            pass
        if not serverBooted():
            self.boot()
        execfile(filepath, globals())
        CeciliaLib.setVar("currentModuleRef", copy.deepcopy(Module))
        CeciliaLib.setVar("interfaceWidgets", copy.deepcopy(Interface))
        try:
            CeciliaLib.setVar("presets", copy.deepcopy(CECILIA_PRESETS))
        except:
            CeciliaLib.setVar("presets", {})
        CeciliaLib.getVar("mainFrame").onUpdateInterface(None)

    def loadModule(self, module):
        del self.plugin1, self.plugin2, self.plugin3, self.out

        if getattr(self, "globalamp", None) != None:
            del self.globalamp
        if getattr(self, "endcall", None) != None:
            del self.endcall
        if getattr(self, "recorder", None) != None:
            del self.recorder
            del self.recamp

        try:
            CeciliaLib.getVar("currentModule").__del__()
            CeciliaLib.setVar("currentModule", None)
        except:
            pass

        currentModule = module()
        currentModule._createOpenSndCtrlReceivers()
        self.out = Sig(currentModule.out)

        self.plugins = CeciliaLib.getVar("plugins")

        if self.plugins[0] == None:
            self.plugin1 = CeciliaNonePlugin(self.out)
            self.plugin1.name = "None"
        else:
            pl = self.plugins[0]
            name, params, knobs = pl.getName(), pl.getParams(), pl.getKnobs()
            self.plugin1 = self.pluginDict[name](self.out, params, knobs)
            self.plugin1.name = name

        if self.plugins[1] == None:
            self.plugin2 = CeciliaNonePlugin(self.plugin1.out)
            self.plugin2.name = "None"
        else:
            pl = self.plugins[1]
            name, params, knobs = pl.getName(), pl.getParams(), pl.getKnobs()
            self.plugin2 = self.pluginDict[name](self.plugin1.out, params, knobs)
            self.plugin2.name = name

        if self.plugins[2] == None:
            self.plugin3 = CeciliaNonePlugin(self.plugin2.out)
            self.plugin3.name = "None"
        else:
            pl = self.plugins[2]
            name, params, knobs = pl.getName(), pl.getParams(), pl.getKnobs()
            self.plugin3 = self.pluginDict[name](self.plugin2.out, params, knobs)
            self.plugin3.name = name

        self.plugin3.out.out()
        CeciliaLib.setVar("currentModule", currentModule)
        currentModule._setWidgetValues()

    def checkForAutomation(self):
        if self.plugins[0] != None:
            if self.plugins[0].getName() == self.plugin1.name:
                self.plugin1.checkForAutomation()
        if self.plugins[1] != None:
            if self.plugins[1].getName() == self.plugin2.name:
                self.plugin2.checkForAutomation()
        if self.plugins[2] != None:
            if self.plugins[2].getName() == self.plugin3.name:
                self.plugin3.checkForAutomation()

    def updatePluginWidgets(self):
        if self.plugins[0] != None:
            if self.plugins[0].getName() == self.plugin1.name:
                self.plugin1.updateWidget()
        if self.plugins[1] != None:
            if self.plugins[1].getName() == self.plugin2.name:
                self.plugin2.updateWidget()
        if self.plugins[2] != None:
            if self.plugins[2].getName() == self.plugin3.name:
                self.plugin3.updateWidget()

    def setPluginValue(self, order, which, x):
        pl = self.plugins[order]
        if pl != None:
            if order == 0 and pl.getName() == self.plugin1.name:
                self.plugin1.setValue(which, x)
            elif order == 1 and pl.getName() == self.plugin2.name:
                self.plugin2.setValue(which, x)
            elif order == 2 and pl.getName() == self.plugin3.name:
                self.plugin3.setValue(which, x)

    def setPluginPreset(self, order, x, label):
        pl = self.plugins[order]
        if pl != None:
            if order == 0 and pl.getName() == self.plugin1.name:
                self.plugin1.setPreset(x, label)
            elif order == 1 and pl.getName() == self.plugin2.name:
                self.plugin2.setPreset(x, label)
            elif order == 2 and pl.getName() == self.plugin3.name:
                self.plugin3.setPreset(x, label)

    def getMidiCtlNumber(self, number, midichnl=1): 
        if not self.midiLearnRange:
            self.midiLearnSlider.setMidiCtl(number)
            self.midiLearnSlider.setMidiChannel(midichnl)
            self.server.stop()
            del self.scan
        else:
            tmp = [number, midichnl]
            if not tmp in self.midiLearnCtlsAndChnls:
                self.midiLearnCtlsAndChnls.append(tmp)
                if len(self.midiLearnCtlsAndChnls) == 2:
                    self.midiLearnSlider.setMidiCtl([self.midiLearnCtlsAndChnls[0][0], self.midiLearnCtlsAndChnls[1][0]])
                    self.midiLearnSlider.setMidiChannel([self.midiLearnCtlsAndChnls[0][1], self.midiLearnCtlsAndChnls[1][1]])
                    self.server.stop()
                    del self.scan

    def midiLearn(self, slider, rangeSlider=False):
        self.midiLearnSlider = slider
        self.midiLearnRange = rangeSlider
        self.midiLearnCtlsAndChnls = []
        self.shutdown()
        self.boot()
        self.scan = CtlScan2(self.getMidiCtlNumber, False)
        self.server.start()

    def getAvailableAudioMidiDrivers(self):
        inputDriverList, inputDriverIndexes = pa_get_input_devices()
        selectedInputDriver = inputDriverList[inputDriverIndexes.index(pa_get_default_input())]
        outputDriverList, outputDriverIndexes = pa_get_output_devices()
        selectedOutputDriver = outputDriverList[outputDriverIndexes.index(pa_get_default_output())]
        midiDriverList, midiDriverIndexes = pm_get_input_devices()
        if midiDriverList == []:
            selectedMidiDriver = ""
        else:
            selectedMidiDriver = midiDriverList[midiDriverIndexes.index(pm_get_default_input())]
        return inputDriverList, selectedInputDriver, outputDriverList, selectedOutputDriver, midiDriverList, selectedMidiDriver
    
    def getSoundInfo(self, path):
        """
        Retrieves information of the sound and prints it to the console.
    
        return (number of channels, sampling rate, duration, fraction of a table, length in samples, bitrate)
        """
        if CeciliaLib.getVar("DEBUG"):
            print '--------------------------------------'
            print path

        info = sndinfo(path)
                
        if info != None:
            samprate = info[2]
            chnls = info[3]
            nsamps = info[0]
            dur = info[1]
            bitrate = info[5]
            format = info[4]
            for i in range(24):
                size = math.pow(2,(i+1))
                if size > nsamps:
                    break
            tableFrac = nsamps / size
            
            if CeciliaLib.getVar("DEBUG"):
                print "channels = %d" % chnls
                print "sampling rate = %s" % samprate
                print "number of samples = %s" % nsamps
                print "duration in sec. = %s" % dur
                print "bitrate = %s" % bitrate
                print "file format = %s" % format

            return (chnls, samprate, dur, tableFrac, nsamps, bitrate, format)
        else:
            print 'Unable to get sound infos. "%s" bypassed!' % path
            return None

    def getSoundsFromList(self, pathList):
        soundDict = dict()
        for path in pathList:
            if os.path.isfile(path):
                infos = self.getSoundInfo(path)
                if infos != None:
                    sndfile = os.path.split(path)[1] 
                    if sndfile not in soundDict.keys():
                        soundDict[CeciliaLib.ensureNFD(sndfile)] = {'samprate': infos[1],
                                        'chnls': infos[0],
                                        'dur': infos[2],
                                        'bitrate': infos[5],
                                        'type': infos[6],
                                        'path': path}
            else:
                if CeciliaLib.getVar("DEBUG"):
                    print 'not a file'
        return soundDict
        
