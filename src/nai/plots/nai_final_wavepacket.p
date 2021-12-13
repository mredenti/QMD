fbuild(p) = sprintf("%d",p)
sbuild(s) = sprintf("%s",s)
TYPE = ''
fout = '~/QMD/src/nai/plots/nai_final_wavepacket.tex'

set output fout
set terminal cairolatex pdf size 7,5

load "../../auxiliary/settings.p"

TITLE = 'NaI case study'

#-------------------- PLOT 1 ---------------------------------------

# plot final wavepacket in position and momentum space on both levels
set multiplot layout 2,2 title TITLE font ",12" 

set lmargin 4
set bmargin 1
set rmargin 4
set tmargin 2

set key horizontal center bottom

un_ab = 1.8897261254535 

set xtics format " "
set xrange [8:16]
plot "~/QMD/src/nai/data/wavepacket.txt" u ($1 / un_ab):($3**2 + $4**2) w l t '$\psi^+(x)$'
set xrange [-0.5:0.5]
plot "~/QMD/src/nai/data/wavepacket.txt" u 2:($5**2 + $6**2) w l t '$\hat{\psi}^+(k)$'
set bmargin 2
set xlabel 'x'
set xtics format "%.0f"
set xrange [8:16]
plot "~/QMD/src/nai/data/wavepacketN17.txt" u ($1 / un_ab):($7**2 + $8**2) w l t '$\psi^-$'
set xlabel 'p'
set xtics format "%.2f"
set xrange [-0.5:0.5]
plot "~/QMD/src/nai/data/wavepacket.txt" u 2:($9**2 + $10**2) w l t '$\psi^-$'

unset multiplot
set output 
unset terminal
