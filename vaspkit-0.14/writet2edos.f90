subroutine writet2edos(spin,rows,fermi,step)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
implicit none
!local variable
real*8 :: fermi,enmax,enmin,step,area
integer :: i,j,rows,columns,nth,iserror,spin,atomnum
real*8,allocatable :: dos(:,:),integ_dos(:,:)
write(*,*)" The Number of atom to plot?"
write(*,*)
write(*,*) "------------->>"
read(*,*)atomnum
write(*,*)
open(unit=11,file='DOSCAR',form='formatted',status='old',iostat=iserror)
if (iserror>0) then
    write(*,*)"The DOSCAR file does not exist"
    goto 200
end if

!skip tdos and pdos of the (n-1) atoms
do i=1,atomnum*(rows+1)
read(11,*)
end do

open(unit=12,file="t2edos.dat",form='formatted',status='replace')
open(unit=13,file="it2edos.dat",form='formatted',status='replace')
if (spin==1) then
write(12,*)'# E    s  p  t2  e'
write(13,*)'# E    Int-s    Int-p    Int-t2   Int-e'
elseif (spin==2) then
write(12,*)'# E    s_up    s_dn     p_up    p_dn   t2_up   t2_dn   e_up   e_dn'
write(13,*)"# Int-s_up    Int-s_dn    Int-p_up    Int-p_dn   Int-t2_up    Int-t2_dn    Int-e_up   Int-e_dn"
endif
columns=9*spin+1
allocate(dos(rows,columns))
allocate(integ_dos(rows,columns))
do i=1,rows
   read(11,'(19E12.4)')(dos(i,j),j=1,columns)
dos(i,1)=dos(i,1)-fermi
   if (spin==2) then
     do j=3,columns
        if((mod(j,2).EQ.1))then
        dos(i,j)=-1*dos(i,j)
        else
        endif
     end do
   endif
if (spin==1) then
write(12,'(5E12.4)')dos(i,1),dos(i,2), &
dos(i,3)+dos(i,4)+dos(i,5), &
dos(i,6)+dos(i,7)+dos(i,9),dos(i,8)+dos(i,10)

else if (spin==2) then
write(12,'(9E12.4)')dos(i,1),dos(i,2),dos(i,3), &
dos(i,4)+dos(i,6)+dos(i,8),dos(i,5)+dos(i,7)+dos(i,9), &
dos(i,10)+dos(i,12)+dos(i,16),dos(i,11)+dos(i,13)+dos(i,17), &
dos(i,14)+dos(i,18),dos(i,15)+dos(i,19)
end if
end do

integ_dos(1,1)=dos(1,1)-fermi
do j=2,columns
integ_dos(1,j)=0
end do
do j=2,columns
   do i=2,rows
     integ_dos(i,1)= dos(i,1)
     call trapz(dos(i,j),dos(i+1,j),step, area)
     integ_dos(i,j)=integ_dos(i-1,j)+area
   end do
end do

do i=1,rows
if (spin==1) then
write(13,'(5F8.3)')integ_dos(i,1),integ_dos(i,2), &
integ_dos(i,3)+integ_dos(i,4)+integ_dos(i,5), &
integ_dos(i,6)+integ_dos(i,7)+integ_dos(i,9),integ_dos(i,8)+integ_dos(i,10)

else if (spin==2) then
write(13,'(9F8.3)')integ_dos(i,1),integ_dos(i,2),integ_dos(i,3), &
integ_dos(i,4)+integ_dos(i,6)+integ_dos(i,8),integ_dos(i,5)+integ_dos(i,7)+integ_dos(i,9), &
integ_dos(i,10)+integ_dos(i,12)+integ_dos(i,16),integ_dos(i,11)+integ_dos(i,13)+integ_dos(i,17), &
integ_dos(i,14)+integ_dos(i,18),integ_dos(i,15)+integ_dos(i,19)
end if
end do

deallocate (dos)
deallocate (integ_dos)
close (12)
close (13)
write(*,*)"Write t2edos.dat and it2edos.dat files succesfully!"
return
200 end subroutine
