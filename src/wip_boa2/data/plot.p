set terminal cairolatex pdf size 6,4


ALPHA = 0.5
DELTA = 0.05 
EPS = 0.1
P0 = 5

str(n) = sprintf("%.3f",n)
str2(n) = sprintf("%.8f",n)
fname(delta,eps,p) = sprintf("delta%.3feps%.3fp%d",delta, eps, p)

OUTPATH = '~/qmd/src/wip_boa2/data/order2'.fname(DELTA, EPS, P0).'.tex'
FILENAME = 'order2'.fname(DELTA, EPS, P0).'.txt' 

set output OUTPATH 

#TITLE = '$\delta=$'.str(DELTA).', $\epsilon$='.str(EPS).', $p_0$='.P0
XLBL  = '$p$'
YLBL  = '$$'

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
set xlabel '$p$'
set key top right


angle(diff) = (2*pi - diff < diff ? 2*pi - diff : diff)
abs_diff(y1,x1, y2,x2) = abs(atan2(y1,x1) - atan2(y2,x2))

set multiplot layout 1,2 title '$\delta = $'.str(DELTA)

set xrange [P0 - 3 : P0 + 3]
set ylabel '$|Arg(\hat{\psi}^{+}_{BOA}) - Arg(\hat{\psi}^+)  |$'
plot FILENAME using 6:(angle(abs_diff($8,$7, $10, $9))) \
        with lines lw 1 t '$\hat{\psi}^+_{\text{BOA2}}$', \
     FILENAME using 6:(angle(abs_diff($12,$11, $10, $9))) \
        with lines lw 1 t '$\hat{\psi}^+_{\text{BOA}}$', \
    

set ylabel '$Arg(\hat{\psi})$'
set xrange [P0 - 0.2 : P0 + 0.2]
plot FILENAME using 6:(atan2($8,$7)) with lines lw 1 t '$\hat{\psi}^+_{\text{BOA2}}$', \
    FILENAME using 6:(atan2($10,$9)) with lines lw 1 t '$\hat{\psi}^+$'

unset multiplot
set output

OUTPATH = '~/qmd/src/wip_boa2/data/theta.tex'

set output OUTPATH 
a = ALPHA
set xlabel '$x$'
set ylabel '$\theta^\prime(x)$'
f(x,d) = - d * a * (1 - tanh(x)**2)/(d**2 + a**2*tanh(x)**2)

plot [-10:10] f(x,0.5) t '$\delta$=0.5' lw 2, f(x, 0.2) t '$\delta$=0.2' lw 2, f(x, 0.05) t '$\delta$=0.05' lw 2 

set output
unset terminal

