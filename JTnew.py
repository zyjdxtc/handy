#calculate JT distortion in Pbnm 
#choose oxygen atoms around Mn[1]
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
for Mn in range(4):
 Mn=Mn+1
 if Mn==1:
#Mn=string.split(lines[num+4])
    Oz1=string.split(lines[num+9])
    Oz2=string.split(lines[num+15]) #need correction 
    Ox1=string.split(lines[num+12])
    Ox2=string.split(lines[num+11]) #need correction 
    Oy1=string.split(lines[num+13])
    Oy2=string.split(lines[num+10]) #need correction

    a1=string.split(lines[vec])
    a2=string.split(lines[vec+1])
    a3=string.split(lines[vec+2])
    z=abs(string.atof(Oz2[2])+string.atof(a1[2])-string.atof(Oz1[2]))
    
    x=abs(string.atof(Ox2[0])+string.atof(a2[0])-string.atof(Ox1[0]))


    y=abs(string.atof(Oy2[1])+string.atof(a2[1])-string.atof(Oy1[1]))

 elif Mn==2:
    Oz1=string.split(lines[num+8])
    Oz2=string.split(lines[num+14]) #need correction                                                                        
    Ox1=string.split(lines[num+11])
    Ox2=string.split(lines[num+12]) #need correction                                                                        
    Oy1=string.split(lines[num+10])
    Oy2=string.split(lines[num+13]) #need correction                                                                        

    a1=string.split(lines[vec])
    a2=string.split(lines[vec+1])
    a3=string.split(lines[vec+2])
    z=abs(string.atof(Oz2[2])-string.atof(a1[2])-string.atof(Oz1[2]))

    x=abs(string.atof(Ox2[0])+string.atof(a1[0])-string.atof(Ox1[0]))


    y=abs(string.atof(Oy2[1])-string.atof(a1[1])-string.atof(Oy1[1]))
 elif Mn==3:
    Oz1=string.split(lines[num+15])
    Oz2=string.split(lines[num+9]) #need correction                                                                        
    Ox1=string.split(lines[num+18])
    Ox2=string.split(lines[num+17]) #need correction                                                                        
    Oy1=string.split(lines[num+19])
    Oy2=string.split(lines[num+16]) #need correction                                                                        

    a1=string.split(lines[vec])
    a2=string.split(lines[vec+1])
    a3=string.split(lines[vec+2])
    z=abs(string.atof(Oz2[2])+string.atof(a3[2])-string.atof(Oz1[2]))

    x=abs(string.atof(Ox2[0])+string.atof(a2[0])-string.atof(Ox1[0]))


    y=abs(string.atof(Oy2[1])+string.atof(a2[1])-string.atof(Oy1[1])) 
 elif Mn==4:
    Oz1=string.split(lines[num+14])
    Oz2=string.split(lines[num+8]) #need correction                                                                         
    Ox1=string.split(lines[num+17])
    Ox2=string.split(lines[num+18]) #need correction                                                                        
    Oy1=string.split(lines[num+16])
    Oy2=string.split(lines[num+19]) #need correction                                                                        

    a1=string.split(lines[vec])
    a2=string.split(lines[vec+1])
    a3=string.split(lines[vec+2])
    z=abs(string.atof(Oz2[2])+string.atof(a3[2])-string.atof(Oz1[2]))

    x=abs(string.atof(Ox2[0])+string.atof(a1[0])-string.atof(Ox1[0]))


    y=abs(string.atof(Oy2[1])-string.atof(a1[1])-string.atof(Oy1[1])) 
#print lines[num+14]
 print 'Mn=', Mn
 print 'a1=',a1
 print 'a2=',a2
#x0=string.atof(Mn[0])
#y0=string.atof(Mn[1])
#z0=string.atof(Mn[2])


 print x,y,z
 print 'ox1',Ox1
 print 'ox2',Ox2
 print 'oy1',Oy1
 print 'oy2',Oy2
 print 'oz1',Oz1
 print 'oz2',Oz2
 print 'Q3=',(z-(x+y)/2)/sqrt(3)*sqrt(2)/0.5294,'a.u.'
 print 'Q2=', (x-y)/2.0*sqrt(2)/0.5294,'a.u.'
