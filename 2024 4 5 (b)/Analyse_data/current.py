import json
import numpy as np

f = open('fitted.json')
fitted_data = json.load(f)
g = open('fitted_current.json')
fitted_current = json.load(g)
GHz = 1e9
mT = 1e-3

m = fitted_current[' small-magnet '].get('m')[0]
c = fitted_current[' small-magnet '].get('c')[0]

for x in fitted_data['fitted_data']:
    resonance_freq = x.get("a")[0]
    print(resonance_freq)
    # resonance_freq = 9.46
    resonance_mag = resonance_freq * GHz * 3.57e-11 #T
    print(resonance_mag)
    # print(resonance_freq)
    I = (resonance_mag / mT - c)/m
    print(I)
    # I = 5.24
    # print('B')
    # print(m * I + c)
    # print(.328 / 3.57e-11 / GHz)
    

    