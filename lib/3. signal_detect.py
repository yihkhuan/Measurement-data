from .spike import SpectrumAnalyzer
import numpy as np
from magpylib import pyplot as plt
import esr

GHZ_UNIT = 1e9
MHZ_UNIT = 1e6
sa = SpectrumAnalyzer()

resonance_freq = 9.7 * GHZ_UNIT #insert resonance freq of resonator
span = 50 * MHZ_UNIT
sa.setup(resonance_freq, span, -10.0)

sa.tg_sweep_points(1000)

not_0DB = True #Change after first time storing
results = np.array([])
i = 0
while i < 20:
    if not_0DB:
        sa.stor_thru()
        sa.level(0.5)
        not_0DB = False
    elif results.size == 0:
        results = np.append(results, sa.scan())
    else:
        results = np.vstack(results, sa.scan())
    
    i = i + 1

spectrum = np.average(results, axis=0)
freq = sa.fetch_xarray()

name = 0.00 # enter current / mag field value
plt.figure()
plt.plot(freq / GHZ_UNIT, spectrum)
plt.savefig(f"./figs/Signal_detection/{name}mT.png")
plt.close()

output = np.vstack(spectrum, freq)
np.savetxt("./figs/Resonator_calibration/resonator_data.csv", output.transpose, delimiter= ",")

