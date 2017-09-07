from math import *
import os,sys,string
#import subprocess as sp
#generate M3[001] rotation in Pbnm symmetry
theta=float(sys.argv[1]) #degree


#use as python R4.py theta(degree)

d=tan(theta/180.0*pi)*0.5
"""
    0.000     0.000     0.000  T T T
    1.000     0.000     0.000  T T T
    0.000     0.000     1.000  T T T
    1.000     0.000     1.000  T T T

    0.500     0.500     0.500  T T T
    0.500    -0.500     0.500  T T T
    0.500     0.500     1.500  T T T
    0.500    -0.500     1.500  T T T

    0.530     0.470     0.000  T T T
    0.470    -0.470     0.000  T T T

    0.470     0.000     0.530  T T T
    1.000    -0.470     0.470  T T T
    1.000     0.470     0.530  T T T
    1.530     0.000     0.470  T T T

    0.470     0.530     1.000  T T T
    0.530    -0.530     1.000  T T T

    0.470     0.000     1.470  T T T
    1.000    -0.470     1.530  T T T
    1.000     0.470     1.470  T T T
    1.530     0.000     1.530  T T T
template
"""
print '0.000     0.000     0.000  T T T'
print '1.000     0.000     0.000  T T T'
print '0.000     0.000     1.000  T T T'
print '1.000     0.000     1.000  T T T'
print '0.500     0.500     0.500  T T T'
print '0.500    -0.500     0.500  T T T'
print '0.500     0.500     1.500  T T T'
print '0.500    -0.500     1.500  T T T'

print 0.5,     0.5,     '0.000  T T T'
print 0.5,     -0.5,    '0.000  T T T'

print 0.5-d,      0.0,       0.5,  'T T T'
print 1.000,     -0.5+d,     0.5, 'T T T'
print 1.000,     0.5-d,      0.5, 'T T T'
print 1.5+d,     0.0,       0.5, 'T T T'

print 0.5,     0.5,     '1.000  T T T'
print 0.5,     -0.5,    '1.000  T T T'

print 0.5-d,     0.0,       1.5,  'T T T'
print 1.0,       -0.5+d,    1.5,  'T T T'
print 1.0,       0.5-d,     1.5,  'T T T'
print 1.5+d,     0.0,       1.5,  'T T T' 
