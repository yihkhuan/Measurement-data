
import json
import numpy as np
import matplotlib.pyplot as plt

f = open('fitted.json')
dictionaries = json.load(f)
GHz = 1e9
freq = np.linspace(8.5,10.5,1000)
fig, axs = plt.subplots(3,1,figsize=(10,10))
index = 0
for x in dictionaries['fitted_data']:
    
    if x.get('name') != 'before_magnet':
        a = x.get('a')[0]
        b = x.get('b')[0]
        al = x.get('Al')[0]
        offset = x.get('offsetl')[0]
        l = al / np.pi * (b / ((freq - a)**2 + b**2)) - offset
        
        axs[index].plot(freq, l, label = x.get('name'))
        axs[index].legend()
        axs[index].set(xlabel = ("Frequency, GHz"), ylabel =('Signal power'))
        axs[index].xaxis.set_label_coords(1.05, -0.025)
        index = index + 1
plt.show()