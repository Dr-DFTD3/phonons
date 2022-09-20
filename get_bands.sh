#!/bin/sh
# rm band*.dat phonon_band.dat
nqpoints=`grep distance band.yaml | wc -l | awk '{print $1}'`   # check how many qpoints was used 
line_number1=`grep -n distance band.yaml | awk NR==1 | awk '{print $1}'  | sed 's/\://g'` #check line number of 1st qpoint
line_number2=`grep -n distance band.yaml | awk NR==2 | awk '{print $1}'  | sed 's/\://g'` # check line number of 2nd qpoint
line_space=`echo "$line_number1 $line_number2" | awk '{print ($2-$1)}'`
nbands=`echo "$line_space" | awk '{print ($1-4)/2}'`

echo "$line_number1 $line_number2 $nqpoints $line_space $nbands"


pre_qx=`grep "q-position" band.yaml |  awk NR==1 | awk '{print $4}'`
pre_qy=`grep "q-position" band.yaml |  awk NR==1 | awk '{print $5}'`
pre_qz=`grep "q-position" band.yaml |  awk NR==1 | awk '{print $6}'`
pre_distance=0.000000


# qpoint_number=1
# while [ $qpoint_number -le $nqpoints ] 
# do
#     echo "qpoint $qpoint_number"
#     current_qx=`grep "q-position" band.yaml |  awk NR==$qpoint_number | awk '{print $4}'`
#     current_qy=`grep "q-position" band.yaml |  awk NR==$qpoint_number | awk '{print $5}'`
#     current_qz=`grep "q-position" band.yaml |  awk NR==$qpoint_number | awk '{print $6}'`

#   distance=`echo "$pre_distance $pre_qx $pre_qy $pre_qz $current_qx $current_qy $current_qz" | awk '{printf "%7.5f", $1+(($5-$2)^2.0+($6-$3)^2.0+($7-$4)^2.0)^0.5}'`
#   echo "$distance"
#     band_number=1
#     while [ $band_number -le $nbands ]
#     do
#       line_number=`echo "$line_number1 $band_number $qpoint_number $line_space" | awk '{print $1+3+($2-1)*2+($3-1)*$4}'`
#       echo  "$line_number"
#       freq=`awk NR==$line_number band.yaml | awk '{print $2}'`
#       echo "$distance $freq" >> band$band_number.dat
#       band_number=$[$band_number+1]
#     done
#  pre_distance=$distance
# pre_qx=$current_qx
# pre_qy=$current_qy
# pre_qz=$current_qz

# qpoint_number=$[$qpoint_number+1]
# done
# cat band*.dat > phonon_band.dat # combine all band to one file (you have to use xmgrace to split data)