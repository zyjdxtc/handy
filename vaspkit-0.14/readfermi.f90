subroutine readfermi(fermi)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
implicit none
real*8 :: fermi,normalization,enmax,enmin,step
integer :: i,rows,columns,nth,iserror
open(unit=11,file='DOSCAR',form='formatted',status='old',iostat=iserror)
if (iserror>0) then
    write(*,*)"The DOSCAR file does not exist"
    goto 200
end if

!skip iformation of start
do i=1,5
   read (11,*)
end do

write(*,*)
!read fermi energy and rows
read (11,*)enmax,enmin,rows,fermi,normalization
step=(enmax-enmin)/(rows-1)
close(11)
return
200 end subroutine
