! this program written in fortran 90 analyzes the DOSCAR output file of VASP
 
! depending on user answers, it may compute the total density of states, or projected density of states of any atom labeled as in the POSCAR file.
 
! the program askes the user what it needs during execution. no input file is needed. for simplicity.
 
! the energies may be translated so that Fermi energy is the reference (abscissa is E-Efermi) if user wants.
 
! it has been written by Maximilien Levesque, while in postdoc @ Ecole Normale Superieure, Paris
 
! in the group of theoretical physical-chemistry of Daniel Borgis
 
! it is free of any copyright. just send me an email max.....en.lev....e at gmail.com for thanks :) or bug reports.
 
! it's based on VASP 4.6 documentation written found at http://cms.mpi.univie.ac.at/vasp/vasp/DOSCAR_file.html
 
! I recommand to use the GNU fortran compiler (gfortran)
 
! for compilation, just type in almost any terminal :    gfortran doscar_analysis.f90 -o doscar_analysis.exe
 
! and then execute it :    ./doscar_analysis.exe
 
! the POSCAR file should be in the directory from which you call doscar_analysis.
 
! for instance, if you have compilde doscar_analysis.exe in  /home/max/bin , and your DOSCAR is in /home/max/vaspoutput/DOSCAR
 
! type :            cd /home/max/vaspoutput/
 
! and then :        ../bin/doscar_analysis.exe
 
! Maximilien Levesque 201108040017
! Maximilien Levesque 201109011504 debug of number of steps in case of local density of states
 
 
 
 
program doscar_analysis
 
implicit none
 
integer :: number_of_atoms ! total number of atoms in POSCAR
 
integer :: i ! dummy
 
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
 
double precision :: n1 , n2 , n3 , n4 , n5 , n6 , n7 , n8 , n9 , n10 , n11 , n12 , n13 , n14 , n15 , n16 , n17 , n18, n19, n20,n21,n22,n23,n24,n25,n26,n27,n28,n29,n30,n31,n32,n33,n34
 
 
 
! open DOSCAR
 
open ( 10 , file = 'DOSCAR' , form = 'formatted' )
 
! first line is the total number of atoms and 3 numbers i don't know what they mean
 
read ( 10 , * ) number_of_atoms , i , i , i
 
! line 2 to 5 are useless
 
do i = 2 , 5 ; read ( 10 , * ) ; end do
 
! line 6 contains Emax , Emin , number_of_steps , Efermi and ?
 
read ( 10 , * ) Emax , Emin , number_of_steps , Efermi , t
 
! ask user what he wants of me
 
77 write ( * , * ) "Do you want to compute the total density of states (press 1) or a projected one (press 2) or a projected atom &
 (press 3)?"
 
read ( * , * ) choice
 
! test if answer is correct
 
if ( choice /= 1 .and. choice /= 2 .and. choice /= 3) then
 
  write ( * , * ) "Only 1 or 2 or 3 is possible."
 
  goto 77
 
end if

if ( choice == 2 ) then

  80 write ( * , * ) "DO you want specific orbital? 1(Y), 2(N)"

  read ( *, * ) choice_specific

  if ( choice_specific /= 1 .and. choice_specific /= 2 ) then

    write ( * , * ) "Only 1 or 2 is possible."

    goto 80

  else if (  choice_specific == 1 ) then

   write ( * , * ) "input the orbital you want: s px py pz dxy dyz dxz dx2-y2 dz2 f-3 f-2 f-1 f0 f1 f2 f3"

   read ( * , * ) orbital

  end if

end if 
! ask user if he wants the DOS of a specific orbital

! ask user if he wants to translate to Fermi level or not
 
88 write ( * , * ) "Do you want to translate all the energies to Fermi energy (press 1 for yes , press 2 for no) ?"
 
read ( * , * ) choice_translate
 
! test if answer is correct
 
if ( choice_translate /= 1 .and. choice_translate /= 2 ) then
 
  write ( * , * ) "Only 1 or 2 is possible."
 
  goto 88
 
end if
 
! ask user if the calculation is polarized or not
 
99 write ( * , * ) "Is system polarized (press 1 for yes , press 2 for no) ?"
 
read ( * , * ) choice_polarization
 
! test if answer is correct
 
if ( choice_polarization /= 1 .and. choice_polarization /= 2 ) then
 
  write ( * , * ) "Only 1 or 2 is possible."
 
  goto 99
 
end if
 
! open file for writting output
 
open ( unit = 11 , file = 'doscar_analysis.out' , form = 'formatted' )
 
! write it Fermi energy
 
write ( 11 , * ) "# E fermi = " , Efermi

!=========================================================================================
! if total DOS is wanted
 
if ( choice == 1 ) then
 
  ! read the number_of_steps next lines.
 
  if ( choice_polarization == 1 ) then
 
    do i = 1 , number_of_steps
 
      read ( 10 , * ) t , dos_up , dos_down
 
      if ( choice_translate == 1 ) write ( 11 , * ) t - Efermi , dos_up , -dos_down , dos_up + dos_down
 
      if ( choice_translate == 2 ) write ( 11 , * ) t , dos_up , -dos_down , dos_up + dos_down
 
    end do
 
  else if ( choice_polarization == 2 ) then
 
    do i = 1 , number_of_steps
 
      read ( 10 , * ) t , dos_up
 
      if ( choice_translate == 1 ) write ( 11 , * ) t - Efermi , dos_up
 
      if ( choice_translate == 2 ) write ( 11 , * ) t , dos_up
 
    end do
 
  end if
 
