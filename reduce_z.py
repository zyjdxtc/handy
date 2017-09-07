import numpy as np
import sys
f=np.loadtxt(sys.argv[1],skiprows=8)
r=float(sys.argv[2])
for i in range(len(f)):
    print f[i,0],f[i,1],f[i,2]*r

