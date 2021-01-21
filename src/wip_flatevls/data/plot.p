fbuild(delta, qc, eps, p) = sprintf("delta%.3fqc%.3feps%.3fp%d",delta, qc, eps, p)
fout = '~/qmd/src/wip_flatevls/data/flatphasesdiff.tex'

set terminal cairolatex pdf size 5,6
load 'settings.p'


#plot for [i=1:1000] 'data'.i.'.txt' using 1:2 title 'Flow '.i

# ------------ PARAMETERS ----------------
array DELTA[4] = [0.05, 0.1, 0.2, 0.5]
array QC[3] = [0.01, 0.05, 0.1] #what is the size of the transition for each q_c 
array EPS[3] = [0.1, 0.05, 0.02]
array P0[3] = [3, 4, 5]
    
#set title sprintf("group %s", idx)

set multiplot layout 3,3 rowsfirst \
    title '\n$\epsilon=0.1, q_c = [0.01, 0.05, 0.1] \downarrow \n$' font ",10" 
unset xlabel
set format x ''
set key

set lmargin 6; set rmargin 0; set bmargin -0.5; set tmargin 1
do for [k=1:3] {
    set yrange [- 0.2 : pi]
    set ylabel '$\Phi(\hat{\psi}^+, \hat{\psi}^+_{BOA})$'
    set ytics
    do for [i=1:3] {
        set xrange [P0[i] - 1.5:P0[i] + 1.5];
        #set lmargin 6; set rmargin 1; set bmargin -1; set tmargin 1
        if (k == 3) {set xlabel '$p$'; set format x '%.1t'; set xtics rotate by 45 right; set bmargin -0.5} 
        if (i == 1) {set format y '%.1t'} 
        plot \
        fr [j=1:4] 'flat'.fbuild(DELTA[j], QC[k], EPS[1], P0[i]).'.txt' \
        using 10:(phase_diff($11,$12,$15,$16)) \
        with lines t '$\delta=$'.str(DELTA[j])
        unset key
        set format y ''
        unset ylabel
    }
}

unset multiplot
set output 
unset terminal
