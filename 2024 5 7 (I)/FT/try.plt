set datafile separator ','
set terminal png


l(x) = Al / pi * (b / ((x - a)**2 + b**2)) - offsetl
a = 9.785
b = .006
Al = 0.001
offsetl = -0.01
set output './try.png'

plot '3.65A.csv' using 1:2 t 'NA data', l(x) t 'Lorentzian'