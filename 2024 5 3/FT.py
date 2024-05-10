import spike as sp
import numpy as np
from matplotlib import pyplot as plt

def mask(array, n):
    masking = array[n:-n]
    masking = np.pad(masking,(n,n),constant_values=0)
    out = array - masking
    return out


freq, loss0 = sp.loss_list(5.44)
# freq = np.linspace(9,10,10000)
freq, loss1 = sp.loss_list(5.71)
freq, loss2 = sp.loss_list(5.71)
absorption1 = loss0 - loss1
absorption2 = loss0 - loss2
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
fft_lorentz1 = np.fft.fft(absorption1)
fft_lorentz2 = np.fft.fft(absorption2)
# ori2 = np.fft.fft(absorption2)

# fft_ones = np.fft.fft(ones)
rate = freq[1] - freq[0]

f = np.fft.fftfreq(freq.shape[-1], d = rate)
fft_lorentz2 = mask(fft_lorentz2,15)
plt.figure()
# plt.plot(f, np.abs(fft_lorentz1), label = 'l1')
plt.plot(f, np.abs(fft_lorentz2), label = 'l2')
# plt.plot(f, np.abs(fft_lorentz3), label = 'l3')
# plt.ylim(-2, 5)
plt.legend()
plt.show()
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

signal1 = np.fft.ifft(fft_lorentz1)
signal2 = np.fft.ifft(fft_lorentz2)
plt.figure()
# plt.plot(t, np.abs(signal1), label = 's1')
plt.plot(t, signal2, label = 'processed data', color = "red")
plt.scatter(freq, absorption2, marker="+", label="real", color = "green")
plt.legend()
plt.show()
plt.close()





