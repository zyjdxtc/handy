#get data from different folders and output data and fit and plot

import numpy as np
import string,sys,re
import matplotlib.pyplot as pl
fname =[] 
c=[]
E=[]
if fname==[]: # read from log file 
	logname=sys.argv[1]
	f=open(logname,'r')
	lines=f.readlines()
	   
else: logname= 'cafm+1coarse'
if string.find(logname,'log')>=0:# if the input is a log file containing several folders
  for l in lines:
       num=re.match('Your job (.*) \(.*',l)
       fname.append(num.group(1))

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
	if (flag==0 or flag2==0):# or iteration==nsw):
		print fname[k], 'has a problem'
	f.close()
	f=open(str(fname[k])+'yjzhou/POSCAR','r')
	lines1=f.readlines()
	temp=string.split(lines1[4])
	c.append(string.atof(temp[2]))
	print temp[2]
	f.close()


else: # if the input itself is a Evsc.dat
    for i in range(len(lines)):
	c.append(float(lines[i].split()[0]))
	E.append(float(lines[i].split()[1]))

for jj in range(len(c)): # buble sort, quite stupid method
        for kk in range(len(c)-jj-1): ## sort fname with c value increasingly
                if(c[kk]>c[kk+1]):
                        tem=c[kk+1]
                        c[kk+1]=c[kk]
                        c[kk]=tem
                        tem=E[kk+1]
                        E[kk+1]=E[kk]
                        E[kk]=tem

print c
print E


fitting=np.polyfit(c,E,4)
p=np.poly1d(fitting)
xmin=0
x=np.linspace(c[0],c[-1],1000)
for i in range(998):
	if ((p(x[i])-p(x[i+1]))*(p(x[i+1])-p(x[i+2]))<0):
		xmin=x[i+1]
		break
if xmin ==0 and p(x[0])>p(x[1]):
	xmin=x[-1]
elif xmin ==0 and p(x[0])<p(x[1]):
	xmin=x[1]
print xmin,p(xmin)
print p

pl.figure()

x=np.linspace(c[0],c[-1],100)
la=pl.plot(c,E,'bs',ms=8,label=logname)
lb=pl.plot(x,p(x),'g-',label='fit to eyes')
lc=pl.plot(xmin,p(xmin),'ro')
pl.annotate(('%.3f' % xmin,'%.5f' % p(xmin)), xy=(xmin,p(xmin)))
           
ll = pl.legend(loc='upper right')
lx = pl.xlabel('c/a')
ly = pl.ylabel('E (eV/f.u.)')


pl.show()
