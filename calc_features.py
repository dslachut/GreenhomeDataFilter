#!/usr/bin/env python

from datetime import datetime,timedelta
from sys import argv

def getDateTime(ts,res):
    out = datetime.utcfromtimestamp(ts/1000)
    out = out.replace(hour=int(out.hour/res),minute=0,second=0,microsecond=0)
    return out

def resolution(flags):
    if 'h' in flags or 'php' in flags:
        return 1
    elif 'qd' in flags or 'qpq' in flags:
        return 6
    elif 'hd' in flags:
        return 12
    elif 'd' in flags: 
        return 24
    return 0
    
def readStatuses(fname,res):
    statuses = []
    with open(fname) as FILE:
        for line in FILE:
            vals = line.split(',')
            status = {}
            status['datetime'] = getDateTime(int(vals[0]),res)
            status['power'] = float(vals[1])
            statuses.append(status)
    return statuses
    
def makePoint(key,flags,res):
    point = {}
    point['pwrsum'] = 0.0
    point['numpts'] = 0
    if 'd' in flags:
        point['day'] = key.weekday()
    if res == 1:
        if 'hd' in flags:
            point['half'] = int(key.hour/12)
        if 'qd' in flags:
            point['quarter'] = int(key.hour/6)
        if 'h' in flags:
            point['hour'] = key.hour
    elif res == 6:
        if 'hd' in flags:
            point['half'] = int(key.hour/2)
        if 'qd' in flags:
            point['quarter'] = key.hour
    elif res == 12:
        if 'hd' in flags:
            point['half'] = key.hour
    return point
    
def rmBad(datapoints,badpoints):
    print 'bad', len(badpoints)
    for key in badpoints:
        if key in datapoints:
            del datapoints[key]
    
def figurePHP(points,badpoints):
    shift = timedelta(hours=1)
    #badpoints = []
    for key,point in points.iteritems():
        try:
            point['php'] = points[key-shift]['pwravg']
        except:
            badpoints.append(key)
    #rmBad(points,badpoints)
    
def figurPQP(points,res,badpoints):#rewrite using pwrsum and numpts!!!!!!
    #badpoints = []
    if res == 1:
        shift = timedelta(hours=6)
        for key,point in points.iteritems():
            pq = (key-shift).hour/6
            pqpsum = 0.0
            pqpcnt = 0
            for i in range(10):
                sh = timedelta(hours=i+1)
                candidate = key-sh
                if candidate.hour/6 == pq:
                    try:
                        pqval += points[candidate]['pwravg']
                    except:
                        continue
                    pqpsum += pqval
                    pqpcnt += 1
                if pqpcnt >= 6:
                    break
            if not (pqpcnt in range(1,7)):
                badpoints.append(key)
            try:
                point['pqp'] = spqpsum / float(pqpcnt)
            except:
                badpoints.append(key)
    if res == 6:
        shift = timedelta(hours=1)
        for key,point in points.iteritems():
            pq = key-shift
            if pq >= 4: pq = 3
            try:
                point['pqp'] = points[pq]['pwravg']
            except:
                badpoints.append(key)
    #rmBad(points,badpoints)
    
def figurePQP(points,res,badpoints):
    #badpoints = []
    if res == 6:
        shift = timedelta(hours=1)
        for key,point in points.iteritems():
            pq = key-shift
            if pq.hour >= 4: pq = pq.replace(hour=3)
            try:
                point['pqp'] = points[pq]['pwravg']
            except:
                badpoints.append(key)
    if res == 1:
        for key,point in points.iteritems():
            qoffset = key.hour % 6
            pwrsum = 0.0
            numpts = 0
            for i in range(1,7):
                shift = timedelta(hours=(i+qoffset))
                pt = key-shift
                try:
                    pwrsum += points[pt]['pwrsum']
                    numpts += points[pt]['numpts']
                except:
                    continue
            if numpts == 0: 
                badpoints.append(key)
            else:
                point['pqp'] = pwrsum/float(numpts)
    #rmBad(points,badpoints)
    
def figurePHalfP(points,res,badpoints):
    #badpoints = []
    if res == 6:
        for key,point in points.iteritems():
            hoffset = key.hour % 2
            pwrsum = 0.0
            numpts = 0
            for i in range(1,3):
                shift = timedelta(hours=(i+hoffset))
                pt = key-shift
                if pt.hour > 3: pt = pt.replace(hour=3)
                try:
                    pwrsum += points[pt]['pwrsum']
                    numpts += points[pt]['numpts']
                except:
                    continue
            if numpts == 0:
                badpoints.append(key)
            else:
                point['pHap'] = pwrsum/float(numpts)
    if res == 1:
        for key,point in points.iteritems():
            hoffset = key.hour % 12
            pwrsum = 0.0
            numpts = 0
            for i in range(1,13):
                shift = timedelta(hours=(i+hoffset))
                pt = key-shift
                try:
                    pwrsum += points[pt]['pwrsum']
                    numpts += points[pt]['numpts']
                except:
                    continue
            if numpts == 0:
                badpoints.append(key)
            else:
                point['pHap'] = pwrsum/float(numpts)
    #rmBad(points,badpoints)
    
