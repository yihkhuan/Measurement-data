import numpy as np
import matplotlib.pyplot as plt
from ESR import average_loss
from tqdm import tqdm
import json

currents = np.arange(2,400) / 100
freq, loss_0 = average_loss(2.96)

g = open('fitted_current.json')
fitted_current = json.load(g)

m = fitted_current[' small-magnet '].get('m')[0]
c = fitted_current[' small-magnet '].get('c')[0]

GHz = 1e9
current = np.array([])
transmission = np.array([])
for i in tqdm(currents):
    try: freq, loss_ave = average_loss(i)
    except: continue
    loss_ave = loss_ave - loss_0
    # print(freq)
    index_resonant = np.where(freq==9.2)[0][0]
    current = np.append(current,i)
    transmission = np.append(transmission,loss_ave[index_resonant])
fig, ax = plt.subplots(layout='constrained')

to_magnetic = lambda x: m * x + c
to_current = lambda x: (x-c)/m
plt.plot(to_magnetic(current),transmission)
ax.set_xlabel('magnetic field strength, mT')
ax.set_ylabel('transmission')
ax.set_title('ESR experiment with isolator')

secax = ax.secondary_xaxis('top', functions=(to_current, to_magnetic))
secax.set_xlabel('current, A')
plt.savefig("./figs_current/current_vs_transmission.png")


