import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pl
import sys
import subprocess as sp
#from mpl_toolkits.mplot3d import Axes3D
def main():
   fname=sys.argv[1]
   sp.call(['gunzip',fname+'.gz'])
   f=open(fname)
   natom=int(sys.argv[2])
   for i in range(8+natom+1):
       f.readline()
   temp=f.readline().split()
   ngx=int(temp[0])
   ngy=int(temp[1])
   ngz=int(temp[2])
   N=ngx*ngy*ngz # total FFT points
   
   data=[]
   print '----------begin read data-------------'
   for i in range(N/5):
       temp=f.readline().split()
       for j in temp:
           data.append( float(j) )
   data=np.array(data)
   Cmax=max(data)
   data=np.reshape(data,(ngz,ngy,ngx))
   z,y,x=np.nonzero(data)
   print x.shape,y.shape,z.shape,data.shape
   n_xy=ngx*ngy
   ave_z=[]
   for i in range(ngz):
       ave_z.append(np.sum(data[i])/n_xy)
   ave_z=np.array(ave_z)
   print '----------begin plotting------------'
   fig=pl.figure()
   ax = fig.add_subplot(111)
   ax.plot(ave_z,'ro')     
   #ax.scatter(x,y,z,s=data/Cmax*20,c='r',marker='o',edgecolor='none',alpha=0.6)
   pl.show() 
   f.close()
   sp.call(['gzip',fname])
if __name__=="__main__":
   main()
       
   