def figurePDP(points,res,badpoints):
    #badpoints = []
    prevDayNum = -1
    prevDayPwr = -1
    for key,point in points.iteritems():
        prevDay = key.replace(day=(key.day-1),hour=0)
        if prevDay.day == prevDayNum:
            point['pdp'] = prevDayPwr
        else:
            pwrsum = 0.0
            numpts = 0
            for i in range(24):
                shift = timedelta(hours=i)
                pt = prevDay + shift
                try: 
                    pwrsum += points[pt]['pwrsum']
                    numpts += points[pt]['numpts']
                except:
                    continue
            if numpts == 0:
                badpoints.append(key)
            else:
                prevDayNum = prevDay.day
                prevDayPwr = pwrsum/float(numpts)
                point['pdp'] = prevDayPwr
    #rmBad(points,badpoints)
    
def figurePwrAvgs(points,badpoints):
    #badpoints = []
    for key,point in points.iteritems():
        try:
            point['pwravg'] = point['pwrsum'] / float(point['numpts'])
        except:
            badpoints.append(key)
            continue
    #rmBad(points,badpoints)
    
def figureTSOnOff(points,res,badpoints):
    #badpoints = []
    maxuse = 0.0
    for key,point in points.iteritems():
        if point['pwravg'] > maxuse:
            maxuse = point['pwravg']
    threshold = maxuse / 10.0
    for key,point in points.iteritems():
        if point['pwravg'] > threshold:
            point['onoff'] = 1
        else:
            point['onoff'] = 0
    lastOn = None
    lastOff = None
    for key in sorted(points.keys()):
        if points[key]['onoff'] == 1:
            lastOn = 0
            try:
                lastOff += res
            except:
                continue
        else:
            lastOff = 0
            try:
                lastOn += res
            except:
                continue
        points[key]['lastOn'] = lastOn
        points[key]['lastOff'] = lastOff
    #rmBad(points,badpoints)
    
def writeStatuses(fname,points,psum=False):
    outLines = []
    for key in sorted(points[points.keys()[0]].keys()):
        if not (key in ['pwravg','pwrsum','numpts','onoff']):
            print key,
    print 'pwravg'
    for key,point in points.iteritems():
        outLine = []
        for k in sorted(point.keys()):
            if not (k in ['pwravg','pwrsum','numpts','onoff']):
                outLine.append(str(point[k]))
        if psum:
            outLine.append(str(point['pwrsum']))
        else:
            outLine.append(str(point['pwravg']))
        outLines.append(','.join(outLine))
    print 'OL', len(outLines)
    with open(fname,'w') as FILE:
        FILE.write('\n'.join(outLines))
    
def parse(rfname,wfname,flags=['d','h','hd','qd','php','pqp','tso','pHap','pdp']):
    res = resolution(flags)
    statuses = readStatuses(rfname,res)
    print 'statuses', len(statuses)
    datapoints = {}
    badpoints = []
    for status in statuses:
        key = status['datetime']
        if not (key in datapoints):
            datapoints[key] = makePoint(key,flags,res)
        datapoints[key]['pwrsum'] += status['power']
        datapoints[key]['numpts'] += 1
    print 'numpts',len(datapoints)
    figurePwrAvgs(datapoints,badpoints)
    print 'pwravg', len(datapoints)
    if 'php' in flags:
        figurePHP(datapoints,badpoints)
    print 'php', len(datapoints)
    if 'pqp' in flags:
        figurePQP(datapoints,res,badpoints)
    print 'pqp', len(datapoints)
    if 'tso' in flags:
        figureTSOnOff(datapoints,res,badpoints)
    if 'pHap' in flags:
        figurePHalfP(datapoints,res,badpoints)
    if 'pdp' in flags:
        figurePDP(datapoints,res,badpoints)
    
    rmBad(datapoints,badpoints)
    
    if 'sum' in flags:
        writeStatuses(wfname,datapoints,psum=True)
    else:
        writeStatuses(wfname,datapoints)

if __name__=='__main__':
    if len(argv) < 3:
        print "Usage: ./calc_features.py readPath writePath features"
    elif len(argv) ==3 :
        parse(argv[1],argv[2])
    else:
        parse(argv[1],argv[2],flags=argv[3:])