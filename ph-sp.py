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
    for RowNum in range(Ntype):
        for rownum in range(3*eachtype[RowNum]):
            i=RowNum
            rnum=0
            while i>0:
                rnum+=3*eachtype[i-1]
                i-=1
            print rnum
            mat[(rownum+rnum),:]/=np.sqrt(mass[RowNum])
            mat[:,(rownum+rnum)]/=np.sqrt(mass[RowNum])
    for i in range(3*Natom):
        for j in range(3*Natom):
            mat[j,i]=(mat[i,j]+mat[j,i])*0.5
            mat[i,j]=mat[j,i]
#print mat[1]
#print mat[:,1]
   
    return mat

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


    
    
def main():
    eachtype=[1,1,2,6]
    S=1
    FM='25821'
    aAFM='24414'
    cAFM='23406'
    fname='yjzhou/OUTCAR'
    Ntype=4
    Natom=10
   
   # (matfm,mass)=secmat(Ntype,Natom,'OUTCAR',eachtype)
    (mataafm,mass)=secmat(Ntype,Natom,aAFM+'yjzhou/OUTCAR',eachtype)
    (matcafm,mass)=secmat(Ntype,Natom,cAFM+'yjzhou/OUTCAR',eachtype)
    force_const=np.zeros((3*Natom,3*Natom),dtype=float)
   # force_const=solve(Natom,matfm,mataafm,matcafm,S)
   # print force_const[0,:]
   # print force_const[1,:]
   # print force_const[2,:]
    print mataafm[0,:]
    print mataafm[1,:]
    print matcafm[0,:]
    print matcafm[1,:]
   # print mass

'''    mat=devmass(force_const,mass,Ntype,Natom,eachtype)
    print mat
    (val,vec)=np.linalg.eigh(mat)

    for v in range(len(val)):
        if val[v] >0:
            val[v]=np.sqrt(val[v])*15.633302/0.03 #VaspToTHz to cm-1
        else:
            val[v]=-1*np.sqrt(-1*val[v])*15.633302/0.03
   
    print 'PM',val #*15.633302**2
    print 'FM'
    sp.call(['grep','THz','OUTCAR'])
    print 'aAFM'
    sp.call(['grep','THz',aAFM+'yjzhou/OUTCAR'])
    print 'cAFM'
    sp.call(['grep','THz',cAFM+'yjzhou/OUTCAR'])

#   print vec
 #   print mat[0,:]
#    print mat[2,:] '''
main()
