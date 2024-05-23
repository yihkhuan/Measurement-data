from spike import SpectrumAnalyzer
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
from tqdm import tqdm
import esr
import datetime
GHZ_UNIT = 1e9
MHZ_UNIT = 1e6
sa = SpectrumAnalyzer()

sa.setup(9.616 * GHZ_UNIT, 100.0 * MHZ_UNIT, -10.0)

sa.tg_sweep_points(500)

freq = sa.fetch_xarray()



fig, ax = plt.subplots()
plt.ion()


# plt.plot(freq / GHZ_UNIT, spectrum)
# # plt.savefig("./figs/Noise_calibration/before_zero.png")
# plt.show()
# plt.close()
print(freq.shape, freq[0]/MHZ_UNIT, freq[-1]/MHZ_UNIT, (freq[1] - freq[0])/MHZ_UNIT)

sa.scan()
sa.stor_thru(1)

for i in tqdm(range(100)):
    spectrum = sa.scan()
sa.stor_thru(1)
sleep(5)

line1, = ax.plot(freq / 1e9, spectrum)
plt.title("S21 of DUT")
plt.xlabel("frequency, GHz")
plt.ylabel("absorbtion, dB")
not_0DB = False #Change after first time storing
results = np.array([])
t = np.ones(50)
stay = True
while stay:
    name = float(input("Enter voltage: "))
    for i in tqdm(t):

        if results.size == 0:
            results = np.append(results, sa.scan())
        else:
            results = np.vstack((results, sa.scan()))
        

    spectrum = np.average(results, axis=0)

    fig.canvas.flush_events()

    line1.set_xdata(freq / 1e9)
    line1.sety_data(spectrum)

    fig.canvas.draw()




sa.close()