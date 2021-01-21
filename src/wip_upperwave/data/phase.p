set terminal cairolatex pdf size 6,6

fname(delta,eps,p) = sprintf("delta%.3feps%.3fp%d",delta, eps, p)
str(n) = sprintf("%.3f",n)


#set style line 1 lt 1 lc rgb "#A00000" lw 3 pt 7 ps 1.5
#set style line 2 lt 1 lc rgb "#00A000" lw 3 pt 7 ps 1.5
#set style line 3 lt 1 lc rgb "#000004" lw 3 pt 7 ps 1.5


ALPHA = 0.5
EPS = 0.1
P0 = 5
array DELTAS[3] = [0.5,0.2,0.05]
OUTPATH = '~/Desktop/qmd/src/wip_upperwave/data/phase.tex'
set output OUTPATH 

TITLE = 'BOA Phase Error? ($\epsilon = 0.1$)'
set multiplot layout 2, 2 title TITLE font ",12"

# -------------- P0 = 3 ---------------
P0 = 3
set title '$\epsilon$='.str(EPS)
set key
set key spacing 2
set xrange [P0 - 2: P0 + 2]
set ylabel '$|Arg(\hat{\psi}^{+}_{BOA}) - Arg(\hat{\psi}^+)  |$'


angle(diff) = (2*pi - diff < diff ? 2*pi - diff : diff)
abs_diff(y1,x1, y2,x2) = abs(atan2(y1,x1) - atan2(y2,x2))



plot for [i=1:3] 'wave'.fname(DELTAS[i],EPS, P0).'.txt' \
    using 8:(angle(abs_diff($10,$9, $12, $11))) with lines lw 1 title '$\delta = $'.str(DELTAS[i]), \
    2*pi
# --- phase against phase ---
set title '$\delta$='.str(DELTAS[2])
set xrange [P0 - 1:P0+1]
set ylabel '$Arg(\hat{\psi})$'
FILENAME = 'wave'.fname(DELTAS[2],EPS, P0).'.txt'
plot FILENAME using 8:(atan2($10,$9)) with lines lw 1 t '$\hat{\psi}^+_{\text{BOA}}$', \
    FILENAME using 8:(atan2($12,$11)) with lines lw 1 t '$\hat{\psi}^+$'
# ----------------- P0 = 5 ----------------
unset title


set tmargin 0
P0 = 5
set xlabel '$p$'
set xrange [P0 - 2: P0 + 2]
plot for [i=1:3] 'wave'.fname(DELTAS[i],EPS, P0).'.txt' \
    using 8:(angle(abs_diff($10,$9, $12, $11))) with lines lw 1 title '$\delta = $'.str(DELTAS[i])
FILENAME ='wave'.fname(DELTAS[2],EPS, P0).'.txt' 
set xrange [P0 - 0.3:P0+0.3]
set ylabel '$Arg(\hat{\psi})$'
plot FILENAME using 8:(atan2($10,$9)) with lines lw 1 t '$\hat{\psi}^+_{\text{BOA}}$', \
    FILENAME using 8:(atan2($12,$11)) with lines lw 1 t '$\hat{\psi}^+$'




unset multiplot 
set output 
unset terminal


