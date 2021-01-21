fbuild(delta, qc, eps, p) = sprintf("delta%.3fqc%.3feps%.3fp%d",delta, qc, eps, p)
fout = '~/qmd/src/wip_flatevls/data/formula.tex'

set terminal cairolatex pdf size 5,4
load 'settings.p'


DELTA = 0.5
P0 = 3
EPS = 0.1
QC = 0.1
YLBL = '$|\hat{\psi}^-(\infty)|^2$'
XLBL = '$p$'

set ylabel YLBL
set xrange [P0 - 0.5: P0 + 1]
set format x ''
set multiplot layout 2,1

plot \
    'flat'.fbuild(DELTA, QC, EPS, P0).'.txt' \
    using 10:($13**2 + $14**2) \
    with lines t 'exact', \
    'flat'.fbuild(DELTA, QC, EPS, P0).'.txt' \
    using 10:($17**2 + $18**2) \
    with lines t 'formula'
    
set ylabel '$|Arg(\hat{\psi}^-) - Arg(\hat{\psi}^-_{BOA})|$'
set xlabel XLBL
set tmargin 0
set format x '%.1t'

plot \
    'flat'.fbuild(DELTA, QC, EPS, P0).'.txt' \
    using 10:(phase_diff($13,$14, $17, $18)) \
    with lines t ''

unset multiplot
set output 
unset terminal

