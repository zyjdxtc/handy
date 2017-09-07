import numpy as np
import cmath as cm
import sys,string,re
from numpy.linalg import inv
import subprocess as sp


def solve(S):
    coeffi=np.zeros((18,18),dtype=float)
    for i in range(3): # fm aafm cafm 3 matrices                                                                             
        for j in range(6): # 6 * 3 = 18 dimensions                                                                           
                           # Cxx,Cyy,Czz,Cyz,Cxz,Cxy; Jz,xx, Jz,yy, Jz,zz, Jz,yz, Jz,xz, Jz,xy; Jx,xx, Jx,yy, Jx,zz, Jx,yz,Jx,xz, Jx,xy                                                                                                                 

            coeffi[i*6+j,j]=1
            if i==0: #fm                                                                                                     

                coeffi[i*6+j,j+6]=-4*S*S #Jz                                                                                 
                if (j+1)/3*3!=(j+1): #Jx                                                                                     

                    if (j==0 or j==1):
                        coeffi[i*6+j,12]=-4*S*S
                        coeffi[i*6+j,13]=-4*S*S
                    elif (j==3 or j==4):
                        coeffi[i*6+j,15]=-4*S*S
                        coeffi[i*6+j,16]=-4*S*S
                else:
                    coeffi[i*6+j,j+12]=-8*S*S
            if i==1: #aafm                                                                                                  \
                                                                                                                             


                coeffi[i*6+j,j+6]=4*S*S #Jz                                                                                 \
                                                                                                                             

                if (j+1)/3*3!=(j+1): #Jx                                                                                    \
                                                                                                                             


                    if (j==0 or j==1):
                        coeffi[i*6+j,12]=-4*S*S
                        coeffi[i*6+j,13]=-4*S*S
                    elif (j==3 or j==4):
                        coeffi[i*6+j,15]=-4*S*S
                        coeffi[i*6+j,16]=-4*S*S
                else:
                    coeffi[i*6+j,j+12]=-8*S*S
            if i==2: #cafm                                                                                                   



                coeffi[i*6+j,j+6]=-4*S*S #Jz                                                                                 


                if (j+1)/3*3!=(j+1): #Jx                                                                                    \
                                                                                                                             


                    if (j==0 or j==1):
                        coeffi[i*6+j,12]=4*S*S
                        coeffi[i*6+j,13]=4*S*S
                    elif (j==3 or j==4):
                        coeffi[i*6+j,15]=4*S*S
                        coeffi[i*6+j,16]=4*S*S
                else:
                    coeffi[i*6+j,j+12]=8*S*S
    return coeffi

def solve1(s):
    a=[]
    a.append([1,-8*s*s,-16*s*s])
    a.append([1,-8*s*s,16*s*s])
    a.append([1,8*s*s,0])
    a=np.array(a)
    return a
def main():
#    s=np.arange(0,10,0.01)
 #   for a in s:
 #       if np.linalg.det(solve(a)) != 0: 
  #  for a in range(100):
        a=1
        print a,solve(a)
   # print solve(a),inv(solve(a))
main()
        
