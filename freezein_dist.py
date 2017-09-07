import numpy as np
import sys,string


Natom=10
fname1=sys.argv[1] #p4/mmm position
f=open('/home/yjzhou/work/vasp/lmosmo/'+fname1+'yjzhou/CONTCAR','r')
lines=f.readlines()
for i in range(len(lines)):
    if string.find(lines[i],'Direct')>=0:
        num=i
        break
temp1=[]
temp2=[]
temp3=[]
for i in range(Natom):
    line=string.split(lines[i+num+1])
    temp1.append(string.atof(line[0]))
    temp2.append(string.atof(line[1]))
    temp3.append(string.atof(line[2]))

position0=np.array([temp1,temp2,temp3])
f.close()

step=string.atof(sys.argv[3])
#Nstep=5
fname2=sys.argv[2] #positions relaxed with distortion
f=open('/home/yjzhou/work/vasp/lmosmo/'+fname2+'yjzhou/CONTCAR','r')
lines=f.readlines()
for i in range(len(lines)):
    if string.find(lines[i],'Direct')>=0:
        num=i
        break
temp1=[]
temp2=[]
temp3=[]

for i in range(Natom):
    line=string.split(lines[i+num+1])
    temp1.append(string.atof(line[0]))
    temp2.append(string.atof(line[1]))
    temp3.append(string.atof(line[2]))
distorted=np.array([temp1,temp2,temp3])
distortion=distorted-position0
#print distortion.T

#for i in range(Nstep):

print 'lmosmo                '    
print  3.89
print '    1.0500000000000000    0.0000000000000000    0.0000000000000000'
print '     0.0000000000000000    1.0500000000000000    0.0000000000000000'
print '     0.0000000000000000    0.0000000000000000    1.9200000000000000'
print '   Sr   La   Mn   O'
print '   1   1   2   6'
print 'Direct'


    
position1= position0+step*distortion
#    position2= position0-(1+i)*step*distortion
 #   print 'Now with the',(1+i)*step,'distortion'
for j in range(Natom):
        
    print position1.T[j,0],position1.T[j,1],position1.T[j,2]
    #for j in range(Natom):    
     #   print position2.T[j,0],position2.T[j,1],position2.T[j,2]
        
