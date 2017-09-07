import string,sys,re

fname=sys.argv[1]
f=open(fname,'r')
lines=f.readlines()
for i in range(len(lines)):
    j=1
    if (string.find(lines[i],'GM5')>=0 and string.find(lines[i],'normfactor')>=0):
        m=re.match('.*normfactor = (.*)',lines[i])
        factor=m.group(1)
#        print factor
        while (string.find(lines[i+j],'GM5')<0 and lines[i+j][0]!=' '):
            temp=string.split(lines[i+j])
 #           print temp
            print float(temp[1])+float(factor)*float(temp[4]),float(temp[2])+float(factor)*float(temp[5]),float(temp[3])+float(factor)*float(temp[6])
            j=j+1

f.close()
