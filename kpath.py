import numpy as np
import numpy.linalg as LA

def k_path(k,lat):
    V=np.dot(lat[0],np.cross(lat[1],lat[2]))
    b=[]
    b.append(np.cross(lat[1],lat[2])/V)
    b.append(np.cross(lat[2],lat[0])/V)
    b.append(np.cross(lat[0],lat[1])/V)
    b=np.array(b)
    kpts=[]
    nkpt=[]
    Npt=40 # normalized points per length
    for i in range(len(k)-1):
        dk=(k[i+1]-k[i])
        Nk=int(LA.norm(np.dot(dk,b))/LA.norm(b[0])*Npt)
        nkpt.append(Nk)
        for j in range(Nk):
            kpts.append(k[i]+dk/Nk*j)

    kpts.append(k[-1])

    kpts=np.array(kpts)
    return kpts    
if __name__=="__main__":
    #k=np.array([[0.,0.,0.5],[0,0,0],[0.5,0.,0.],\
	#	[0.5,0.0,0.25],[0.,0.,0],[0.5,0.5,0]])
    k = np.array([[0.,0.,0.],[0.5,0,0],[0.5,0.5,0.],\
            [0.,0.0,0.],[0.5,0.5,0.5]])
    lat = np.array([[4,0,0],[0,4,0],[0,0,4.]])
    #lat=np.array([[3.7636001110,0,0],[0,3.7636001110 ,0],[0,0,13.]])#np.array([[0.5,-0.5,0],[0,0,1],[6,6,0]])

    lat=1.*lat
    kpts=k_path(k,lat)
    print "Kpts"
    
    print len(kpts)
    print "reciprocal"
    for i in range(len(kpts)):
    	print kpts[i,0],kpts[i,1],kpts[i,2],1
