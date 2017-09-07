for i in `seq 1 6`;
do

  cd Supercell_$i

  lines=$( awk 'END {print NR}' force_constants.${i}.dat )

  # Loop over force constants
  for j in `seq 1 $lines`;
  do

    awk -v awk_line=$j 'NR==awk_line {print}' force_constants.${i}.dat > disp.dat
    atom=$(awk '{print $1}' disp.dat)
    disp=$(awk '{print $2}' disp.dat)
    cd atom.${atom}.disp.${disp}/positive/
    if [ ! -f "forces.dat" ];then
        ~/handy/fetch_forces_vasp.sh
    fi
    cd ../negative
    if [ ! -f "forces.dat" ];then
        ~/handy/fetch_forces_vasp.sh
    fi
  done
done
