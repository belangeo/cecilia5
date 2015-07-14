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
        info = CeciliaLib.getVar("userInputs")[name]
        chnls = CeciliaLib.getVar("nchnls")
        for filein in CeciliaLib.getControlPanel().cfileinList:
            if filein.name == name:
                break
        offset = filein.getOffset()
        mode = filein.getMode()
        if mode == 0:
            snd_chnls = info['nchnls'+self.name]
            if snd_chnls == 1:
                self.table = SndTable([CeciliaLib.toSysEncoding(info['path']) for i in range(chnls)], start=info["off"+self.name])
            else:
                self.table = SndTable(CeciliaLib.toSysEncoding(info['path']), start=info["off"+self.name])
        else:
            self.table = NewTable(length=offset, chnls=chnls, feedback=0.0)
            self.livein = Input(chnl=[x for x in range(chnls)], mul=0.7)
            self.filltabrec = TableRec(self.livein, self.table, fadetime=0.05).play()
    
    def sig(self):
        return self.table

class CeciliaSampler:
    def __init__(self, parent, name, user_pitch, user_amp):
        self.type = "sampler"
        self.parent = parent
        self.baseModule = parent
        self.name = name
        self.user_pitch = user_pitch
        self.user_amp = user_amp
        info = CeciliaLib.getVar("userInputs")[name]
        totalTime = CeciliaLib.getVar("totalTime")
        chnls = CeciliaLib.getVar("nchnls")
        samplerList = CeciliaLib.getVar("userSamplers")
        for sampler in samplerList:
            if sampler.name == name:
                sinfo = sampler.getSamplerInfo()
                break
        self.sampler = sampler
        self.mode = self.sampler.mode

        self.start_play, self.start_midi = False, False
        self.dur_play, self.dur_midi = False, False
        self.xfade_play, self.xfade_midi = False, False
        self.gain_play, self.gain_midi = False, False
        self.pitch_play, self.pitch_midi = False, False

        if self.mode != 1:
            graph_lines = {}
            for line in CeciliaLib.getVar("grapher").plotter.getData():
                if line.name.startswith(self.name):
                    graph_lines[line.name] = line
           
            paths = [slider.getPath() for slider in sampler.getSamplerSliders()]
            
            ################ start ################
            start_init, self.start_play, self.start_rec = sinfo['loopIn'][0], sinfo['loopIn'][1], sinfo['loopIn'][2]
            try:
                self.start_midi, start_midictl, start_midichnl = sinfo['loopIn'][3], sinfo['loopIn'][4], sinfo['loopIn'][5]
                self.start_mini, self.start_maxi = sinfo['loopIn'][6], sinfo['loopIn'][7]
                self.start_osc = sinfo['loopIn'][8]
            except:
                self.start_midi, start_midictl, start_midichnl, self.start_mini, self.start_maxi = False, None, 1, 0, 1
                self.start_osc = None
            line = graph_lines[self.name+'start']
            curved = line.getCurved()
            if curved:
                self.start_table = CosTable()
            else:
                self.start_table = LinTable()
            if not self.start_play and not self.start_midi:
                self.start = SigTo(value=start_init, time=0.025, init=start_init)
            if self.start_play:
                data = line.getData()
                data = [tuple(x) for x in data]
                self.setGraph('start', data)
                self.start = TableRead(self.start_table, freq=1.0/totalTime).play()
            elif self.start_midi:
                self.start = Midictl(start_midictl, self.start_mini, self.start_maxi, start_init, start_midichnl)
                self.start.setInterpolation(False)
            elif self.start_osc != None:
                self.baseModule._addOpenSndCtrlWidget(self.start_osc[0], self.start_osc[1], self, name='start')
            if self.start_rec:
                self.start_record = ControlRec(self.start, filename=paths[0], rate=1000, dur=totalTime).play()
            
            ################  dur  ################
            dur_init, self.dur_play, self.dur_rec = sinfo['loopOut'][0], sinfo['loopOut'][1], sinfo['loopOut'][2]
            try:
                self.dur_midi, dur_midictl, dur_midichnl = sinfo['loopOut'][3], sinfo['loopOut'][4], sinfo['loopOut'][5]
                self.dur_mini, self.dur_maxi = sinfo['loopOut'][6], sinfo['loopOut'][7]
                self.dur_osc = sinfo['loopOut'][8]
            except:
                self.dur_midi, dur_midictl, dur_midichnl, self.dur_mini, self.dur_maxi = False, None, 1, 0, 1
                self.dur_osc = None
            line = graph_lines[self.name+'end']
            curved = line.getCurved()
            if curved:
                self.dur_table = CosTable()
            else:
                self.dur_table = LinTable()
            if not self.dur_play and not self.dur_midi:
                self.dur = SigTo(value=dur_init, time=0.025, init=dur_init)
            if self.dur_play:
                data = line.getData()
                data = [tuple(x) for x in data]
                self.setGraph('end', data)
                self.dur = TableRead(self.dur_table, freq=1.0/totalTime).play()
            elif self.dur_midi:
                self.dur = Midictl(dur_midictl, self.dur_mini, self.dur_maxi, dur_init, dur_midichnl)
                self.dur.setInterpolation(False)
            elif self.dur_osc != None:
                self.baseModule._addOpenSndCtrlWidget(self.dur_osc[0], self.dur_osc[1], self, name='dur')
            if self.dur_rec:
                self.dur_record = ControlRec(self.dur, filename=paths[1], rate=1000, dur=totalTime).play()
            
            ################ xfade ################
            xfade_init, self.xfade_play, self.xfade_rec = sinfo['loopX'][0], sinfo['loopX'][1], sinfo['loopX'][2]
            try:
                self.xfade_midi, xfade_midictl, xfade_midichnl = sinfo['loopX'][3], sinfo['loopX'][4], sinfo['loopX'][5]
                self.xfade_osc = sinfo['loopX'][6]
            except:
                self.xfade_midi, xfade_midictl, xfade_midichnl = False, None, 1
                self.xfade_osc = None
            line = graph_lines[self.name+'xfade']
            curved = line.getCurved()
            if curved:
                self.xfade_table = CosTable()
            else:
                self.xfade_table = LinTable()
            if not self.xfade_play and not self.xfade_midi:
                self.xfade = SigTo(value=xfade_init, time=0.025, init=xfade_init)
            if self.xfade_play:
                data = line.getData()
                data = [tuple(x) for x in data]
                self.setGraph('xfade', data)
                self.xfade = TableRead(self.xfade_table, freq=1.0/totalTime).play()
            elif self.xfade_midi:
                self.xfade = Midictl(xfade_midictl, 0, 50, xfade_init, xfade_midichnl)
                self.xfade.setInterpolation(False)
            elif self.xfade_osc != None:
                self.baseModule._addOpenSndCtrlWidget(self.xfade_osc[0], self.xfade_osc[1], self, name='xfade')
            if self.xfade_rec:
                self.xfade_record = ControlRec(self.xfade, filename=paths[2], rate=1000, dur=totalTime).play()
           
            ################ gain ################
            gain_init, self.gain_play, self.gain_rec = sinfo['gain'][0], sinfo['gain'][1], sinfo['gain'][2]
            try:
                self.gain_midi, gain_midictl, gain_midichnl = sinfo['gain'][3], sinfo['gain'][4], sinfo['gain'][5]
                self.gain_osc = sinfo['gain'][6]
            except:
                self.gain_midi, gain_midictl, gain_midichnl = False, None, 1
                self.gain_osc = None
            line = graph_lines[self.name+'gain']
            curved = line.getCurved()
            if curved:
                self.gain_table = CosTable()
            else:
                self.gain_table = LinTable()
            if not self.gain_play and not self.gain_midi:
                self.gain_in = SigTo(value=gain_init, time=0.025, init=gain_init)
            if self.gain_play:
                data = line.getData()
                data = [tuple(x) for x in data]
                self.setGraph('gain', data)
                self.gain_in = TableRead(self.gain_table, freq=1.0/totalTime).play()
            elif self.gain_midi:
                self.gain_in = Midictl(gain_midictl, -48, 18, gain_init, gain_midichnl)
                self.gain_in.setInterpolation(False)
            elif self.gain_osc != None:
                self.baseModule._addOpenSndCtrlWidget(self.gain_osc[0], self.gain_osc[1], self, name='gain')
            if self.gain_rec:
                self.gain_record = ControlRec(self.gain_in, filename=paths[3], rate=1000, dur=totalTime).play()
            self.gain = Pow(10, self.gain_in * 0.05, mul=self.user_amp)
            
            ################ pitch ################
            pitch_init, self.pitch_play, self.pitch_rec = sinfo['transp'][0], sinfo['transp'][1], sinfo['transp'][2]
            try:
                self.pitch_midi, pitch_midictl, pitch_midichnl = sinfo['transp'][3], sinfo['transp'][4], sinfo['transp'][5]
                self.pitch_osc = sinfo['transp'][6]
            except:
                self.pitch_midi, pitch_midictl, pitch_midichnl = False, None, 1
                self.pitch_osc = None
            line = graph_lines[self.name+'trans']
            curved = line.getCurved()
            if curved:
                self.pitch_table = CosTable()
            else:
                self.pitch_table = LinTable()
            if not self.pitch_play and not self.pitch_midi:
                self.pitch_in = SigTo(value=pitch_init, time=0.025, init=pitch_init)
            if self.pitch_play:
                data = line.getData()
                data = [tuple(x) for x in data]
                self.setGraph('trans', data)
                self.pitch_in = TableRead(self.pitch_table, freq=1.0/totalTime).play()
            elif self.pitch_midi:
                self.pitch_in = Midictl(pitch_midictl, -48, 48, pitch_init, pitch_midichnl)
                self.pitch_in.setInterpolation(False)
            elif self.pitch_osc != None:
                self.baseModule._addOpenSndCtrlWidget(self.pitch_osc[0], self.pitch_osc[1], self, name='pitch')
            if self.pitch_rec:
                self.pitch_record = ControlRec(self.pitch_in, filename=paths[4], rate=1000, dur=totalTime).play()
            self.pitch = Pow(1.0594630943593, self.pitch_in, self.user_pitch)
            if CeciliaLib.getVar("automaticMidiBinding") and CeciliaLib.getVar("useMidi"):
                self.checkNoteIn = Notein(poly=1, scale=0, first=0, last=120)
                self.onNewNote = Change(self.checkNoteIn["pitch"])
                self.noteTrigFunc = TrigFunc(self.onNewNote, self.newMidiPitch)

            if self.mode == 0:
                self.table = SndTable(CeciliaLib.toSysEncoding(info['path']), start=info["off"+self.name])
            elif self.mode == 2:
                self.table = NewTable(length=self.sampler.getOffset(), chnls=chnls)
                self.livein = Input(chnl=[x for x in range(chnls)], mul=0.7)
                self.filltabrec = TableRec(self.livein, self.table).play()
            elif self.mode == 3:
                self.table = NewTable(length=self.sampler.getOffset(), chnls=chnls)
                self.table2 = NewTable(length=self.sampler.getOffset(), chnls=chnls)
                self.livein = Input(chnl=[x for x in range(chnls)], mul=0.7)
                self.rectrig = Metro(time=self.sampler.getOffset(), poly=2).play()
                self.tmprec1 = TrigTableRec(self.livein, self.rectrig[0], self.table)
                self.tmprec2 = TrigTableRec(self.livein, self.rectrig[1], self.table2)
                self.morphind = Counter(self.rectrig.mix(1), min=0, max=2, dir=0)
                self.interp = SigTo(self.morphind, time=0.1)

            self.pitch_rnd = [x for x in self.parent.polyphony_spread for y in range(len(self.table))]
            if self.mode != 3:
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
                self.mix = Mix(self.looper, voices=chnls, mul=self.parent.polyphony_scaling)
            else:
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
                self.looper2 = Looper( table=self.table2,
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
                self.loopinterp = Interp(self.looper, self.looper2, self.interp)
                self.mix = Mix(self.loopinterp, voices=chnls, mul=self.parent.polyphony_scaling)
                
        else:
            self.mix = Input(chnl=[x for x in range(chnls)], mul=0.7)

    def setValueFromOSC(self, val, name):
        if self.mode != 1:
            if name == 'start':
                val = rescale(val, ymin=self.start_mini, ymax=self.start_maxi)
                self.sampler.getSamplerFrame().loopInSlider.setValue(val)
                if not self.sampler.getSamplerFrame().loopInSlider.slider.IsShownOnScreen():
                    self.sampler.getSamplerFrame().loopInSlider.sendValue(val)
            elif name == 'dur':
                val = rescale(val, ymin=self.dur_mini, ymax=self.dur_maxi)
                self.sampler.getSamplerFrame().loopOutSlider.setValue(val)
                if not self.sampler.getSamplerFrame().loopOutSlider.slider.IsShownOnScreen():
                    self.sampler.getSamplerFrame().loopOutSlider.sendValue(val)
            elif name == 'xfade':
                val = rescale(val, ymin=0, ymax=50)
                self.sampler.getSamplerFrame().loopXSlider.setValue(val)
                if not self.sampler.getSamplerFrame().loopXSlider.slider.IsShownOnScreen():
                    self.sampler.getSamplerFrame().loopXSlider.sendValue(val)
            elif name == 'gain':
                val = rescale(val, ymin=-48, ymax=18)
                self.sampler.getSamplerFrame().gainSlider.setValue(val)
                if not self.sampler.getSamplerFrame().gainSlider.slider.IsShownOnScreen():
                    self.sampler.getSamplerFrame().gainSlider.sendValue(val)
            elif name == 'pitch':
                val = rescale(val, ymin=-48, ymax=48)
                self.sampler.getSamplerFrame().transpSlider.setValue(val)
                if not self.sampler.getSamplerFrame().transpSlider.slider.IsShownOnScreen():
                    self.sampler.getSamplerFrame().transpSlider.sendValue(val)

    def getWidget(self, name):
        if name == 'start':
            widget = self.sampler.getSamplerFrame().loopInSlider
        elif name == 'dur':
            widget = self.sampler.getSamplerFrame().loopOutSlider
        elif name == 'xfade':
            widget = self.sampler.getSamplerFrame().loopXSlider
        elif name == 'gain':
            widget = self.sampler.getSamplerFrame().gainSlider
        elif name == 'pitch':
            widget = self.sampler.getSamplerFrame().transpSlider
        return widget

    def updateWidgets(self):
        if self.mode != 1:
            if self.start_midi and not self.start_play:
                val = self.start.get()
                wx.CallAfter(self.sampler.getSamplerFrame().loopInSlider.setValue, val)
            if self.dur_midi and not self.dur_play:
                val = self.dur.get()
                wx.CallAfter(self.sampler.getSamplerFrame().loopOutSlider.setValue, val)
            if self.xfade_midi and not self.xfade_play:
                val = self.xfade.get()
                wx.CallAfter(self.sampler.getSamplerFrame().loopXSlider.setValue, val)
            if self.gain_midi and not self.gain_play:
                val = self.gain_in.get()
                wx.CallAfter(self.sampler.getSamplerFrame().gainSlider.setValue, val)
            if self.pitch_midi and not self.pitch_play:
                val = self.pitch_in.get()
                wx.CallAfter(self.sampler.getSamplerFrame().transpSlider.setValue, val)

    def newMidiPitch(self):
        if not self.pitch_midi:
            pit = self.checkNoteIn.get()
            self.sampler.getSamplerFrame().transpSlider.setValue(pit - 60)
            if not self.sampler.getSamplerFrame().transpSlider.slider.IsShownOnScreen():
                self.sampler.getSamplerFrame().transpSlider.sendValue(pit - 60)

    def setGraph(self, which, func):
        if self.mode != 1:
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
        if self.mode != 1:
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

    def getDur(self):
        if self.mode != 1:
            return self.table.getDur(False)
        else:
            return CeciliaLib.getVar("totalTime")

    def setSound(self, snd):
        if self.mode == 0:
            self.table.setSound(snd)
    
    def setStart(self, x):
        if self.mode != 1:
            if not self.start_play:
                self.start.value = x
    
    def setDur(self, x):
        if self.mode != 1:
            if not self.dur_play:
                self.dur.value = x
    
    def setXfade(self, x):
        if self.mode != 1:
            if not self.xfade_play:
                self.xfade.value = x
    
    def setGain(self, x):
        if self.mode != 1:
            if not self.gain_play:
                self.gain_in.value = x
    
    def setPitch(self, x):
        if self.mode != 1:
            if not self.pitch_play:
                self.pitch_in.value = x

    def setLoopMode(self, x):
        if self.mode != 1:
            self.looper.mode = x
            if self.mode == 3:
                self.looper2.mode = x
    
    def setXfadeShape(self, x):
        if self.mode != 1:
            self.looper.xfadeshape = x
            if self.mode == 3:
                self.looper2.xfadeshape = x

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
            log = self.widget.getLog()
            if curved and log:
                self.table = CosLogTable()
            elif curved:
                self.table = CosTable()
            elif log:
                self.table = LogTable()
            else:
                self.table = LinTable()
        else:
            self.play = self.rec = self.midi = self.openSndCtrl = 0
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
            data = line.getData()
            data = [tuple(x) for x in data]
            self.setGraph(data)
            self.reader = TableRead(self.table, freq=1.0/totalTime).play()
        elif self.midi:
            if log:
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
        val = rescale(val, ymin=self.widget.getMinValue(), ymax=self.widget.getMaxValue(), ylog=self.widget.getLog())
        wx.CallAfter(self.widget.setValue, val)

class CeciliaRange:
    def __init__(self, dic, baseModule):
        self.type = "range"
        self.name = dic["name"]
        gliss = dic["gliss"]
        up = dic["up"]
        totalTime = CeciliaLib.getVar("totalTime")
        self.baseModule = baseModule
        self.oscTmpVals = [0,0]

        if not up:
            self.graph_lines = [None, None]
            for line in CeciliaLib.getVar("grapher").plotter.getData():
                if self.name == line.name:
                    if line.suffix == "min":
                        self.graph_lines[0] = line
                    elif line.suffix == "max":
                        self.graph_lines[1] = line

            self.widget = self.graph_lines[0].slider
            self.play = self.widget.getPlay()
            self.rec = self.widget.getRec()
            self.midi = self.widget.getWithMidi()
            self.openSndCtrl = self.widget.getWithOSC()
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
            self.play = self.rec = self.midi = self.openSndCtrl = 0
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
        elif self.openSndCtrl:
            oscTuples = self.widget.getOpenSndCtrl()
            if oscTuples[0] != ():
                port, address = oscTuples[0][0], oscTuples[0][1]
                self.baseModule._addOpenSndCtrlWidget(port, address, self, 0)
            if oscTuples[1] != ():
                port, address = oscTuples[1][0], oscTuples[1][1]
                self.baseModule._addOpenSndCtrlWidget(port, address, self, 1)

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
        wx.CallAfter(self.widget.setValue, val)

    def setValueFromOSC(self, val, which):
        val = rescale(val, ymin=self.widget.getMinValue(), ymax=self.widget.getMaxValue(), ylog=self.widget.getLog())
        wx.CallAfter(self.widget.setOneValue, val, which)

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
        self._OSCOutList = []

        ###### Public attributes ######
        self.sr = CeciliaLib.getVar("sr")
        self.nchnls = CeciliaLib.getVar("nchnls")
        self.totalTime = CeciliaLib.getVar("totalTime")
        self.server = CeciliaLib.getVar("audioServer").server
        self.filepath = os.path.split(CeciliaLib.getVar("currentCeciliaFile", unicode=True))[0]
        self.number_of_voices = 1
        self.polyphony_spread = [1.0]
        self.polyphony_scaling = 1.0
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
                    self._definePolyTranspo(togPop.getLabel())
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
        """
        Creates a SndTable object from the name of a cfilein widget.

        A SndTable is a memory filled with the samples of the current audio file.

        Parameters:

        name : string
            The name assigned to a cfilein widget in the Interface declaration.

        """
        self._fileins[name] = CeciliaFilein(self, name)
        return self._fileins[name].sig()

    def addSampler(self, name, pitch=1, amp=1):
        """
        Creates a sampler/looper from the name of a csampler widget.

        A sampler comes with an interface window allowing the control of the looping
        parameters (direction, start point, loop duration, crossfade duration, gain,
        pitch, etc.)

        Parameters:

        pitch : float or PyoObject
            External pitch control added to the value of the transposition slider.
        amp : float or PyoObject
            External amplitude control added to the value of the gain slider.

        """
        self._samplers[name] = CeciliaSampler(self, name, pitch, amp)
        return self._samplers[name].sig()

    def getSamplerDur(self, name):
        return self._samplers[name].getDur()
        
    def duplicate(self, seq, num):
        """
        Duplicates elements in a sequence according to the `num` parameter.

        This method is useful to creates lists that match the number of channels
        multiplied by the number of voices from a cpoly or a splitter widget.

        Parameters:

        seq : list
            List of values to duplicate.
        num : int
            Number of iteration for each value in the sequence.

        Example:

        freqs = duplicate([100, 200, 300], 4)
        print freqs
        [100, 100, 100, 100, 200, 200, 200, 200, 300, 300, 300, 300]

        """
        tmp = [x for x in seq for i in range(num)]
        return tmp

    def setGlobalSeed(self, x):
        """
        Sets the Server's global seed used by objects from the random family.

        
        """
        CeciliaLib.getVar("audioServer").server.globalseed = x
    ############################

    ###### Private methods ######
    def _definePolyTranspo(self, chord):
        if self.number_of_voices <= 1:
            return
        tmp = 0
        for i in range(self.number_of_voices):
            tmp -= {0: 0, 1: 3, 2: 3, 3: 2, 4: 2, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1}.get(i, 1)
        self.polyphony_scaling = pow(10.0, tmp * 0.05)
        if chord == "None":
            self.polyphony_spread = [1.0] * self.number_of_voices
            return
        else:
            self.polyphony_spread = [1.0]
        pool = POLY_CHORDS[chord]
        for i in range(1, self.number_of_voices):
            note = pool[i%len(pool)]
            if i % 2 == 1 or note < 1.0:
                self.polyphony_spread.append(midiToTranspo(note+60))
            else:
                self.polyphony_spread.append(midiToTranspo(note-12+60))
            
    def _deleteOscReceivers(self):
        if hasattr(self, "oscReceivers"):
            del self.oscReceivers

    def _createOpenSndCtrlReceivers(self):
        if self._openSndCtrlDict:
            self.oscReceivers = {}
            for key in self._openSndCtrlDict.keys():
                self.oscReceivers[key] = OscReceive(key, self._openSndCtrlDict[key])
                for slider in self._openSndCtrlSliderDict[key]:
                    if type(slider) == type(()):
                        slider, side = slider[0], slider[1]
                        if slider.type == "sampler": # sampler slider
                            widget = slider.getWidget(side)
                            path = widget.openSndCtrl[1]
                            val = rescale(widget.getValue(), xmin=widget.getMinValue(), xmax=widget.getMaxValue(), xlog=widget.getLog())
                            self.oscReceivers[key].setValue(path, val)
                            if widget.OSCOut != None:
                                tmpout = OscDataSend("f", widget.OSCOut[1], widget.OSCOut[2], widget.OSCOut[0])
                                tmpout.send([val])
                                self._OSCOutList.append(tmpout)
                        else: # range slider
                            widget = slider.widget
                            path = widget.openSndCtrl[side][1]
                            val = rescale(widget.getValue()[side], xmin=widget.getMinValue(), xmax=widget.getMaxValue(), xlog=widget.getLog())
                            self.oscReceivers[key].setValue(path, val)
                            if widget.OSCOut != None:
                                if widget.OSCOut[side] != ():
                                    tmpout = OscDataSend("f", widget.OSCOut[side][1], widget.OSCOut[side][2], widget.OSCOut[side][0])
                                    tmpout.send([val])
                                    self._OSCOutList.append(tmpout)
                    else: # slider
                        widget = slider.widget
                        path = widget.openSndCtrl[1]
                        val = rescale(widget.getValue(), xmin=widget.getMinValue(), xmax=widget.getMaxValue(), xlog=widget.getLog())
                        self.oscReceivers[key].setValue(path, val)
                        if widget.OSCOut != None:
                            tmpout = OscDataSend("f", widget.OSCOut[1], widget.OSCOut[2], widget.OSCOut[0])
                            tmpout.send([val])
                            self._OSCOutList.append(tmpout)

    def _addOpenSndCtrlWidget(self, port, address, slider, side=0, name=""):
        if self._openSndCtrlDict.has_key(port):
            self._openSndCtrlDict[port].append(address)
            if slider.type == 'sampler':
                self._openSndCtrlSliderDict[port].append((slider, name))
            elif slider.type == 'slider':
                self._openSndCtrlSliderDict[port].append(slider)
            elif slider.type == 'range':
                self._openSndCtrlSliderDict[port].append((slider, side))
        else:
            self._openSndCtrlDict[port] = [address]
            if slider.type == 'sampler':
                self._openSndCtrlSliderDict[port] = [(slider, name)]
            elif slider.type == 'slider':
                self._openSndCtrlSliderDict[port] = [slider]
            elif slider.type == 'range':
                self._openSndCtrlSliderDict[port] = [(slider, side)]

    def _checkForAutomation(self):
        for sampler in self._samplers.values():
            sampler.checkForAutomation()
        for slider in self._sliders.values():
            if slider.rec:
                slider.record.write()

    def _updateWidgets(self):
        if self._samplers != {}:
            for key in self._samplers.keys():
                self._samplers[key].updateWidgets()
        for slider in self._sliders.values():
            if slider.play == 1 or slider.midi:
                slider.updateWidget()
        if self._openSndCtrlDict:
            for key in self._openSndCtrlDict.keys():
                values = self.oscReceivers[key].get(all=True)
                for i in range(len(values)):
                    slider = self._openSndCtrlSliderDict[key][i]
                    if type(slider) != type(()):
                        slider.setValueFromOSC(values[i])
                    else:
                        which = slider[1]
                        slider[0].setValueFromOSC(values[i], which)
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
            self._sliders[dic["name"]] = CeciliaRange(dic, self)
        elif typ == "csplitter":
            self._sliders[dic["name"]] = CeciliaSplitter(dic)
        setattr(self, dic["name"], self._sliders[dic["name"]].sig())

    def _addGraph(self, dic):
        self._graphs[dic["name"]] = CeciliaGraph(dic)
        setattr(self, dic["name"], self._graphs[dic["name"]].sig())

    def __del__(self):
        self.oscReceivers = {}
        self._OSCOutList = []
        for key in self.__dict__.keys():
            del self.__dict__[key]
        del self

class CeciliaPlugin:
    def __init__(self, input, params=None, knobs=None):
        self.input = InputFader(input)
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

    def sig1(self):
        if self.play_p1 == 0:
            return self._p1
        else:
            return self.reader_p1

    def sig2(self):
        if self.play_p2 == 0:
            return self._p2
        else:
            return self.reader_p2

    def sig3(self):
        if self.play_p3 == 0:
            return self._p3
        else:
            return self.reader_p3

    def setPreset(self, x, label):
        self.preset = x
        if self.preset == 0:
            self.out.interp = 0
        else:
            self.out.interp = 1

    def setInput(self, input, fadetime=0.05):
        self.input.setInput(input, fadetime)

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
        self.out = Freeverb(self.input, size=self.sig2() * 0.1, damp=self.sig3(), bal=self.sig1() * self.preset)

    def setPreset(self, x, label):
        self.preset = x
        self.out.bal = self.sig1() * self.preset

class CeciliaWGReverbPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        self.out = WGVerb(self.input, feedback=self.sig2(), cutoff=self.sig3(), bal=self.sig1() * self.preset)

    def setPreset(self, x, label):
        self.preset = x
        self.out.bal = self.sig1() * self.preset

class CeciliaFilterPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
            typ = 0
        else:
            inter = 1
            typ = self.preset - 1
        self.filter = Biquad(self.input, freq=self.sig2(), q=self.sig3(), type=typ, mul=self.sig1())
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
        self.filter = EQ(self.input, freq=self.sig1(), q=self.sig2(), boost=self.sig3(), type=typ)
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
        self.out = Chorus(self.input, depth=self.sig2(), feedback=self.sig3(), bal=self.sig1()*self.preset)

    def setPreset(self, x, label):
        self.preset = x
        self.out.bal = self.sig1() * self.preset

class CeciliaEQ3BPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.low = EQ(self.input, freq=250, q=0.707, boost=self.sig1(), type=1)
        self.mid = EQ(self.low, freq=1500, q=0.707, boost=self.sig2(), type=0)
        self.high = EQ(self.mid, freq=2500, q=0.707, boost=self.sig3(), type=2)
        self.out = Interp(self.input, self.high, inter)

class CeciliaCompressPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.dbtoamp = DBToA(self.sig3())
        self.comp = Compress(self.input, thresh=self.sig1(), ratio=self.sig2(), lookahead=4, knee=.5, mul=self.dbtoamp)
        self.out = Interp(self.input, self.comp, inter)

class CeciliaGatePlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.gate = Gate(self.input, thresh=self.sig1(), risetime=self.sig2(), falltime=self.sig3(), lookahead=4)
        self.out = Interp(self.input, self.gate, inter)

class CeciliaDistoPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.gain = DBToA(self.sig3())
        self.disto = Disto(self.input, drive=self.sig1(), slope=self.sig2(), mul=self.gain)
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
            self.lfoamp = Sine(freq=self.sig1(), mul=.5, add=.5)
            self.iamp = 1.0 - self.sig2()
            self.modamp = self.input * (self.lfoamp * self.sig2() + self.iamp)
            self.lforing = Sine(freq=self.sig1(), mul=self.sig2())
            self.modring = self.input * self.lforing
        else:
            self.lfoamp = Sine(freq=self.sig1(), phase=[self.zero, self.sig3()], mul=.5, add=.5)
            self.iamp = 1.0 - self.sig2()
            self.modamp = self.input * (self.lfoamp * self.sig2() + self.iamp)
            self.lforing = Sine(freq=self.sig1(), phase=[self.zero, self.sig3()], mul=self.sig2())
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
        self.phaser = Phaser(self.input, freq=self.sig1(), spread=self.sig3(), q=self.sig2(), feedback=0.8, num=8, mul=.5)
        self.out = Interp(self.input, self.phaser, inter)

class CeciliaDelayPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.gain = DBToA(self.sig3())
        self.delaytime = SigTo(self.sig1(), time=.1, init=.1)
        self.delay = Delay(self.input, delay=self.delaytime, feedback=self.sig2())
        self.delaymix = Interp(self.input, self.delay, self.sig3())
        self.out = Interp(self.input, self.delaymix, inter)

class CeciliaFlangePlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.lfo = Sine(freq=self.sig2(), mul=self.sig1()*0.005, add=0.005)
        self.delay = Delay(self.input, delay=self.lfo, feedback=self.sig3())
        self.delaymix = self.delay + self.input
        self.out = Interp(self.input, self.delaymix, inter)

class CeciliaHarmonizerPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.harmo = Harmonizer(self.input, transpo=self.sig1(), feedback=self.sig2())
        self.mix = Interp(self.input, self.harmo, self.sig3())
        self.out = Interp(self.input, self.mix, inter)

class CeciliaResonatorsPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.wg1 = Waveguide(self.input, freq=self.sig1(), dur=30, mul=.05)
        self.f2 = self.sig1() * self.sig2()
        self.wg2 = Waveguide(self.input, freq=self.f2, dur=30, mul=.05)
        self.f3 = self.sig1() * self.sig2() * self.sig2()
        self.wg3 = Waveguide(self.input, freq=self.f3, dur=30, mul=.05)
        self.f4 = self.sig1() * self.sig2() * self.sig2() * self.sig2()
        self.wg4 = Waveguide(self.input, freq=self.f4, dur=30, mul=.05)
        self.total = self.wg1 + self.wg2 + self.wg3 + self.wg4
        self.mix = Interp(self.input, self.total, self.sig3())
        self.out = Interp(self.input, self.mix, inter)

class CeciliaDeadResonPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)
        if self.preset == 0:
            inter = 0
        else:
            inter = 1
        self.wg1 = AllpassWG(self.input, freq=self.sig1(), feed=.995, detune=self.sig2(), mul=.1)
        self.wg2 = AllpassWG(self.input, freq=self.sig1()*0.993, feed=.995, detune=self.sig2(), mul=.1)
        self.total = self.wg1 + self.wg2
        self.mix = Interp(self.input, self.total, self.sig3())
        self.out = Interp(self.input, self.mix, inter)

