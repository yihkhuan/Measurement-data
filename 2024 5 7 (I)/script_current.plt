set term qt font "Times-New-Roman,12"
#CD into the right file before using this script
#cd '../Resonator data/'
set datafile separator ','

#obtain the index of the only peak in the data set
init(name) = sprintf("set fit logfile './Analyse_data/fit_%s.log';",name) . \
sprintf("set output './Analyse_data/figs/current.png';")

always = sprintf("set xtics nomirror;") . \
sprintf("set autoscale xfix;") . \
sprintf("set title 'Current vs magnetic field' font 'Times-New-Roman,22';") . \
sprintf("set xlabel 'Total current, A' font 'Times-New-Roman,18';") . \
sprintf("set ylabel 'Magnetic field, mT' font 'Times-New-Roman,18';") . \
sprintf("set label;") . \
sprintf("set tics font ',12';") . \
sprintf("set key font 'Times-New-Roman,14';")
#print  STATS_index_max_y



#Fitting the curve
y(x) = m * x + c
m = 1
c = 50

linearfit(name) = sprintf("fit y(x) '%s.txt' u 1:2 via m,c;",name)


#plot the window showing the peak
#set terminal png size 1000,1000
setting = sprintf("set x2tics;") . sprintf("set xtics nomirror;")
printing(name) = sprintf("set terminal png size 600,600;") . \
sprintf("plot '%s.txt' using 1:2 t '%s';",name,name)

reprinting(name) = sprintf("replot '%s.txt' using 1:2 t '%s';",name,name)

#output the fitted values to a file
fit_output(name) = sprintf("print '{';") . \
sprintf("print '\"m\" : [', m,',', m_err, '],';") . \
sprintf("print '\"c\" : [', c,',', c_err, ']';") . \
sprintf("print '},';")

array name[5]
name [1] = "0mm"
#name [2] = "small-magnet"
#name [3] = "electromagnet+NdFeB-small"

ff(name) = sprintf("stats '%s.txt' nooutput;",name)

set print './Analyse_data/current.json'
print '{'
print '"',name [1],'"', ' :'

array g[3]
array h[3]

reset
eval init(name [1])
eval linearfit(name [1])
eval fit_output(name [1])
eval always
eval printing(name [1])
g[1] = m
h[1] = c
y1(x) = g[1] * x + h[1]
set output './Analyse_data/figs/current.png'
replot y1(x) t ""

# print '"',name [2],'"', ' :'
# reset
# eval init(name [2])
# eval linearfit(name [2])
# eval fit_output(name [2])
# eval always
# eval reprinting(name [2])
# g[2] = m
# h[2] = c
# y2(x) = g[2] * x + h[2]
# set output './Analyse_data/figs/current.png'
# replot y2(x) t ""

print '}'
set print








