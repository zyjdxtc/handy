subroutine writetdos(spin,rows,fermi,step)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
implicit none
!initializing all parameters
integer :: spin
real*8 :: fermi,normalization,enmax,enmin,step
integer :: i,j,rows,columns,nth,iserror
real*8,allocatable :: dos(:,:)

open(unit=12,file="tdos.dat",form='formatted',status='replace')
if (spin==1) then
write(*,*)"No Spin-polarized calculation"
write(12,*)'# E       tdos      Int'
elseif (spin==2) then
write(*,*)"Spin-polarized calculation"
write(12,*)'# E       tdos_up       tdos_dn       Int_up       Int_dn'
else
endif
columns=2*spin+1
allocate(dos(rows,columns))
write(*,*)
do i=1,rows
!filename= "tdos.dat"
   read(11,'(5E12.4)')(dos(i,j),j=1,columns)
   dos(i,1)=dos(i,1)-fermi
   if (spin==2) then
     do j=3,columns
        if((mod(j,2).EQ.1))then
        dos(i,j)=-1*dos(i,j)
        else
        endif
     end do
   endif
write(12,'(F8.3,4E13.4)')dos(i,1),(dos(i,j),j=2,columns)
end do
deallocate (dos)
close (12)
write(*,*)"Write tdos.dat file succesfully!"
200 return 
end subroutine
