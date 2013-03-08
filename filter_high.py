#!/usr/bin/env python

from sys import argv
from math import sqrt

def main(fname,StdDevs=10):
    pwrvalLst = []
    with open(fname) as FILE:
        for line in FILE:
            val = line.split(',')
            pwrval = float(val[1])
            if pwrval >= 0.0:
                pwrvalLst.append(pwrval)
    pwrvalSum = sum(pwrvalLst)
    pwrvalCnt = len(pwrvalLst)
    pwrvalAvg = pwrvalSum / float(pwrvalCnt)
    pwrvalSDM = []
    for val in pwrvalLst:
        pwrvalSDM.append((val-pwrvalAvg)**2)
    pwrvalStD = sqrt(sum(pwrvalSDM)/float(pwrvalCnt))
    with open(fname) as FILE:
        for line in FILE:
            val = line.split(',')
            y = float(val[1])
            if y > (pwrvalAvg + (pwrvalStD * StdDevs)):
                print y
    print pwrvalAvg, pwrvalStD, pwrvalAvg + (pwrvalStD * StdDevs)

def main2(fname, cut = 2400.0):
    outlines = []
    with open(fname) as FILE:
        for line in FILE:
            if float(line.split(',')[1]) < cut:
                outlines.append(line)
            else: print line,
    outs = ''.join(outlines)
    with open(fname,'w') as FILE:
        FILE.write(outs)

if __name__=='__main__':
    if len(argv) == 3:
        main2(argv[1],float(argv[2]))
    else:
        main2(argv[1])