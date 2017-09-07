
#For getting the force matrix and eigenval and eigenvecs 

import numpy as np
import cmath as cm
import sys,string,re
from numpy.linalg import inv
import subprocess as sp
def secmat(Ntype,Natom,fname,eachtype):

    f=open(fname,'r')
    lstart=0
    lines=f.readlines()
    mass=[]
    u=1.66053886E-27 #kg
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

    mat=-1*np.array(dynmat)

#    force_constants=np.zeros((Natom,Natom,3,3),dtype=float)
 #   for i in range( Natom ):
  #      for j in range( Natom ):
   #         force_constants[i, j] = mat[i*3:(i+1)*3, j*3:(j+1)*3]

    return (mat,mass)

def secmat_simp(Natom,fname):
    f=open(fname,'r')
    lines=f.readlines()
    rows=[]
    dynmat=[]
    f.close()
    
    for i in range(3*Natom):
        temp=string.split(lines[i])
        for j in range(3*Natom):
            rows.append(string.atof(temp[j]))
        dynmat.append(rows)
        rows=[]
    mat=-1*np.array(dynmat)
    return mat


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
   
    return mat,massM

def get_mat(mat,xyz): # get the x or y or z component from known matrix elements
    c=np.zeros((10,10))
    m,n=mat.shape
    for i in range(m/3):
        for j in range (m/3):
            c[i,j]=mat[i*3+xyz,j*3+xyz]
    
    return c


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

def perovskite(S): #C-fm C-cafm C-aafm C-aafmy , bases: C-pm J''x J''y J''z  
    coefficient=[[1,-S*S*4,-S*S*4,-S*S*3],\
                 [1,S*S*4,S*S*4,-S*S*3],\
                 [1,-S*S*4,-S*S*4,S*S*3],\
                 [1,-S*S*4,S*S*4,-S*S*3]]
             
    coefficient=np.array(coefficient)
    return coefficient
    

def multip(mat,col):
    (m,n)=mat.shape
    newcol=np.zeros(col.shape,dtype=float)
    for i in range(m):
        for j in range(n):
            newcol[i]=newcol[i]+mat[i,j]*col[j]
    return newcol

def sort(val,vec):
    for i in range(len(val)):
      for j in range(len(val)-i-1):
        if val[j]>val[j+1]:
            temp=val[j]
            val[j]=val[j+1]
            val[j+1]=temp
            for m in range(len(val)):
                temp1=vec[m,j]
                vec[m,j]=vec[m,j+1]
                vec[m,j+1]=temp1 #Sort the eigen values and vectors                 
    return val,vec


