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
	    if pos[-1][j]<-0.2:
		pos[-1][j] += 1.0
	    elif pos[-1][j]>=0.8:
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

def generatePOS(coord_undis,pos_undis,coord_dis,pos_dis,n,fhead):
    n=int(n)
    diff=(pos_dis-pos_undis)/n
    coorddiff=(coord_dis-coord_undis)/n
    p,q=pos_dis.shape
    format='%10.7f %10.7f %10.7f'
    for i in range(n+1):
	temp=diff*i+pos_undis
	tempcoord=coorddiff*i+coord_undis
	f=open('POS_'+str(i),'w')
	f.writelines(fhead[0])
	for k in range(3):
	    f.write(format %(tempcoord[k,0], tempcoord[k,1], tempcoord[k,2])) 
	    f.write('\n')
	f.writelines(fhead[1])
	for j in range(p):
	    f.write(format %(temp[j,0],temp[j,1],temp[j,2]))
	    f.write('\n')
        f.close()
    print diff

if __name__=='__main__':
    undis=sys.argv[1]
    dis=sys.argv[2]
    N=sys.argv[3]
    coordundis,posundis,fhead,specundis=readpos(undis)
    coorddis,posdis,fhead,specdis=readpos(dis)
    posundis=sort1(posundis,specundis)
    posdis=sort1(posdis,specdis)
    generatePOS(coordundis,posundis,coorddis,posdis,N,fhead)
    print '------------------------------------------------'
    print posundis
    print '------------------------------------------------'
    print posdis
