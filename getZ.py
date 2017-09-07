from scipy import *
import sys
from optparse import OptionParser 

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

for i in range(len(files)):
    for j in options.col_ind:
	#ax.plot(data[i][:,0],data[i][:,int(j)],label=files[i]+'.'+str(j))
	w = data[i][:,0]
	w0 = min(abs(w)) # smallest frequency
	#print w0
	w1 = list(w)
	ind = w1.index(w0)
	k0 = (data[i][ind,int(j)] - data[i][ind-1,int(j)])/(2*w0)
	print 'file', i,'y ind',j,'slope',k0, 'Z', 1./(1-k0)

