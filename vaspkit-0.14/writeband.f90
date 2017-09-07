      subroutine writeband
      implicit real*8(a-h,o-z) 
      parameter (nbd = 300) 
      parameter (nkd = 500) 
      parameter (nxd = 400) 
      parameter (natmd = 40) 
      dimension a(3,3),b(3,3),c(3),e(nkd,nbd),sk(nkd,3) 
      dimension xx(nxd) ,wei(nkd) 
      dimension dump(20),oc(nkd,nbd,natmd,4) 
      open(7,file='PROCAR',form='FORMATTED',status='OLD') 
      pi = 3.141592654 
      read(7,103) dump 
      write(*,*)
      write(*,*)"================= Spin options ======================"
      write(*,*)"1: No Spin-polarized calculation                     "
      write(*,*)"2: Spin-polarized calculation                        "
      write(*,*)
      write(*,*) "------------->>"
      read(*,*)ispin
      write(*,*)
      if ((ispin.ne.1).and.(ispin.ne.2)) then 
      write(*,*) ' INPUT ERROR, ispin must equal to 1 or 2 ' 
      stop 
      endif 
                                                                        
!     write(*,*) 'Enter # of interval (npoints) and division (ndiv):'   
!     read (*,*) npoints,ndiv                                           
      open(9,file='KPOINTS',form='FORMATTED',status='OLD') 
      read(9,100) temp 
      read(9,*) ndiv 
                                                                        
      write(*,*) 'Enter the range of energy to plot:' 
      write(*,*)
      write(*,*) "------------->>"
      read (*,*) er1,er2 
      emin=min(er1,er2) 
      emax=max(er1,er2) 
      call readfermi(ef) 
      if (ispin.eq.1) then 
      open(11,file='band.dat') 
      elseif (ispin.eq.2) then 
      open(11,file='band-up.dat') 
      open(12,file='band-dn.dat') 
      endif 
                                                                        
      open(8,file='POSCAR',form='FORMATTED',status='OLD') 
      read(8,100) temp 
!      write(6,100) temp                                                
  100  format(20a4) 
      read (8,*) aa 
!      WRITE(6,*) aa                                                    
!                                                                       
!      *** read lattice constant from POSCAR**                          
!                                                                       
      do i=1,3 
         read (8,*) (a(i,j),j=1,3) 
!       WRITE(6,500) (a(i,j),j=1,3)                                     
  500  format (3f12.8) 
      enddo 
      do i=1,3 
         do j=1,3 
         a(i,j)=aa*a(i,j) 
         enddo 
!       WRITE(6,500) (a(i,j),j=1,3)                                     
      enddo 
!                                                                       
!     *** read lattice vector from POSCAR***                            
!                                                                       
      volume=a(1,1)*a(2,2)*a(3,3)+a(1,2)*a(2,3)*a(3,1)                  &
     &+a(1,3)*a(2,1)*a(3,2)-a(1,1)*a(2,3)*a(3,2)                        &
     &-a(1,2)*a(2,1)*a(3,3)-a(1,3)*a(2,2)*a(3,1)                        
      do i=1,3 
          if (i .eq. 1) then 
            j=2 
            k=3 
          else if (i .eq. 2) then 
            j=3 
            k=1 
          else 
            j=1 
            k=2 
          endif 
        c(1)=a(j,2)*a(k,3)-a(j,3)*a(k,2) 
        c(2)=a(j,3)*a(k,1)-a(j,1)*a(k,3) 
        c(3)=a(j,1)*a(k,2)-a(j,2)*a(k,1) 
        do j=1,3 
           b(i,j)=2*pi*c(j)/volume 
!         WRITE (6,*) b(i,j)                                            
        enddo 
       enddo 
                                                                        
                                                                        
      do 9000 isp=1,ispin 
                                                                        
      read(7,104) nk,nband,nion 
      do 1000 k = 1,nk 
      read(7,103) dump 
      read(7,105) kp,(sk(k,j),j=1,3),wei(k) 
