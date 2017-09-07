from scipy import *
import sys,copy
import numpy.linalg as LA
poscar = open(sys.argv[1],'r')
lines = poscar.readlines()
scale = float(lines[1].split()[0])
pos = []
nat = [int(i) for i in lines[6].split()]
for i in range(8,8+sum(nat)):
    pos.append([float(j) for j in lines[i].split()])
pos = array(pos)
poscar0 = open(sys.argv[2],'r')
lines0= poscar0.readlines()
pos0=[]
for i in range(8,8+sum(nat)):
    pos0.append([float(j) for j in lines0[i].split()])
pos0 = array(pos0)
x = [float(i) for i in lines[2].split()]
x = array(x)
lines2 = copy.deepcopy(lines[:8])
lines2[2] = str(2*x[0]) +'   '+ str(x[1])+'    '+ str(x[2])+'   \n'
lines2[6] = ' '.join([str(2*i) for i in nat]) + '\n'

pos_diff = LA.norm(pos-pos0)*scale
print pos_diff

