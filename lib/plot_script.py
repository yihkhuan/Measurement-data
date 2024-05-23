import esr
from matplotlib import pyplot as plt


axis = "z"


name, distance, magnetic_flux = esr.split_datablock(f"magnets {axis} axis (real).csv", ",")
title = f"magnetic flux density in {axis} axis"
ylabel = "magnetic flux density (mT)"
xlabel = "position (mm)"

plt.title(title, fontsize = 20)
plt.ylabel(ylabel, fontsize=20)
plt.xlabel(xlabel, fontsize=20)
plt.xticks(fontsize = 13)
plt.yticks(fontsize = 13)

plt.subplots_adjust(bottom=0.2,left=0.2)


for i in range(3):
    label = name[i].replace("#","")
    plt.plot(distance[i], magnetic_flux[i], label = label)
plt.legend()
# plt.show()
plt.savefig(f"magnet plot {axis} axis.png")