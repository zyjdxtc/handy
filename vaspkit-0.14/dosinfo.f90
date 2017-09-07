subroutine dosinfo(option)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.

!initializing all parameters
implicit none
integer :: spin,option
real*8 :: fermi,normalization,enmax,enmin,step
integer :: i,j,rows,columns,nth,iserror
real*8,allocatable :: dos(:,:)
write(*,*)
write(*,*)"================= Spin options ======================"
write(*,*)"1: No Spin-polarized calculation                     "
write(*,*)"2: Spin-polarized calculation                        "
write(*,*)
!write(*,*)"Your Choice?"
write(*,*) "------------>>"
read(*,*)spin
open(unit=11,file='DOSCAR',form='formatted',status='old',iostat=iserror)
if (iserror>0) then
    write(*,*)"The DOSCAR file does not exist"
    stop
end if

!skip iformation of start
do i=1,5
   read (11,*)
end do

write(*,*)
!read fermi energy and rows
read (11,*)enmax,enmin,rows,fermi,normalization
step=(enmax-enmin)/(rows-1)
if (option==0) then
call writetdos(spin,rows,fermi,step)
else if (option==1) then
call writepdos(spin,rows,fermi,step)
else if (option==2) then
call writet2edos(spin,rows,fermi,step)
end if
return
end subroutine

