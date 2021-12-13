fbuild(p) = sprintf("%d",p)
sbuild(s) = sprintf("%s",s)
TYPE = ''
fout = '~/QMD/src/wip_lz/plots/momentum.tex'

set output fout
set terminal cairolatex pdf size 5,4

load "../../auxiliary/settings.p"

TITLE = 'Mass error vs delta'

#-------------------- PLOT 1 ---------------------------------------
set multiplot layout 2,1 title TITLE font ",12" 

set lmargin 10
set rmargin 13
set bmargin 1 
set tmargin 1.5 

set format y "10^%+03T" 
set format x "" 

set logscale y
set key horizontal right top

set key vertical
set pointsize 0.5

set ylabel 'Absolute error' 
#set xtics format ""
plot "~/QMD/src/wip_lz/data/lzadia.txt" u 1:(abs($2 - $3)) ls 1 t "LZadia", \
      "~/QMD/src/wip_lz/data/sa.txt" u 1:(abs($2 - $3)) ls 2 t "SA", \
      "~/QMD/src/wip_lz/data/sa2.txt" u 1:(abs($2 - $3)) ls 3 t "SA2", \
      "~/QMD/src/wip_lz/data/sa3.txt" u 1:(abs($2 - $3)) ls 4 t "SA3" 

unset key
set ylabel 'Relative error' 

plot "~/QMD/src/wip_lz/data/lzadia.txt" u 1:(abs($2 - $3)/$2) ls 1 t "lzadia", \
       "~/QMD/src/wip_lz/data/sa.txt" u 1:(abs($2 - $3)/$2) ls 2 t "SA", \
       "~/QMD/src/wip_lz/data/sa2.txt" u 1:(abs($2 - $3)/$2) ls 3  t "SA2", \
      "~/QMD/src/wip_lz/data/sa3.txt" u 1:(abs($2 - $3)/$2) ls 4 t "SA3" 

unset multiplot
set output 
