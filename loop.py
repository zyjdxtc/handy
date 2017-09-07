import string,os,sys,math
import subprocess as sp
#os.popen('elk<elk.in')
f=open('elk.in','r')
line=f.readlines()
f.close()
scale0=9.5
step=0.1
scale1=10.5
N=int((scale1-scale0)/step +1)
writeflag=0
data=open('data.dat','w') #E vs V data
data1=[] #dataset array
sp.call(['elk','<elk.in']) #run elk.in
en=open('TOTENERGY.OUT','r').readlines()
data1.append(str(scale0)+' '+en[-1]) #read the last energy,

for num in range(N):
    fnew=open('elk.in','w')
    
    for l in range(len(line)):
        if (writeflag==1):
          
            line[l]=str(scale0+step*(num+1))+'\n'
   
            writeflag=0
            break
        else:
            if (string.find(line[l],'scale')==0):
                writeflag=1
    fnew.writelines(line)
   
    fnew.close()
    sp.call(['elk','<elk.in']) #run the new input file
    print 'now the scale is', scale0+step*(num+1)
    en=open('TOTENERGY.OUT','r').readlines()
    data1.append(str(scale0+step*(num+1))+' '+en[-1])
    os.rename('TOTENERGY.OUT','TOTENERGY'+str(num+1)+'.OUT') #rename the TOTENERGY, just in case

data.writelines(data1)
data.close()
#sp.call(['elk','<elk.in'])
