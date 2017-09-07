# Hex axes
import numpy as np

def asite(x):
    a=np.array([[x,x,x],[x+1/2.,x+1/2.,x+1/2.]])
    return a
def bsite(x,y,z):
    b=np.array([[x,y,z],[z,x,y],[y,z,x],[z+1/2.,y+1/2.,x+1/2.],[y+1/2.,x+1/2.,z+1/2.],[x+1/2.,z+1/2.,y+1/2.]])
    return b

def main():
    z_La=0.0
    z_Mn=0.252
    x_O=0.23 #0.69452075944534708
    y_O=0.71 #-0.52237151889069411
    z_O=0.22 #0.62786075944534692
    origin=np.array([0,0,0])
    La=asite(z_La)
    Mn=asite(z_Mn)
    O=bsite(x_O,y_O,z_O)
    for i in range(1):
        for j in range(len(La)):            
            temp= La[j]+origin[i]
            for k in range(len(temp)):
                if temp[k]>1.0:
                    temp[k]=temp[k]-1.0
            print '%10.5f '*3 %(temp[0],temp[1],temp[2]) #, '#La'
    for i in range(1):
        for j in range(len(Mn)):
            temp= Mn[j]+origin[i]
            for k in range(len(temp)):
                if temp[k]>1.0:
                    temp[k]=temp[k]-1.0

            print '%10.5f '*3 %(temp[0],temp[1],temp[2]) #, '#Mn'

    for i in range(1):
        for j in range(len(O )):
            temp= O[j]+origin[i]
            for k in range(len(temp)):
                if temp[k]>1.0:
                    temp[k]=temp[k]-1.0

            print '%10.5f '*3 %(temp[0],temp[1],temp[2]) # , '#O'


main()
