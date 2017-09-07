subroutine writexsf(outputname,atomtype,totalatoms,realvector,lattlen,natoms,atomsymbol,atomcoodinate)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
!include 'atom.f90'
implicit none
character(len=10), intent(in) :: outputname
integer, intent(in) :: atomtype, totalatoms
real(kind=8), intent(in) :: realvector(3,3),lattlen(3)
character(len=2), intent(in) :: atomsymbol(atomtype)
integer, intent(in) :: natoms(atomtype)
integer :: atomnum(atomtype)
real(kind=8), intent(in) :: atomcoodinate(totalatoms,3)
integer :: i,j=1,k=1
character(len=4)::outformat=".xsf"

!local variables
character(len=2):: eletable(100)
data eletable /  "H",  "He", "Li", "Be", "B",  "C",  "N",  "O", &
  "F",  "Ne", "Na", "Mg", "Al", "Si", "P",  "S", &
  "Cl", "Ar", "K",  "Ca", "Sc", "Ti", "V",  "Cr",&
  "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge",&
  "As", "Se", "Br", "Kr", "Rb", "Sr", "Y",  "Zr",&
  "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",&
  "In", "Sn", "Sb", "Te", "I",  "Xe", "Cs", "Ba",&
  "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd",&
  "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf",&
  "Ta", "W",  "Re", "Os", "Ir", "Pt", "Au", "Hg",&
  "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra",&
  "Ac", "Th", "Pa", "U",  "Np", "Pu", "Am", "Cm",&
  "Bk", "Cf", "Es", "Fm"/

do i=1,atomtype
   do j=1,100
      if (trim(eletable(j)) .EQ. trim(atomsymbol(i))) then
      atomnum(i)=j
      exit
      end if
   end do
end do
open(unit=11,file=trim(outputname)//trim(outformat))
write(11,*)
write(11,*)"CRYSTAL"
write(11,*)
write(11,*)"PRIMVEC"
write(11,"(3F12.7)")((realvector(i,j),j=1,3),i=1,3)
write(11,*)"PRIMCOORD"
write(11,"(2I3)")totalatoms,1
do i=1,atomtype
   do j=1,natoms(i)
   write(11,"(I3,3F9.3)")atomnum(i),atomcoodinate(k,1)*lattlen(1),atomcoodinate(k,2)*lattlen(2),atomcoodinate(k,3)*lattlen(3)
   k=k+1
   end do
end do
return
end subroutine
