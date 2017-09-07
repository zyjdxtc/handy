
import numpy as np
import sys
data = np.loadtxt(sys.argv[1])
xlow = int(sys.argv[2])
xhigh = int(sys.argv[3])

for i in range(30):
    temp = []
    for j in range(xlow, xhigh):
	
    	temp.append(np.sum(data[j-10 : j+11, 3:], axis = 0)/21.0)
    for j in range(xlow,xhigh):
	data[j,3:] = temp[j-xlow][:]
for j in range(xhigh,len(data)):
    data[j,3:] = temp[-1][:]
fout = open('output.dat','w')
for i in range(len(data)):
    for j in range(len(data[i])):
    	print >> fout, data[i,j],
    print >> fout, ''

