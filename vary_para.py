import string as st
import subprocess as sp



def main():
    para='KPOINTS'
    change=['4 4 4','6 6 6','8 8 8','10 10 10']
    fname='job'
    f=open(fname,'r')
    lines=f.readlines()
    f.close()
    for i in range(len(lines)):
        if st.find(lines[i],para)>=0:
            star=i
            break
    for i in range(len(change)):
        lines[star+4]=change[i]+'\n'
        f=open(fname,'w')
        f.writelines(lines)
        f.close()
        sp.call(['qsub',fname])
        print para,'=',change[i]
main()
