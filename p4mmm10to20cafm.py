#enlarge 1 1 2 unit cell to \sqrt 2 \sqrt 2 2 superlattice, p4/mmm sym

import string as st

def main():
    fname='test10'
    f= open(fname,'r')
    lines=f.readlines()
    temp=st.split(lines[2])
    a0=(temp[0])
    temp=st.split(lines[4])
    c=temp[2]
    a0half=str(float(a0)/2.0)
    newlines=[]
  #  for l in range(len(lines)):
  #      if st.find(lines[l],'Car')>=0 or st.find(lines[l],'Dire') >=0:
    print 'lmosmo'
    print 1.0
    print a0+'     '+'-'+a0+'     ',0
    print a0+'     '+a0+'     ',0
    print 0.0,0.0,c
    print 'Sr La Mn O'
    print '2 2 4 12'
    print 'Cartesian'
#####################################   sr
    temp=st.split(lines[6])
    print ('    '+temp[0]+'    '+temp[1]+'    '+temp[2])
    
    print ('    '+a0+'    '+temp[1]+'    '+temp[2])

####################################  la
    temp=st.split(lines[7])
    print ('    '+temp[0]+'    '+temp[1]+'    '+temp[2])

    print ('    '+a0+'    '+temp[1]+'    '+temp[2])


######################################   mn

    temp=st.split(lines[8])
    print('    '+temp[0]+'    '+'-'+temp[1]+'    '+temp[2])
    print('    '+temp[0]+'    '+temp[1]+'    '+temp[2])
    temp=st.split(lines[9])
    print('    '+temp[0]+'    '+'-'+temp[1]+'    '+temp[2])
    print('    '+temp[0]+'    '+temp[1]+'    '+temp[2])
##################################### o1 o2

    temp=st.split(lines[10])
    print('    '+temp[0]+'    '+'-'+temp[1]+'    '+temp[2])
    print('    '+temp[0]+'    '+temp[1]+'    '+temp[2])
    temp=st.split(lines[13])
    print('    '+temp[0]+'    '+'-'+temp[1]+'    '+temp[2])
    print('    '+temp[0]+'    '+temp[1]+'    '+temp[2])

######################################## o3 o4 o4 o3
    temp=st.split(lines[11])
    print('    '+temp[0]+'    '+temp[1]+'    '+temp[2])
    temp1=st.split(lines[12])
    print('    '+a0+'    '+'-'+temp1[1]+'    '+temp1[2])
    print('    '+a0+'    '+temp1[1]+'    '+temp1[2])
    print('    '+str(3*float(a0half))+'    '+temp[1]+'    '+temp[2])

####################################### o5 o6 o6 o5
    temp=st.split(lines[14])
    print('    '+temp[0]+'    '+temp[1]+'    '+temp[2])
    temp1=st.split(lines[15])
    print('    '+a0+'    '+'-'+temp1[1]+'    '+temp1[2])
    print('    '+a0+'    '+temp1[1]+'    '+temp1[2])
    print('    '+str(3*float(a0half))+'    '+temp[1]+'    '+temp[2])

#################################
    f.close()


main()

