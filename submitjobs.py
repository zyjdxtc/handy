#This code is for submitting jobs of frozen phonon calculations
import string,os,sys,math
import subprocess as sp

jobname='jobchg'
f=open(jobname,'r')
line=f.readlines()
f.close()
natom=2
atomname=['Sr','Sr','La','La','Mn1','Mn2','Mn1','Mn2','O1','O3','O4','O2','O5','O6','O1','O3','O4','O2','O5','O6']
movingatoms=[5,7]#[1,2,3,4,5,7,6,8,9,15,12,18,10,16,11,17,13,19,14,20] #order of displacing atoms, 2 for one group.
step=0.02

for l in range(len(line)):
    if string.find(line[l],'POSCAR')>=0:
        startline=l+8
for i in range(natom/2):
    n=movingatoms[i]+startline
    m=movingatoms[i+1]+startline
   
    line1=line[n] # for restoring
    line2=line[m] #
    for j in range(3):
        temp1=string.split(line[n])
        temp2=string.split(line[m])

        for k in range(2):
            temp1[j]=str(float(temp1[j])+step-3.0*k*step) #default is temp1 + step. when k=1, is (temp1+step)+step-3step=temp1-step  
            temp2[j]=str(float(temp2[j])+step-3.0*k*step)
            line[n]='      '+temp1[0]+'          '+temp1[1]+'          '+temp1[2]+'\n'
            line[m]='      '+temp2[0]+'          '+temp2[1]+'          '+temp2[2]+'\n'
            line[6]='#$ -N C1' + '-'+(atomname[movingatoms[i]-1])+'-'+(atomname[movingatoms[i+1]-1])+'-'+str(j+1)+'-'+str(k)+'\n' #write names

            f=open(jobname,'w')
            f.writelines(line)
            f.close()
            sp.call(['qsub',jobname]) #run 
        line[n]=line1 #restore
        line[m]=line2 
        f=open(jobname,'w')
        f.writelines(line)
        f.close()
