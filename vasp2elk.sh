#! /bin/bash
#!
#! script to transform the CONTRACAR into =.str file
#!
######################################################
cwd=`pwd`
input=$1
zero=0
rm output
output_file="output"

if [ -f $cwd/$1 ]; then
  echo "Input file is" $1
else 
  echo "The input file is not correct!"
fi

i=1
while read line
do
  #echo $line
  if [ $i == 1 ]; then
    cmpd=$line
    echo $cmpd
  fi
  if [ $i == 2 ]; then
    latt=` echo $line | cut -f 1 -d ' '`
    echo $latt
  fi
  if [ $i == 3 ]; then
    a11=`echo $line | cut -f 1 -d ' '`
    a12=`echo $line | cut -f 2 -d ' '`
    a13=`echo $line | cut -f 3 -d ' '`
    echo $a11 $a12 $a13
  b11=`expr $a11*$latt | bc -l`
  b12=`expr $a12*$latt | bc -l`
  b13=`expr $a13*$latt | bc -l`
  c11=`expr $b11/0.52917706 | bc -l`
  c12=`expr $b12/0.52917706 | bc -l`
  c13=`expr $b13/0.52917706 | bc -l`
  printf "%16.12f%16.12f%16.12f\n" $c11 $c12 $c13>> $output_file
  fi
  if [ $i == 4 ]; then
    a21=`echo $line | cut -f 1 -d ' '`
    a22=`echo $line | cut -f 2 -d ' '`
    a23=`echo $line | cut -f 3 -d ' '`
    echo $a21 $a22 $a23
  b21=`expr $a21*$latt | bc -l`
  b22=`expr $a22*$latt | bc -l`
  b23=`expr $a23*$latt | bc -l`
  c21=`expr $b21/0.52917706 | bc -l`
  c22=`expr $b22/0.52917706 | bc -l`
  c23=`expr $b23/0.52917706 | bc -l`
  printf "%16.12f%16.12f%16.12f\n" $c21 $c22 $c23 >> $output_file
  fi
  if [ $i == 5 ]; then
    a31=`echo $line | cut -f 1 -d ' '`
    a32=`echo $line | cut -f 2 -d ' '`
    a33=`echo $line | cut -f 3 -d ' '`
    echo $a31 $a32 $a33
  b31=`expr $a31*$latt | bc -l`
  b32=`expr $a32*$latt | bc -l`
  b33=`expr $a33*$latt | bc -l`
  c31=`expr $b31/0.52917706 | bc -l`
  c32=`expr $b32/0.52917706 | bc -l`
  c33=`expr $b33/0.52917706 | bc -l`
  printf "%16.12f%16.12f%16.12f\n" $c31 $c32 $c33 >> $output_file
  fi
  if [ $i == 6 ]; then
    elmt1=`echo $line | cut -f 1 -d ' '`
    elmt2=`echo $line | cut -f 2 -d ' '`
    elmt3=`echo $line | cut -f 3 -d ' '`
    echo $elmt1 $elmt2 $elmt3 
  fi
  if [ $i == 7 ]; then
    n1=`echo $line | cut -f 1 -d ' '` 
    n2=`echo $line | cut -f 2 -d ' '` 
    n3=`echo $line | cut -f 3 -d ' '` 
    n4=`echo $line | cut -f 4 -d ' '` 
    n12=`expr $n1+$n2  | bc`
    n13=`expr $n12+$n3 | bc`
    n14=`expr $n13+$n4 | bc`
    echo $n14 >> $output_file
  m1=9
  o1=`expr 8+$n1  | bc`
  m2=`expr $o1+1  | bc`
  o2=`expr $o1+$n2| bc`
  m3=`expr $o2+1  | bc`
  o3=`expr $o2+$n3| bc`
  
  fi
  if [[ $i -ge $m1  &&  $i -le $o1 ]]; then
    if [ $i -eq $m1 ]; then
    echo "'$elmt1.in'" >> $output_file
    echo $n1 >> $output_file
    fi
    echo  $line 0.0 0.0 0.0>> $output_file
  fi
  if [[ $i -ge $m2  &&  $i -le $o2 ]]; then
    if [ $i -eq $m2 ]; then
    echo "'$elmt2.in'" >> $output_file
    echo $n2 >> $output_file
    fi
    echo $line 0.0 0.0 0.0 >> $output_file
  fi
  if [[ $i -ge $m3  &&  $i -le $o3 ]]; then
    if [ $i -eq $m3 ]; then
    echo "'$elmt3.in'" >> $output_file
    echo $n3 >> $output_file
    fi
    echo $line 0.0 0.0 0.0 >> $output_file
  fi
  let i=i+1
done < $1 

