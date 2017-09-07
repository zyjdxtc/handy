from scipy import *
import pylab as pl
from optparse import OptionParser
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
        data.append(loadtxt(files[i]))
fig=pl.figure()
ax=fig.add_subplot(111)

for i in range(len(files)):
    for j in options.col_ind:
        ax.plot(data[i][:,0],(1./(data[i][:,int(j)*2+1]+1j*data[i][:,int(j)*2+2])).imag - data[i][:,0],label=files[i]+'.'+str(j))
#if parser.xlimit:
#       ax.set_xlim(xlimit)
ax.legend(loc='best')
pl.show()
fig.savefig("ginv.pdf")

