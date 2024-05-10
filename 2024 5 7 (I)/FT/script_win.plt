set term qt font "Times-New-Roman,12"
set datafile separator ','
#CD into the right file before using this script
#cd '../Resonator data/'


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
getValue(row,col,filename) = system('awk -F"," "{if (NR == '.row.') print $'.col.'}" '.filename.'')

#selecting the window
dw = 6
array A[3]
get_Values(name) = sprintf("A[3] = getValue(STATS_index_max_y - dw + 1,1, '%s.csv');",name) . \
sprintf("A[1] = getValue(STATS_index_max_y + dw + 1,1, '%s.csv');",name) . \
sprintf("A[2] = getValue(STATS_index_max_y + 1 ,1, '%s.csv');",name)

#Fitting the curve

l(x) = Al / pi * (b / ((x - a)**2 + b**2)) - offsetl
a = 9.785
b = .002
Al = 0.0005
offsetl = -0.1

lfit(name) = sprintf("fit [A[3] : A[1]] l(x) '%s.csv' u 1:2 via a, b, offsetl, Al;",name)

#plot the window showing the peak
#set terminal png size 1000,1000
setting = sprintf("set x2tics;") . sprintf("set xtics nomirror;")
printing(name) = sprintf("set xrange [A[3] : A[1]];") . \
sprintf("set terminal png size 600,600;") . \
sprintf("plot '%s.csv' using 1:2 t 'NA data', l(x) t 'Lorentzian';",name,name)

#output the fitted values to a file
fit_output(name) = sprintf("print '{';") . \
sprintf("print '\"name\" : \"%s\",';", name) . \
sprintf("print '\"resonance-frequency\" : ', a, ',' ;") . \
sprintf("print '\"bandwidth\" : ', b, ',';") . \
sprintf("print '\"amplitude\" : ', Al, ',';") . \
sprintf("print '\"offset\": ', offsetl;") . \
sprintf("print '},';")

array name[7]
name [1] = '3.65A'
name [2] = '3.67A'
name [3] = "3.67A"
name [4] = "3.68A"
name [5] = "3.69A"
name [6] = "3.70A"
name [7] = "3.71A"


ff(name) = sprintf("stats '%s.csv' nooutput;",name)
set print './Analyse_data/fitted.json'
print '{'

do for [i = 1:7] {
print '"', name [i], '": '
reset
set datafile separator ','

eval init(name [i])

eval get_Values(name [i])

a = A [2] + 0

eval lfit(name [i])


eval fit_output(name [i])
eval always
eval printing(name [i])
}

print ']'
print '}'
set print












