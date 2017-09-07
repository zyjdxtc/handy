subroutine getmod(a,getmodel)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
implicit none
real(kind=8)::a(3),getmodel
getmodel=sqrt(a(1)**2+a(2)**2+a(3)**2)
return
end subroutine
