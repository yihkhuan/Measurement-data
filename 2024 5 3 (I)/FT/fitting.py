import spike as sp
import numpy as np
magnet = ' double-magnet '
# esrcontour(magnet, True, (current_mag(4.85, magnet),current_mag(5.9, magnet)), (9.45,9.55))

# esrcontour(magnet, True)
# print(mag_current(331,' double-magnet '))
freq, loss0 = sp.loss_list(5.63)
filename = sp.current_list(5.61, 5.83)
loss0 = np.zeros(freq.shape[-1])
# filename = sp.current_list(5.62,5.68)
# filename.append(5.15)
# sp.esrcontour(magnet, loss0, True, (335, 345), (9.4, 9.8))
# sp.esrcontour(magnet, loss0, True, xlim=(346.5,352), ylim=(9.77,9.81))
sp.esrcontour(magnet, filename)
# sp.get_resonator_params(filename, loss0, magnet)
# print(sp.get_g(magnet))
print(filename)
print(sp.mag_current((9.79 - 50 * 1e-3)/ sp.EXPECTED_GRADIENT, magnet))
print(349.36 * sp.EXPECTED_GRADIENT)