fbuild(delta, c, alpha, eps, p, n) = sprintf("delta%.3fc%.3falpha%.3feps%.3fp%d%.3fn",delta, c, alpha, eps, p, n)
fout = '~/qmd/src/wip_flatevls/data/single/flatn1.tex'

set terminal cairolatex pdf size 5.5,7
load '../settings.p'


#plot for [i=1:1000] 'data'.i.'.txt' using 1:2 title 'Flow '.i

# ------------ PARAMETERS ----------------
DELTA = 0.5
ALPHA =  pi #what is the size of the transition for each q_c 
C = -pi
EPS = 1./10
P0 = 5
T = 20/P0
n = 1

PHASE_DIFF_LBL = '$\Phi(\phi, \psi)$'
ABS_DIFF_LBL = '$|\phi|^2 - |\psi|^2$'

i = {0.0, 1.0}

FILENAME = 'flat'.fbuild(DELTA, C, ALPHA, EPS, P0, n).'.txt'

qc = pi/2/ALPHA
gamma = -C/2/ALPHA

stats FILENAME\
    using 12 every ::1::1 prefix 'pmin' noout
stats FILENAME \
    using 12 every ::2::2 prefix 'pmax' noout
dp = abs(pmin_min - pmax_max)
getValue(col1, col2,filename) = system('awk ''NR > 1 {sum+=(($'.col1.')**2 + ($'.col2.')**2)} END {print sum}'' '.filename.'')
getValue2(col1, col2, col3, col4, filename) = system('awk ''NR > 1 {sum+=(($'.col1.' - $'.col3.')**2 + ($'.col2.' - $'.col4.')**2)} END {print sum}'' '.filename.'')


l2norm(col1, col2) = sprintf('%.4f', getValue(col1, col2, FILENAME) * dp) 
l2relnorm(col1, col2, col3, col4) =sprintf('%.4f', getValue2(col1, col2, col3, col4, FILENAME) * dp / (getValue(col3,col4,FILENAME)*dp)) 

TITLE = sprintf('\n$\epsilon=%.3f, q_c=%.2f, \gamma=%.2f , p_0=%d , \delta=%.2f \n$', EPS, qc, gamma, P0, DELTA) 

set multiplot layout 3,2 rowsfirst \
    title TITLE font ",10" 

unset xlabel
set format x ''
set format y '%.1e'
set key
set lmargin 12; set rmargin 1; set bmargin 0; set tmargin 3

array cols[2] = [17, 19] 
array lbls[2] = ['BOA$+$', 'Formula+']

do for [row=1:3] {
    #set yrange [- 0.2 : pi]
    #set ylabel '$\Phi(\hat{\psi}^+, \hat{\psi}^+_{BOA})$' # make a list of labels
    #set ytics
    if (row==3){set bmargin -2}
    do for [col=1:2] {
        if (col == 1){set ylabel ABS_DIFF_LBL}
        if (col == 2){set ylabel PHASE_DIFF_LBL}
        set title ''
        set xrange [P0-2.5:P0 + 2.5];
        if (row == 3) {set xlabel '$p$'; set format x '%.1f'; set xtics rotate by 45 right;} 
        if (row == 1 & col ==1) {
        set title '$||\hat{\psi}^+||_{L^2}$='.l2norm(13,14)
        plot FILENAME using 12:(($17**2 + $18**2) - ($13**2 + $14**2)) with lines t lbls[1]}
        
        if (row == 1 & col ==2) {
        set title '$||\hat{\psi}_{\text{BOA}} - \hat{\psi}^+||_{L^2rel}=$'.l2relnorm(13,14,17,18);
        plot FILENAME using 12:(phase_diff($13,$14,$17,$18)) with lines t lbls[1]}
        
        if (row == 2 & col ==1) {set format y '%.1e'; 
        set title '$||\hat{\psi}^+_{\text{form}}||_{L^2}$='.l2norm(19,20) 
        plot for [i=1:2] FILENAME\
        using 12:(((column(cols[i]))**2 + (column(cols[i]+1))**2) - ($13**2 + $14**2)) with lines t lbls[i]}
        
        if (row == 2 & col ==2) {
            set title '$||\hat{\psi}^+_{\text{form}} - \hat{\psi}^+||_{L^2rel}=$'.l2relnorm(13,14,19,20);
        plot for [j=1:2] FILENAME \
        using 12:(phase_diff($13,$14,column(cols[j]),column(cols[j]+1))) with lines t lbls[j]}
        
        if (row == 3 & col ==1) {
            set title '$||\hat{\psi}^-_{\text{form}}||_{L^2}=$'.l2norm(21,22)
            plot FILENAME using 12:(($21**2 + $22**2) -($15**2 + $16**2) ) with lines t 'Formula-'}
        if (row == 3 & col ==2) {
        set title '$||\hat{\psi}^-_{\text{form}} - \hat{\psi}^-||_{L^2rel}=$'.l2relnorm(21, 22, 15, 16);
        plot FILENAME using 12:(phase_diff($15,$16,$21,$22)) with lines t 'Formula-'}
        unset ylabel
    }
}

unset multiplot
set output 
unset terminal
