#!/bin/sh

echo "[=========================================]"
echo "[==========] FREE SURFACE FLOW [==========]"
echo "[=========================================]"
echo "[Processing water level:]"
#python3 hladina_update.py
echo "[Processing velocity profiles:]"
python3 velprofile.py
sleep 1
echo "[Preparing velocity profile data:]"
# ... v rychlostech neco spatne
FILE=prutok_y*
LINE=1
#sed -i "$LINE"' s/^/#/' "$FILE"
for i in prutok_y*; do
	sed -i "$LINE"' s/^/#/' "$i"
done
sleep 1
mv $FILE ./flow/
sleep 1
# Nacteni
echo "[Processing VFR:]"
FILES=./flow/*
for file in $FILES;do
#echo $file
var=$(echo -q $file | sed 's/.*Flow\(.*\).csv.*/\1/')
#var=$(echo -q $file | sed 's/.*Long\(.*\).csv.*/\1/')
#echo $var
  if [[ "$file" == *"$var"* ]];then
    #printf '%s\n' "$file"
				#echo $file
				echo $var
				varr=$(echo $var | sed 's/-/./g')
				echo $varr
				for ffile in $FILES;do
  			if [[ "$ffile" == *"$varr"* ]];then
    	printf '%s\n' "$ffile"
    	printf '%s\n' "$file"
					gnuplot -e "filename='$file'" -e "pos='$varr'" -e "filenamemt='$ffile'" g_plot_FVRs.gp
					gnuplot -e "filename='$file'" -e "pos='$varr'" -e "filenamemt='$ffile'" g_plot_VELs.gp
					fi
				done
  fi
echo "[=========================================]"
done
echo "[Done.]"
