import numpy as np
import json
import spike as sp

magnet = ' double-magnet '
with open("./Analyse_data/fitted.json","r") as g:
    resonator = json.load(g)

resonator_freq = resonator["fitted_data"][0].get('a')[0]

print(sp.mag_current((resonator_freq)/ sp.EXPECTED_GRADIENT, magnet))
output = (sp.mag_current((resonator_freq - 50 * 1e-3)/ (sp.EXPECTED_GRADIENT), magnet), sp.mag_current((resonator_freq + 50 * 1e-3)/ (sp.EXPECTED_GRADIENT), magnet))

print(output)
print((50 * 1e-3)/ (sp.EXPECTED_GRADIENT * 20)) #0.089 A away from centre