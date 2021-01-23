angle(diff) = (2*pi - diff < diff ? 2*pi - diff : diff)
phase_diff(x_real,x_imag, y_real,y_imag) = angle(abs(atan2(x_imag,x_real) - atan2(y_imag,y_real)))
#mean_phase(p0, x_real, x_imag, pgrid) = 
str(a) = sprintf('%.3f', a)
inttostr(a) = sprintf('%d', a)

set output fout

# linestyles
set style line 1 lt 1 lc rgb "#A00000" lw 1 pt 5 ps 0.5
set style line 2 lt 1 lc rgb "#00A000" lw 1 pt 6 ps 0.5
set style line 3 lt 1 lc rgb "#000004" lw 1 pt 7 ps 0.5 
set style line 4 lt 1 lc rgb "#0000A0" lw 1 pt 4 ps 1.5
set style line 5 lt 1 lc rgb "#D0D000" lw 6 pt 7 ps 1.5
set style line 6 lt 1 lc rgb "#00D0D0" lw 6 pt 7 ps 1.5
set style line 7 lt 1 lc rgb "#B200B2" lw 6 pt 7 ps 1.5
set style line 12 lc rgb '#808080' lt 0 lw 1
set style line 11 lc rgb '#808080' lt 1

# legend
set key spacing 1.5

# Draw the grid lines for both the major and minor tics
set grid back ls 12
set grid xtics
set grid ytics

# nomirror means do not put tics on the opposite side of the plot
set xtics nomirror
set ytics nomirror

set border 3 back ls 11
