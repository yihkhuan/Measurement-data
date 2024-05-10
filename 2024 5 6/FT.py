import spike as sp
import numpy as np
from matplotlib import pyplot as plt

def mask(array, n):
    masking = array[n:-n]
    masking = np.pad(masking,(n,n),constant_values=0)
    out = array - masking
    return out


freq, loss0 = sp.loss_list(10.11)
# freq = np.linspace(9,10,10000)

currentlist = sp.current_list()
for current in currentlist:
    freq, loss2 = sp.loss_list(current)

    absorption2 = loss0 - loss2
    freq = freq[::25]
    absorption2 = absorption2[::25]
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
    fft_lorentz2 = mask(fft_lorentz2,5)
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

    print(t.max(), freq.max())


    signal2 = np.fft.ifft(fft_lorentz2)
    plt.figure()
    # plt.plot(t, np.abs(signal1), label = 's1')
    plt.plot(freq, signal2, label = 'processed data', color = "red")
    plt.scatter(freq, absorption2, marker="+", label="real", color = "green")
    plt.legend()
    plt.savefig(f"./figs/FT_{current}A.png")
    # plt.show()
    plt.close()





