from optparse import OptionParser
import numpy as np
import sys


parser=OptionParser()
parser.add_option("-y",type="int",nargs=1,dest="col_ind")
parser.add_option("-x",type="float",nargs=2,dest="x_limit")
(options, args) = parser.parse_args()
files=args
data=np.zeros(np.loadtxt(files[0]).shape)

for i in range(len(files)):
	data +=np.loadtxt(files[i])
data/=len(files)
for i in range(len(data)):
    for j in range(len(data[0])):
	print data[i][j],
    print  

#if parser.xlimit:
#	ax.set_xlim(xlimit)

