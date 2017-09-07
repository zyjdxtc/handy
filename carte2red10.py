# This is for cartesian positions to reduced positions of sqrt(2)*sqrt(2)*2 cell

from math import *
import sys,os,string
import subprocess as sp

inputname=sys.argv[1]
f=open(inputname,'r')
lines= f.readlines()
f.close()
num=0
vec=0
for l in range(len(lines)):
    if(string.find(lines[len(lines)-l-1],'POSITION')>0): #search from the end
        num=len(lines)-l-1  #find 'POSITION'
    if(string.find(lines[len(lines)-l-1],'direct lattice vectors')>0):
        vec=len(lines)-l-1 
        break
num=num+2 #beginning of data
vec=vec+1 #beginning of lattice vector 

aa=string.split(lines[vec])
bb=string.split(lines[vec+1])
cc=string.split(lines[vec+2])

a=sqrt(string.atof(aa[0])**2+string.atof(aa[1])**2)
b=sqrt(string.atof(bb[0])**2+string.atof(bb[1])**2)
c=string.atof(cc[2])

for i in range(10):
    temp=string.split(lines[num+i])
    print string.atof(temp[0])/a, string.atof(temp[1])/b, string.atof(temp[2])/c

print 'Basis vectors'
print a,0,0
print 0,b,0
print 0,0,c
