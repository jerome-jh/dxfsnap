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
    print(sys.argv[0],'<significant digits> <DXF input file>')
    print()
    print('\tRound all X,Y,Z coordinates to the given number of significant digits. Output modified DXF to stdout.')
    print()

if __name__ == '__main__':
    ## Significant digits
    try:
        digits = int(sys.argv[1])
        filein = open(sys.argv[2], 'rt')
    except:
        usage()
        quit()
    fileout = sys.stdout
    cont = True
    while cont:
        group = filein.readline()
        value = filein.readline()
        if group != '' and value != '':
            g = int(group)
            if g in itertools.chain(*groups):
                v = float(value)
                v = round(v, digits)
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

