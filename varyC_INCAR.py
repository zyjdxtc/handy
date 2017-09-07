#Vary c in the POSCAR and submit the job
# Use as python varyC_POSCAR.py [FILE] [step] [# of points]

import string,sys,time
import subprocess as sp
fname=sys.argv[1]
#print fname
step=string.atof(sys.argv[2])
Np=string.atof(sys.argv[3])

f=open(fname,'r')
lines=f.readlines()
f.close()

for l in range(len(lines)):
    if (string.find(lines[l],'POSCAR')>0):
        num=l+5
        break
temp=string.split(lines[num])
ini=string.atof(temp[2])

for i in range(int(Np/2)):
    f=open(fname,'w')
    lines[num]='        '+temp[0]+'      '+temp[1]+'      '+str(ini+step*(i+1))+'\n'
    f.writelines(lines)
    f.close()

    sp.call(['qsub',fname])
    time.sleep(2)
    print 'job submitted, c=',ini+step*(1+i)
  
    f=open(fname,'w')
    lines[num]='        '+temp[0]+'      '+temp[1]+'      '+str(ini-step*(i+1))+'\n'
    f.writelines(lines)
    f.close()
    time.sleep(2)
    sp.call(['qsub',fname])
    print 'job submitted, c=',ini-step*(1+i)
    

