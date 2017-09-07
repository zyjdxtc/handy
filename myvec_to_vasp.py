############################################################################################
#This code is to transform eigenvectors of phonon modes between my way and VASP way
#Use: python myvec_vasp.py filename mode(v2m or m2v)
############################################################################################


import numpy as np
import string as st
import sys

fname=sys.argv[1]
#fvasp=sys.argv[2]
choice=sys.argv[2]

mass=[87.620,138.9,54.938,54.938,16,16,16,16,16,16]
name=['Sr','La','Mn1','Mn2','O1z','O1x','O1y','O2z','O2x','O2y']
f=open(fname,'r')
lines1=f.readlines()
f.close()
#f=open(fvasp,'r')
#lines2=f.readlines()

if choice == 'v2m':
    amp=[]

    if st.find(fname,'cafm')<0:
     for i in range(10):

        temp=st.split(lines1[i+2])
        amp.append(float(temp[-1])/mass[i])
  
    else:
     for i in range(10):

        temp=st.split(lines1[i])
        amp.append(float(temp[-1])/mass[i])
  
    norm=sum(amp)

    for i in range(10):
        amp[i]=amp[i]/norm
        print name[i]+' Amplitude',amp[i]
elif choice == 'm2v':
    amp=[]

    for i in range(10):
        temp=st.split(lines1[i])
        amp.append(float(temp[-1])*mass[i])
  
    norm=sum(amp)
    
    amp[i]=amp[i]/norm
    for i in range(10):
        amp[i]=amp[i]/norm
        print name[i]+' Amplitude',amp[i]
else:
    print 'You have chosen an unknown mode~'
