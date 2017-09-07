#Makefile for vaspkit

FC=gfortran
FFLAGS= -O2
LFLAGS= $(FFLAGS)
EXE= vaspkit                                                             
SRC= cross.f90 dosinfo.f90 mainmenu.f90 getmod.f90 readfermi.f90 reciplatt.f90 structinfo.f90 trapz.f90 writeband.f90 writepband.f90 writeden.f90 writet2edos.f90 writecif.f90 writepdos.f90 writetdos.f90 writexsf.f90                                                                                 
                                                                            
#                                                                           
# No need to edit below this line                                           
#                                                                           
                                                                            
.SUFFIXES:                                                                  
.SUFFIXES: .f90 .o                                                          
                                                                            
OBJ=	$(SRC:.f90=.o)                                                        
                                                                            
.f90.o:                                                                     
	$(FC) $(FFLAGS) -c $<                                                     
                                                                            
all:	$(EXE)                                                                
                                                                            
$(EXE):	$(OBJ)                                                              
	$(FC) $(LFLAGS) -o $@ $(OBJ)                                              
                                                                            
$(OBJ):	$(MF)                                                               
                                                                            
tar:                                                                        
	tar cvf $(EXE).tar $(MF) $(SRC)                                           
                                                                            
clean:                                                                      
	rm -f $(OBJ) $(EXE)                                              

