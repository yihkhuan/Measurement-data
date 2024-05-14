import spike as sp
import matplotlib.pyplot as plt

magnet = ' 3mm '
# esrcontour(magnet, True, (current_mag(4.85, magnet),current_mag(5.9, magnet)), (9.45,9.55))

difference = 0.1 #A
# lowerBound, upperBound = sp.current_decider(magnet)

currents = sp.current_list()
for current in currents:
    freq, loss0 = sp.loss_list(current)
    index = currents.index(current)
    filename = sp.current_list(currents[index + 1], current + difference)
    sp.esrcontour(magnet, loss0, filename)
    plt.savefig(f"{current}_3D-plot.csv")