import numpy as np
import string,sys
import matplotlib.pyplot as pl
fname = 'afm_1.dat'
f=open(fname,'r')
lines=f.readlines()
c=[]
E=[]

leng=len(lines)
#for l in range(leng):
#	if (string.find(lines[leng-l],'TOTEN')>0):


for l in range(leng):
       	temp=string.split(lines[l])	
	if (temp[0]<='9' and temp[0]>='0'):
		c.append(string.atof(temp[0]))
		E.append(string.atof(temp[1]))

fitting=np.polyfit(c,E,4)
p=np.poly1d(fitting)

x=np.linspace(c[0],c[-1],1000)
for i in range(1000):
	if ((p(x[i])-p(x[i+1]))*(p(x[i+1])-p(x[i+2]))<0):
		xmin=x[i+1]
		break
print xmin,p(xmin)
print p
print E

pl.figure()

x=np.linspace(c[0],c[-1],100)
la=pl.plot(c,E,'.',label='afm with 1 strain')
lb=pl.plot(x,p(x),label='fit to eyes')
lc=pl.plot(xmin,p(xmin),'o')
pl.annotate(('%.3f' % xmin,'%.4f' % p(xmin)), xy=(xmin,p(xmin)))
           
ll = pl.legend(loc='upper right')
lx = pl.xlabel('c/a')
ly = pl.ylabel('E (eV/f.u.)')


pl.show()
