# This code is to read forces from OUTCAR, and calculate force matrix using frozen phonons at Gamma point
# Symmetries between atoms are utilized, by defining unitary matrices between those atoms.


import numpy as np
import numpy.linalg as li
import string 
from numpy.linalg import inv

def readforce(fname,Natom):
    f=open(fname,'r')
    lines=f.readlines()
    for i in range(len(lines)):
        if string.find(lines[len(lines)-i-1],'POSITION')>=0:
            num=len(lines)-i+1
            break
    force=np.zeros((Natom,3),dtype=float)
    for i in range(Natom):
        temp=string.split(lines[num+i])
        
        for j in range(3):
            force[i,j]=float(temp[3+j])
    f.close()
    return force

def fillmat(fmat,mat,natom,xyz): #xyz = 0,1,2
    m,n=mat.shape
    num=0

    #while num<3*m:
    for i in range(m):
        for j in range(3):
            if num==30: break
            fmat[(natom-1)*3+xyz,num]=mat[i,j]
            num=num+1
    return fmat
    
def chooseatom(mat,atom): 
    mat2=np.zeros((len(atom),3),dtype=float)
    for i in range(len(atom)):
            
                mat2[i,:]=mat[(atom[i]-1),:]
    return mat2

def fillmat_y(mat,natom,xyz): #fill y component from x component due to symmetry
    m,n=mat.shape
    for i in range(n/3+1): #i is the index of atoms, start with 1
       # for j in range(n/3):
        if i==6 or i==9:
            mat[(natom-1)*3+xyz,(i-1)*3]=mat[(natom-1)*3+xyz-1,(i)*3+1]
            mat[(natom-1)*3+xyz,(i-1)*3+1]=mat[(natom-1)*3+xyz-1,(i)*3]
            mat[(natom-1)*3+xyz,(i-1)*3+2]=mat[(natom-1)*3+xyz-1,(i)*3+2]
        elif i==7 or i==10:
            mat[(natom-1)*3+xyz,(i-1)*3]=mat[(natom-1)*3+xyz-1,(i-2)*3+1]
            mat[(natom-1)*3+xyz,(i-1)*3+1]=mat[(natom-1)*3+xyz-1,(i-2)*3]
            mat[(natom-1)*3+xyz,(i-1)*3+2]=mat[(natom-1)*3+xyz-1,(i-2)*3+2]
        else:
            mat[(natom-1)*3+xyz,(i-1)*3]=mat[(natom-1)*3+xyz-1,(i-1)*3+1]
            mat[(natom-1)*3+xyz,(i-1)*3+1]=mat[(natom-1)*3+xyz-1,(i-1)*3]
            mat[(natom-1)*3+xyz,(i-1)*3+2]=mat[(natom-1)*3+xyz-1,(i-1)*3+2]
    return mat

def fillsymmirror(mat,fillingatom,filledatom,U):
    m,n=mat.shape
    for i in range(n/3):
        temp=mat[(filledatom-1)*3:((filledatom-1)*3+3),i*3:(i*3+3)]
       # print 'temp=',temp
        mat[(fillingatom-1)*3:(fillingatom-1)*3+3,i*3:i*3+3]=np.dot(np.dot(U.T,temp),U)
    return mat
def fillsymrot(mat,fillingatom,filledatom,U): #particularly for #7 atom
    m,n=mat.shape
    for i in range(n/3):
        if i+1 ==6 or i+1==9:
            temp=mat[(filledatom-1)*3:((filledatom-1)*3+3),(i+1)*3:((i+1)*3+3)]
            mat[(fillingatom-1)*3:(fillingatom-1)*3+3,i*3:i*3+3]=np.dot(np.dot(U.T,temp),U)
        elif i+1==7 or i+1==10:
            temp=mat[(filledatom-1)*3:((filledatom-1)*3+3),(i-1)*3:((i-1)*3+3)]
            mat[(fillingatom-1)*3:(fillingatom-1)*3+3,i*3:i*3+3]=np.dot(np.dot(U.T,temp),U)
        else:
            temp=mat[(filledatom-1)*3:((filledatom-1)*3+3),(i)*3:((i)*3+3)]
            mat[(fillingatom-1)*3:(fillingatom-1)*3+3,i*3:i*3+3]=np.dot(np.dot(U.T,temp),U)
    return mat

