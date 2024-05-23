import esr

name, current, teslameter, gaussmeter = esr.split_data('magnet data.csv', ',')
tesla_parameter = esr.fit_linear(current, teslameter)
gauss_parameter = esr.fit_linear(current, gaussmeter)


import matplotlib.pyplot as plt

fig, ax = plt.subplots()


ax = esr.UTM_2D_plot(ax, current[0], teslameter[0], 
                title= "Calibration of Teslameter",
                 xlabel= "current, A",
                  ylabel= "magnetic field, mT",
                  label= "teslameter")

ax.scatter(current[0], gaussmeter[0], marker = "x", label = "gaussmeter")

gradient_teslameter = tesla_parameter[0]
intercept_teslameter = tesla_parameter[1]
ax.plot(current[0], gradient_teslameter * current[0] + intercept_teslameter)

gradient_gaussmeter = gauss_parameter[0]
intercept_gaussmeter = gauss_parameter[1]
ax.plot(current[0], gradient_gaussmeter * current[0] + intercept_gaussmeter)
# print(current)
# print(teslameter)
# plt.figure()
# plt.plot(current, teslameter)
plt.legend()
plt.savefig("teslameter_calibration.png")