subroutine trapz(a,b,step,area)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
! Code URI: http://abintio.workstag.com.

implicit none
real(8),intent(in) :: a, b, step
real(8),intent(out) :: area
area=(a+b)*step/2

return 
end subroutine
