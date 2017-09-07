#Calculate the octahedral rotations M[001] and R[110]

import sys
import numpy as np
import string as st

def M3(pos,label):
    Mn1=label[0]+3
    O=label[1]+3
    Mn2=label[2]+3
    a2=(pos[Mn1][0]-pos[O][0])**2+(pos[Mn1][1]-pos[O][1])**2
    b2=(pos[Mn2][0]-pos[O][0])**2+(pos[Mn2][1]-pos[O][1])**2
    c2=(pos[Mn1][0]-pos[Mn2][0])**2+(pos[Mn1][1]-pos[Mn2][1])**2
    ab=np.sqrt(a2)*np.sqrt(b2)
    angle=np.arccos((a2+b2-c2)/2/ab)/np.pi*180
    theta=90-angle/2
    print pos[Mn1]
    print pos[Mn2]
    print pos[O]
    return theta

def R4(pos,label): # calculate the angle in yz plane
    Mn1=label[0]+3
    O=label[1]+3
    Mn2=label[2]+3
    a2=(pos[Mn1][1]-pos[O][1])**2+(pos[Mn1][2]-pos[O][2])**2
    b2=(pos[Mn2][1]-pos[O][1])**2+(pos[Mn2][2]-pos[O][2])**2
    c2=(pos[Mn1][1]-pos[Mn2][1])**2+(pos[Mn1][2]-pos[Mn2][2])**2
    ab=np.sqrt(a2)*np.sqrt(b2)
    angle=np.arccos((a2+b2-c2)/2/ab)/np.pi*180
    theta=90-angle/2
    print pos[Mn1]
    print pos[Mn2]
    print pos[O]

    return theta

def car(lines):
    pos=[]
    temp=lines[1].split()
    scale=float(temp[0])
    for j in range(3):
          line=lines[j+2].split()
          temp=[]
          for i in range(len(line)):
              
              temp.append(float(line[i])*scale)
          temp=np.array(temp)
          pos.append(temp)
    if st.find(lines[7],'D')>=0:
        for i in range(20):
            temp0=lines[8+i].split()
            postmp=float(temp0[0])*pos[0]+float(temp0[1])*pos[1]+float(temp0[2])*pos[2]
            pos.append(postmp)
    else:
        for i in range(20):
            temp0=lines[8+i].split()
            postmp=[float(temp0[0]),float(temp0[1]),float(temp0[2])]
            postmp=np.array(postmp)
            pos.append(postmp)
    return pos




def main():
    fname=sys.argv[1]
    f=open(fname,'r')
    lines=f.readlines()
    pos=car(lines)
#    pos[4+3]=pos[4+3]+pos[1]
#    pos[5+3]=pos[5+3]+pos[0]
    labelR=[4,12,5]

    labelM=[4,12,5]
    thetaM=M3(pos,labelM)
    
    print 'M3+=',thetaM
    thetaR=R4(pos,labelR)
    print 'R4+=',thetaR
main()    

