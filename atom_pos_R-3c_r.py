# Hex axes
import numpy as np

def asite():
    a=np.array([[0,0,0],[0.5,0.5,0.5]])
    return a
def bsite():
    b=np.array([[0.25,0.25,0.25],[0.75,0.75,0.75]])
    return b
def esite(x):
    e=np.array([[x,-x+1/2.,1/4.],[1/4.,x,-x+1/2.],[-x+1/2.,1/4.,x],[-x,x+1/2.,3/4.],\
               [3/4.,-x,x+1/2.],[x+1/2.,3/4.,-x]])
    return e
def main():
    z_La=0.0
    z_Mn=0.25
    x_O=0.5
   
    origin=np.array([0,0,0])
    La=bsite()
    Mn=asite()
    O=esite(x_O)
    for i in range(1):
        for j in range(len(La)):            
            temp= La[j]+origin[i]
            for k in range(len(temp)):
                if temp[k]>1.0:
                    temp[k]=temp[k]-1.0
            print '%10.7f '*3 %(temp[0],temp[1],temp[2])
    for i in range(1):
        for j in range(len(Mn)):
            temp= Mn[j]+origin[i]
            for k in range(len(temp)):
                if temp[k]>1.0:
                    temp[k]=temp[k]-1.0

            print '%10.7f '*3 %(temp[0],temp[1],temp[2])

    for i in range(1):
        for j in range(len(O )):
            temp= O[j]+origin[i]
            for k in range(len(temp)):
                if temp[k]>1.0:
                    temp[k]=temp[k]-1.0

            print '%10.7f '*3 %(temp[0],temp[1],temp[2])


main()
