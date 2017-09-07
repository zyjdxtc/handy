program mainmenu
! Copyright (C) 2009 W. Wang
! This file is distributed under the terms of the GNU General Public License.
! See the file COPYING for license details.
! Code URI: http://abintio.workstag.com.
implicit none
integer :: i,tag
integer :: ntyat
!integer,allocatable :: natoms(:)
!character(len=2), allocatable :: atomsymbo(:)
!call atominfo(ntyat)
!write(*,*)ntyat
write(*,*)
write(*,*)
write(*,*)"+---------------------------------------------------+"
write(*,*)"|>>>   Postprocesing tool for VASP                  |"       
write(*,*)"|      Current version: 0.14 (03.Dec.2009)          |"
write(*,*)"|...................................................|"
write(*,*)"|>>>   Written by Wei Wang (XJTU)                   |"
write(*,*)"|      Contact Me: wonvein@ymail.com                |"
write(*,*)"|...................................................|"
write(*,*)"|>>>   Code URL: http://abinitio.workstag.com       |"
write(*,*)"|      License: GNU General Public License          |"
write(*,*)"+---------------------------------------------------+"
write(*,*)
write(*,*)"Choose the problem to solve:                         "
write(*,*)"=============== Structure options ==================="
write(*,*)"1: POSCAR                                            "
write(*,*)"2: CONTCAR                                           "
write(*,*)"                                                     "
write(*,*)"=============== DOS options ========================="
write(*,*)"11: Total DOS                                        "
write(*,*)"12: Projected  DOS                                   "
write(*,*)"13: T2g-Eg DOS                                       "
write(*,*)
write(*,*)"=============== Energy Band options ================="
write(*,*)"21: Band                                             "
write(*,*)"22: Projected Band                                   "
write(*,*)"                                                     "
write(*,*)"=============== Density options ====================="
write(*,*)"31: Charge Density                                   "
write(*,*)"32: Spin Density                                     "
write(*,*)"                                                     "
write(*,*)"=============== MISC options ========================"
write(*,*)"                                                     "
write(*,*)"0: Quit                                              "

write(*,*) "------------>>"
write(*,*)

100 read(unit=*,fmt=*)tag


select case(tag)
case(0)
goto 101
case(1)
call structinfo(1)
case(2)
call structinfo(2)
case(11)
call dosinfo(0)
case(12)
call dosinfo(1)
case(13)
call dosinfo(2)
case(21)
call writeband
case(22)
call writepband
case(31)
call writeden(31)
case(32)
call writeden(32)
case default
write(*,*)
write(*,*)"Don't kid me! please try again..."
write(*,*)
write(*,*)"Choose the problem to solve:                         "
write(*,*)
goto 100
end select
101 write(*,*)
write(*,*)"+---------------------------------------------------+"
write(*,*)"+                 End                               +"
write(*,*)"+---------------------------------------------------+"
write(*,*)
end 
