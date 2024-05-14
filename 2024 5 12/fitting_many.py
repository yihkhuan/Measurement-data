import spike as sp
import matplotlib.pyplot as plt

magnet = ' double-magnet '
# esrcontour(magnet, True, (current_mag(4.85, magnet),current_mag(5.9, magnet)), (9.45,9.55))

difference =  sp.current_diff(magnet)#A
# lowerBound, upperBound = sp.current_decider(magnet)


currents = sp.current_list(0, 5)
print(currents)
for current in currents:
    try:
        freq, loss0 = sp.loss_list(current)
        index = currents.index(current)
        
        filename = sp.current_list(currents[index + 1], current + 2 * difference)
        sp.esrcontour(magnet, loss0, filename)
        plt.show()
        # plt.savefig(f"{current}_3D-plot.csv")
    except:
        continue