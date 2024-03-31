import numpy as np
import matplotlib.pyplot as plt
from ESR import average_loss
from tqdm import tqdm

currents = np.arange(3,400) / 100
freq, loss_0 = average_loss(3.06)

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
plt.figure()
plt.xlim(left=3.4,right=4)
plt.scatter(current,transmission)
plt.savefig("./figs_current/current_vs_transmission.png")

