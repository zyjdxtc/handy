# Hex axes
import numpy as np

def asite(z):
    a=np.array([[0,0,z],[0,0,z+0.5]])
    return a
def bsite(x,y,z):
    b=np.array([[x,y,z],[-y,x-y,z],[-x+y,-x,z],[-y,-x,z+1/2.],[-x+y,y,z+1/2.],[x,x-y,z+1/2.]])
    return b

def main():
    z_La=0.0
    z_Mn=0.252
    x_O=-0.3
    y_O=-0.35
    z_O=0.6
    origin=np.array([[0,0,0],[2/3.0,1/3.0,1/3.] ,[1/3.,2/3.,2/3.]])
    La=asite(z_La)
    Mn=asite(z_Mn)
    O=bsite(x_O,y_O,z_O)
    for i in range(len(origin)):
        for j in range(len(La)):            
            temp= La[j]+origin[i]
            for k in range(len(temp)):
                if temp[k]>1.0:
                    temp[k]=temp[k]-1.0
            print '%10.7f '*3 %(temp[0],temp[1],temp[2])
    for i in range(len(origin)):
        for j in range(len(Mn)):
            temp= Mn[j]+origin[i]
            for k in range(len(temp)):
                if temp[k]>1.0:
                    temp[k]=temp[k]-1.0

            print '%10.7f '*3 %(temp[0],temp[1],temp[2])

    for i in range(len(origin)):
        for j in range(len(O )):
            temp= O[j]+origin[i]
            for k in range(len(temp)):
                if temp[k]>1.0:
                    temp[k]=temp[k]-1.0

            print '%10.7f '*3 %(temp[0],temp[1],temp[2])


main()
