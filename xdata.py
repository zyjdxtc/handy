# convert the EvsV data, find out the lowest E, and set it to zero
# then shift the whole data set with that point

# use as: python xdata.py [FILE] [start] [step]

# NEED to set start and step value for length scale
import string,sys
fname=sys.argv[1]

f=open(fname,'r')
line1=f.readlines()
f.close()

start=string.atof(sys.argv[2]) #start value of the variable
step=string.atof(sys.argv[3])
mini=[]

for l in range(len(line1)):
    line1[l]=string.split(line1[l])
    mini.append(string.atof(line1[l][1]))
print mini
print min(mini)
f=open(fname,'w')
for l in range(len(line1)):
    line1[l][1]=str(string.atof(line1[l][1])-min(mini))
    line1[l][0]=str(start+l*step)
    line1[l]=line1[l][0]+'  '+line1[l][1]+'\n'

f.writelines(line1)

f.close()
    
