import spike as sp
import numpy as np
from os import chdir
from tqdm import tqdm
from os import system

dirnames = np.arange(0,400) / 100

for dir in tqdm(dirnames):
    try:
        freq, loss = sp.average_loss_list(dir)
        output = np.vstack((freq * 1e9, loss))
        np.savetxt("%.2fA.csv" % dir, output.transpose(), delimiter= ", ")

    except:

        continue
