from numpy import *
#To generate a k path
n=30 #number of points in each division
l=5  #number of divisions 

path=[]
nodes=[]
#start pt is gamma
nodes.append(array([0.0,0.0,0.])) #gamma
nodes.append(array([0.5,0.,0.])) #X
nodes.append(array([0.5,0.5,0.])) #M
nodes.append(array([0.5,0.5,0.5])) #R
nodes.append(array([0.0,0.0,0.0]))

for k in range(len(nodes)-1):
    delta=(nodes[k+1]-nodes[k])/n*1.0 #first division
    for i in range(n):
        path.append(nodes[k]+i*delta)

delta=(nodes[2]-nodes[0])/n*1.0 #first division
for i in range(n):
      path.append(nodes[0]+i*delta)
path.append(nodes[2]) #back to M

print n*l+1
for i in range(n*l+1):
    print '%6f %6f %6f %2.2f' %(path[i][0],path[i][1],path[i][2],1.0)

