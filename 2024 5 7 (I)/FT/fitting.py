import spike as sp
import numpy as np

magnet = ' 0mm '
# esrcontour(magnet, True, (current_mag(4.85, magnet),current_mag(5.9, magnet)), (9.45,9.55))

# esrcontour(magnet, True)
# print(mag_current(331,' double-magnet '))
freq, loss0 = sp.loss_list(3.65)
loss0 = np.zeros(freq.shape[-1])
filename = sp.current_list(3.64, 3.72)
# filename = sp.current_list(5.62,5.68)
# filename.append(5.15)

# sp.get_resonator_params(filename, loss0, magnet)
sp.esrcontour(magnet, filename, True)
print(sp.get_g(magnet))
print(filename)
