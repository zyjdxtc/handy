subroutine reciplatt(realvector,recipvector)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
implicit none
real(8),intent(in) :: realvector(3,3)
real(8),intent(out) :: recipvector(3,3)
real,parameter :: twopi=6.2831852

!local variables
real(8) :: volume
call cross(realvector(:,2),realvector(:,3),recipvector(:,1))
call cross(realvector(:,3),realvector(:,1),recipvector(:,2))
call cross(realvector(:,1),realvector(:,2),recipvector(:,3))
volume=realvector(1,1)*(realvector(2,2)*realvector(3,3)-realvector(2,3)*realvector(3,2))&
       +realvector(1,2)*(realvector(2,3)*realvector(3,1)-realvector(2,1)*realvector(3,3))&
       +realvector(1,3)*(realvector(2,1)*realvector(3,2)-realvector(2,2)*realvector(3,1))
write(*,*)volume
recipvector(:,:)=(twopi/volume)*recipvector(:,:)
return
end subroutine
