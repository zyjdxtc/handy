#For getting the force matrix and eigenval and eigenvecs 

import numpy as np
import cmath as cm
import sys,string,re
from numpy.linalg import inv
import subprocess as sp
def secmat(Ntype,Natom,fname,eachtype):
   # Ntype=4
   # Natom=20
   # fname=['OUTCAR','DYNMAT']
    f=open(fname,'r')
    lstart=0
    lines=f.readlines()
    mass=[]
    #eachtype=[2,2,4,12]#[1,1,2,6]
    u=1.66053886E-27 #kg
    e=1.6E-19 #C
    h=6.63E-34

    f.close()
    for l in range(len(lines)):
        if string.find(lines[len(lines)-l-1],'SECOND DERIVATIVES (NOT SYMMETRIZED)')>=0:
            lstart=len(lines)-l-1
            break

    rows=[]
    dynmat=[]#temp mat
    for i in range(3*Natom):
        temp=string.split(lines[lstart+3+i])
        for j in range(3*Natom):
            rows.append(string.atof(temp[j+1]))
#    print rows
        dynmat.append(rows)
        rows=[]
        num=0

    for l in lines:
            if num>=Ntype:
                break
            if string.find(l,'POMASS')>0:
               # print l
                num+=1
                m=re.match('.*MASS = (.*); .*',l) 
                mass.append(string.atof(string.strip(m.group(1))))
    #print mass
    

    mat=-1*np.array(dynmat)
#    force_constants=np.zeros((Natom,Natom,3,3),dtype=float)
 #   for i in range( Natom ):
  #      for j in range( Natom ):
   #         force_constants[i, j] = mat[i*3:(i+1)*3, j*3:(j+1)*3]

    return (mat,mass)


#print mat
def devmass(mat,mass,Ntype,Natom,eachtype):
    massM=np.zeros((3*Natom,3*Natom))
    for RowNum in range(Ntype):
        for rownum in range(3*eachtype[RowNum]):
            i=RowNum
            rnum=0
            while i>0:
                rnum+=3*eachtype[i-1]
                i-=1
            print rnum
            massM[(rownum+rnum),(rownum+rnum)]=mass[RowNum]
           
    for i in range(3*Natom):
        for j in range(3*Natom):
            mat[j,i]=(mat[i,j]+mat[j,i])*0.5
            mat[i,j]=mat[j,i]
#print mat[1]
#print mat[:,1]
   
    return mat,massM

def get_array(mat,Natom,i,j): # get the array of known matrix elements
    c=[]
    c.append(mat[3*i,3*j])
    c.append(mat[3*i+1,3*j+1])
    c.append(mat[3*i+2,3*j+2])
    c.append(mat[3*i+1,3*j+2])
    c.append(mat[3*i,3*j+2])
    c.append(mat[3*i,3*j+1])
    return c

def solve(Natom,matfm,mataafm,matcafm,S):
    coeffi=np.zeros((18,18),dtype=float)
    for i in range(3): # fm aafm cafm 3 matrices
        for j in range(6): # 6 * 3 = 18 dimensions
                           # Cxx,Cyy,Czz,Cyz,Cxz,Cxy; Jz,xx, Jz,yy, Jz,zz, Jz,yz, Jz,xz, Jz,xy; Jx,xx, Jx,yy, Jx,zz, Jx,yz, Jx,xz, Jx,xy 
     
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
            if i==1: #aafm                                                                                                            
         

                coeffi[i*6+j,j+6]=4*S*S #Jz                                                                                               
  
                if (j+1)/3*3!=(j+1): #Jx                                                                                                       
  

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
                                   
  
                if (j+1)/3*3!=(j+1): #Jx                                                                                                       
  

                    if (j==0 or j==1):
                        coeffi[i*6+j,12]=4*S*S
                        coeffi[i*6+j,13]=4*S*S
                    elif (j==3 or j==4):
                        coeffi[i*6+j,15]=4*S*S
                        coeffi[i*6+j,16]=4*S*S
                else:
                    coeffi[i*6+j,j+12]=8*S*S
                    
    force_const=np.zeros((3*Natom,3*Natom),dtype=float)
    print coeffi,np.linalg.det(coeffi)
    #print inv(coeffi)
    for i in range(Natom):
        for j in range(Natom):
          if j>=i: 
            c=[]
            c.append(get_array(matfm,Natom,i,j))
            c.append(get_array(mataafm,Natom,i,j))
            c.append(get_array(matcafm,Natom,i,j))
            c=np.array(c).flatten()
            solution=np.dot(inv(coeffi),c)
            force_const[3*i,3*j]=solution[0]
            force_const[3*i+1,3*j+1]=solution[1]
            force_const[3*i+2,3*j+2]=solution[2]
            force_const[3*i+1,3*j+2]=solution[3]
            force_const[3*i+2,3*j+1]=solution[3]
            force_const[3*i,3*j+2]=solution[4]
            force_const[3*i+2,3*j]=solution[4]
            force_const[3*i,3*j+1]=solution[5]
            force_const[3*i+1,3*j]=solution[5]
    print c
    for i in range(3*Natom):
        for j in range(3*Natom):
            if j<i:
                force_const[i,j]=force_const[j,i]
    return force_const