else if ( choice == 2 ) then
 
  ! if projected DOS is wanted
 
  ! first ask user which atom he is interested in
 
  1010 write ( * , * ) "Which atom (same label as in POSCAR and first label is 1 (not 0)) ?"
 
  read ( * , * ) choice_atom
 
  ! test if answer is correct
 
  if ( choice_atom < 1 .or. choice_atom > number_of_atoms ) then
 
    write ( * , * ) "Wrong answer"
 
    goto 1010
 
  end if
 
  ! go to line corresponding to good label
 
  ! ignore first total dos lines
 
  do i = 1 , number_of_steps ; read ( 10 , * ) ; end do
 
  ! ignore non wanted atoms
 
  if ( choice_atom > 1 ) then
 
    do i = 1 , ( choice_atom - 1) * ( number_of_steps + 1 ) ; read ( 10 , * ) ; end do
 
  end if
 
  ! read useless line
 
  read ( 10 , * )
 
  ! read info. format is s+ s- px+ px- py+ py- pz+ pz- dxy+ dxy- dyz+ dyz- dz2+ dz2- dxz+ dxz- dx2-y2+ dx2-y2- 
  ! or s px py pz dxy dyz dz2 dxz dx2-y2
 
  if ( choice_specific /= 1) then

  do i = 1 , number_of_steps
 
    if ( choice_polarization == 1 ) then
   
      read ( 10 , * ) t , n1 , n2 , n3 , n4 , n5 , n6 , n7 , n8 , n9 , n10 , n11 , n12 , n13 , n14 , n15 , n16 , n17 , n18 &
                      ,n19,n20,n21,n22,n23,n24,n25,n26,n27,n28,n29,n30,n31,n32,n33,n34
 
      dos_up = n1 + n3 + n5 + n7 + n9 + n11 + n13 + n15 + n17+n19+n21+n23+n25+n27+n29+n31+n33
 
      dos_down = n2 + n4 + n6 + n8 + n10 + n12 + n14 + n16 + n18+n20+n22+n24+n26+n28+n30+n32+n34
 
      if ( choice_translate == 1 ) write ( 11 , * ) t - Efermi , dos_up , -dos_down , dos_up + dos_down
 
      if ( choice_translate == 2 ) write ( 11 , * ) t , dos_up , -dos_down , dos_up + dos_down
 
    else if ( choice_polarization == 2 ) then
 
      read ( 10 , * ) t , n1 , n2 , n3 , n4 , n5 , n6 , n7 , n8 , n9,n10,n11,n12,n13,n14,n15,n16
 
      dos_up = n1 + n2 + n3 + n4 + n5 + n6 + n7 + n8 + n9+n10+n11+n12+n13+n14+n15+n16
 
      if ( choice_translate == 1 ) write ( 11 , * ) t - Efermi , dos_up
 
      if ( choice_translate == 2 ) write ( 11 , * ) t , dos_up
 
    end if
 
  end do

  else 
    
   do i = 1 , number_of_steps

    if ( choice_polarization == 1 ) then

      read ( 10 , * ) t , n1 , n2 , n3 , n4 , n5 , n6 , n7 , n8 , n9 , n10 , n11 , n12 , n13 , n14 , n15 , n16 , n17 , n18&
                      ,n19,n20,n21,n22,n23,n24,n25,n26,n27,n28,n29,n30,n31,n32,n33,n34
      
      if ( orbital == 's') then   

        dos_up = n1 

        dos_down = n2

      else if ( orbital == 'px') then

        dos_up = n3

        dos_down = n4

      else if ( orbital == 'py') then

        dos_up = n5

        dos_down = n7

      else if ( orbital == 'pz') then

        dos_up = n7

        dos_down = n9

      else if ( orbital == 'dxy') then

        dos_up = n9

        dos_down = n10

      else if ( orbital == 'dyz') then

        dos_up = n11

        dos_down = n12

      else if ( orbital == 'dz2') then

        dos_up = n13

        dos_down = n14

      else if ( orbital == 'dxz') then

        dos_up = n15

        dos_down = n16

      else if ( orbital == 'dx2-y2') then

        dos_up = n17

        dos_down = n18

      end if

      if ( choice_translate == 1 ) write ( 11 , * ) t - Efermi , dos_up , -dos_down , dos_up + dos_down

      if ( choice_translate == 2 ) write ( 11 , * ) t , dos_up , -dos_down , dos_up + dos_down

    else if ( choice_polarization == 2 ) then

      read ( 10 , * ) t , n1 , n2 , n3 , n4 , n5 , n6 , n7 , n8 , n9

      if ( orbital == 's' ) then

        dos_up = n1

      else if ( orbital == 'px') then

        dos_up = n2

      else if ( orbital == 'py') then

        dos_up = n3

      else if ( orbital == 'pz') then

        dos_up = n4

      else if ( orbital == 'dxy') then

        dos_up = n5

      else if ( orbital == 'dyz') then

        dos_up = n6

      else if ( orbital == 'dxz') then

        dos_up = n7

      else if ( orbital == 'dx2-y2') then

        dos_up = n8

      else if ( orbital == 'dz2') then

        dos_up = n9

      end if 


      if ( choice_translate == 1 ) write ( 11 , * ) t - Efermi , dos_up

      if ( choice_translate == 2 ) write ( 11 , * ) t , dos_up
    
    end if

   end do

  end if
 
end if
 
 
! close DOSCAR
 
close ( 10 )
 
! close output file doscar_analysis.out
 
close ( 11 )
 
write ( * , * ) 'done. look at    doscar_analysis.out'
 
write ( * , * ) 'To read it, you may use      xmgrace -nxy doscar_analysis.out'
 
end program doscar_analysis
