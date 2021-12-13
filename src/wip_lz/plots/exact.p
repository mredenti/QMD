fbuild(p) = sprintf("%d",p)
sbuild(s) = sprintf("%s",s)
TYPE = ''
fout = '~/QMD/src/wip_lz/plots/exact.tex'

set output fout
set terminal cairolatex pdf size 5,2

load "../../auxiliary/settings.p"

TITLE = 'Mass error vs delta'

#-------------------- PLOT 1 ---------------------------------------

set lmargin 10
set rmargin 13
set bmargin 4 
set tmargin 1

set format y "10^%+03T" 
set logscale y
set key horizontal right top

set key vertical
set pointsize 0.5

set ylabel 'Exact mass' 
#set xtics format ""
set xlabel '$\delta$'
plot "~/QMD/src/wip_lz/data/lzadia.txt" u 1:2 t ""


set output 
