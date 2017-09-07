import numpy as np
import pylab as pl
import sys 
from parse import parse_procar


def gau(x,x0,sigma):
    return np.exp(-(x-x0)**2/2/sigma/sigma)


def main():
  
  data=parse_procar(sys.argv[1])
  
  Ef=float(sys.argv[2])
  fig=pl.figure()
#ax=fig.add_subplot(111)
  nkpt=data[3].shape[0]
  dE=0.1
  sigma=0.02
  nband=data[3].shape[1]
  E=np.arange(-5,5,dE)
  kpt=np.arange(0,nkpt,1)
  spect=np.zeros((nkpt,len(E)))
  for x in range(nkpt):
      for y in range(len(E)):
      	  result=0
	  for j in range(nband):
	      result+=gau(data[3][x,j,0],E[y],sigma)*sum(data[-2][x,:,j,0,0])
	  spect[x,-1-y]=result
  #for i in range(nkpt):
  #    spect[i]*=1.0/max(spect[i])
  #def readspect(x,y,sigma,data):
  #   result=0
  #   for j in range(nband):
#	result+=gau(data[3][x,j,0],E[y],sigma)*sum(data[-2][x,:,j,0,0])
#     return result
#  spect=readspect(X,Y,sigma,data)   
  #for i in range(nkpt):
  #   for j in range(nband):
  #   	for energy in range(NE)
  #   col=sum(data[-2][i,:,:,0,0])
  #   pl.scatter([i]*data[3].shape[1],data[3][i,:,0],s=15, c=col,vmin=min(col),vmax=max(col),edgecolors='none')
  pl.imshow(spect.T,alpha=.9, interpolation='bicubic')
  pl.colorbar()
  for i in range(len(E)):
      if E[i]<Ef and E[i+1]>Ef:
          pl.axhline(y=len(E)-1-i,color='w')
          break
  pl.show()
main()
