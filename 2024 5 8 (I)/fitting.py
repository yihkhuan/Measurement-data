import spike as sp

magnet = ' 0mm '
# esrcontour(magnet, True, (current_mag(4.85, magnet),current_mag(5.9, magnet)), (9.45,9.55))

# esrcontour(magnet, True)
# print(mag_current(331,' double-magnet '))
freq, loss0 = sp.loss_list(3.558)
filename = sp.current_list(3.606, 3.647)
# filename = sp.current_list(5.62,5.68)
# filename.append(5.15)
# sp.esrcontour(magnet, loss0, True, (335, 345), (9.4, 9.8))
sp.esrcontour(magnet, loss0, filename)
# sp.get_resonator_params(filename, loss0, magnet)
# print(sp.get_g(magnet))

print(sp.mag_current((9.68 - 50 * 1e-3 )/ sp.EXPECTED_GRADIENT, magnet))
# print(1 / sp.EXPECTED_GRADIENT)