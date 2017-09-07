import numpy as np
from pyspglib import spglib as sp
from ase import Atoms
import sys
import string as st
def read_vasp( filename ):
    file = open( filename )

    lines = file.readlines()

    line1 = [ x for x in lines[0].split() ]
    symbols = line1

    scale = float(lines[1])

    cell = []
    for i in range( 2, 5 ):
        cell.append( [ float(x) for x in lines[i].split()[:3] ] )
    cell = np.array( cell ) * scale

    try:
        num_atoms = np.array([ int(x) for x in lines[5].split() ])
        line_at = 6
    except ValueError:
        symbols = [ x for x in lines[5].split() ]
        num_atoms = np.array([ int(x) for x in lines[6].split() ])
        line_at = 7
    expaned_symbols=[]
    for i in range (len(num_atoms)):
	for j in range(num_atoms[i]):
	    expaned_symbols.append(symbols[i])

    if lines[ line_at ][0].lower() == 's':
        line_at += 1

    is_scaled = True
    if ( lines[ line_at ][0].lower() == 'c' or
         lines[ line_at ][0].lower() == 'k' ):
        is_scaled = False

    line_at += 1

    positions = []
    for i in range( line_at, line_at + num_atoms.sum() ):
        positions.append( [ float(x) for x in lines[i].split()[:3] ] )

    if is_scaled:
        atoms = Atoms( symbols=expaned_symbols,
                       cell=cell,
                       scaled_positions=positions )
    else:
        atoms = Atoms( symbols=expaned_symbols,
                       cell=cell,
                       positions=positions )

    return atoms

def sym_ana(fname):
#	tol=float(sys.argv[2])
	atoms=read_vasp(fname)
	dataset0=sp.get_symmetry_dataset(atoms,symprec=1e-5)	
	tempsg=dataset0
	print '1e-5 precision',tempsg['international']
	print '1e-5 precision',tempsg['origin_shift']
	for i in range(800):
		tol=0.001*i+0.001
		dataset=sp.get_symmetry_dataset(atoms,symprec=tol)
#	sym=sp.get_spacegroup(atoms,symprec=tol)
#	print sym
		if tempsg['international']!=dataset['international']:
			print 'group\t supergroup'
			print tempsg['hall'],';',dataset['hall']
			print tempsg['international'],'\t',dataset['international']
			print tempsg['number'],'\t',dataset['number']
			print 'origin',tempsg['origin_shift'],'\t',dataset['origin_shift']
			print 'wyckoff',tempsg['wyckoffs']
			print 'new_wyckoff',dataset['wyckoffs']
			print 'equivalent atoms old',tempsg['equivalent_atoms']
			print 'equivalent atoms new',dataset['equivalent_atoms']
			print 'tolerance',tol
			print '--------------------------------------------------------------------------------------\n'
			tempsg=dataset
		if i==800-1 and dataset0['international']==dataset['international']:
			print 'cannot find superSG, but initial sym is',dataset0['international'],dataset0['number']

if __name__=='__main__':
        fname=sys.argv[1]
	sym_ana(fname)
