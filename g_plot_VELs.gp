## nastaveni vystupu
set terminal png size 800, 600 font "Verdana,22"
str_output = 'g_plot_avgV_srovnani_y='.pos.'.png'
set output str_output

## popisky
set xlabel "time [s]"
set ylabel "V [m/s]"
str_title = "Avg. velocity, y = ".pos
set title str_title
set datafile separator ";"
set loadpath "./flow/"

## nastaveni grafu
set grid ytics lc rgb "#bbbbbb" lw 1 lt 0
set grid xtics lc rgb "#bbbbbb" lw 1 lt 0
# set key at graph 0.44, 0.98
set key right bottom

## plot
plot filename using 1:10 with lines lw 4 linetype rgb "green" title sprintf('CV vel. in'), filename using 1:11 with lines lw 4 linetype rgb "blue" title sprintf('Vel. W.'), filenamemt using 2:3 with lines lw 4 linetype rgb "red" title sprintf(' MT vel.')



