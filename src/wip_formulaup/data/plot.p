set terminal cairolatex pdf size 7,4


ALPHA = 0.5
DELTA = 0.2
EPS = 0.1
P0 = 5

str(n) = sprintf("%.3f",n)
str2(n) = sprintf("%.8f",n)
fname(delta,eps,p) = sprintf("delta%.3feps%.3fp%d",delta, eps, p)

OUTPATH = '~/Desktop/qmd/src/wip_formulaup/data/formula'.fname(DELTA, EPS, P0).'.tex'
FILENAME = 'wave'.fname(DELTA, EPS, P0).'.txt' 

set output OUTPATH 

TITLE = '$\delta=$'.str(DELTA).', $\epsilon$='.str(EPS).', $p_0$='.P0
XLBL  = '$itr$'
YLBL  = '$p$'

# linestyles
set style line 1 lt 1 lc rgb "#A00000" lw 3 pt 7 ps 1.5
set style line 2 lt 1 lc rgb "#00A000" lw 3 pt 7 ps 1.5
set style line 3 lt 1 lc rgb "#000004" lw 3 pt 7 ps 1.5

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


set tics scale 0         
set xrange [P0 - 0.5 : P0 + 0.5]
set xlabel '$p$'
set key top right

set multiplot layout 1, 2 title TITLE font ",12"

#-------------------- PLOT 1 ---------------------------------------
plot FILENAME using 6:(($7)**2+($8)**2) axes x1y1 \
                with lines ls 3 t '$\hat{\psi}^_{\text{guess}}$', \
     FILENAME using 6:(($9)**2+($10)**2) axes x1y1 \
                with lines ls 1 t '$\hat{\psi}^+$' 

plot FILENAME using 6:(abs(atan2($8,$7) - atan2($10,$9))) axes x1y1 \
                with lines ls 3 t '$\hat{\psi}^_{\text{guess}}$' #, \
    # FILENAME using 6:(atan2($9, $10)) axes x1y1 \
     #           with lines ls 1 t '$\hat{\psi}^+$' 

unset multiplot
set output
unset terminal
