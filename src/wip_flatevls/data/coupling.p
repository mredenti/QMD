fout = '~/qmd/src/wip_flatevls/data/coupling.tex'

set terminal cairolatex pdf size 5,3
load 'settings.p'

array QC[3] = [0.01, 0.05, 0.1] #what is the size of the transition for each q_c 

f(x, qc) = qc**2 / (qc**2 + x**2) 

set xrange [-5:5]
set xlabel '$x$'
set ylabel '$\theta^\prime(x)$'
plot for [i=1:3] f(x, QC[i]) t '$q_c=$'.str(QC[i]) lw 4

set output 
unset terminal

