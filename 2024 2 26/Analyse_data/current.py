import json
import numpy as np


f = open('fitted.json')
fitted_data = json.load(f)
# g = open('fitted_current.json')
# fitted_current = json.load(g)
GHz = 1e9
mT = 1e-3

# m = fitted_current['big_magnet'].get('m')
# c = fitted_current['big_magnet'].get('c')

for x in fitted_data['fitted_data']:
    resonance_freq = x.get('a')[0] #GHz
    resonance_mag = resonance_freq * GHz * 3.57e-11 #T
    # I = (resonance_mag - c)/m
    

    