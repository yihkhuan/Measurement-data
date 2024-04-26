import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
import spike as sp
filenames = ["1.csv",
             "2.csv",
             "3.csv"]

GHz = 1e9

currents = np.arange(400,600) / 100
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
            
freq, loss_0 = sp.loss_list(0.37)
for i in tqdm(currents):
    
    try: freq, loss_ave = sp.loss_list(i)
    except: continue
    loss_ave = loss_0 - loss_ave
    plt.figure()
    
    
    outname = "./%.2fA.png" % (i)
    magnetic_field = sp.current_mag(i, ' double-magnet ')
    sp.UTM_2D_plot(freq,loss_ave, 
                " Absortion vs MW frequency" + " - %.2f mT" % (magnetic_field), 
                "Frequency, GHz",
                "Absorption, dB",
                outname)



            
    