from optparse import OptionParser
import numpy as np
import pylab as pl
import sys


def my_callback(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

parser=OptionParser()
parser.add_option("-y",type="string",action='callback',callback=my_callback,dest="col_ind")
parser.add_option("-x",type="float",nargs=2,dest="x_limit")
(options, args) = parser.parse_args()
files=args
data=[]
for i in range(len(files)):
	data.append(np.loadtxt(files[i]))
fig=pl.figure()
ax=fig.add_subplot(111)
ys = options.col_ind
if not ys:
    ys = range(1,len(data[0][0]))

for i in range(len(files)):
    for j in ys:
	ax.plot(data[i][:,0],data[i][:,int(j)],label=files[i]+'.'+str(j))
#if parser.xlimit:
#	ax.set_xlim(xlimit)
ax.legend(loc='best')
pl.show()
fig.savefig("curve.pdf")
