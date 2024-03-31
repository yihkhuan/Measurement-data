import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

filenames = ["1.csv",
             "2.csv",
             "3.csv"]



GHz = 1e9

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

freq, loss_0 = loss(5.24)
for i in tqdm(currents):
    
    try: freq, loss_ave = loss(i)
    except: continue
    loss_ave = loss_ave - loss_0
    plt.figure()
    plt.ylabel("transmission, dB")
    plt.xlabel("Frequency, GHz")
    B = 19.713 * i + 224.92
    plt.title("B0 = %.2f mT" % (B))
    # plt.xlim((8.6, 9.8))
    plt.plot(freq[::5],loss_ave[::5])
    plt.savefig("./figs/%.2fA.png" % (i))



            
    