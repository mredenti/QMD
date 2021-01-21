fout = '~/qmd/src/wip_flatevls/data/transitionestimate.tex'

set terminal cairolatex pdf size 4,5
load 'settings.p'

array delta[3] = [0.05, 0.5, 2] 
f(x, p, e, d) = exp(- x/e * 2*d/p)

set xrange [0:3]
set ylabel 'Mass - $\approx$ transition rate'
set xlabel '$q_c$'

plot for [i=1:3] f(x, 3, 0.05, delta[i]) t '$\delta=$'.sprintf('%.3f', delta[i])


set output 
unset terminal

