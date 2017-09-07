subroutine writecif(outputname,atomtype,totalatoms,basicvector,latticelength,natoms,atomsymbol,atomcoodinate)
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
                                                                                                                        
implicit none                                                                                                           
character(len=10), intent(in) :: outputname
integer, intent(in) :: atomtype, totalatoms
real(kind=8), intent(in) :: basicvector(3,3),latticelength(3)                                                                                   
character(len=2), intent(in) :: atomsymbol(atomtype)                                                                              
integer, intent(in) :: natoms(atomtype)                                                                                        
real(kind=8), intent(in) :: atomcoodinate(totalatoms,3)                                                                             

!local variable
real(kind=8) :: alpha,beta,gamma                                                                         
integer :: i,j,k
character(len=24)::datetime                                                                                             
character(len=4)::outformat=".cif"                                                                                             

!calculate angle between two basicvector
alpha=acos(dot_product(basicvector(1,:),basicvector(3,:))/(latticelength(1)*latticelength(3)))*180/3.1415926
beta=acos(dot_product(basicvector(2,:),basicvector(3,:))/(latticelength(2)*latticelength(3)))*180/3.1415926
gamma=acos(dot_product(basicvector(1,:),basicvector(2,:))/(latticelength(1)*latticelength(2)))*180/3.1415926
                                                                                                                        
! convert to CIF files                                                                                                  
call fdate(datetime)
open(unit=11,file=trim(outputname)//trim(outformat))                                                                                      
88 format(A80)                                                                                                          
write(unit=11,FMT="(A20,A34)")"_audit_creation_date",datetime                                                           
100 format(A14      F31.5)                                                                                              
write(unit=11,FMT="(A46)") "_pd_phase_name                     'CIF files'"                                             
write(unit=11,FMT=100) '_cell_length_a',latticelength(1)                                                                            
write(unit=11,FMT=100) '_cell_length_b',latticelength(2)                                                                 
write(unit=11,FMT=100) '_cell_length_c',latticelength(3)                                                                            
write(unit=11,FMT="(A17,F28.6)") '_cell_angle_alpha',alpha                                                              
write(unit=11,FMT="(A16,F29.6)") '_cell_angle_beta',beta                                                                
write(unit=11,FMT="(A17,F28.6)") '_cell_angle_gamma',gamma                                                              
write(unit=11,FMT="(A46)") "_symmetry_space_group_name_H-M         'P 1  '"                                             
write(unit=11,FMT="(A40)") "_symmetry_Int_Tables_number            1"                                                   
                                                                                                                        
write(unit=11,FMT="(A5)")"loop_"                                                                                        
write(unit=11,FMT="(A26)")"_symmetry_equiv_pos_as_xyz"                                                                  
write(unit=11,FMT="(A13)")"'x, y, z'"                                                                                   
                                                                                                                        
write(unit=11,FMT="(A5)")"loop_"                                                                                        
write(unit=11,FMT="(A19)")"_atom_site_label"                                                                            
write(unit=11,FMT="(A23)")"_atom_site_occupancy"                                                                        
write(unit=11,FMT="(A21)")"_atom_site_fract_x"                                                                          
write(unit=11,FMT="(A21)")"_atom_site_fract_y"                                                                          
write(unit=11,FMT="(A21)")"_atom_site_fract_z"                                                                          
write(unit=11,FMT="(A35)")"_atom_site_thermal_displace_type"                                                            
write(unit=11,FMT="(A28)")"_atom_site_U_iso_or_equiv"                                                                   
write(unit=11,FMT="(A25)")"_atom_site_type_symbol"                                                                      
i=1                                                                                                                     
 do j=1,atomtype                                                                                                           
      do k=1,natoms(j)                                                                                                  
      write(unit=11,FMT="(3x,A2,I3.3,F5.1,F9.3,F9.3,F9.3,A6,F7.3 A4)")&                                              
      &adjustr(atomsymbol(j)),k,1.0,atomcoodinate(i,1),atomcoodinate(i,2),atomcoodinate(i,3),"Uiso",1.0,adjustr(atomsymbol(j))   
      i=i+1                                                                                                             
      end do                                                                                                            
   end do                                                                                                               
close(11) 
return                                                                                                                    
!201 stop                                                                                                                
end subroutine                                                                                                                   

