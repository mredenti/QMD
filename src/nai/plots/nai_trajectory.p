fbuild(p) = sprintf("%d",p)
sbuild(s) = sprintf("%s",s)
TYPE = ''
fout = '~/QMD/src/nai/plots/nai_trajectory'.sprintf(TYPE).'.tex'

set output fout
set terminal cairolatex pdf size 6,3

load "../../auxiliary/settings.p"

TITLE = 'NaI case study'

#-------------------- PLOT 1 ---------------------------------------

set logscale y
set key horizontal center bottom

set multiplot layout 1,2 title TITLE font ",12" 

set lmargin 8
set bmargin 3
set rmargin 4
set tmargin 2

set xtics format " "
set ylabel '$\|\phi^+\|_{L^2}$'
set format y "10^{%L}"


set key vertical
set pointsize 0.5

set xlabel 'itr'
set ylabel '$\|\phi\|_{L^2}$'
set xtics font ", 8" rotate by 45 right
set format x "%.0f"

set yrange [10**(-3):1]
plot "~/QMD/src/nai/data/observablesdt800.txt" u 1:11 t '$\phi^-$'

# set ytics format " "
unset ylabel
unset key

set ytics
unset logscale y
unset yrange
set format y "%.2f"

#############################################################
#set title 'Mean Momentum Up$' # energy?

set ylabel 'position'
plot "~/QMD/src/nai/data/observables.txt" u 1:2, \
       "" u 1:3 

unset multiplot
set output 
unset terminal
