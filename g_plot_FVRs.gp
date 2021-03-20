## nastaveni vystupu
set terminal png size 800, 600 font "Verdana,22"
str_output = 'g_plot_FVR_srovnani_y='.pos.'.png'
set output str_output

## popisky
set xlabel "time [s]"
set ylabel "Q [m^3/s]"
str_title = "Volume Flow, y = ".pos
set title str_title
set datafile separator ";"
set loadpath "./flow/"

## nastaveni grafu
set grid ytics lc rgb "#bbbbbb" lw 1 lt 0
set grid xtics lc rgb "#bbbbbb" lw 1 lt 0
# set key at graph 0.44, 0.98
set key right bottom

## plot
plot filename using 1:(1*$18) with lines lw 4 linetype rgb "red" title sprintf('CV InFlow'), filename using 1:(1*$14) with lines lw 4 linetype rgb "green" title sprintf('CV OutFlow'), filenamemt using 2:4 with lines lw 4 linetype rgb "blue" title sprintf('MT vel.')

## odpadky
#, '_ResultFlow.csv' using 1:12 with lines lw 3 linetype rgb "blue" title sprintf('InVolume World'), '_ResultFlow.csv' using 1:15 with lines lw 3 linetype rgb "dark-orange" title sprintf('OutVolume Inlet'), '_ResultFlow.csv' using 1:16 with lines lw 3 linetype rgb "cyan" title sprintf('OutVolume Wolrd')


