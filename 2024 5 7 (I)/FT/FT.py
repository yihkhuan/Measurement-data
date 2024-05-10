import spike as sp
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

def mask(array, n):
    masking = array[n:-n]
    masking = np.pad(masking,(n,n),constant_values=0)
    out = array - masking
    return out

def split_data(filename: str, delimiter: str = ""):
    # Read data lines
    with open(filename, "r") as f:
        data_lines = f.readlines()

    # Separate data blocks
    data_blocks = []
    current_block = []
    for line in data_lines:
        if line.strip() == "":  # Check for empty line
            # print(current_block)
            if current_block:
                data_blocks.append(current_block)
            current_block = []
        else:
            current_block.append(line.strip())  # Strip trailing newline
    if current_block:
        data_blocks.append(current_block)
    name = []
    x = np.array([])
    y = np.array([])
    #Converting data block into Ndarray format
    for i in range(len(data_blocks)):
        # Choose block to plot (modify index for different blocks)
        chosen_block = data_blocks[i]

        # Extract data points (adapt based on your actual data format)
        
        x_data = np.array([])
        y_data = np.array([])
        for line in chosen_block:
            if delimiter != "":
                values = line.split(delimiter)
            else:
                values = line.split()# Assuming data is space-separated
            try:
                x_data = np.append(x_data, float(values[0]))
                y_data = np.append(y_data, float(values[1]))
            except:
                continue

        name.append(chosen_block[0])
        x = np.append(x, x_data)
        x = np.reshape(x,(len(data_blocks),-1))
        y = np.append(y, y_data)
        y = np.reshape(y,(len(data_blocks),-1))

    return (name, x, y)

freq, loss0 = sp.loss_list(3.84)
# freq = np.linspace(9,10,10000)

currentlist = sp.current_list(3.64,3.72)

for current in tqdm(currentlist):

    freq, loss2 = sp.loss_list(current)
    # name, freq, data = split_data("UR-5.csv", ",")

    # freq = freq[0] / 1e9
    absorption2 = loss0 - loss2
    freq = freq
    absorption2 = absorption2
    def lorentz(x, gamma, x0):
        y = (.5 * gamma) / np.pi / ((x-x0) * (x-x0) + (.5 * gamma))
        return y
    # absorption2 = np.sin(50 * freq)

    # l1 = lorentz(freq, 0.017, 9.4)
    # l2 = lorentz(freq, 0.017, 9.3)
    # l3 = lorentz(freq, 0.017, 9.2)

    # fft_lorentz1 = np.fft.fft(l1)
    # fft_lorentz2 = np.fft.fft(l2)
    # fft_lorentz3 = np.fft.fft(l3)

    ones = np.ones(freq.shape[-1])

    fft_lorentz2 = np.fft.fft(absorption2)
    # ori2 = np.fft.fft(absorption2)

    # fft_ones = np.fft.fft(ones)
    rate = freq[1] - freq[0]

    f = np.fft.fftfreq(freq.shape[-1], d = rate)
    fft_lorentz2 = mask(fft_lorentz2, 7)
    plt.figure()
    # plt.plot(f, np.abs(fft_lorentz1), label = 'l1')
    plt.plot(f, np.abs(fft_lorentz2), label = 'l2')
    # plt.plot(f, np.abs(fft_lorentz3), label = 'l3')
    # plt.ylim(-2, 5)
    plt.legend()
    # plt.show()
    plt.close()


    rate = f[1] - f[0]
    from time import sleep
    t = np.fft.fftfreq(f.shape[-1], d = rate)
    a = 0
    m = ".3f" % t.max() 

    while "%.3f" % t.max()  != "%.3f" % freq.max():
        t = np.fft.fftfreq(f.shape[-1], d = rate) + freq[a]
        a = a + 1




    signal2 = np.fft.ifft(fft_lorentz2)
    plt.figure()
    # plt.plot(t, np.abs(signal1), label = 's1')
    plt.plot(freq, signal2.real, label = 'processed data', color = "red")
    plt.scatter(freq, absorption2, marker="+", label="real", color = "green")
    plt.legend()
    # plt.xlim(9.575, 9.650)
    # plt.ylim(absorption2.max()-3, absorption2.max())
    plt.savefig(f"./figs/FT_{current}A.png")
    # plt.show()
    plt.close()

    output = np.vstack((freq.real, signal2.real))
    np.savetxt(f"./FT/{current}A.csv",output.transpose(), delimiter=', ', fmt='%.3f')