def main():
    step=0.02 # Angstrom
    Natom=[10,20,40]
    atom=[[1,3,5,6,9,10,11,12,13,14],[1,3,6,8,10,13,14,12,17,18],[2,4,5,7,9,13,14,11,17,18],[1,5,9,10,17,18,19,20,21,22]]# atom[1] is for substitution
    xx='yjzhou/FORCE'
    f0=readforce('28930'+xx,Natom[1])
    f1x=readforce('29005'+xx,Natom[1])
    f1_x=readforce('29006'+xx,Natom[1])
   
    fmat=np.zeros((30,30),dtype=float)
    #print f1z,f1_z
    #print (f1_x-f0)/step
    f1x=chooseatom(f1x,atom[0])
    f1_x=chooseatom(f1_x,atom[0])
   
    f0=chooseatom(f0,atom[0])
    f1y=chooseatom(readforce('29011'+xx,Natom[1]),atom[0])
    f1_y=chooseatom(readforce('29008'+xx,Natom[1]),atom[0])


    f1z=readforce('29009'+xx,Natom[1])
    f1z=chooseatom(f1z,atom[0])
    f1_z=chooseatom(readforce('29012'+xx,Natom[1]),atom[0])
    
    f2x=chooseatom(readforce('29013'+xx,Natom[1]),atom[0])
    f2_x=chooseatom(readforce('29014'+xx,Natom[1]),atom[0])
    f2y=chooseatom(readforce('29015'+xx,Natom[1]),atom[0])
    f2_y=chooseatom(readforce('29016'+xx,Natom[1]),atom[0])

    f2z=chooseatom(readforce('29017'+xx,Natom[1]),atom[0])
    f2_z=chooseatom(readforce('29018'+xx,Natom[1]),atom[0])
    
    f3x=chooseatom(readforce('29019'+xx,Natom[1]),atom[0])
    f3_x=chooseatom(readforce('29020'+xx,Natom[1]),atom[0])
    f3y=chooseatom(readforce('29076'+xx,Natom[1]),atom[0])
    f3_y=chooseatom(readforce('29083'+xx,Natom[1]),atom[0])

    f3z=chooseatom(readforce('29021'+xx,Natom[1]),atom[0])
    f3_z=chooseatom(readforce('29022'+xx,Natom[1]),atom[0])

    f4x=chooseatom(readforce('29023'+xx,Natom[1]),atom[0])
    f4_x=chooseatom(readforce('29024'+xx,Natom[1]),atom[0])
    f4y=chooseatom(readforce('29079'+xx,Natom[1]),atom[0])
    f4_y=chooseatom(readforce('29080'+xx,Natom[1]),atom[0])

    f4z=chooseatom(readforce('29081'+xx,Natom[1]),atom[0])
    f4_z=chooseatom(readforce('29082'+xx,Natom[1]),atom[0])

    f5x=chooseatom(readforce('29025'+xx,Natom[1]),atom[0])
    f5_x=chooseatom(readforce('29026'+xx,Natom[1]),atom[0])
    f5y=chooseatom(readforce('29027'+xx,Natom[1]),atom[0])
    f5_y=chooseatom(readforce('29028'+xx,Natom[1]),atom[0])
    f5z=chooseatom(readforce('29029'+xx,Natom[1]),atom[0])
    f5_z=chooseatom(readforce('29030'+xx,Natom[1]),atom[0])

    f8x=chooseatom(readforce('29031'+xx,Natom[1]),atom[0])
    f8_x=chooseatom(readforce('29032'+xx,Natom[1]),atom[0])
    f8y=chooseatom(readforce('29033'+xx,Natom[1]),atom[0])
    f8_y=chooseatom(readforce('29364'+xx,Natom[1]),atom[0]) #

    f8z=chooseatom(readforce('29365'+xx,Natom[1]),atom[0]) #
    f8_z=chooseatom(readforce('29036'+xx,Natom[1]),atom[0])

    f6x=chooseatom(readforce('29038'+xx,Natom[1]),atom[0])
    f6_x=chooseatom(readforce('29039'+xx,Natom[1]),atom[0])
    f6z=chooseatom(readforce('29042'+xx,Natom[1]),atom[0])
    f6_z=chooseatom(readforce('29043'+xx,Natom[1]),atom[0])
    f6y=chooseatom(readforce('29040'+xx,Natom[1]),atom[0])
    f6_y=chooseatom(readforce('29041'+xx,Natom[1]),atom[0])

    f7x=chooseatom(readforce('29125'+xx,Natom[1]),atom[0])
    f7_x=chooseatom(readforce('29126'+xx,Natom[1]),atom[0])
    f7y=chooseatom(readforce('29127'+xx,Natom[1]),atom[0])
    f7_y=chooseatom(readforce('29128'+xx,Natom[1]),atom[0])
    f7z=chooseatom(readforce('29129'+xx,Natom[1]),atom[0])
    f7_z=chooseatom(readforce('29130'+xx,Natom[1]),atom[0])
    f9x=chooseatom(readforce('29132'+xx,Natom[1]),atom[0])
    f9_x=chooseatom(readforce('29133'+xx,Natom[1]),atom[0])
    f9y=chooseatom(readforce('29134'+xx,Natom[1]),atom[0])
    f9_y=chooseatom(readforce('29136'+xx,Natom[1]),atom[0])
    f9z=chooseatom(readforce('29137'+xx,Natom[1]),atom[0])
    f9_z=chooseatom(readforce('29138'+xx,Natom[1]),atom[0])

    f10x=chooseatom(readforce('29139'+xx,Natom[1]),atom[0])
    f10_x=chooseatom(readforce('29140'+xx,Natom[1]),atom[0])
    f10y=chooseatom(readforce('29141'+xx,Natom[1]),atom[0])
    f10_y=chooseatom(readforce('29142'+xx,Natom[1]),atom[0])
    f10z=chooseatom(readforce('29143'+xx,Natom[1]),atom[0])
    f10_z=chooseatom(readforce('29144'+xx,Natom[1]),atom[0])


    fmat=fillmat(fmat,0.5*((f1x-f0)/step-(f1_x-f0)/step),1,0)
    fmat=fillmat(fmat,0.5*((f1y-f0)/step-(f1_y-f0)/step),1,1)
    fmat=fillmat(fmat,0.5*((f1z-f0)/step-(f1_z-f0)/step),1,2)

    fmat=fillmat(fmat,0.5*((f2x-f0)/step-(f2_x-f0)/step),2,0)
    fmat=fillmat(fmat,0.5*((f2y-f0)/step-(f2_y-f0)/step),2,1)
    fmat=fillmat(fmat,0.5*((f2z-f0)/step-(f2_z-f0)/step),2,2)

    fmat=fillmat(fmat,0.5*((f3x-f0)/step-(f3_x-f0)/step),3,0)
    fmat=fillmat(fmat,0.5*((f3y-f0)/step-(f3_y-f0)/step),3,1)
    fmat=fillmat(fmat,0.5*((f3z-f0)/step-(f3_z-f0)/step),3,2)

    fmat=fillmat(fmat,0.5*((f4x-f0)/step-(f4_x-f0)/step),4,0)
    fmat=fillmat(fmat,0.5*((f4y-f0)/step-(f4_y-f0)/step),4,1)
    fmat=fillmat(fmat,0.5*((f4z-f0)/step-(f4_z-f0)/step),4,2)

    fmat=fillmat(fmat,0.5*((f6x-f0)/step-(f6_x-f0)/step),6,0)
    fmat=fillmat(fmat,0.5*((f6y-f0)/step-(f6_y-f0)/step),6,1)
    fmat=fillmat(fmat,0.5*((f6z-f0)/step-(f6_z-f0)/step),6,2)

    fmat=fillmat(fmat,0.5*((f5x-f0)/step-(f5_x-f0)/step),5,0)
    fmat=fillmat(fmat,0.5*((f5y-f0)/step-(f5_y-f0)/step),5,1)
    fmat=fillmat(fmat,0.5*((f5z-f0)/step-(f5_z-f0)/step),5,2)

    fmat=fillmat(fmat,0.5*((f9x-f0)/step-(f9_x-f0)/step),9,0)
    fmat=fillmat(fmat,0.5*((f9y-f0)/step-(f9_y-f0)/step),9,1)
    fmat=fillmat(fmat,0.5*((f9z-f0)/step-(f9_z-f0)/step),9,2)

    fmat=fillmat(fmat,0.5*((f8x-f0)/step-(f8_x-f0)/step),8,0)
    fmat=fillmat(fmat,0.5*((f8y-f0)/step-(f8_y-f0)/step),8,1)
    fmat=fillmat(fmat,0.5*((f8z-f0)/step-(f8_z-f0)/step),8,2)

    fmat=fillmat(fmat,0.5*((f7x-f0)/step-(f7_x-f0)/step),7,0)
    fmat=fillmat(fmat,0.5*((f7y-f0)/step-(f7_y-f0)/step),7,1)
    fmat=fillmat(fmat,0.5*((f7z-f0)/step-(f7_z-f0)/step),7,2)

    fmat=fillmat(fmat,0.5*((f10x-f0)/step-(f10_x-f0)/step),10,0)
    fmat=fillmat(fmat,0.5*((f10y-f0)/step-(f10_y-f0)/step),10,1)
    fmat=fillmat(fmat,0.5*((f10z-f0)/step-(f10_z-f0)/step),10,2)

