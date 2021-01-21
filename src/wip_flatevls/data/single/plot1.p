fbuild(delta, c, alpha, eps, p) = sprintf("delta%.3fc%.3falpha%.3feps%.3fp%d",delta, c, alpha, eps, p)
fout = '~/qmd/src/wip_flatevls/data/single/l2.tex'

set terminal cairolatex pdf size 6,4
load '../settings.p'


#plot for [i=1:1000] 'data'.i.'.txt' using 1:2 title 'Flow '.i

# ------------ PARAMETERS ----------------
DELTA = 0.5
ALPHA =  pi/2 #what is the size of the transition for each q_c 
C = -pi/3
qc = pi/2/ALPHA
gamma = -C/2/ALPHA
array EPS[4] = [1./10, 1./20, 1./30, 1./40]
array P0[2] = [2,5]
array ASCI[4] = [1,2,3,4]

getValue(col1, col2,filename) = system('awk ''NR > 1 {sum+=(($'.col1.')**2 + ($'.col2.')**2)} END {print sum}'' '.filename.'')
getValue2(col1, col2, col3, col4, filename) = system('awk ''NR > 1 {sum+=(($'.col1.' - $'.col3.')**2 + ($'.col2.' - $'.col4.')**2)} END {print sum}'' '.filename.'')

l2norm(col1, col2) = getValue(col1, col2, FILENAME)
l2relnorm(col1, col2, col3, col4, dp) =getValue2(col1, col2, col3, col4, FILENAME) * dp / (getValue(col3,col4,FILENAME)*dp) 



TITLE = sprintf('\n$q_c=%.2f, \gamma=%.2f, \delta=%.2f \n$', qc, gamma, DELTA) 

set multiplot layout 1,2 rowsfirst \
    title TITLE font ",10" 

set format y '%.2e'
set key
set lmargin 6; set rmargin 6; set bmargin -2; set tmargin 2

set xtics
set xlabel '$\epsilon$'
set xtics ("1/10" 0.1, "1/20" 0.2, "1/30" 0.3, "1/40" 0.4)
array L2ERR[4]
do for [ix=1:4] {
    FILENAME = 'flat'.fbuild(DELTA, C, ALPHA, EPS[ix], P0[1]).'.txt'
    stats FILENAME\
        using 12 every ::1::1 prefix 'pmin' noout
    stats FILENAME \
        using 12 every ::2::2 prefix 'pmax' noout
    dp = abs(pmin_min - pmax_max)
    L2ERR[ix] = l2relnorm(21,22, 15, 16, dp)
}
plot EPS using (ASCI[$1]):(L2ERR[$1]) lw 8 t 'P0='.P0[1] 

do for [ix=1:4] {
    FILENAME = 'flat'.fbuild(DELTA, C, ALPHA, EPS[ix], P0[2]).'.txt'
    stats FILENAME\
        using 12 every ::1::1 prefix 'pmin' noout
    stats FILENAME \
        using 12 every ::2::2 prefix 'pmax' noout
    dp = abs(pmin_min - pmax_max)
    L2ERR[ix] = l2relnorm(21,22, 15, 16, dp)
}
do for [i=1:4]{
    print(L2ERR[i])
}
plot EPS u (ASCI[$1]):(L2ERR[$1]) lw 8 t 'P0='.P0[2] 



unset multiplot
set output 
unset terminal
