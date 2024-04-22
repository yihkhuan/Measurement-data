import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import spike as sp
from json import dump

filenames = [   5.28,
                5.42,
                5.50,
                5.60,
                5.80,
                6.00]



GHz = 1e9

currents = np.arange(300,601) / 100
# currents = np.arange(1)


freq, loss_0 = sp.loss_list(0.39)
for i in tqdm(currents):
    try: freq, loss_ave = sp.loss_list(i)
    except: continue
    absorption = loss_0 - loss_ave
    plt.figure()
    plt.ylabel("absorbtion, dB")
    plt.xlabel("Frequency, GHz")
    B = 19.713 * i + 224.92
    plt.title("B0 = %.2f mT" % (B))
    # plt.xlim((8.6, 9.8))
    plt.plot(freq,absorption)
    plt.savefig("./figs/%.2fA.png" % (i))

fig = []
ax = []


dict_list = {}


for name in filenames:
    freq, loss_ave = sp.loss_list(name)
    absorption = loss_0 - loss_ave

    params = sp.lorentzian_fit(freq, absorption)
    dict_list.update({"%.2f" % (name): {
                        "amplitude"           : params[0],
                        "bandwidth"           : params[1],
                        "resonance-frequency" : params[2],
                        "offset"              : params[3]
                        }
                    })
    
    l = sp.lorentz(freq,*params)
    plt.figure()
    # fig[filenames.index(name)], ax[filenames.index(name)] = plt.subplots()
    plt.scatter(freq,absorption)
    
    sp.UTM_2D_plot(freq,l,
                   title = "signal fitting",
                   xlabel = "frequency, GHz",
                   ylabel = "absorption",
                   filename = "fitting %.2fA.png" % (name),
                   )
    
with open("fitting_params.json", "w") as outfile:
    dump(dict_list,outfile)

            
    