###################################################################
#Initial filling ends. Begin symmetrical considerations
##################################################################

 #   U67=np.array([[0,1,0],[1,0,0],[0,0,1]]) #exchange x y (ex: #6,#7 atoms)
 #   U69=np.array([[1,0,0],[0,1,0],[0,0,-1]]) #mirror in z (example: #6,#9toms)
 #   fmat=fillsymmirror(fmat,4,3,U69)
 #   fmat=fillsymrot(fmat,7,6,U67)
 #   fmat=fillsymmirror(fmat,9,6,U69)
 #   fmat=fillsymmirror(fmat,10,7,U69)

#there is a rotation of coordinate system, To correct it:
    for i in range(30):
#        for j in range(30):
#            if ((i+1)/3*3==(i+1) and (j+1)/3*3!=j+1) or ((i+1)/3*3!=(i+1) and (j+1)/3*3==j+1):
#                fmat[i,j]=-fmat[i,j]
    
    
        print fmat[i,0],fmat[i,1],fmat[i,2],fmat[i,3],fmat[i,4],fmat[i,5],\
              fmat[i,6],fmat[i,7],fmat[i,8],fmat[i,9],fmat[i,10],fmat[i,11],\
              fmat[i,12],fmat[i,13],fmat[i,14],fmat[i,15],fmat[i,16],fmat[i,17],\
              fmat[i,18],fmat[i,19],fmat[i,20],fmat[i,21],fmat[i,22],fmat[i,23],\
              fmat[i,24],fmat[i,25],fmat[i,26],fmat[i,27],fmat[i,28],fmat[i,29]
main()
