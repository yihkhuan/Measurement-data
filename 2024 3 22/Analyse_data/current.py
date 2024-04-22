import json
import numpy as np

f = open('fitted.json')
fitted_data = json.load(f)
g = open('fitted_current.json')
fitted_current = json.load(g)
GHz = 1e9
mT = 1e-3

m = fitted_current['electromagnet+NdFeB-small'].get('m')[0]
c = fitted_current['electromagnet+NdFeB-small'].get('c')[0]

for x in fitted_data['fitted_data']:
    resonance_freq = x.get('a')[0] #GHz
    resonance_mag = resonance_freq * GHz * 3.57e-11 #T
    print(resonance_mag / mT)
    I = (resonance_mag / mT - c)/m
    print(I)
    

    