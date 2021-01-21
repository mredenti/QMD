fbuild(delta, qc, eps, p) = sprintf("delta%.3fqc%.3feps%.3fp%d",delta, qc, eps, p)
fout = '~/qmd/src/wip_flatevls/data/flatphases1diff.tex'

set terminal cairolatex pdf size 5,3
load 'settings.p'


#plot for [i=1:1000] 'data'.i.'.txt' using 1:2 title 'Flow '.i

# ------------ PARAMETERS ----------------
array DELTA[3] = [0.1, 0.5, 2]
array QC[74]  #what is the size of the transition for each q_c 
do for [i=1:74] { 
  QC[i] = 0.01 + 0.04*(i - 1)
}
array EPS[3] = [0.1, 0.05, 0.02]
array P0[3] = [3, 4, 5]
    

set ytics
set xtics
set xlabel '$\delta$'
set ylabel '$\Phi(\hat{\psi}^+(\bar{p}), \hat{\psi}^+_{BOA}(\bar{p})$'
set key 
set title sprintf('$p_0=%d, \epsilon=%.3f$', P0[1], EPS[2])

getValue(row,col,filename) = system('awk ''{if (NR == '.row.') print $'.col.'}'' '.filename.'')

array MEAN_PHASE[74]
array MEAN_PHASE2[74]
array MEAN_PHASE3[74]
do for [j=1:74] {
    fname = 'flat'.fbuild(DELTA[1], QC[j], EPS[2], P0[1]).'.txt' 
    stats fname\
        using 10 every ::1::1 prefix 'pmin' noout
    stats fname \
        using 10 every ::2::2 prefix 'pmax' noout
    dp = abs(pmin_min - pmax_max)
    print(j)
    row = int((P0[1] - pmin_min)/dp) 
    MEAN_PHASE[j] = phase_diff(getValue(row, 11, fname), \
                               getValue(row, 12, fname), \
                              getValue(row, 15, fname), \
                             getValue(row, 16, fname))
}

do for [j=1:74] {
    fname = 'flat'.fbuild(DELTA[2], QC[j], EPS[2], P0[1]).'.txt' 
    stats fname\
        using 10 every ::1::1 prefix 'pmin' noout
    stats fname \
        using 10 every ::2::2 prefix 'pmax' noout
    dp = abs(pmin_min - pmax_max)
    row = int((P0[1] - pmin_min)/dp) 
    MEAN_PHASE2[j] = phase_diff(getValue(row, 11, fname), \
                               getValue(row, 12, fname), \
                              getValue(row, 15, fname), \
                             getValue(row, 16, fname))
}
do for [j=1:74] {
    fname = 'flat'.fbuild(DELTA[3], QC[j], EPS[2], P0[1]).'.txt' 
    stats fname\
        using 10 every ::1::1 prefix 'pmin' noout
    stats fname \
        using 10 every ::2::2 prefix 'pmax' noout
    dp = abs(pmin_min - pmax_max)
    row = int((P0[1] - pmin_min)/dp) 
    MEAN_PHASE3[j] = phase_diff(getValue(row, 11, fname), \
                               getValue(row, 12, fname), \
                              getValue(row, 15, fname), \
                             getValue(row, 16, fname))
}


plot DELTA u (QC[$1]):(MEAN_PHASE[$1]) w lp ls 1 t '$\delta=$'.str(DELTA[1]), \
    DELTA u (QC[$1]):(MEAN_PHASE2[$1]) w lp ls 2 t '$\delta=$'.str(DELTA[2]), \
    DELTA u (QC[$1]):(MEAN_PHASE3[$1]) w lp ls 3 t '$\delta=$'.str(DELTA[3]) 
#plot sample [i=1:4] '+' using (DELTA[i]):(MEAN_PHASE3[i]) \
 #   w lp ls 4 t '$q_c=$'.str(QC[3]) 

set output 
unset terminal
