import spike as sp

magnet = ' double-magnet '
# esrcontour(magnet, True, (current_mag(4.85, magnet),current_mag(5.9, magnet)), (9.45,9.55))

# esrcontour(magnet, True)
# print(mag_current(331,' double-magnet '))
freq, loss0 = sp.loss_list(5.11)
filename = sp.current_list(5.12,5.24)
# filename = sp.current_list(5.62,5.68)
# filename.append(5.15)
# sp.esrcontour(magnet, loss0, True, (335, 345), (9.4, 9.8))
sp.esrcontour(magnet, loss0, filename, True)
sp.get_resonator_params(filename, loss0, magnet)
print(sp.get_g(magnet))


# print(1 / sp.EXPECTED_GRADIENT)