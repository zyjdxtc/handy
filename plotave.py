from optparse import OptionParser
import numpy as np
import pylab as pl
import sys


parser=OptionParser()
parser.add_option("-y",type="int",nargs=1,dest="col_ind")
parser.add_option("-x",type="float",nargs=2,dest="x_limit")
(options, args) = parser.parse_args()
files=args
data=[]
for i in range(len(files)):
        data.append(np.loadtxt(files[i]))
fig=pl.figure()
ax=fig.add_subplot(111)

data1=0

for i in range(len(files)):
        data1+=data[i]/len(files)
ax.plot(data1[:,0], data1[:,options.col_ind])
#        ax.plot(data[i][:,0],data[i][:,0]*data[i][:,options.col_ind],label=files[i])
#if parser.xlimit:
#       ax.set_xlim(xlimit)
ax.legend(loc='best')
pl.show()

