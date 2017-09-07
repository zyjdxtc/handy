echo ion x > P.dat
for i in OUTCAR-*
do grep 'Ionic dipole moment' $i | awk {'print $5'} >> P.dat
done
echo ion y >>P.dat
for i in OUTCAR-*
do grep 'Ionic dipole moment' $i | awk {'print $6'} >> P.dat
done
echo ion z >>P.dat
for i in OUTCAR-*
do grep 'Ionic dipole moment' $i | awk {'print $7'} >> P.dat
done

echo e x >>P.dat
for i in OUTCAR-*
do grep 'Total electronic dipole moment' $i | awk {'print $6'} >> P.dat
done

echo e y >>P.dat
for i in OUTCAR-*
do grep 'Total electronic dipole moment' $i | awk {'print $7'} >> P.dat
done

echo e z >>P.dat
for i in OUTCAR-*
do grep 'Total electronic dipole moment' $i | awk {'print $8'} >> P.dat
done


