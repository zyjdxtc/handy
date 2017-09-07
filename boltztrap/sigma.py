# Example of how to use vasp2boltz.py
# Create a .py file with a content similar to the following
# It is necessary to have ASE installed:
# https://wiki.fysik.dtu.dk/ase/

from ase import io
from ase.lattice.spacegroup import Spacegroup
import vasp2boltz
ao = io.read('CONTCAR')
bs = vasp2boltz.get_vasp_bandstructure()
vasp2boltz.write_bandstructure_boltztrap(bs)
vasp2boltz.write_structure_boltztrap(ao)
vasp2boltz.write_intrans_boltztrap()
