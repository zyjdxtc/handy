#plot e band structure from the EIGENVAL file.
#plot 2bands on top of each other
import numpy as np
import matplotlib.pyplot as pl
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import sys,string
import numpy.linalg as LA

def plotband(ax,fname,fermi,erange,spin,col):
	f= open(fname,'r')
	lines=f.readlines()
	N=20 #points in each section
	startline=1000 #a large number at beginning

	#fig=pl.figure()
	n=-1
	onekpt=[]
	band=[]
	kpt2=[]
	i=0
	kpts=[]
	while i<len(lines):
	    temp=string.split(lines[i])
	    if ((string.find(lines[i],'E')>0 and len(temp)==4)):
		kpt1=lines[i]
		kpts.append([float(temp[0]),float(temp[1]),float(temp[2])])
		startline=i
		n=n+1
		
		if (kpt2==kpt1):
		    i=i+len(band[0])
		    n=n-1
		    kpts.pop() # remove this kpt
		kpt2=kpt1
		if len(onekpt)>1:
		    band.append(onekpt)
		    onekpt=[]
		num=n
	#print startline
	    elif(i>startline and len(temp)<4 and len(temp)>1):
	      
		#print temp
		onekpt.append(float(temp[spin])-fermi)
		if (i==len(lines)-1):
		    band.append(onekpt)
	    i=i+1
	kpts=np.array(kpts)

	print len(band[-1]),len(band[0])
	print num
	bandstr=np.array(band)
	print bandstr
	for i in range(len(band[0])):
	    if(erange != 0 ):
		pl.plot(bandstr[:,i],c=col)
	    elif erange ==0:
		pl.plot(bandstr[:,i],c=col)
	#ax=fig.add_subplot(111)
	pl.axhline(y=0)

	#kpath=np.array([[0,0,0],[0.5,0.,0],[0.5,0.5,0],[0,0,0]])
	kpath=np.array([[0,0,0],[0.5,0.,0],[0.5,0.5,0],[0,0,0]])
	#kpath=np.array([[0.0,0.0,0],[0.,0.,0.5],[1.0/3,1.0/3,0.5],[1.0/3,1.0/3,0.],[0,0.,0.],[0.5,0,0],[0.5,0,0.5]])
	xticker=[]
	j=0
	for i in range(len(kpts)):
	    
	    if LA.norm(kpts[i]-kpath[j])==0:
		xticker.append(i)
		j+=1
		pl.axvline(x=i)

	#pl.xlabel('kpath')
	pl.ylabel('Energy (eV)')
	#pl.title('Band structure near fermi energy')
	pl.xlim(0,num)
	if erange!=0:
	     pl.ylim(-erange,erange)
	#xlabels = ["$\Gamma$","A","H",'K',"$\Gamma$",'M','L']
	xlabels= ["$\Gamma$","X","M",'$\Gamma$']
	ax.set_xticks(xticker)
	ax.set_xticklabels(xlabels)
	#ax.reset_ticks()
	#pl.show()    


def main():
	fname = sys.argv[1]  # EIGVALUE file
	fermi=string.atof(sys.argv[2]) #fermi level
	erange=float(sys.argv[7]) # plotting range from fermi level
	spin=int(sys.argv[3]) #choose to plot band for spin 1 or 2
	fname2=sys.argv[4]
	fermi2=float(sys.argv[5])
	spin2=int(sys.argv[6])
	fig=pl.figure()
	ax=fig.add_subplot(111)
	plotband(ax,fname,fermi,erange,spin,'k')
	plotband(ax,fname2,fermi2,erange,spin2,'r')
	pl.show()

if __name__=='__main__':
    main()
