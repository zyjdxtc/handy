from scipy import *
import pylab as pl
import sys
G = loadtxt(sys.argv[1])
num = (len(G[0])-1)/2

beta = float(sys.argv[2])
trange = linspace(0,beta,1001)
Gtau = zeros((1001,num))
f = open('Gtau.out','w')


for i,tau in enumerate(trange):
    print >> f, tau,
    for col in range(num):
	if col==1:
	  if tau==0:
	    for j,wn in enumerate(G[:,0]):
            	Gtau[i,col] += 2/beta*(G[j,col*2+1])
	    #Gtau[i,col]+= sum(G[:,col*2+1])/beta
	  elif tau==beta:
	    #print tau
	    for j,wn in enumerate(G[:,0]):
                Gtau[i,col] -= 2/beta*(G[j,col*2+1])	
	    #Gtau[i,col]+= -sum(G[:,col*2+1])/beta
    	  else:
	    for j,wn in enumerate(G[:,0]):
    	   	Gtau[i,col] += 2/beta*(G[j,col*2+1]*cos(wn*tau) + (G[j,col*2+2] + 1./wn)*sin(wn*tau))
    	    Gtau[i,col]-=0.5
	else:
	    for j,wn in enumerate(G[:,0]):
                Gtau[i,col] += 2/beta*(G[j,col*2+1]*cos(wn*tau) + (G[j,col*2+2] + 1./wn)*sin(wn*tau))
            Gtau[i,col]-=0.5
    	print >> f, Gtau[i,col],
    print >>f,''
f.close()
