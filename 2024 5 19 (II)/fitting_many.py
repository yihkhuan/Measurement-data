import spike as sp
import matplotlib.pyplot as plt

magnet = ' double-magnet '
# esrcontour(magnet, True, (current_mag(4.85, magnet),current_mag(5.9, magnet)), (9.45,9.55))

difference = sp.current_diff(magnet) #A
# lowerBound, upperBound = sp.current_decider(magnet)
print(difference)
currents = sp.current_list(start=4.6)
for current in currents:
    freq, loss0 = sp.loss_list(current)
    index = currents.index(current)
    filename = sp.current_list(currents[index + 1], current + 2 * difference)
    sp.esrcontour(magnet, loss0, filename)
    plt.show()