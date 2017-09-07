#this code calculate the residue of phonon modes, and apply ASR

import numpy as np

def asr(mat):
    mat_new=mat
    m,n=mat.shape
    residue=[]
    for i in range(3):
      	for j in range(3):
	    for na in range(m/3):
		temp=0.0
		for nb in range(m/3):
		   temp=temp+mat[3*na+i,3*nb+j]
        	mat_new[3*na+i,3*na+j]=mat[3*na+i,3*na+j]-temp
		residue.append(temp)
    temp=np.array(temp)
    return mat_new
