import spike as sp

magnet = ' 0mm '
# esrcontour(magnet, True, (current_mag(4.85, magnet),current_mag(5.9, magnet)), (9.45,9.55))

# esrcontour(magnet, True)
# print(mag_current(331,' double-magnet '))
freq, loss0 = sp.loss_list(9.79)
filename = sp.current_list()
# filename = sp.current_list(5.62,5.68)
# filename.append(5.15)
# sp.esrcontour(magnet, loss0, True, (327, 360), (9.52, 9.56))
sp.esrcontour(magnet,loss0, xlim = (327, 360), ylim = (9.52, 9.56))
sp.get_resonator_params(filename, loss0, magnet)
# print(sp.get_g(magnet))