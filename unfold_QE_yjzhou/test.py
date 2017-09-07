import  xml.etree.ElementTree as ET 
tree = ET.parse('data-file.xml')
root = tree.getroot()
nat = int(root.find('.//NUMBER_OF_ATOMS').text.split()[0])
orb_s = []
for i in range(nat):
    atom = root.find('.//ATOM.'+str(i+1)).attrib
    print atom
    orb_s.append([float(pos) for pos in atom['tau'].split()])
    orb_s[-1].append(int(atom['INDEX']))
print orb_s
