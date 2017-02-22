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

# Random:
# Randomly choose, within a certain range, a new next value
# arg 1: maxStepSize (negative value not allowed stepSize == 0)
# arg 2: maximum value allowed

import random

class Drunk:
    def __init__(self, minValue, maxValue):
        self.lastValue = random.randint(minValue, maxValue)
        self.minValue = minValue
        self.maxValue = maxValue

    def next(self, maxStepSize=-2):
        """Method to call a new value from a generator objet.

drunk, droneAndJump, repeater and loopseg:
maxStepSize = -2

markov:
no argument

--- PARAMETERS ---

maxStepSize : Maximum step size for each call. If negative, repetition are not permitted.
"""
        if self.lastValue < self.minValue or self.lastValue > self.maxValue:
            return random.randint(self.minValue, self.maxValue)

        direction = self.getDirection()
        stepSize = self.getStepSize(direction, abs(maxStepSize))

        if maxStepSize < 0:
            minStepSize = 1
        else:
            minStepSize = 0

        self.lastValue += direction * random.randint(minStepSize, stepSize)

        if self.lastValue < self.minValue:
            self.lastValue = self.minValue
        elif self.lastValue > self.maxValue:
            self.lastValue = self.maxValue
        else:
            self.lastValue = self.lastValue

        return self.lastValue

    def getDirection(self):
        if self.lastValue == self.minValue:
            return 1
        elif self.lastValue == self.maxValue:
            return -1
        else:
            return random.choice([1, -1])

    def getStepSize(self, direction, maxStepSize):
        if direction == -1:
            return min(maxStepSize, self.lastValue - self.minValue)
        else:
            return min(maxStepSize, self.maxValue - self.lastValue)

    def setLastValue(self, val):
        self.lastValue = val

class DroneAndJump(Drunk):
    def __init__(self, minValue, maxValue):
        Drunk.__init__(self, minValue, maxValue)
        self.minValue = minValue
        self.maxValue = maxValue
        self.beforeLastValue = random.randint(minValue, maxValue)
        self.lastValue = self.beforeLastValue + 1

    def next(self, maxStepSize=-2):
        if self.beforeLastValue != self.lastValue:
            self.lastValue = self.beforeLastValue
            return self.beforeLastValue

        self.beforeLastValue = self.lastValue
        self.lastValue = Drunk.next(self, abs(maxStepSize))
        return self.lastValue

    def getStepSize(self, direction, maxStepSize):
        if random.randint(0, 100) < 25:
            return Drunk.getStepSize(self, direction, maxStepSize)
        else:
            return Drunk.getStepSize(self, direction, 0)

    def setLastValue(self, val):
        self.beforeLastValue = val
        self.lastValue = self.beforeLastValue + 1

class Repeater(Drunk):
    def __init__(self, minValue, maxValue):
        Drunk.__init__(self, minValue, maxValue)
        self.minValue = minValue
        self.maxValue = maxValue
        self.lastValue = random.randint(minValue, maxValue)

    def next(self, maxStepSize=-2):
        self.lastValue = Drunk.next(self, abs(maxStepSize))
        return self.lastValue

    def getStepSize(self, direction, maxStepSize):
        if random.randint(0, 100) < 20:
            return Drunk.getStepSize(self, direction, maxStepSize)
        else:
            return Drunk.getStepSize(self, direction, 0)

class Loopseg(Drunk):
    def __init__(self, minValue, maxValue):
        Drunk.__init__(self, minValue, maxValue)
        self.minValue = minValue
        self.maxValue = maxValue
        self.recordedValues = []
        self.recordState = 2
        self.recordPlayback = 0
        self.loopPlayback = 1
        self.recordLength = random.randint(3, 6)
        self.recordLoopTime = random.randint(1, 4)

    def next(self, maxStepSize=-2):
        if self.recordState == 2:
            self.lastValue = Drunk.next(self, maxStepSize)
            self.recordState = random.choice([2, 2, 2, 1])

        if len(self.recordedValues) != self.recordLength and self.recordState == 1:
            self.lastValue = Drunk.next(self, maxStepSize)
            self.recordedValues.append(self.lastValue)
        elif self.recordState == 1 or self.recordState == 0:
            self.recordState = 0
            if self.recordPlayback < self.recordLength:
                self.loopAround()
            else:
                if self.loopPlayback < self.recordLoopTime:
                    self.recordPlayback = 0
                    self.loopPlayback += 1
                    self.loopAround()
                else:
                    self.recordedValues = []
                    self.recordState = 2
                    self.recordPlayback = 0
                    self.loopPlayback = 1
                    self.recordLength = random.randint(3, 6)
                    self.recordLoopTime = random.randint(1, 4)
                    self.lastValue = Drunk.next(self, maxStepSize)
                    self.recordedValues = [self.lastValue]
        return self.lastValue

    def loopAround(self):
        self.lastValue = self.recordedValues[self.recordPlayback]
        self.recordPlayback += 1