########################### 
# template for printout
##########################
def printJ(J,xyz,s,size): #s for symmetrize the matrix

    format1='%7.1f   %7.1f   %7.1f   %7.1f   %7.1f   %7.1f   %7.1f   %7.1f   %7.1f   %7.1f'
    format2='    %7s   %7s   %7s   %7s   %7s   %7s   %7s   %7s   %7s   %7s'
    print format2 %('Sr','La','Mn1','Mn2','Oz1','Ox1','Oy1','Oz2','Ox2','Oy2')
    m,n=J.shape
    atom=['Sr ','La ','Mn1','Mn2','Oz1','Ox1','Oy1','Oz2','Ox2','Oy2']
    if size==1:
      for i in range(m/3):
        if s=='s' or s=='S': #J[i,j]=(J[i,j]+J[j,i])/2
            print atom[i],format1 %( (J[i*3+xyz,xyz]+J[xyz,i*3+xyz])/2*1e4,  (J[i*3+xyz,3+xyz]+J[xyz+3,i*3+xyz])/2*1e4, (J[i*3+xyz,6+xyz]+J[xyz+6,i*3+xyz])/2*1e4, (J[i*3+xyz,xyz+9]+J[xyz+9,i*3+xyz])/2*1e4,(J[i*3+xyz,xyz+12]+J[xyz+12,i*3+xyz])/2*1e4, (J[i*3+xyz,xyz+15]+J[xyz+15,i*3+xyz])/2*1e4, (J[i*3+xyz,xyz+18]+J[xyz+18,i*3+xyz])/2*1e4, (J[i*3+xyz,xyz+21]+J[xyz+21,i*3+xyz])/2*1e4, (J[i*3+xyz,xyz+24]+J[xyz+24,i*3+xyz])/2*1e4, (J[i*3+xyz,xyz+27]+J[xyz+27,i*3+xyz])/2*1e4)

        else:    
            print atom[i],format1 %( J[i*3+xyz,xyz]*1e4,  J[i*3+xyz,3+xyz]*1e4, J[i*3+xyz,6+xyz]*1e4, J[i*3+xyz,xyz+9]*1e4, J[i*3+xyz,xyz+12]*1e4, J[i*3+xyz,xyz+15]*1e4, J[i*3+xyz,xyz+18]*1e4, J[i*3+xyz,xyz+21]*1e4, J[i*3+xyz,xyz+24]*1e4, J[i*3+xyz,xyz+27]*1e4)
    elif size==2:
      for i in range(m):
          if s=='s' or s== 'S':
              print atom[i],format1 %(J[0,i]/2*1e4+ J[i,0]/2*1e4, J[1,i]/2*1e4+J[i,1]/2*1e4,J[2,i]/2*1e4+ J[i,2]/2*1e4, J[3,i]/2*1e4+J[i,3]/2*1e4, J[4,i]/2*1e4+J[i,4]/2*1e4, J[5,i]/2*1e4+J[i,5]/2*1e4, J[6,i]/2*1e4+J[i,6]/2*1e4,J[7,i]/2*1e4+ J[i,7]/2*1e4,J[8,i]/2*1e4+ J[i,8]/2*1e4,J[9,i]/2*1e4+ J[i,9]/2*1e4)
          else:
              print atom[i],format1 %(J[i,0]*1e4, J[i,1]*1e4, J[i,2]*1e4, J[i,3]*1e4, J[i,4]*1e4, J[i,5]*1e4, J[i,6]*1e4, J[i,7]*1e4, J[i,8]*1e4, J[i,9]*1e4)

def printmodes(vec):
    atom=['Sr ','La ','Mn1','Mn2','Oz1','Ox1','Oy1','Oz2','Ox2','Oy2']
    format1='%9.5f   %9.5f   %9.5f'
    for i in range(len(vec)/3):
        print atom[i], format1 %(vec[3*i],vec[3*i+1],vec[3*i+2])

###################################################################
# project eigen modes of phonons onto eigenvectors of J matrices
###################################################################

def proj(eigval,eigvec,mode):
    #check if the mode is normalized
    norm=0
    for j in range(len(mode)):
        norm=norm+mode[j]*mode[j]
    norm=np.sqrt(norm)
    if np.abs(norm-1)>=1e-2:
        for j in range(len(mode)):
            mode[i]=mode[i]/norm
    temp=0
    for i in range(len(eigval)):
        temp=np.dot(mode,eigvec[:,i])*eigval[i]+temp
    return temp
    

def main():
    eachtype=[1,1,2,6]
    S=1
    FM='../23400'
    aAFM='27876'
    gAFM='dynmatgafm2.dat'
    cAFM='dynmatcafm1.dat'
    
    aAFMy='dynmataafmy.dat'
    fname='yjzhou/OUTCAR'
    Ntype=4
    Natom=[10,20,40]
   
    (matfm,mass)=secmat(Ntype,Natom[0],FM+'yjzhou/OUTCAR',eachtype)
    (mataafm,mass)=secmat(Ntype,Natom[0],aAFM+'yjzhou/OUTCAR',eachtype)
    matcafm=secmat_simp(Natom[0],cAFM)
    matgafm=secmat_simp(Natom[0],gAFM)
    mataafmy=secmat_simp(Natom[0],aAFMy)
   
