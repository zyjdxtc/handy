#get data from different folders and output data and fit and plot

import numpy as np
import string,sys
import matplotlib.pyplot as pl


def plot(fname,amp):
  E=[]
  for k in range(len(fname)):
	f=open(str(fname[k])+'yjzhou/OUTCAR','r')
	lines=f.readlines()
	leng=len(lines)
	flag=0 # flag of finding 'TOTEN'
	flag2=0 #flag for a complete outcar
	for l in range(leng):
		if (string.find(lines[leng-l-1],'General timing and accounting informations for this job:')>=0):
			flag2=1
		if (string.find(lines[leng-l-1],'TOTEN')>0): 
			temp=string.split(lines[leng-l-1])	
			for j in range(len(temp)):
				if (temp[j]>='-' and temp[j]<='9'):
					E.append(string.atof(temp[j]))
					flag=1
			break
	if (flag==0 or flag2==0):
		print fname[k], 'has a problem'
	f.close()

  EE=[]
  for i in range(len(E)):
    EE.append(E[-i-1])
  EE=EE+E[1:]
  fitting=np.polyfit(amp,EE,4)
  print fitting
  p=np.poly1d(fitting)
  print p
  return EE,p
#x=np.linspace(c[0],c[-1],1000)
#for i in range(1000):
#	if ((p(x[i])-p(x[i+1]))*(p(x[i+1])-p(x[i+2]))<0):
#		xmin=x[i+1]
#		break
#print xmin,p(xmin)
#print p

def main():
	#fname = [[27044,27042,27040,27037,24727,27038,27039,27041,27043],[27434,27435,27436,27437,24759,27428,27429,27430,27431]]
	fname=[[24727,27830,27872,27832,27833,24953,27834,27835,27836],[24759,27776,27778,27777,27779,27047,27780,27781,27789]]
        amp=[-1.8,-1.4,-1.2,-1,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1,1.2,1.4,1.8]#np.arange(-1.6,1.7,0.2)
	(Eafm,p1)=plot(fname[0],amp)

	(Efm,p2)=plot(fname[1],amp)

	pl.figure()

	x=np.linspace(amp[0],amp[-1],100)
	la=pl.plot(amp,Eafm,'bs',ms=8,label='AFM')
	lb=pl.plot(x,p1(x),'g-',label='fit to eyes')
#	lc=pl.plot(amp,Efm,'ro',ms=8,label='FM')
#        ld=pl.plot(x,p2(x),'k-',label='fit to eyes')
#lc=pl.plot(xmin,p(xmin),'ro')
#pl.annotate(('%.3f' % xmin,'%.4f' % p(xmin)), xy=(xmin,p(xmin)))
           
	ll = pl.legend(loc='upper left')
	lx = pl.xlabel('In-plane FE distortion amplitude')
	ly = pl.ylabel('E (eV/f.u.)')


	pl.show()

main()
