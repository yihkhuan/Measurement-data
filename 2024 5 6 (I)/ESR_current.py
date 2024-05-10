import numpy as np
import matplotlib.pyplot as plt
from spike import loss_list
from tqdm import tqdm
import json

currents = np.arange(000,1200) / 100
freq, loss_0 = loss_list(11.31)

g = open('./Analyse_data/current.json')
fitted_current = json.load(g)

m = fitted_current[' 0mm '].get('m')[0]
c = fitted_current[' 0mm '].get('c')[0]

GHz = 1e9


f = open('./Analyse_data/fitted.json')
resonator = json.load(f)
data = resonator.get('fitted_data')[0]
resonance_fre = data.get('a')[0]

range = np.linspace(-0.05,0.05,10)
print(resonance_fre + range)
for frequency in (resonance_fre + range):
    print(frequency)
    current = np.array([])
    transmission = np.array([]) 
    for i in tqdm(currents):
        try: freq, loss_ave = loss_list(i)
        except: continue
        loss_ave = loss_0 - loss_ave
        # print(freq)
        diff_array = np.abs(freq - frequency)
        index_resonant = np.where(diff_array == np.abs(freq - frequency).min())[0][0]
        
        current = np.append(current,i)
        transmission = np.append(transmission,loss_ave[index_resonant])
    plt.figure()
    # fig, ax = plt.subplots(layout='constrained')

    to_magnetic = lambda x: m * x + c
    to_current = lambda x: (x-c)/m
    plt.plot(to_magnetic(current)[1:-1],transmission[1:-1])
    plt.xlabel('magnetic field strength, mT')
    plt.ylabel('transmission')
    plt.title('ESR experiment with isolator, resonance frequncy = ' + "%.4f" % frequency + " GHz")
    # secax = ax.secondary_xaxis('top', functions=(to_current, to_magnetic))
    # secax.set_xlabel('current, A')
    plt.savefig("./figs/current_vs_transmission "+ "%.4f" % frequency +".png")
    plt.close()