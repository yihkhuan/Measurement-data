import numpy as np
import matplotlib.pyplot as plt
from ESR import loss
from tqdm import tqdm
import json

currents = np.arange(500,600) / 100
freq, loss_0 = loss(5.24)

g = open('fitted_current.json')
fitted_current = json.load(g)

m = fitted_current[' small-magnet '].get('m')[0]
c = fitted_current[' small-magnet '].get('c')[0]

GHz = 1e9
current = np.array([])
transmission = np.array([])

resonance_freq = 9.46
for i in tqdm(currents):
    try: freq, loss_ave = loss(i)
    except: continue
    loss_ave = loss_ave - loss_0
    # print(freq)
    index_resonant = np.where(freq==resonance_freq)[0][0]
    current = np.append(current,i)
    transmission = np.append(transmission,loss_ave[index_resonant])
fig, ax = plt.subplots(layout='constrained')

to_magnetic = lambda x: m * x + c
to_current = lambda x: (x-c)/m
plt.plot(to_magnetic(current)[1:],transmission[1:])
ax.set_xlabel('magnetic field strength, mT')
ax.set_ylabel('transmission')
ax.set_title('ESR experiment with isolator, resonance frequncy = ' + str(resonance_freq) + " GHz")
secax = ax.secondary_xaxis('top', functions=(to_current, to_magnetic))
secax.set_xlabel('current, A')
plt.savefig("./figs/current_vs_transmission.png")