! this program written in fortran 90 analyzes the DOSCAR output file of VASP
 
! it reads PDOS information in DOSCAR, using Gaussian smearing, to calculate the integrated PDOS 
! for each ion, each lm
! output in PDOSI_gau.dat
 
 
 
program doscar_analysis
 
implicit none
 
integer :: number_of_atoms ! total number of atoms in POSCAR
 
integer :: i,j,l,l1,l2 ! dummy
 
double precision :: t ! dummy
 
double precision :: Emax , Emin ! max and min value of the energy (absciss limits)
 
integer :: number_of_steps ! discretization of the abscissa
 
double precision :: Efermi ! Fermi energy of the system
 
integer :: choice ! choice made by user
 
integer :: choice_specific ! if specific orbital wanted

integer :: orbital_num ! specific orbital number

character(len = 10) :: orbital

integer :: choice_translate ! choice made by user : translate or not to fermi energy
 
integer :: choice_polarization ! choice made by user : polarization enabled or not
 
integer :: choice_atom ! choice made by user : label of the atom the user wants the PDOS of
 
double precision :: dos_up , dos_down ! local value of dos spin up and spin down
 
double precision :: n1 , n2 , n3 , n4 , n5 , n6 , n7 , n8 , n9 , n10 , n11 , n12 , n13 , n14 , n15 , n16 , n17 , n18, n19

double precision :: Nup,Ndn,Ntot !to count the occupied states

double precision :: dE, dosi_up,dosi_down, dos_upold, dos_dnold, dos_upold2,sum1,sum2

REAL, DIMENSION(:), ALLOCATABLE :: PAR(:,:,:), DOS(:,:),n(:),SDOS(:),pdosi(:) ! PAR file

! open DOSCAR
 
open ( 10 , file = 'DOSCAR' , form = 'formatted' )
 
! first line is the total number of atoms and 3 numbers i don't know what they mean
 
read ( 10 , * ) number_of_atoms , i , i , i
 
! line 2 to 5 are useless
 
do i = 2 , 5 ; read ( 10 , * ) ; end do
 
! line 6 contains Emax , Emin , number_of_steps , Efermi and ?
 
read ( 10 , * ) Emax , Emin , number_of_steps , Efermi , t

dE=(Emax-Emin)/(number_of_steps-1)
dos_upold=0
dos_upold2=0
dos_dnold=0
Nup=0
Ndn=0
Ntot=0





! ask user if the calculation is polarized or not
 
99 write ( * , * ) "Is system polarized (press 1 for yes , press 2 for no) ?"
 
read ( * , * ) choice_polarization
 
! test if answer is correct
 
if ( choice_polarization /= 1 .and. choice_polarization /= 2 ) then
 
  write ( * , * ) "Only 1 or 2 is possible."
 
  goto 99
 
end if

101 write(*,*) "Anchor Efermi to 0? (1 for yes, 2 for no)"

read (*,*) choice_translate

if (choice_translate /=1 .and. choice_translate/=2) then
  write(*,*) "Only 1 or 2 is possible."
  goto 101
end if


! allocate DOS, PAR
if (choice_polarization ==1) then

  allocate(DOS(number_of_steps,5))
  allocate(PAR(number_of_steps,number_of_atoms,18))
  allocate(n(18))
  allocate(SDOS(18))
  allocate(pdosi(18))
else
  
  allocate(DOS(number_of_steps,3))
  allocate(PAR(number_of_steps,number_of_atoms,9))
  allocate(n(9))
  allocate(SDOS(9))
  allocate(pdosi(9))
end if

DOS=0
PAR=0
open(unit=11,file='PDOSI.dat',status='UNKNOWN')
! get total DOS
  if ( choice_polarization == 1 ) then

    do i = 1 , number_of_steps

      read (10,*) (DOS(i,j),j=1,5)
      if ( choice_translate == 1 )  DOS(i,1)=DOS(i,1)-Efermi

    end do

  else if ( choice_polarization == 2 ) then

    do i = 1 , number_of_steps

      read ( 10 , * ) (DOS(i,j),j=1,3)

      if ( choice_translate == 1 ) DOS(i,1)=DOS(i,1)-Efermi

    end do

  end if
 
 
do j =1, number_of_atoms
  read(10,*) 
  write(11,*) "ion #",j
  dos_upold=0
  dos_dnold=0
  pdosi=0
  do i = 1 , number_of_steps
 
    if ( choice_polarization == 1 ) then
   
      read ( 10 , * ) t ,(n(l),l=1,18) 
 
      do l1=1,18,2
         if (n(l1)/=0) PAR(i,j,l1 ) = n(l1)/DOS(i,2)
	 if (n(l1+1)/=0) PAR(i,j,l1+1) = n(l1+1)/DOS(i,3)
	 if (t<=Efermi .and. DOS(i+1,0)>=Efermi) then
            SDOS(l1)=(DOS(i,4)-dos_upold)*PAR(i,j,l1)+pdosi(l1)
	    SDOS(l1+1) = (DOS(i,5)-dos_dnold)*PAR(i,j,l1+1)+pdosi(l1+1)
         end if
	 
      end do
      

      write(11,'(F8.4,18E12.4)') t,((DOS(i,4)-dos_upold)*PAR(i,j,l1)+pdosi(l1),(DOS(i,5)-dos_dnold)*PAR(i,j,l1+1)+pdosi(l1+1)&
      ,l1=1,18,2)
      do l1=1,18,2
         pdosi(l1)=(DOS(i,4)-dos_upold)*PAR(i,j,l1)+pdosi(l1)
	 pdosi(l1+1)=(DOS(i,5)-dos_dnold)*PAR(i,j,l1+1)+pdosi(l1+1)
      end do
      dos_upold=DOS(i,4)
      dos_dnold=DOS(i,5)

    else if ( choice_polarization == 2 ) then

      read ( 10 , * ) t ,(n(l),l=1,9)
      do l1=1,9
         if (n(l1)/=0) PAR(i,j,l1) = n(l1)/DOS(i,2)
	 if (t<=Efermi .and. DOS(i+1,0)>=Efermi) SDOS(l1)=(DOS(i,3)-dos_upold)*PAR(i,j,l1)+pdosi(l1)
      end do
      write(11,'(F8.4,9E12.4)') t, ( (DOS(i,3)-dos_upold)*PAR(i,j,l1)+pdosi(l1),l1=1,9,1)
      do l1=1,9
         pdosi(l1)=(DOS(i,3)-dos_upold)*PAR(i,j,l1)+pdosi(l1)
      end do
      dos_upold=DOS(i,3)
    end if
 
  end do
  if ( choice_polarization == 1 ) then
       sum1=0
       sum2=0
       do l1=1,18,2
          sum1=sum1+SDOS(l1)
	  sum2=sum2+SDOS(l1+1)
       end do
       write(11,'(A,I3,20E12.4)') "tot",j,(SDOS(l1),l1=1,18), sum1,sum2
  else if ( choice_polarization == 2 ) then
       sum1=0
       do l1=1,9
          sum1=sum1+SDOS(l1)
       end do
       write(11,'(A,I3,10E12.4)') "tot", j,(SDOS(l1),l1=1,9),sum1
  end if
end do
 
 
! close DOSCAR
 
close ( 10 )
close(11) 
! close output file doscar_analysis.out
 
 
DEALLOCATE (PAR)
deallocate(n)
deallocate(DOS)
deallocate(SDOS)
deallocate(pdosi)
end program doscar_analysis

