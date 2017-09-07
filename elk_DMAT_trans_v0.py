# transform the Y_lm basis in the DMATLU of ELK to cubic harmonic basis, dxy dyz etc.

import numpy as np
import string as st
import sys

def main():
    fname=sys.argv[1]
    f=open(fname,'r')
    lines=f.readlines()
    spec_info=[]
    for i in range(len(lines)):
	if lines[i].find('species') >=0:
	    temp=lines[i].split()
	    spec_info.append([int(temp[0]),int(temp[1]),int(temp[2]),i]) # [species, atom, orbital angular moment, line number]
    format='%10.6f %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f'
    ibysqrt2=1j/np.sqrt(2)
    bysqrt2=1.0/np.sqrt(2)
    
    trans_mat=[[ibysqrt2,0,0,0,bysqrt2,ibysqrt2,0,0,0,bysqrt2],[0,ibysqrt2,0,bysqrt2,0,0,ibysqrt2,0,bysqrt2,0]\
		,[0,0,1,0,0,0,0,1,0,0],[0,ibysqrt2,0,-ibysqrt2,0,0,ibysqrt2,0,-ibysqrt2,0],\
		[-ibysqrt2,0,0,0,bysqrt2,-ibysqrt2,0,0,0,bysqrt2],\
		[ibysqrt2,0,0,0,bysqrt2,ibysqrt2,0,0,0,bysqrt2],[0,ibysqrt2,0,bysqrt2,0,0,ibysqrt2,0,bysqrt2,0]\
                ,[0,0,1,0,0,0,0,1,0,0],[0,ibysqrt2,0,-ibysqrt2,0,0,ibysqrt2,0,-ibysqrt2,0],\
                [-ibysqrt2,0,0,0,bysqrt2,-ibysqrt2,0,0,0,bysqrt2]]
    trans_mat=np.mat(trans_mat)
    for i in range(len(spec_info)):
	l=spec_info[i][2]
        startline=spec_info[i][3]
        dim = (2*l+1)*2 # dimension of the matrix, 10x10 for d electron
        d=dim/2
        mat=np.zeros((dim,dim),dtype=complex)
        for j in range(d*d):
	    temp=lines[startline+3+j].split()    
	    ii=int(temp[0])
	    jj=int(temp[1])
	    mat[ii+l,jj+l]=float(temp[2])+1j*float(temp[3])
	for j in range(d*d):
            temp=lines[startline+3+d*d+2+j].split()
            ii=int(temp[0])
            jj=int(temp[1])
            mat[ii+l,jj+l+d]=float(temp[2])+1j*float(temp[3])

        for j in range(d*d):
            temp=lines[startline+3+(d*d+2)*2+j].split()
            ii=int(temp[0])
            jj=int(temp[1])
            mat[ii+l+d,jj+l]=float(temp[2])+1j*float(temp[3])
	for j in range(d*d):
            temp=lines[startline+3+(d*d+2)*3+j].split()
            ii=int(temp[0])
            jj=int(temp[1])
            mat[ii+l+d,jj+l+d]=float(temp[2])+1j*float(temp[3])
	print 'DMAT(Y_lm) of species',spec_info[i][0],'atom',spec_info[i][1],'#real part'
        for j in range(dim):
	    print format %(mat[j,0].real,mat[j,1].real,mat[j,2].real,mat[j,3].real\
               ,mat[j,4].real,mat[j,5].real,mat[j,6].real,mat[j,7].real,mat[j,8].real,mat[j,9].real)	

	cubic_harm=np.zeros((dim,dim),dtype=complex)
        cubic_harm=np.dot(np.dot(trans_mat.H,mat),trans_mat)

        print 'DMAT(cubic_harm) of species',spec_info[i][0],'atom',spec_info[i][1],'#real part'
        for j in range(dim):
            print format %(cubic_harm[j,0].real,cubic_harm[j,1].real,cubic_harm[j,2].real,cubic_harm[j,3].real\
               ,cubic_harm[j,4].real,cubic_harm[j,5].real,cubic_harm[j,6].real,\
		cubic_harm[j,7].real,cubic_harm[j,8].real,cubic_harm[j,9].real)

main()