##############################################
# get elements from a single direction x,y,z
############################################
    
    matfm1x=get_mat(matfm,0)
    matfm1z=get_mat(matfm,2)
    matcafm1x=get_mat(matcafm,0)
    matcafm1z=get_mat(matcafm,2)
    mataafm1x=get_mat(mataafm,0)
    mataafm1z=get_mat(mataafm,2)
    mataafmy1x=get_mat(mataafmy,0)
    mataafmy1z=get_mat(mataafmy,2)


    column=np.zeros((4,len(matfm1x),len(matfm1x)),dtype=float)
#    for i in range(30):
#        for j in range(30):
#            if i<j:
#                matfm[i,j]=(matfm[i,j]+matfm[j,i])/2
#                matfm[j,i]=matfm[i,j]
#                matcafm[i,j]=(matcafm[i,j]+matcafm[j,i])/2
#                matcafm[j,i]=matcafm[i,j]
#                matgafm[i,j]=(matgafm[i,j]+matgafm[j,i])/2
#                matgafm[j,i]=matgafm[i,j]
#                mataafmy[i,j]=(mataafmy[i,j]+mataafmy[j,i])/2
#                mataafmy[j,i]=mataafmy[i,j]

    column[0]=matfm1z
    column[1]=matcafm1z  
    column[2]=mataafm1z
    column[3]=mataafmy1z  
    
    
    coeff=perovskite(7.0/4)
    eigvector=multip(inv(coeff),column)

    massM= np.zeros((3*Natom[0],3*Natom[0]))
    for RowNum in range(Ntype):
      for rownum in range(3*eachtype[RowNum]):
        i=RowNum
        rnum=0
        while i>0:
            rnum+=3*eachtype[i-1]
            i-=1

        massM[(rownum+rnum),(rownum+rnum)]=mass[RowNum]
    massM1=get_mat(massM,0)

    matnew=np.dot(inv(massM1),eigvector[0])# divided the mass matrix
    #mat=devmass(eigvector[0],mass,Ntype,Natom[0],eachtype[0])

    (val,vec)=np.linalg.eig(matnew)
    val,vec=sort(val,vec)
   
    
    for v in range(len(val)):
        if val[v] >0:
            val[v]=np.sqrt(val[v])*15.633302/0.03 #VaspToTHz to cm-1
        else:
            val[v]=-1*np.sqrt(-1*val[v])*15.633302/0.03
   
#    print 'PM',val #*15.633302**2
#    printmodes(vec[:,0])
#    printmodes(vec[:,1])
#    printmodes(vec[:,2])

##################################################
#print sp-ph coupling for the chosen spin order
##################################################
    (val1,vec1)=np.linalg.eig(eigvector[1])
    val1,vec1=sort(val1,vec1)
    (val2,vec2)=np.linalg.eig(eigvector[2])
    val2,vec2=sort(val2,vec2)
    (val3,vec3)=np.linalg.eig(eigvector[3])
    val3,vec3=sort(val3,vec3)
    
    form='%7.3f   %7.3f   %7.3f   %7.3f   %7.3f \n  %7.3f   %7.3f   %7.3f   %7.3f   %7.3f'
#    print 
    print val3
    for i in range(len(val3)):
        print  vec3[:,i]
#    print 'eigvals',val
#    for i in range(len(val)):

#       printmodes (vec[:,i])
 #   printJ(mataafm1z,0,'a',2)
#    printJ(eigvector[1],0,'s',1)
#    printJ(eigvector[1],1,'s',1)
#    printJ(eigvector[1],2,'s',1)
#    print 'Spin-phonon couplings of FM state, for each phonon mode at Gamma '
#    print '%24s %15s %15s %15s' %('frequence of mode','x','y','z')
#    for i in range(len(val)):
#        lam1=proj(val1,vec1,vec[:,i])
#        lam2=proj(val2,vec2,vec[:,i])
#        lam3=proj(val3,vec3,vec[:,i])
#        print '%24.5f %15.5f %15.5f %15.5f' %(val[i],lam1,lam2,lam3)

main()
