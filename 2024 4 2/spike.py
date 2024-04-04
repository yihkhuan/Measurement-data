import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

GHz = 1e9
mT = 1e-3

def loss_list(current: float) -> tuple: 
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

def average_loss_list(current: float) -> tuple:
    filenames = []

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

def esrcontour():
    current = current_list()
    current = np.array(current)
    # print(current[0])
    freq, loss_0 = loss_list(current[0])
    I, F = np.meshgrid(current[1:],freq)
    lossmesh = np.array([])
    for i in current[1:]:
        freq, loss = loss_list(i)
        loss = loss_0 - loss
        lossmesh = np.append(lossmesh,loss)
    lossmesh = np.reshape(lossmesh,(-1,freq.shape[-1]))

    fig, ax = plt.subplots()
    cp = ax.contourf(I, F, lossmesh.transpose(), cmap='rainbow', levels=100, zorder=1)
    cb = plt.colorbar(cp,orientation = 'vertical')
    cb.ax.tick_params(labelsize = 16)
    cb.set_label(label="absorption (dB)", fontsize=20)
    ax.set_xlabel("current (A)",fontsize=20)
    ax.set_ylabel("frequency (GHz)",fontsize=20)
    ax.tick_params(axis='both',which='major',labelsize=13)
    ax.set_title("Contour plot of ESR signal", fontsize = 20)

    plt.tight_layout()
    plt.savefig("./figs/ESR_contour.png")
    pass

def current_list():
    currents = np.arange(0,600) / 100
    current = []
    for i in tqdm(currents):
        finding = find("%.2fA.csv"%i,"./")
        if finding is True:
            current.append(i)
        else:
            pass
    return current


def find_all(name: str, path: str):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
        else:
            return False
    pass
        
# print(find("5.24.csv",'./'))
# for root,dirs,files in os.walk("./"):
#     print(files)
# print(current_list())
# current = current_list()
# current = np.array(current)
# freq, loss_0 = loss(current[0])
# print(freq.shape[-1])
esrcontour()