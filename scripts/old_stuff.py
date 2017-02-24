def removeDuplicates(seq):
   result = []
   for item in seq:
       if item not in result:
           result.append(item)
   return result

###### Interpolation functions ######
def interpolate(lines, size, listlen):
   scale = size / lines[-1][0]
   templist = []
   for i in range(listlen - 1):
       t = lines[i + 1][0] - lines[i][0]
       num = int(round(t * scale))
       if num == 0:
           pass
       else:
           step = (lines[i + 1][1] - lines[i][1]) / num
           for j in range(num):
               templist.append(lines[i][1] + (step * j))
   return templist

def interpolateCurved(lines, size, listlen):
    lines = removeDuplicates(lines)
    scale = size / float(len(lines))
    depth = int(round(scale))
    off = int(1. / (scale - depth))
    templist = []
    for i in range(len(lines) - 1):
        num = depth
        if (i % off) == 0: num = depth + 1
        step = (lines[i + 1][1] - lines[i][1]) / num
        for j in range(num):
            templist.append(lines[i][1] + (step * j))
    return templist

def interpolateLog(lines, size, listlen, yrange):
    scale = size / lines[-1][0]
    templist = []
    for i in range(listlen - 1):
        t = lines[i + 1][0] - lines[i][0]
        num = int(round(t * scale))
        if num == 0:
            pass
        else:
            step = (lines[i + 1][1] - lines[i][1]) / num
            for j in range(num):
                templist.append(lines[i][1] + (step * j))
    list = []
    if yrange[0] == 0: yoffrange = .00001
    else: yoffrange = yrange[0]
    totalRange = yrange[1] - yoffrange
    currentTotalRange = math.log10(yrange[1] / yrange[0])
    currentMin = math.log10(yrange[0])
    for p in templist:
        if p == 0: p = .00001
        ratio = (p - yoffrange) / totalRange
        list.append(math.pow(10, ratio * currentTotalRange + currentMin))
    return list
