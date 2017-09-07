#!/usr/bin/python

import sys, string

if len(sys.argv)<3 or len(sys.argv)>6:
    print 'Usage: python band_comp_abinit2abinit.py [abinit _EIG file1] ...'
    print '          ... [abinit _EIG file2] [eV](optional) [nbdbuf #] (optional)'
    sys.exit()

# Check third argument
eVconv = ''
str_nbdbuf = ''
nbdbuf = 0
if len(sys.argv)==4:
    eVconv = str(sys.argv[3]) # Assume Ha values and convert to eV
    print '# Values assumed to be in Ha and converted to eV'
if len(sys.argv)==5:
    str_nbdbuf = str(sys.argv[3])
    nbdbuf = int(sys.argv[4])
    print '# Ignoring the last ','%3i'%nbdbuf,' bands'
if len(sys.argv)==6:
    eVconv = str(sys.argv[3]) # Assume Ha values and convert to eV
    print '# Values assumed to be in Ha and converted to eV'
    str_nbdbuf = str(sys.argv[4])
    nbdbuf = int(sys.argv[5])
    print '# Ignoring the last ','%3i'%nbdbuf,' bands'

# Parse abinit file 1
input_file1_name = str(sys.argv[1]) # name of first input file (first argument)
input_file1_r = open(input_file1_name,'r')  # open it as read file       
abinit_file1_data = input_file1_r.readlines()
input_file1_r.close()
# Read in k-point data as a list of numbers, by k-point
abinit_band1_data = []
k_point_list = []
for iline in range(2,len(abinit_file1_data)):
    # Skip line if it is a k-point spec.
    if abinit_file1_data[iline].find('kpt#') > -1:
        continue
    # Accumulate values
    new_values = map(float,string.split(abinit_file1_data[iline]))
    k_point_list.extend(new_values)
    # If we are on last line, finish appending
    if iline == len(abinit_file1_data)-1:
        abinit_band1_data.append(k_point_list)
        break
    # If the next line is a k-point spec., append.
    if abinit_file1_data[iline+1].find('kpt#') > -1:
        abinit_band1_data.append(k_point_list)
        k_point_list = []
        continue

nkpt1 = len(abinit_band1_data)
nbands1 = len(abinit_band1_data[0])

# Parse abinit file 2
input_file2_name = str(sys.argv[2]) # name of second input file (second argument)
input_file2_r = open(input_file2_name,'r')  # open it as read file       
abinit_file2_data = input_file2_r.readlines()
input_file2_r.close()
# Read in k-point data as a list of numbers, by k-point
abinit_band2_data = []
k_point_list = []
for iline in range(2,len(abinit_file2_data)):
    # Skip line if it is a k-point spec.
    if abinit_file2_data[iline].find('kpt#') > -1:
        continue
    # Accumulate values
    new_values = map(float,string.split(abinit_file2_data[iline]))
    k_point_list.extend(new_values)
    # If we are on last line, finish appending
    if iline == len(abinit_file2_data)-1:
       abinit_band2_data.append(k_point_list)
       break
    # If the next line is a k-point spec., append.
    if abinit_file2_data[iline+1].find('kpt#') > -1:
       abinit_band2_data.append(k_point_list)
       k_point_list = []
       continue

nkpt2 = len(abinit_band2_data)
nbands2 = len(abinit_band2_data[0])

# Check that the file contain the same number of
# nkpt and nbands
if nkpt2!=nkpt1 or nbands2!=nbands1:
   print ' ERROR: number of k-points or bands not the same!'
   sys.exit()

# Start the output
print '#   k-point       abinit val          elk val             diff        %diff'

# Now we begin the reading and comparison of the data
Ha_to_eV = 27.21138386
avg_diff = 0.0
avg_percentage = 0.0
nvals = 0
min_diff = 1000000000.0
max_diff = -100000000.0
input_file2_current_line='\n'
previous_kpt_val = -1.0
for band in range((nbands1-nbdbuf)):
    for kpt in range(nkpt1):
        # Calculate difference,average,max,min
        if eVconv=='eV':
            abinit_band1_data[kpt][band] = abinit_band1_data[kpt][band]*Ha_to_eV
            abinit_band2_data[kpt][band] = abinit_band2_data[kpt][band]*Ha_to_eV
            diff = abinit_band2_data[kpt][band] - abinit_band1_data[kpt][band]
        else:
            diff = abinit_band2_data[kpt][band] - abinit_band1_data[kpt][band]
        percentage = (abinit_band1_data[kpt][band]/abinit_band2_data[kpt][band]\
                      - 1.0)*100.0
        avg_diff = avg_diff + abs(diff)
        avg_percentage = avg_percentage + abs(percentage)
        nvals = nvals + 1
        if diff<min_diff:
            min_diff = diff
            min_percentage = percentage
        if diff>max_diff:
            max_diff = diff
            max_percentage = percentage
        if abs(abinit_band1_data[kpt][band])<0.1 or \
           abs(abinit_band2_data[kpt][band])<0.1:
            print '%14.9f'%float(kpt),'%18.9E'%abinit_band1_data[kpt][band],\
                  '%18.9E'%abinit_band2_data[kpt][band],'%12.3E'%diff,\
                  ' (','%7.3f'%percentage,'%)'
        else:
            print '%14.9f'%float(kpt),'%14.9f'%abinit_band1_data[kpt][band],\
                  '%18.9f'%abinit_band2_data[kpt][band],'%16.3E'%diff,\
                  ' (','%7.3f'%percentage,'%)'
    print '     '

avg_diff = avg_diff/float(nvals)
avg_percentage = avg_percentage/float(nvals)

print ''
print '#'
print '#        nvals:','%5i'%nvals
if eVconv=='eV':
    print '# average diff:','%12.6F'%avg_diff,' eV'
    print '# minimum diff:','%12.6F'%min_diff,' eV'
    print '# maximum diff:','%12.6F'%max_diff,' eV'
else:
    print '# average diff:','%12.6F'%avg_diff,' Ha'
    print '# minimum diff:','%12.6F'%min_diff,' Ha'
    print '# maximum diff:','%12.6F'%max_diff,' Ha'

print '#'
print '# NOTE: Abinit values are read in fixed format with five decimal'
print '#       places. For low values, four or three decimal figures'
print '#       may be the highest precision you can get.'
