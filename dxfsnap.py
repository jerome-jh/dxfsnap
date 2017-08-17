#!/usr/bin/python3

import os
import sys
import itertools

##
## From https://www.autodesk.com/techpubs/autocad/acad2000/dxf/group_codes_in_numerical_order_dxf_01.htm
## 10     Primary point; this is the start point of a line or text entity, center of a circle, and so on
##        DXF: X value of the primary point (followed by Y and Z value codes 20 and 30)
##        APP: 3D point (list of three reals)
## 11-18  Other points
##        DXF: X value of other points (followed by Y value codes 21-28 and Z value codes 31-38)
##        APP: 3D point (list of three reals)
## 20, 30 DXF: Y and Z values of the primary point
## 21-28, DXF: Y and Z values of other points 
## 31-37
## 38     DXF: entity's elevation if nonzero
##

## We do not touch 38
groups = (range(10,19), range(20,29), range(30,38))

def usage():
    print(sys.argv[0],'<power of ten> <DXF input file>')
    print()
    print('\tRound all X,Y,Z coordinates to the given power of 10. Output modified DXF to stdout.')
    print()
    print('\tExamples:')
    print('\t\t' + sys.argv[0], 0, 'toto.dxf > tutu.dxf')
    print('\t\t- round to nearest integer, output to "tutu.dxf"')
    print()
    print('\t\t' + sys.argv[0], -3, 'toto.dxf')
    print('\t\t- three significant digits after decimal point, output to stdout')
    print()
    print('\t\t' + sys.argv[0], 1, 'toto.dxf')
    print('\t\t- round to multiples of 10, output to stdout')
    print()

def get_round_f(pot):
    if pot <= 0:
        ## Use built-in Python round()-ing
        ## round(0.5) = 0 but that does not look too bad
        def round_f(f):
            return round(f, -pot)
        return round_f
    else:
        ## Round "as I learned in school" in this case because
        ## pot=1, round(5)=0 will never look acceptable
        m = 10**pot
        def round_f(f):
            if f < 0:
                sign = -1
            else:
                sign = 1
            return m * int(sign * 0.5 + f / m)
        return round_f

def test_round():
    assert(get_round_f(1)(5) == 10)
    assert(get_round_f(1)(4.9999) == 0)
    assert(get_round_f(1)(-5) == -10)
    assert(get_round_f(1)(-4.9999) == 0)
    assert(get_round_f(2)(150) == 200)
    assert(get_round_f(2)(149.9999999) == 100)
    assert(get_round_f(2)(-150) == -200)
    assert(get_round_f(2)(-149.9999999) == -100)

if __name__ == '__main__':
    test_round()
    try:
        digits = int(sys.argv[1])
        filein = open(sys.argv[2], 'rt')
    except:
        usage()
        quit()
    fileout = sys.stdout
    cont = True
    do_round = get_round_f(digits)
    while cont:
        group = filein.readline()
        value = filein.readline()
        if group != '' and value != '':
            g = int(group)
            if g in itertools.chain(*groups):
                v = float(value)
                v = do_round(v)
                fileout.write(group)
                fileout.write(str(v) + os.linesep)
            else:
                fileout.write(group)
                fileout.write(value)
        else:
            ## End of file
            cont = False
    filein.close()
    fileout.close()

