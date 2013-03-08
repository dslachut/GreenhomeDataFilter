#!/usr/bin/env python

from sys import argv,exit

def main(fname,cut=0.0):
    lines = []
    outlines = []
    with open(fname) as FILE:
        lines = FILE.readlines()
    for line in lines:
        vals = line.split(',')
        try:
            if float(vals[1]) >= cut:
                outlines.append(line)
        except:
            print 'BAD: %s' % line
    outs = ''.join(outlines)
    with open(fname,'w') as FILE:
        FILE.write(outs)

if __name__=='__main__':
    if len(argv) == 2:
        exit(main(argv[1]))
    elif len(argv) == 3:
        exit(main(argv[1],cut=float(argv[2])))