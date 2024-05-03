set term qt font "Times-New-Roman,12"
#CD into the right file before using this script
#cd '../Resonator data/'
set datafile separator ','

#obtain the index of the only peak in the data set
init(name) = sprintf("stats '%s.csv' nooutput;", name) . \
sprintf("set fit logfile './Analyse_data/fit_%s.log';",name) . \
sprintf("set output './Analyse_data/figs/%s.png';",name)

always = sprintf("set xtics nomirror;") . \
sprintf("set x2tics;") . \
sprintf("set autoscale xfix;") . \
sprintf("set autoscale x2fix;") . \
sprintf("set title 'Fitting of U resonator' font 'Times-New-Roman,22';") . \
sprintf("set xlabel 'Signal frequency, GHz' font 'Times-New-Roman,18';") . \
sprintf("set ylabel 'Attenuation, dB' font 'Times-New-Roman,18';") . \
sprintf("set x2label 'Magnetic field, T' font 'Times-New-Roman,18';") . \
sprintf("set label;") . \
sprintf("set tics font ',12';") . \
sprintf("set key font 'Times-New-Roman,14';")
#print  STATS_index_max_y

#obtain the corresponding frequency depending on the index obtained
getValue(row,col,filename) = system('awk "{if (NR == '.row.') print $'.col.'}" '.filename.'')

#selecting the window
dw = 15
array A[3]
get_Values(name) = sprintf("A[3] = getValue(STATS_index_max_y - dw + 1,1, '%s.csv') * 1e-9;",name) . \
sprintf("A[1] = getValue(STATS_index_max_y + dw + 1,1, '%s.csv') * 1e-9;",name) . \
sprintf("A[2] = getValue(STATS_index_max_y + 1 ,1, '%s.csv') * 1e-9;",name)

#Fitting the curve

l(x) = Al / pi * (b / ((x - a)**2 + b**2)) - offsetl
a = 10
b = .5
Al = 35
offsetl = 40
g(x) = Ag / (d * (2 * pi)**(1/2)) * exp(-0.5 * ((x-c) / d)**2) - offsetg
c = 10
d = 2
Ag = 35
offsetg = 40
e1(x) = h1 * exp(i1 * (x - j1)) - offset1
h1 = 35
i1 = .5
j1 = 10
offset1 = 40
e2(x) = h2 * exp(i2 * (-x + j2)) - offset2
h2 = 35
i2 = .5
j2 = 10
offset2 = 40


lfit(name) = sprintf("fit [A[3] : A[1]] l(x) '%s.csv' u ($1*1e-9):2 via a, b, offsetl, Al;",name)
gfit(name) = sprintf("fit [A[3] : A[1]] g(x) '%s.csv' u ($1*1e-9):2 via c, d, offsetg, Ag;",name)
efit1(name) = sprintf("fit [A[3] : A[2]] e1(x) '%s.csv' u ($1*1e-9):2 via h1, i1, j1, offset1;",name)
efit2(name) = sprintf("fit [A[2] : A[1]] e2(x) '%s.csv' u ($1*1e-9):2 via h2, i2, j2, offset2;",name)

#plot the window showing the peak
#set terminal png size 1000,1000
setting = sprintf("set x2tics;") . sprintf("set xtics nomirror;")
printing(name) = sprintf("set xrange [A[3] : A[1]];") . \
sprintf("set x2range [A[3] * 0.0357 : A[1] * 0.0357 ];") . \
sprintf("set terminal png size 600,600;") . \
sprintf("plot '%s.csv' using ($1*1e-9):2 t 'NA data', '%s.csv' using ($1*3.57e-11):(NaN) axes x2y1 t '', l(x) t 'Lorentzian';",name,name)

#output the fitted values to a file
fit_output(name) = sprintf("print '{';") . \
sprintf("print '\"name\" : \"%s\",';", name) . \
sprintf("print '\"a\" : [', a,',', a_err, '],';") . \
sprintf("print '\"b\" : [', b,',', b_err, '],';") . \
sprintf("print '\"Al\" : [', Al,',', Al_err, '],';") . \
sprintf("print '\"offsetl\" : [', offsetl,',', offsetl_err, ']';") . \
sprintf("print '},';")

array name[2]
name [1] = "UR-5"
#name [2] = "UR-6"


ff(name) = sprintf("stats '%s.csv' nooutput;",name)

set print './Analyse_data/fitted.json'
print '{'
print '"fitted_data" : ['
do for [i = 1:1] {
reset
eval init(name [i])
eval get_Values(name [i])
a = A [2]
c = A [2]
j1 = A [2]
j2 = A [2]
eval lfit(name [i])
eval fit_output(name [i])
eval always
eval printing(name [i])
}

print ']'
print '}'
set print










