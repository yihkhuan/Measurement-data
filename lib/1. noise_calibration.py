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

sa.setup(9.67 * GHZ_UNIT, 1.0 * GHZ_UNIT, -10.0)

sa.tg_sweep_points(1000)

freq = sa.fetch_xarray()



plt.figure()
date_time = datetime.datetime.now()
outputFile = f"{date_time.year}_{date_time.month}_{date_time.day}-{date_time.hour}{date_time.minute}"
np.savetxt(outputFile, [])

with open(outputFile, "ab") as output:
    output.write(b"\n")
    output.write(b"\n")
    np.savetxt(output, freq.transpose(), header="ydata")
output.close()
# plt.plot(freq / GHZ_UNIT, spectrum)
# # plt.savefig("./figs/Noise_calibration/before_zero.png")
# plt.show()
# plt.close()
print(freq.shape, freq[0]/MHZ_UNIT, freq[-1]/MHZ_UNIT, (freq[1] - freq[0])/MHZ_UNIT)

for i in tqdm(range(100)):
    spectrum = sa.scan()

sa.stor_thru(1)
sleep(5)
# spectrum = sa.scan()
# plt.figure()
# plt.plot(freq / GHZ_UNIT, spectrum)
# # plt.savefig("./figs/Noise_calibration/before_zero.png")
# plt.show()
# plt.close()


# sa.stor_thru(2)

# spectrum = sa.scan()
# plt.figure()
# plt.plot(freq / GHZ_UNIT, spectrum)
# # plt.savefig("./figs/Noise_calibration/before_zero.png")
# plt.show()
# plt.close()



not_0DB = False #Change after first time storing
results = np.array([])
t = np.ones(100)
stay = True
while stay:
    name = float(input("Enter voltage: "))
    for i in tqdm(t):

        if results.size == 0:
            results = np.append(results, sa.scan())
        else:
            results = np.vstack((results, sa.scan()))
        

    spectrum = np.average(results, axis=0)
    

    # if esr.find("csv", "./figs/Signal_detection/"):
    #     off_resonance = esr.find_all(".csv", "./figs/Signal_detection/")[0]
    #     freq, loss0 = esr.split_data("./figs/Signal_detection/" + off_resonance)
    #     absorption = loss0 - spectrum
    #     plt.figure()
    #     plt.plot(freq / GHZ_UNIT, absorption)
    #     # plt.savefig(f"./figs/Noise_calibration/{name}mT.png")
    #     plt.show()
    #     plt.close()
    # else:

    #     pass

    # print(spectrum.shape)
    # print(freq.shape)
    
    # print(output.transpose())
    # np.savetxt('./%s.csv'%name, output.transpose(), delimiter= ",")

    with open(outputFile, "ab") as output:
        output.write(b"\n")
        output.write(b"\n")
        np.savetxt(output, spectrum.transpose(), header = name)
    output.close()
    
    try:
        stay = int(input("Do you want to stay (1/0): "))
    except:
        stay = int(input("Do you want to stay (1/0): "))



sa.close()