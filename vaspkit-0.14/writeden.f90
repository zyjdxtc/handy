subroutine writeden(tag)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.

!..............................................................
!    read density from name=CHG file of VASP
!..............................................................
!    tag =31 - total charge \____ only for CHGCAR
!         =32 - spin density /
!..............................................................
implicit none
integer, intent(in) :: tag

!local variable
character title*20,type_coodinates*20
integer :: NGX,NGY,NGZ,ntyat=1,totalatoms=0,status=0,i,j,k
integer,allocatable :: natoms(:)
real*8 :: scale, basic_vectorx,basic_vectory,basic_vectorz,x,y,z
real*8, allocatable :: grid(:,:,:)

! read CHG file
open(unit=11,file='CHG')
if (tag==31) then
   open(unit=12,file='chgden.vasp')
else if (tag==32) then
   open(unit=12,file='spnden.vasp')
end if

read(11,'(A15)') title
write(12,'(a15)') title
read(11,*) scale
write(12,"(F6.3)") scale

do i=1,3
read(11,*) basic_vectorx,basic_vectory,basic_vectorz
write(12,'(3F13.7)')basic_vectorx,basic_vectory,basic_vectorz
end do

do while(status<=0)
allocate(natoms(ntyat))
read(unit=11,fmt=*,iostat=status)(natoms(i),i=1,ntyat)
ntyat=ntyat+1

deallocate(natoms)
backspace(11)
end do
ntyat=ntyat-2
backspace(11)
allocate(natoms(ntyat))
read(unit=11,fmt=*,iostat=status)(natoms(i),i=1,ntyat)
write(12,*)(natoms(i),i=1,ntyat)
do i=1,ntyat
totalatoms=natoms(i)+totalatoms
end do
deallocate(natoms)
read(11,*) type_coodinates
write(12,*) type_coodinates
do i=1,totalatoms
read(11,*) x,y,z
write(12,"(3F11.7)") x,y,z
end do
read(11,*)    
write(12,*)

read(11,*) NGX,NGY,NGZ
write(12,'(3I5)') NGX,NGY,NGZ
allocate(grid(NGX,NGY,NGZ))

if (tag==32) then
   read(11,"(10E12.5E2)") (((grid(i,j,k),i=1,NGX),j=1,NGY),k=1,NGZ)
   read(11,*)
else if (tag==0) then
end if

read(11,"(10E12.5E2)") (((grid(i,j,k),i=1,NGX),j=1,NGY),k=1,NGZ)
write(12,"(10E14.5E2)") (((grid(i,j,k),i=1,NGX),j=1,NGY),k=1,NGZ)
close(11)
close(12)
write(*,*)
write(*,*)"Write Density file successfully!"
return
end subroutine 
