import spike as sp

magnet = ' double-magnet '
# esrcontour(magnet, True, (current_mag(4.85, magnet),current_mag(5.9, magnet)), (9.45,9.55))
sp.BOHR_MAGNETONesrcontour(magnet, True, (340, 344), (9.4, 9.8))
# esrcontour(magnet, True)
# print(mag_current(331,' double-magnet '))
freq, loss0 = sp.loss_list(0.44)
filename = sp.current_list()
# filename.append(5.15)
sp.get_resonator_params(filename, loss0, magnet)
print(sp.get_g(magnet))
