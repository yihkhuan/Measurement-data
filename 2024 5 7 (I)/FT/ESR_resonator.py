import numpy as np
import matplotlib.pyplot as plt

filenames = ["isolator.csv",
             "xisolator.csv"]



GHz = 1e9

currents = np.arange(0,400) / 100
# currents = np.arange(1)
def loss(file):
    loss = np.array([])

    # Read data lines
    
    with open(file, "r") as f:
        data_lines = f.readlines()

    freq = np.array([])
    for data in data_lines:
        values = data.split(",")
        freq = np.append(freq,float(values[0]) / GHz)
        loss = np.append(loss,float(values[1]))
    
    # loss = np.reshape(loss,(3,-1))
    # loss = loss.transpose()

    
    return (freq,loss)
    # print(dB)
            
freq=[]
signal=[]
for file in filenames:
    i = filenames.index(file)
    temp_freq, temp_signal = loss(file)

    signal_loss = temp_signal 
    plt.plot(temp_freq,signal_loss,label=file)
    plt.xlim((9,10))
plt.legend()
plt.savefig("resonator.png")





            
    