set terminal cairolatex pdf size 6,7



ALPHA = 0.5
DELTA = 0.05
EPS = 0.1
P0 = 5

str(n) = sprintf("%.3f",n)
str2(n) = sprintf("%.8f",n)
fname(delta,eps,p) = sprintf("delta%.3feps%.3fp%d",delta, eps, p)
OUTPATH = '~/Desktop/qmd/src/wip_upperwave/data/'.fname(DELTA, EPS, P0).'.tex'
FILENAME = fname(DELTA, EPS, P0).'.txt'
FILENAME2 = 'wave'.fname(DELTA, EPS, P0).'.txt' 

set output OUTPATH 

TITLE = '$\delta=$'.str(DELTA).', $\epsilon$='.str(EPS).', $p_0$='.P0
XLBL  = '$itr$'
YLBL  = '$p$'

# linestyles
set style line 1 lt 1 lc rgb "#A00000" lw 6 pt 7 ps 1.5
set style line 2 lt 1 lc rgb "#00A000" lw 6 pt 7 ps 1.5
set style line 3 lt 1 lc rgb "#000004" lw 6 pt 7 ps 1.5
set style line 4 lt 1 lc rgb "#0000A0" lw 6 pt 7 ps 1.5
set style line 5 lt 1 lc rgb "#D0D000" lw 6 pt 7 ps 1.5
set style line 6 lt 1 lc rgb "#00D0D0" lw 6 pt 7 ps 1.5
set style line 7 lt 1 lc rgb "#B200B2" lw 6 pt 7 ps 1.5

set style line 11 lc rgb '#808080' lt 1
set border 3 back ls 11
# define grid
set style line 12 lc rgb '#808080' lt 0 lw 1
set grid back ls 12

# On both the x and y axes split each space in half and put a minor tic there
#set mxtics 2
#set mytics 2

#set style line 80 lt 0 lc rgb "#808080"
#set border 3 back ls 80
#set style line 81 lt 0 lc rgb "#808080" lw 0.5
#set grid back ls 81

# Draw the grid lines for both the major and minor tics
set grid xtics
set grid ytics
#set grid mxtics
#set grid mytics

set key center right
set key spacing 2

# nomirror means do not put tics on the opposite side of the plot
set xtics nomirror
set ytics nomirror




set tmargin 1
set bmargin 1 
set lmargin 8
set rmargin 8
unset xtics
unset ytics

set multiplot layout 4, 1 title TITLE font ",12"

# -------------------------- PLOT 1 --------------------------------
set tics scale 0
set format x ""
unset xrange
set format y2 "%.4f"
# make sure you do not need change to representation for mass
set y2tics font ", 6" 
set format y2 "%.2t*10^{%S}"
set border 0 
set border 8 linecolor rgb "#000004" lw 8
set ylabel YLBL
plot FILENAME using 6:3 axes x1y1 with lines ls 1 t '$\bar{p}+$', \
FILENAME using 6:4 axes x1y1 with lines ls 2 t '$\bar{p}-$', \
FILENAME using 6:5 axes x2y2 with lines ls 3 t '$\|\psi^+\|_{L^2}$'
# ---------------------------     ------------------------------


# -------------------------- PLOT 2 --------------------------------
set tics scale 0         
#unset key 
unset xrange
unset title
unset format x
unset format y2
set bmargin -3
set tmargin 0.5

#set y2range [0.1:0.5]
#set xrange [700:1400]

set xtics rotate by 45 right font ",6"
#set title TITLE 
set xlabel XLBL  
set ylabel '$x$' 
unset y2tics

set border 1 lw 5 lc rgb '#808080' 

plot FILENAME using 6:1 axes x1y1 with lines ls 1 t '$\bar{x}+$', \
FILENAME using 6:2 axes x2y2 with lines ls 2 t '$\bar{x}^-$'
# ---------------------------     ------------------------------


# -------------------------- PLOT 3 --------------------------------
set tics scale 0         
unset xrange
unset title
set xrange [P0-1:P0+1]
set xlabel '$p$'
set tmargin 1
set bmargin -0.5
set y2tics
unset ytics
unset ylabel

set key top right

stats FILENAME2 using 8 every ::1::1 prefix 'pmin' noout
stats FILENAME2 using 8 every ::2::2 prefix 'pmax' noout
stats FILENAME2 using (($8)*(($9)**2 + ($10)**2)*(abs(pmin_min - pmax_max))) prefix 'boa' noout 
stats FILENAME2 using (($8)*(($11)**2 + ($12)**2)*(abs(pmin_min - pmax_max))) prefix 'psiup' noout
stats FILENAME2 using (($8)*(($2)**2 + ($3)**2)*(abs(pmin_min - pmax_max))) prefix 'psiupdiff' noout
stats FILENAME2 using ((($11)**2 + ($12)**2)*(abs(pmin_min - pmax_max))) prefix 'psiup2' noout
stats FILENAME2 using ((($2)**2 + ($3)**2)*(abs(pmin_min - pmax_max))) prefix 'psiupdiff2' noout
stats FILENAME2 using ((($13)**2 + ($14)**2)*(abs(pmin_min - pmax_max))) prefix 'psidown2' noout

#plot sqrt(ALPHA**2*tanh(x)**2 + DELTA**2)#, \
     #-sqrt(ALPHA**2*tanh(x)**2 + DELTA**2)  
plot FILENAME2 using 8:(($13)**2+($14)**2) axes x1y2 \
                 with lines ls 2 t '$\hat{\psi}^-$'.'('.str2(psidown2_sum).')', \
     FILENAME2 using 8:(($2)**2 + ($3)**2) axes x1y2 \
                with lines ls 4 t '$\hat{\psi}^+_{\Delta}$'.'('.str2(psiupdiff2_sum).')', \
    FILENAME2 using 8:(($17)**2 + ($18)**2) axes x1y2 \
                with lines ls 1 t '$\hat{\psi}^-_{\text{shift}}$'.'('.str2(psiupdiff2_sum).')', 

set ylabel '$| |^2$'
set origin 0.0,0.25
set ytics
unset y2tics
set key left
plot FILENAME2 using 8:(($9)**2+($10)**2) axes x1y1 \
                with lines ls 3 t '$\hat{\psi}^+_{\text{BOA}}$'.'('.str(boa_sum).')', \
     FILENAME2 using 8:(($11)**2+($12)**2) axes x1y1 \
                with lines ls 1 t '$\hat{\psi}^+$'.'('.str2(psiup2_sum + psidown2_sum).')' 

#-------------------- PLOT 4 ---------------------------------------
set origin 0.0,0.0
plot FILENAME2 using 8:(($15)**2+($16)**2) axes x1y1 \
                with lines ls 3 t '$\hat{\psi}^_{\text{guess}}$', \
     FILENAME2 using 8:(($11)**2+($12)**2) axes x1y1 \
                with lines ls 1 t '$\hat{\psi}^+$'.'('.str2(psiup2_sum + psidown2_sum).')' 


unset multiplot
set output
unset terminal
