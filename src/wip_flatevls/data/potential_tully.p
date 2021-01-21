fout = '~/qmd/src/wip_flatevls/data/potential_tully.tex'

set terminal cairolatex pdf size 6,3
load 'settings.p'

array b[3] = [0.8, 1.5] 
a = 1
c = 0.05
d = 1

Z(x, a, b) = a * abs(x) / x * (1 - exp(-b * abs(x)))
X(x, c, d) =  c * exp(-d*x**2)
Z_prime(x,a,b) = a*b*exp(-b*abs(x))
X_prime(x, c, d) = - d * 2 * x * X(x, c, d)

f(x, a, b, c, d) = sqrt(Z(x, a, b)**2 + X(x, c, d)**2)

theta_prime(x,a,b,c,d) = (X_prime(x, c, d) * Z(x,a,b) \
                            - X(x,c,d)*Z_prime(x,a,b)) \
                            / (Z(x,a,b)**2 + X(x,c,d)**2)

set xrange [-10:10]
set xlabel '$x$'
set ylabel '$\rho(x)$'

set multiplot layout 1,2 title '\n$a=1, c=0.05, d=1$\n'

set key right center
plot for [i=1:2] f(x, a, b[i], c, d) t '$b=$'.str(b[i]) lw 4

set rmargin 0.3
unset key
set ylabel '$\theta^\prime(x)$'
plot for [i=1:2] theta_prime(x, a, b[i], c, d) t '$b=$'.inttostr(b[i]) lw 4


unset multiplot
set output 
unset terminal

