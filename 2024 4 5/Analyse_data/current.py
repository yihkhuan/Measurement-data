import json
import numpy as np

# f = open('fitted.json')
# fitted_data = json.load(f)
g = open('current.json')
fitted_current = json.load(g)
GHz = 1e9
mT = 1e-3

m = fitted_current[' big-magnet '].get('m')[0]
c = fitted_current[' big-magnet '].get('c')[0]


resonance_freq = 9.46
resonance_mag = resonance_freq * GHz * 3.57e-11 #T
print(resonance_mag)
I = (resonance_mag / mT - c)/m
print(I)
print(I/2)

    