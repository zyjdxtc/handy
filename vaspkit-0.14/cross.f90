subroutine cross(x,y,z)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
implicit none
! arguments
real(8), intent(in) :: x(3)
real(8), intent(in) :: y(3)
real(8), intent(out) :: z(3)
z(1)=x(2)*y(3)-x(3)*y(2)
z(2)=x(3)*y(1)-x(1)*y(3)
z(3)=x(1)*y(2)-x(2)*y(1)
return
end subroutine