class CeciliaChaosModPlugin(CeciliaPlugin):
    def __init__(self, input, params, knobs):
        CeciliaPlugin.__init__(self, input, params, knobs)

        self.lfolo = Lorenz(self.sig1(), self.sig2(), stereo=True, mul=0.5, add=0.5)
        self.lforo = Rossler(self.sig1(), self.sig2(), stereo=True, mul=0.5, add=0.5)
        self.lfo = Sig(self.lfolo)
        self.iamp = 1.0 - self.sig3()
        self.modu = self.input * (self.lfo * self.sig3() + self.iamp)

        if self.preset == 0:
            inter = 0
        else:
            if self.preset == 1:
                self.lfo.value = self.lfolo
            else:
                self.lfo.value = self.lforo
            inter = 1
            
        self.out = Interp(self.input, self.modu, inter)

    def setPreset(self, x, label):
        self.preset = x
        if self.preset == 0:
            self.out.interp = 0
        else:
            if self.preset == 1:
                self.lfo.value = self.lfolo
            else:
                self.lfo.value = self.lforo
            self.out.interp = 1

class AudioServer():
    def __init__(self):
        self.amp = 1.0
        sr, bufsize, nchnls, duplex, host, outdev, indev, firstin, firstout = self.getPrefs()
        jackname = CeciliaLib.getVar("jack").get("client", "cecilia5")
        if CeciliaLib.getVar("DEBUG"):
            print "AUDIO CONFIG:"
            print "sr: %s, buffer size: %s, num of channels: %s, duplex: %s, host: %s, output device: %s, input device: %s" % (sr, bufsize, nchnls, duplex, host, outdev, indev)
            print "first physical input: %s, first physical output: %s\n" % (firstin, firstout)
        self.server = Server(sr=sr, buffersize=bufsize, nchnls=nchnls, duplex=duplex, audio=host, jackname=jackname)
        if CeciliaLib.getVar("DEBUG"):
            self.server.verbosity = 15
        if host == 'jack':
            self.server.setJackAuto(True, True)
        self.setTimeCallable()
        self.timeOpened = True
        self.recording = False
        self.withTimer = False
        self.withSpectrum = False
        self.pluginObjs = [None] * NUM_OF_PLUGINS
        self.out = self.spectrum = None
        self.pluginDict = {"Reverb": CeciliaReverbPlugin, "WGVerb": CeciliaWGReverbPlugin, "Filter": CeciliaFilterPlugin, "Para EQ": CeciliaEQPlugin, 
                           "Chorus": CeciliaChorusPlugin, "3 Bands EQ": CeciliaEQ3BPlugin, "Compress": CeciliaCompressPlugin, "Gate": CeciliaGatePlugin, 
                           "Disto": CeciliaDistoPlugin, "AmpMod": CeciliaAmpModPlugin, "Phaser": CeciliaPhaserPlugin, "Delay": CeciliaDelayPlugin, 
                           "Flange": CeciliaFlangePlugin, "Harmonizer": CeciliaHarmonizerPlugin, "Resonators": CeciliaResonatorsPlugin, 
                           "DeadReson": CeciliaDeadResonPlugin, 'ChaosMod': CeciliaChaosModPlugin}

    def getPrefs(self):
        sr = CeciliaLib.getVar("sr")
        bufsize = int(CeciliaLib.getVar("bufferSize"))
        nchnls = CeciliaLib.getVar("nchnls")
        duplex = CeciliaLib.getVar("enableAudioInput")
        host = CeciliaLib.getVar("audioHostAPI")
        outdev = CeciliaLib.getVar("audioOutput")
        indev = CeciliaLib.getVar("audioInput")
        firstin = CeciliaLib.getVar("defaultFirstInput")
        firstout = CeciliaLib.getVar("defaultFirstOutput")
        return sr, bufsize, nchnls, duplex, host, outdev, indev, firstin, firstout

    def dump(self, l):
        pass

    def start(self, timer=True, rec=False):
        if CeciliaLib.getVar("DEBUG"):
            print "Audio server start: begin"
        self.timeOpened = True
        fade = CeciliaLib.getVar("globalFade")
        self.globalamp = Fader(fadein=fade, fadeout=fade, dur=CeciliaLib.getVar("totalTime")).play()
        self.out.mul = self.globalamp
        if CeciliaLib.getVar("automaticMidiBinding") and CeciliaLib.getVar("useMidi"):
            if CeciliaLib.getVar("DEBUG"):
                print "Audio server start: use midi"
                print "midi input device: %d" % CeciliaLib.getVar("midiDeviceIn")
            self.checkCtl7 = Midictl(ctlnumber=7, minscale=-48, maxscale=18, init=0)
            self.checkCtl7.setInterpolation(False)
            self.onNewCtl7Value = Change(self.checkCtl7)
            self.ctl7TrigFunc = TrigFunc(self.onNewCtl7Value, self.newCtl7Value)
        if rec:
            self.recording = True
            fileformat = AUDIO_FILE_FORMATS[CeciliaLib.getVar("audioFileType")]
            sampletype = CeciliaLib.getVar("sampSize")
            self.recamp = SigTo(self.amp, time=0.05, init=self.amp)
            self.recorder = Record(self.pluginObjs[-1].out * self.recamp, 
                                   CeciliaLib.toSysEncoding(CeciliaLib.getVar("outputFile")), CeciliaLib.getVar("nchnls"),
                                   fileformat=fileformat, sampletype=sampletype, buffering=8)
        if CeciliaLib.getVar("showSpectrum"):
            self.withSpectrum = True
            self.specamp = SigTo(self.amp, time=0.05, init=self.amp, mul=self.pluginObjs[-1].out)
            self.spectrum = Spectrum(self.specamp, function=self.dump)
        if CeciliaLib.getVar("startOffset") > 0.0:
            self.server.startoffset = CeciliaLib.getVar("startOffset")
        if timer:
            self.withTimer = True
            self.server.start()
        else:
            self.server.start()
            CeciliaLib.resetControls()
        if CeciliaLib.getVar("DEBUG"):
            print "Audio server start: end\n"

    def stop(self):
        if CeciliaLib.getVar("DEBUG"):
            print "Audio server stop: begin"
        if self.withTimer:
            self.withTimer = False
        self.server.stop()
        if self.recording:
            self.recording = False
            self.recorder.stop()
        if self.withSpectrum:
            self.withSpectrum = False
            self.spectrum.poll(False)
            self.spectrum.stop()
        self.timeOpened = False
        if CeciliaLib.getVar("grapher") != None:
            CeciliaLib.getVar("grapher").cursorPanel.setTime(CeciliaLib.getVar("startOffset"))
        time.sleep(.15)
        if CeciliaLib.getVar("currentModule") != None:
            CeciliaLib.getVar("currentModule")._deleteOscReceivers()
        if CeciliaLib.getVar("DEBUG"):
            print "Audio server stop: end\n"

    def shutdown(self):
        self.server.shutdown()

    def boot(self):
        sr, bufsize, nchnls, duplex, host, outdev, indev, firstin, firstout = self.getPrefs()
        if CeciliaLib.getVar("DEBUG"):
            print "AUDIO CONFIG:"
            print "sr: %s, buffer size: %s, num of channels: %s, duplex: %s, host: %s, output device: %s, input device: %s" % (sr, bufsize, nchnls, duplex, host, outdev, indev)
            print "first physical input: %s, first physical output: %s\n" % (firstin, firstout)
            print "MIDI CONFIG: \ninput device: %d\n" % CeciliaLib.getVar("midiDeviceIn")
        self.server.setSamplingRate(sr)
        self.server.setBufferSize(bufsize)
        self.server.setNchnls(nchnls)
        self.server.setDuplex(duplex)
        self.server.setOutputDevice(outdev)
        self.server.setInputOffset(firstin)
        self.server.setOutputOffset(firstout)
        if CeciliaLib.getVar("enableAudioInput"):
            self.server.setInputDevice(indev)
        if CeciliaLib.getVar("useMidi"):
            self.server.setMidiInputDevice(CeciliaLib.getVar("midiDeviceIn"))
        self.server.boot()

    def reinit(self):
        jackname = CeciliaLib.getVar("jack").get("client", "cecilia5")
        if CeciliaLib.getVar("toDac"):
            sr, bufsize, nchnls, duplex, host, outdev, indev, firstin, firstout = self.getPrefs()
            self.server.reinit(audio=host, jackname=jackname)
        else:
            self.server.reinit(audio="offline_nb", jackname=jackname)
            dur = CeciliaLib.getVar("totalTime")
            filename = CeciliaLib.toSysEncoding(CeciliaLib.getVar("outputFile"))
            fileformat = AUDIO_FILE_FORMATS[CeciliaLib.getVar("audioFileType")]
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
                wx.CallAfter(CeciliaLib.getControlPanel().closeBounceToDiskDialog)
            if time >= (CeciliaLib.getVar("totalTime")):
                wx.CallAfter(CeciliaLib.stopCeciliaSound)
        else:
            CeciliaLib.getVar("grapher").cursorPanel.setTime(CeciliaLib.getVar("startOffset"))
            CeciliaLib.getVar("interface").controlPanel.setTime(0, 0, 0, 0)

    def recstart(self):
        self.server.recstart()

    def recstop(self):
        self.server.recstop()

    def newCtl7Value(self):
        val = self.checkCtl7.get()
        CeciliaLib.getControlPanel().gainSlider.SetValue(val)

    def setAmp(self, x):
        self.amp = math.pow(10.0, x * 0.05)
        self.server.amp = self.amp
        try:
            self.recamp.value = self.amp
        except:
            pass
        try:
            self.specamp.value = self.amp
        except:
            pass

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

    def isAudioServerBooted(self):
        if self.server.getIsBooted():
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
        try:
            execfile(filepath, globals())
        except IOError:
            execfile(CeciliaLib.toSysEncoding(filepath), globals())
        CeciliaLib.setVar("currentModuleRef", copy.deepcopy(Module))
        CeciliaLib.setVar("interfaceWidgets", copy.deepcopy(Interface))
        try:
            CeciliaLib.setVar("presets", copy.deepcopy(CECILIA_PRESETS))
        except:
            CeciliaLib.setVar("presets", {})
        CeciliaLib.getVar("mainFrame").onUpdateInterface(None)

    def loadModule(self, module):
        for i in range(NUM_OF_PLUGINS):
            if self.pluginObjs[i] != None:
               del self.pluginObjs[i].out
               self.pluginObjs[i] = None 
        if self.spectrum != None:
            del self.specamp
            del self.spectrum._timer
            del self.spectrum
            self.spectrum = None
        if self.out != None:
            del self.out
        if CeciliaLib.getVar("systemPlatform") == "darwin":
            try:
                del self.globalamp
            except:
                pass
            try:
                del self.out
            except:
                pass
            try:
                del self.endcall
            except:
                pass
            try:
                del self.recorder
                del self.recamp
            except:
                pass
            try:
                del self.checkCtl7
                del self.onNewCtl7Value
                del self.ctl7TrigFunc
            except:
                pass
        try:
            CeciliaLib.getVar("currentModule").__del__()
            CeciliaLib.setVar("currentModule", None)
        except:
            pass

        currentModule = module()
        currentModule._createOpenSndCtrlReceivers()
        self.out = Sig(currentModule.out)

        plugins = CeciliaLib.getVar("plugins")

        for i in range(NUM_OF_PLUGINS):
            if i == 0:
                tmp_out = self.out
            else:
                tmp_out = self.pluginObjs[i-1].out
            if plugins[i] == None:
                self.pluginObjs[i] = CeciliaNonePlugin(tmp_out)
                self.pluginObjs[i].name = "None"
            else:
                pl = plugins[i]
                name, params, knobs = pl.getName(), pl.getParams(), pl.getKnobs()
                self.pluginObjs[i] = self.pluginDict[name](tmp_out, params, knobs)
                self.pluginObjs[i].name = name

        self.pluginObjs[NUM_OF_PLUGINS-1].out.out()
        CeciliaLib.setVar("currentModule", currentModule)
        currentModule._setWidgetValues()

    def movePlugin(self, vpos, dir):
        i1 = vpos
        i2 = vpos + dir
        tmp = self.pluginObjs[i2]
        self.pluginObjs[i2] = self.pluginObjs[i1]
        self.pluginObjs[i1] = tmp
        for i in range(NUM_OF_PLUGINS):
            if i == 0:
                tmp_out = self.out
            else:
                tmp_out = self.pluginObjs[i-1].out
            self.pluginObjs[i].setInput(tmp_out)
            self.pluginObjs[i].out.play()
        self.pluginObjs[NUM_OF_PLUGINS-1].out.out()

    def setPlugin(self, order):
        plugins = CeciliaLib.getVar("plugins")
        tmp = self.pluginObjs[order]
        if order == 0:
            tmp_out = self.out
        else:
            tmp_out = self.pluginObjs[order-1].out
        if plugins[order] == None:
            self.pluginObjs[order] = CeciliaNonePlugin(tmp_out)
            self.pluginObjs[order].name = "None"
        else:
            pl = plugins[order]
            name, params, knobs = pl.getName(), pl.getParams(), pl.getKnobs()
            self.pluginObjs[order] = self.pluginDict[name](tmp_out, params, knobs)
            self.pluginObjs[order].name = name
        if order < (NUM_OF_PLUGINS - 1):
            self.pluginObjs[order+1].setInput(self.pluginObjs[order].out)
        else:
            self.pluginObjs[order].out.out()
        del tmp

    def checkForAutomation(self):
        plugins = CeciliaLib.getVar("plugins")
        for i in range(NUM_OF_PLUGINS):
            if plugins[i] != None:
                if plugins[i].getName() == self.pluginObjs[i].name:
                    self.pluginObjs[i].checkForAutomation()

    def updatePluginWidgets(self):
        plugins = CeciliaLib.getVar("plugins")
        for i in range(NUM_OF_PLUGINS):
            if plugins[i] != None:
                if plugins[i].getName() == self.pluginObjs[i].name:
                    self.pluginObjs[i].updateWidget()

    def setPluginValue(self, order, which, x):
        plugins = CeciliaLib.getVar("plugins")
        if plugins[order] != None:
            if plugins[order].getName() == self.pluginObjs[order].name:
                self.pluginObjs[order].setValue(which, x)

    def setPluginPreset(self, order, which, label):
        plugins = CeciliaLib.getVar("plugins")
        if plugins[order] != None:
            if plugins[order].getName() == self.pluginObjs[order].name:
                self.pluginObjs[order].setPreset(which, label)

    def setPluginGraph(self, order, which, func):
        plugins = CeciliaLib.getVar("plugins")
        if plugins[order] != None:
            if plugins[order].getName() == self.pluginObjs[order].name:
                self.pluginObjs[order].setGraph(which, func)
        
    def getMidiCtlNumber(self, number, midichnl=1): 
        if not self.midiLearnRange:
            self.midiLearnSlider.setMidiCtl(number)
            self.midiLearnSlider.setMidiChannel(midichnl)
            wx.CallLater(250, self.server.stop)
        else:
            tmp = [number, midichnl]
            if not tmp in self.midiLearnCtlsAndChnls:
                self.midiLearnCtlsAndChnls.append(tmp)
                if len(self.midiLearnCtlsAndChnls) == 2:
                    self.midiLearnSlider.setMidiCtl([self.midiLearnCtlsAndChnls[0][0], self.midiLearnCtlsAndChnls[1][0]])
                    self.midiLearnSlider.setMidiChannel([self.midiLearnCtlsAndChnls[0][1], self.midiLearnCtlsAndChnls[1][1]])
                    wx.CallLater(250, self.server.stop)

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
        defaultInputDriver = inputDriverList[inputDriverIndexes.index(pa_get_default_input())]
        outputDriverList, outputDriverIndexes = pa_get_output_devices()
        defaultOutputDriver = outputDriverList[outputDriverIndexes.index(pa_get_default_output())]
        midiDriverList, midiDriverIndexes = pm_get_input_devices()
        if midiDriverList == []:
            defaultMidiDriver = ""
        else:
            defaultMidiDriver = midiDriverList[midiDriverIndexes.index(pm_get_default_input())]
        return inputDriverList, inputDriverIndexes, defaultInputDriver, outputDriverList, outputDriverIndexes, \
                defaultOutputDriver, midiDriverList, midiDriverIndexes, defaultMidiDriver
    
    def validateAudioFile(self, path):
        if sndinfo(CeciliaLib.toSysEncoding(path)) != None:
            return True
        else:
            return False

    def getSoundInfo(self, path):
        """
        Retrieves information of the sound and prints it to the console.
    
        return (number of channels, sampling rate, duration, fraction of a table, length in samples, bitrate)
        """
        if CeciliaLib.getVar("DEBUG"):
            print '--------------------------------------'
            print path

        info = sndinfo(CeciliaLib.toSysEncoding(path))
                
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
        if CeciliaLib.getVar("DEBUG"):
            print
        return soundDict
        
