# transform the cubic harmonic basis in the vasp to DMATLU of ELK spherical harmonic Y_lm.
# this version is for d orbitals

import numpy as np
import string as st
import sys
import numpy.linalg as LA
def main():
    fname=sys.argv[1]
    f=open(fname,'r')
    lines=f.readlines()
    f.close()
    spec_info=[]
    text1=' : species, atom, l\n'
    text2=' : ispn, jspn; m1, m2, dmatlu below\n'
    natom = int(lines[0].split()[0])
    ispe =  (lines[0].split()[1])
    format='%10.6f %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f'
    ibysqrt2=1j/np.sqrt(2)
    bysqrt2=1.0/np.sqrt(2)
    l = 2
    dim = 2*(2*l+1) # dimension of matrix
    d=dim/2

#Note: the trans_mat U is the one that of Y_lm * U = cubic harm    
    trans_mat1=[[ibysqrt2,0,0,0,bysqrt2],[0,ibysqrt2,0,bysqrt2,0]\
		,[0,0,1,0,0],[0,ibysqrt2,0,-ibysqrt2,0],\
		[-ibysqrt2,0,0,0,bysqrt2]]
    trans_mat1=np.mat(trans_mat1)
    trans_mat=LA.inv(trans_mat1)
    f=open('DMATLU.OUT','w')
    
    for i in range(natom):
	#read matrix
	dmat=np.zeros((dim,dim),dtype=complex)
	for j in range(dim):
	    temp=lines[1+j+i*(dim+1)].split()
	    for k in range(len(temp)):
		dmat[j,k]=float(temp[k])+0j
	#write as Y_lm
        f.write('\n')
	f.write('\n')
        f.write(ispe+' '+str(i+1)+' '+str(l)+text1)
	f.write('\n')
	#write up up block 
	f.write('1 1 '+text2)

	dmat_Ylm=np.dot(np.dot(trans_mat.H,dmat[0:d,0:d]),trans_mat)
	for j in range(d):
	    for k in range(d):
		f.write('   '+str(j-l)+' '+str(k-l)+' '+str(dmat_Ylm[j,k].real)+' '+str(dmat_Ylm[j,k].imag)+'\n')
        f.write('\n')
	#write up down block
        f.write('1 2 '+text2)

        dmat_Ylm=np.dot(np.dot(trans_mat.H,dmat[0:d,d:d+d]),trans_mat)

        for j in range(d):
            for k in range(d):
                f.write('   '+str(j-l)+' '+str(k-l)+' '+str(dmat_Ylm[j,k].real)+' '+str(dmat_Ylm[j,k].imag)+'\n')
        f.write('\n')

	#write down up block
        f.write('2 1 '+text2)

        dmat_Ylm=np.dot(np.dot(trans_mat.H,dmat[d:d+d,0:d]),trans_mat)

        for j in range(d):
            for k in range(d):
                f.write('   '+str(j-l)+' '+str(k-l)+' '+str(dmat_Ylm[j,k].real)+' '+str(dmat_Ylm[j,k].imag)+'\n')
        f.write('\n')
	#write down down block
        f.write('2 2 '+text2)

        dmat_Ylm=np.dot(np.dot(trans_mat.H,dmat[d:d+d,d:d+d]),trans_mat)

        for j in range(d):
            for k in range(d):
                f.write('   '+str(j-l)+' '+str(k-l)+' '+str(dmat_Ylm[j,k].real)+' '+str(dmat_Ylm[j,k].imag)+'\n')
        f.write('\n')


    f.close()  

main()
