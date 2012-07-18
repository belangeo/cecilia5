#!/usr/bin/env python
# encoding: utf-8
"""
Grapher's line parser.
"""

def import_after_effects_automation(text):
    lines = text.splitlines()
    if not 'Adobe After Effects' in lines[0]:
        return None

    inside_data = False
    need_to_check_minmax = False
    framesPerSecond = 29.97
    mini = 0
    maxi = 1
    data = []

    for line in lines[1:]:
        if 'Units Per Second' in line:
            elements = line.split("\t")
            index = elements.index('Units Per Second')
            framesPerSecond = float(elements[index+1])
            break

    for i, line in enumerate(lines[1:]):
        if line.strip() == "":
            continue
        else:
            elements = line.split("\t")
            while "" in elements:
                elements.remove("")
            if "Frame" in elements:
                inside_data = True
                if len(elements) == 1:
                    need_to_check_minmax = True
                elif "percent" in elements:
                    mini, maxi = 0, 100
                elif "degrees" in elements:
                    mini, maxi = -360, 360
                else:
                    need_to_check_minmax = True
            elif "End of Keyframe Data" in elements:
                inside_data = False
            elif inside_data:
                data.append([float(elements[0]) / framesPerSecond, float(elements[1])])

    if need_to_check_minmax:
        mini, maxi = min([x[1] for x in data]), max([x[1] for x in data])

    data = [[x[0]/data[-1][0], x[1]] for x in data]
    data = [[x[0], (x[1] - mini) / (maxi - mini)] for x in data]
    if data[0][0] != 0.0:
        tmp = [0.0, data[0][1]]
        data.insert(0, tmp)
    data = {'curved': False, 'data': data}
    return data
    