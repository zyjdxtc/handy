subroutine structinfo (tag)                                                                                                      
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
                                                                                                                        
implicit none
integer,intent(in) :: tag

!local varible
real(kind=8) :: realvector(3,3),recipvector(3,3),scale,lattlen(3)
real(kind=8),allocatable :: atomcoodinate(:,:)
integer :: atomtype=1,i,j,totalatoms=0,error,status=0,format                                                           
integer,allocatable :: natoms(:)                                                                                        
character(len=2),allocatable :: atomsymbol(:)                                                                              
character(len=24)::datetime,outputname,title                                                                                             
character(len=1)::isselecdynaordirect,isdirect                                                                          

write(*,*)                                                                                                              
89 format(3x,A80)                                                                                                      
write(*,*)"============ cif or xsf format opinions ============"
write(*,*)"1: cif format                                       "
write(*,*)"2: XcrysDen (xsf) format                            "
write(*,*)"                                                    "
read(*,*)format
write(*,*)"                                                    "
if ((format.ne.1).and.(format.ne.2)) then
write(*,*) ' INPUT ERROR, format must equal to 1 or 2 '
stop
endif
if (tag==1) then                                                                                                     
open(unit=12,file='POSCAR',form='formatted',status='old',iostat=error)                                                
outputname="poscar"                                                                                                      
else if(tag==2) then                                                                                                 
open(unit=12,file='CONTCAR',form='formatted',status='old',iostat=error)                                               
outputname="contcar"                                                                                                     
end if
                                                                                                                  
if (error>0) then                                                                                                     
write(*,*)"The file does not exist"
write(*,*)                                                                                     
stop                                                                                                                
end if                                                                                                                  
read(12,*)title                                                                                                              
read(unit=12,fmt=*) scale        
read(unit=12,fmt=*) ((realvector(I,J),J=1,3),I=1,3)
realvector(:,:)=scale*realvector(:,:)
do while(status<=0)                                                                                                     
allocate(natoms(atomtype))                                                                                                 
read(unit=12,fmt=*,iostat=status)(natoms(i),i=1,atomtype)                                                                  
atomtype=atomtype+1                                                                                                           
deallocate(natoms)                                                                                                      
backspace(12)                                                                                                           
end do                                                                                                                  

atomtype=atomtype-2                                                                                                           
backspace(12)                                                                                                           
allocate(natoms(atomtype))                                                                                                 
read(unit=12,fmt=*,iostat=status)(natoms(i),i=1,atomtype)                                                                  

do i=1,atomtype
totalatoms=natoms(i)+totalatoms
end do

!read OUTCAR                                                                                                                        
allocate(atomsymbol(atomtype))                                                                                                
open(unit=13,file='OUTCAR',form='formatted',status='old',iostat=error)
if (error>0) then
write(*,*)"The OUTCAR file does not exist"
write(*,*)
endif
!skip 10 rows from begin
do i=1,10
read(unit=13,fmt=*)
end do
read(unit=13,fmt="(A21)")(atomsymbol(i),i=1,atomtype)
close(13)
write(*,"(A24,10A3)")"The atomic symbol are: ",(atomsymbol(i),i=1,atomtype)                                                            
write(*,*)                                                                                                              

allocate(atomcoodinate(totalatoms,3))                                                                                    
read(12,*)isselecdynaordirect                                                                                           
if ((isselecdynaordirect=='S').or.(isselecdynaordirect=='s')) then                                                      
read(12,*)isselecdynaordirect                                                                                           
write(*,*)"Selective Dynamics is activated!!"
write(*,*)
else                                                                                                                    
end if                                                                                                                  
do i=1,totalatoms
read(12,*)atomcoodinate(i,1),atomcoodinate(i,2),atomcoodinate(i,3)
end do
                                                                                                                        
do i=1,3
call getmod(realvector(i,:),lattlen(i))
end do
if ((isselecdynaordirect=='d').or.(isselecdynaordirect=='D')) then                                                      
else if ((isselecdynaordirect=='C').or.(isselecdynaordirect=='C')&                                                      
&.or.(isselecdynaordirect=='k').or.(isselecdynaordirect=='K')) then                                                    
  do i=1,totalatoms                                                                                                       
  atomcoodinate(i,1)=atomcoodinate(i,1)/lattlen(1)                                                                              
  atomcoodinate(i,2)=atomcoodinate(i,2)/lattlen(2)                                                                    
  atomcoodinate(i,3)=atomcoodinate(i,3)/lattlen(3)                                                                     
  end do                                                                                                                  
  else
  end if
if (format==1) then
call writecif(outputname,atomtype,totalatoms,realvector,lattlen,natoms,atomsymbol,atomcoodinate) 
else if (format==2) then
call writexsf(outputname,atomtype,totalatoms,realvector,lattlen,natoms,atomsymbol,atomcoodinate)                            
else
end if

deallocate(natoms) 
deallocate(atomsymbol)
deallocate(atomcoodinate)                                                             
write(*,*)"Converted successfully!"
close(12)
return                                                                                                              
end subroutine          
