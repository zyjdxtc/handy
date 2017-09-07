import numpy as np
import string as st
import sys


if __name__=='__main__':
  fname=sys.argv[1]
  digits=sys.argv[2]

  f=open(fname,'r')
  lines=f.readlines()
  for i in range(len(lines)):
	if st.find(lines[i],'Direct')>=0:
	   startline=i+1
  format= '%.'+digits+'f %.'+digits+'f %.'+digits+'f'
  for j in range(startline,len(lines)):
#        temp=[round(float(lines[j].split()[0]),int(digits)),round(float(lines[j].split()[1]),int(digits)),round(float(lines[j].split()[2]),int(digits))]
	temp=[float(lines[j].split()[0]),float(lines[j].split()[1]),float(lines[j].split()[2])]
	print format %(temp[0],temp[1],temp[2])
  f.close()
