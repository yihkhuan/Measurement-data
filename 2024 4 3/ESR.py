import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

filenames = ["1.csv",
             "2.csv",
             "3.csv"]



GHz = 1e9
mT = 1e-3
currents = np.arange(500,600) / 100
# currents = np.arange(1)
def average_loss(current):
    loss = np.array([])

    address = "./%.2fA" % (current)
    # address = "./0A"
    os.chdir(address)

    # Read data lines
    for file in filenames:
        with open(file, "r") as f:
            data_lines = f.readlines()

        freq = np.array([])
        for data in data_lines:
            values = data.split(",")
            freq = np.append(freq,float(values[0]) / GHz)
            loss = np.append(loss,float(values[1]))
    
    loss = np.reshape(loss,(3,-1))
    loss = loss.transpose()

    os.chdir("../")
    loss = np.average(loss,axis=1)
    return (freq,loss)
    # print(dB)
            
def loss(current):
    freq = np.array([])
    loss = np.array([])
    file = "%.2fA.csv" % current
    with open(file, "r") as f:
        data_lines = f.readlines()

    for data in data_lines:
        values = data.split(",")
        freq = np.append(freq,float(values[0]) / GHz)
        loss = np.append(loss,float(values[1]))
    return (freq,loss)

def resonatorplot():
    to_magnetic = lambda x: x * GHz * 3.57e-11  #mT
    to_frequency = lambda x: x / GHz /  3.57e-11  #GHz
    fig, ax = plt.subplots(layout='constrained')
    ax.set_xlabel('frequency, GHz')
    ax.set_ylabel('transmission, dB')
    ax.set_title('Resonator characterisation')
    secax = ax.secondary_xaxis('top', functions=(to_magnetic, to_frequency))
    secax.set_xlabel('magnetic field, T')
    return (fig,ax)

# for i in tqdm(currents):
    
#     try: freq, loss_ave = loss(i)
#     except: continue
#     loss_ave = loss_0 - loss_ave
#     plt.figure()
#     plt.ylabel("absorbtion, dB")
#     plt.xlabel("Frequency, GHz")
#     B = 19.713 * i + 224.92
#     plt.title("B0 = %.2f mT" % (B))
#     # plt.xlim((8.6, 9.8))
#     plt.plot(freq,loss_ave)
#     plt.savefig("./figs/%.2fA.png" % (i))



            
    