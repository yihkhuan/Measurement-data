import numpy as np
import json
import spike as sp

magnet = ' 3mm '
with open("./Analyse_data/fitted.json","r") as g:
    resonator = json.load(g)

resonator_freq = resonator["fitted_data"][0].get('a')[0]

print((resonator_freq * 1e-3)/ sp.EXPECTED_GRADIENT)
output = (sp.mag_current((resonator_freq - 50 * 1e-3)/ (sp.EXPECTED_GRADIENT), magnet), sp.mag_current((resonator_freq + 50 * 1e-3)/ (sp.EXPECTED_GRADIENT), magnet))

print(output)