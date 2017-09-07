import string as st
import sys
import numpy as np
f=open(sys.argv[1])
iatom=int(sys.argv[2])
jatom=int(sys.argv[3])
lines=f.readlines()

scale=float(lines[1].split()[0])
coord=[]
for i in range(3):
    temp=lines[2+i].split()
    templine=[]
    for j in range(3):
        templine.append(float(temp[j]))
    coord.append(templine)
coord=np.array(coord)
pos1=[]
pos2=[]
for i in lines[7+iatom].split():
    pos1.append(float(i))
for i in lines[7+jatom].split():
    pos2.append(float(i))

pos1=np.array(pos1)
pos2=np.array(pos2)
pos2[1]-=1
posdis=pos1-pos2
refpos=np.array([0.25,-0.25,0.])
#posdis=pos-refpos
print posdis
print coord
dist=np.linalg.norm(scale*np.dot(posdis,coord))
print dist-np.linalg.norm(scale*np.dot(refpos,coord))