!     write(6,105) kp,(sk(k,j),j=1,3),wei(k)                            
      read(7,103) dump 
      do  nb = 1,nband 
      read(7,106) nb1,e(k,nb),occ 
!     write(6,106) nb1,e(k,nb),occ                                      
      read(7,103) dump 
      read(7,103) dump 
!     write(6,*) 'nion=',nion                                           
      niont = nion +1 
      if (nion .eq. 1) niont = 1 
      do  ion = 1,niont 
      read(7,107) (oc(k,nb,ion,j),j=1,4) 
!     write(6,107) (oc(k,nb,ion,j),j=1,4)                               
      enddo 
      read(7,103) dump 
!     write(6,103) dump                                                 
      enddo 
 1000 continue 
                                                                        
      weight = 0.0 
      do k = 1, nk 
      weight = weight + wei(k) 
      enddo 
                                                                        
      do k = 1,nk 
      wei(k) =  wei(k) / weight 
      enddo 
                                                                        
  101 format(10x,f9.5) 
  102 format(f10.5) 
  103 format(20a4) 
  104 format(16x,i3,20x,i5,19x,i4) 
  105 format(10x,i3,5x,3f11.8,13x,f11.8) 
  106 format(4x,i4,9x,f14.8,7x,f12.8) 
  107 format(3x,4f7.3) 
                                                                        
                                                                        
!                                                                       
!     *** find reciprocal lattice vector ***                            
      xx(1) = 0.0 
      nn = 1 
      do k = 1,nk-1 
      dkx=(sk(k+1,1)-sk(k,1))*b(1,1) + (sk(k+1,2)-sk(k,2))*b(2,1)       &
     &   + (sk(k+1,3)- sk(k,3))*b(3,1)                                  
      dky=(sk(k+1,1)-sk(k,1))*b(1,2) + (sk(k+1,2)-sk(k,2))*b(2,2)       &
     &   + (sk(k+1,3)- sk(k,3))*b(3,2)                                  
      dkz=(sk(k+1,1)-sk(k,1))*b(1,3) + (sk(k+1,2)-sk(k,2))*b(2,3)       &
     &   + (sk(k+1,3)- sk(k,3))*b(3,3)                                  
      del =  sqrt ( dkx**2 + dky**2 + dkz**2 ) 
      nn = nn +1 
      xx(nn) = xx(nn-1) + del 
      enddo 
                                                                        
      do n=1,nband 
        if (mod(n,2).ne.0) then 
         do k=1,nk 
          ee = e(k,n) - ef 
          if ( ee .gt. emax ) ee = emax 
          if ( ee .lt. emin ) ee = emin 
         write (10+isp,300) xx(k),ee 
         enddo 
        elseif (mod(n,2).eq.0) then 
         do i=nk,1,-1 
          ee = e(i,n) - ef 
          if ( ee .gt. emax ) ee = emax 
          if ( ee .lt. emin ) ee = emin 
          write (10+isp,300) xx(i),ee 
         enddo 
        endif 
      enddo 
  300 format (f12.8,2x,f12.8) 
                                                                        
      if (mod(nband,2) .ne. 0) then 
          write (10+isp,300) xx(nk),emin 
          write (10+isp,300) xx(1),emin 
      else 
          write (10+isp,300) xx(1),emin 
      endif 
!                                                                       
!     *** write xx-ee ***                                               
!                                                                       
        npoints=nk/ndiv 
       do n=2,npoints 
         kk=(n-1)*ndiv 
        write (10+isp,300) xx(kk),emin 
        write (10+isp,300) xx(kk),emax 
        write (10+isp,300) xx(kk),emin 
      enddo 
        write (10+isp,300) xx(nk),emin 
        write (10+isp,300) xx(nk),emax 
        write (10+isp,300) xx(1),emax 
        write (10+isp,300) xx(1),emin 
        zero=0.0 
        write (10+isp,300) xx(1),zero 
        write (10+isp,300) xx(nk),zero 
                                                                        
 9000  continue 
       write(*,*)"Write Energy Band file successfully!" 
       return 
      END subroutine                                          
