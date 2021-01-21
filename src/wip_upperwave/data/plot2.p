set terminal cairolatex pdf size 6,4

ALPHA = 0.5
DELTA = 0.5
EPS = 0.1
P0 = 5

str(n) = sprintf("%.3f",n)
str2(n) = sprintf("%.8f",n)
fname(delta,eps,p) = sprintf("delta%.3feps%.3fp%d",delta, eps, p)
OUTPATH = '~/qmd/src/wip_upperwave/data/guess'.fname(DELTA, EPS, P0).'.tex'
FILENAME = fname(DELTA, EPS, P0).'.txt'
FILENAME2 = 'guess'.fname(DELTA, EPS, P0).'.txt' 

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

set multiplot layout 1, 2 title TITLE font ",12"


# -------------------------- PLOT ABS2 --------------------------------
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

plot FILENAME2 using 1:(($4)**2+($5)**2) axes x1y1 \
                with lines ls 3 t '$\hat{\psi}^+_{\text{guess}}$', \
     FILENAME2 using 1:(($2)**2+($3)**2) axes x1y1 \
                with lines ls 1 t '$\hat{\psi}^+$' 
# ---------------------- PLOT PHASE -------------------------
angle(diff) = (2*pi - diff < diff ? 2*pi - diff : diff)
abs_diff(y1,x1, y2,x2) = abs(atan2(y1,x1) - atan2(y2,x2))

set xrange [P0 - 3 : P0 + 3]
set ylabel '$|Arg(\hat{\psi}^{+}_{guess}) - Arg(\hat{\psi}^+)  |$'

plot FILENAME using 1:(atan2($5,$4)) with lines lw 3 \
        t '$\hat{\psi}^+_{\text{guess}}$', \
    FILENAME using 1:(atan2($3,$2)) with lines lw 3 \
        t '$\hat{\psi}^+$'
#plot FILENAME using 1:(angle(abs_diff($3,$2, $5, $4))) \
 #       with lines lw 1 t ''

unset multiplot
set output
unset terminal
