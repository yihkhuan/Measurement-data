#setup
set datafile separator ','
set term qt font "Times-New-Roman,12"
filename = '2024_4_28_FT.csv'
set fit nolog
set fit quiet


##lorentzian function
l(x) = amplitude / pi * (linewidth / ((x - resonanceFreq)**2 + linewidth**2))
resonanceFreq = 9625
linewidth = .011
amplitude = 0.09


#fitting range
dw = 35
x_leftWidth = NaN
xmax = NaN
x_rightWidth = NaN


#functions
setOut(name) = sprintf("set output './figs/%s.png';", name)

plotFormat = sprintf("set xtics nomirror;") . \
sprintf("set x2tics;") . \
sprintf("set autoscale xfix;") . \
sprintf("set autoscale x2fix;") . \
sprintf("set title 'Fitting of data' font 'Times-New-Roman,22';") . \
sprintf("set xlabel 'Signal frequency, GHz' font 'Times-New-Roman,18';") . \
sprintf("set ylabel 'Absorption, dB' font 'Times-New-Roman,18';") . \
sprintf("set label;") . \
sprintf("set tics font ',12';") . \
sprintf("set key font 'Times-New-Roman,14';") . \
sprintf("set terminal png size 600,600;")

fit_output(name) = sprintf("print '\"%s\" : {';", name) . \
sprintf("print '\"resonance-frequency\" : ', resonanceFreq,',';") . \
sprintf("print '\"bandwidth\" : ', linewidth,',';") . \
sprintf("print '\"amplitude\" : ', amplitude;") . \
sprintf("print '},';")


#misc variables
magneticField = NaN



set print './fitting_params.json'
print '{'

do for [datablock = 1 : 9] {
    reset
    eval setOut("testing")
    # plot filename i datablock u 0:2
    plot filename i datablock u ($0 == 1 ? magneticField = $2 : NaN):1 

    stats filename i datablock u 1:3 nooutput
    plot filename i datablock u ($0 == STATS_index_max_y - dw +1 ? x_leftWidth = $1 : NaN):1 
    plot filename i datablock u ($0 == STATS_index_max_y + 1 ? resonanceFreq = $1*1e-9 : NaN):1
    plot filename i datablock u ($0 == STATS_index_max_y + dw +1 ? x_rightWidth = $1 : NaN):1
    linewidth = .034
    amplitude = 0.015
    #i index starts from zero
    #x-column is column 1
    #y-column is column 2
    fit [x_leftWidth*1e-9 : x_rightWidth*1e-9] l(x) filename i datablock u ($1*1e-9):3 via resonanceFreq, linewidth, amplitude
    
    eval fit_output(sprintf("%.4f", magneticField))
    eval setOut(sprintf("%.4f", magneticField))
    eval plotFormat
    set xrange [x_leftWidth*1e-9 : x_rightWidth*1e-9]
    plot filename i datablock u ($1*1e-9):3 t "data", l(x) t "fitting"

}

print '}'
set print