def chooseatom(mat,atom): #the changesign option decides if we want to change the sign of matrix(x,y directions)
    mat2=np.zeros((3*len(atom),3*len(atom)),dtype=float)
    for i in range(len(atom)):
        for j in range(len(atom)):
            for m in range(3):
                mat2[i*3,j*3+m]=mat[(atom[i]-1)*3,(atom[j]-1)*3+m]
                mat2[i*3+1,j*3+m]=mat[(atom[i]-1)*3+1,(atom[j]-1)*3+m]
                mat2[i*3+2,j*3+m]=mat[(atom[i]-1)*3+2,(atom[j]-1)*3+m]
    #if changesign==1:
        
    return mat2

def perovskite(S): #C-fm C-aafm C-cafm C-gafm C-aafmx C-cafmy, bases: C-pm J''x J''y J''z J''2// J''2p 
    coefficient=[[1,-S*S*2,-S*S*2,-S*S*2,-S*S*4,-S*S*8],\
                 [1,-S*S*2,-S*S*2,S*S*2,-S*S*4,S*S*8],\
                 [1,S*S*2,S*S*2,-S*S*2,-S*S*4,S*S*8],\
                 [1,S*S*2,S*S*2,S*S*2,-S*S*4,-S*S*8],\
                 [1,-S*S*2,S*S*2,-S*S*2,S*S*4,0],\
                 [1,S*S*2,-S*S*2,S*S*2,S*S*4,0]]
    coefficient=np.array(coefficient)
    return coefficient
    

def multip(mat,col):
    (m,n)=mat.shape
    newcol=np.zeros(col.shape,dtype=float)
    for i in range(m):
        for j in range(n):
            newcol[i]=newcol[i]+mat[i,j]*col[j]
    return newcol

def main():
    eachtype=[[1,1,2,6],[2,2,4,12],[4,4,8,24]]
    S=1
    FM='../23400'
    aAFM='27876'
    gAFM='27567'
    cAFM='27566'
    cAFMy='27569'
    aAFMx='27568'
    fname='yjzhou/OUTCAR'
    Ntype=4
    Natom=[10,20,40]
    atomcafm=[2,4,5,7,9,13,14,11,17,18]
    atomaafmx=[1,3,5,6,9,10,11,12,13,14]
    atomcafmy=[1,5,9,10,17,18,19,20,21,22]
   
    (matfm,mass)=secmat(Ntype,Natom[0],FM+'yjzhou/OUTCAR',eachtype[0])
    (mataafm,mass)=secmat(Ntype,Natom[0],aAFM+'yjzhou/OUTCAR',eachtype[0])
    (matcafm,mass)=secmat(Ntype,Natom[1],cAFM+'yjzhou/OUTCAR',eachtype[1])
    (matgafm,mass)=secmat(Ntype,Natom[1],gAFM+'yjzhou/OUTCAR',eachtype[1])
    (mataafmx,mass)=secmat(Ntype,Natom[1],aAFMx+'yjzhou/OUTCAR',eachtype[1])
    (matcafmy,mass)=secmat(Ntype,Natom[2],cAFMy+'yjzhou/OUTCAR',eachtype[2])
    print matcafmy[0:3,6:9]
    print matcafmy[3:6,3:6]
    print matcafmy[6:9,36:39]
   # force_const=np.zeros((3*Natom,3*Natom),dtype=float)
   # force_const=solve(Natom,matfm,mataafm,matcafm,S)
   # print force_const[0,:]
   # print force_const[1,:]
   # print force_const[2,:]
    matcafm2=chooseatom(matcafm,atomcafm)
    mataafmx2=chooseatom(mataafmx,atomaafmx)
    matcafmy2=chooseatom(matcafmy,atomcafmy)
    matgafm2=chooseatom(matgafm,atomcafm) #atomgafm=atomcafm

    for i in range(10): #invert x,y in matcafmy
        temp=mataafmx2[i*3+0]
        mataafmx2[i*3+0]=mataafmx2[i*3+1]
        mataafmx2[i*3+1]=temp
        temp=mataafmx2[:,i*3+0]
        mataafmx2[:,i*3+0]=mataafmx2[:,i*3+1]
        mataafmx2[:,i*3+1]=temp
        matcafm2[i*3+2]=-matcafm2[i*3+2] # add - to z components of matcafm,matgafm
        matcafm2[:,i*3+2]=-matcafm2[:,i*3+2]
        matgafm2[i*3+2]=-matgafm2[i*3+2]
        matgafm2[:,i*3+2]=-matgafm2[:,i*3+2]
    column=np.zeros((6,len(matfm),len(matfm)),dtype=float)
    column[0]=matfm
    column[1]=mataafm
    column[2]=matcafm2
    column[3]=matgafm2
    column[4]=mataafmx2
    column[5]=matcafmy2
    
    coeff=perovskite(7.0/4)
    eigvector=multip(inv(coeff),column)

   # print eigvector[0]
    mat=devmass(eigvector[0],mass,Ntype,Natom[0],eachtype[0])
    
#    print mat
    (val,vec)=np.linalg.eigh(mat)

    for v in range(len(val)):
        if val[v] >0:
            val[v]=np.sqrt(val[v])*15.633302/0.03 #VaspToTHz to cm-1
        else:
            val[v]=-1*np.sqrt(-1*val[v])*15.633302/0.03
   
    print 'PM',val #*15.633302**2
#    print 'FM'
#    sp.call(['grep','THz','OUTCAR'])
#    print 'aAFM'
#    sp.call(['grep','THz',aAFM+'yjzhou/OUTCAR'])
#    print 'cAFM'
#    sp.call(['grep','THz',cAFM+'yjzhou/OUTCAR'])

#   print vec
    print matcafmy2[:,2]
    print matcafmy2[2,:] 
main()
