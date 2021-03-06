subroutine writepdos(spin,rows,fermi,step)
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

open(unit=12,file="pdos.dat",form='formatted',status='replace')
open(unit=13,file="ipdos.dat",form='formatted',status='replace')
if (spin==1) then
write(12,*)'# E    s     p    d'
write(13,*)'# E    Int-s    Int-p    Int-d'
elseif (spin==2) then
write(12,*)'# E    s_up    s_dn     p_up    p_dn   d_up   d_dn'
write(13,*)'# E    Int-s_up    Int-s_dn    Int-p_up    Int-p_dn   Int-d_up   Int-d_dn'
else
endif
columns=3*spin+1
allocate(dos(rows,columns))
allocate(integ_dos(rows,columns))
do i=1,rows
   read(11,'(8E12.4)')(dos(i,j),j=1,columns)
dos(i,1)=dos(i,1)-fermi
   if (spin==2) then
     do j=3,columns
        if((mod(j,2).EQ.1))then
        dos(i,j)=-1*dos(i,j)
        else
        endif
     end do
   endif
write(12,'(F8.3,8E13.4)')dos(i,1),(dos(i,j),j=2,columns)
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

if(spin==1) then
write(13,'(3F8.3)')((integ_dos(i,j),j=1,columns),i=1,rows)
else 
write(13,'(7F8.3)')((integ_dos(i,j),j=1,columns),i=1,rows)
end if


deallocate (dos)
deallocate (integ_dos)
close (12)
close (13)
write(*,*)"Write pdos.dat and ipdos.dat files succesfully!"
return
200 end subroutine
