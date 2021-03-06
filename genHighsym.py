# read poscar of high symmetry and distorted one, and split the distorted into segments
import string as st
import numpy as np
import sys
def readpos(fname):
    f=open(fname,'r')
    pos=[]
    lines=f.readlines()
    N=0
    f.close()
    spec=[]
    coord=[]
    for i in lines[6].split():
       spec.append(int(i))
       N=N+int(i)
    for i in range(2,5):
	temp=lines[i].split()
	coord.append([float(temp[0]),float(temp[1]),float(temp[2])])
    coord=np.array(coord)
    for i in range(N):
	temp=lines[8+i].split()
    	pos.append([float(temp[0]),float(temp[1]),float(temp[2])])
	for j in range(3):
	    if pos[-1][j]<-0.1:
		pos[-1][j] += 1.0
	    elif pos[-1][j]>=0.9:
		pos[-1][j] -= 1.0
    pos=np.array(pos)
    fhead=[]
    fhead.append(lines[0:2])
    fhead.append(lines[5:8])
    return coord,pos,fhead,spec

def sort1(pos,spec):
    linemark=0
    N=0
    for num in spec:
	for i in range(num):
	    for j in range(N,N+num-i-1):
	      if pos[j,0]-pos[j+1,0]>0.1:
                temp1=pos[j].copy()
                pos[j]=pos[j+1]
                pos[j+1]=temp1
	      elif abs(pos[j,0]-pos[j+1,0])<0.1 and pos[j,1]-pos[j+1,1]>0.1:
                temp1=pos[j].copy()
                pos[j]=pos[j+1]
                pos[j+1]=temp1

	      elif abs(pos[j,0]-pos[j+1,0])<0.1 and abs(pos[j,1]-pos[j+1,1])<0.1 and pos[j,2]-pos[j+1,2]>0.1:
                temp1=pos[j].copy()
                pos[j]=pos[j+1]
                pos[j+1]=temp1
	N += num
    return pos

def generatePOS(coord_undis,pos_undis,fhead,spec):
    print pos_undis
    pos_inverted=-1.0*pos_undis
    p,q=pos_undis.shape
    pos_temp=[]
    tor=1e-7
    for i in range(p):
        for j in range(3):
            if abs(pos_inverted[i,j])<0.1: continue 
	    else:
		pos_inverted[i,j]=round(pos_inverted[i,j]-round((pos_inverted[i,j]+tor)/abs(tor+pos_inverted[i,j])),8)
        pos_temp.append(pos_inverted[i])
    pos_temp=np.array(pos_temp)
    pos_new=sort1(pos_temp,spec)
    print pos_new
    pos_final=0.5*(pos_new+pos_undis)
    format='%10.7f %10.7f %10.7f'
    f=open('POSCAR-t0','w')
    f.writelines(fhead[0])
    for k in range(3):
       f.write(format %(coord_undis[k,0], coord_undis[k,1], coord_undis[k,2])) 
       f.write('\n')
    f.writelines(fhead[1])
    for j in range(p):
       f.write(format %(pos_final[j,0],pos_final[j,1],pos_final[j,2]))
       f.write('\n')
    f.close()

if __name__=='__main__':
    undis=sys.argv[1]
    coordundis,posundis,fhead,specundis=readpos(undis)
    posundis=sort1(posundis,specundis)
    generatePOS(coordundis,posundis,fhead,specundis)
    print '------------------------------------------------'
