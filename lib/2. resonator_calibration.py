from .spike import SpectrumAnalyzer
import numpy as np
from magpylib import pyplot as plt
import esr

GHZ_UNIT = 1e9
MHZ_UNIT = 1e6
sa = SpectrumAnalyzer()

sa.setup(6.0 * GHZ_UNIT, 5.0 * GHZ_UNIT, -10.0)

sa.tg_sweep_points(1000)

spectrum = sa.scan()
freq = sa.fetch_xarray()

index = np.where(freq == np.freq.max())[0][0]

spectrum = sa.scan((freq[index, 50 * MHZ_UNIT]))
freq = sa.fetch_xarray()

esr.curve_fit(esr.lorentz, freq, spectrum, ())

plt.figure()
plt.plot(freq / GHZ_UNIT, spectrum)
plt.savefig("./figs/Resonator_calibration/resonator_calibration.png")
plt.close()

output = np.vstack(spectrum, freq)
np.savetxt("./figs/Resonator_calibration/resonator_data.csv", output.transpose, delimiter= ",")
