import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from scipy.optimize import curve_fit
from scipy.stats import linregress
import json

GHz = 1e9
mT = 1e-3
PLANK_CONSTANT = 6.626e-34
BOHR_MAGNETON = 9.27e-24

def loss_list(current: float) -> tuple: 
    freq = np.array([])
    loss = np.array([])
    file = "%.2fA.csv" % current
    with open(file, "r") as f:
        data_lines = f.readlines()

    for data in data_lines:
        values = data.split(",")
        freq = np.append(freq,float(values[0]) / GHz)
        loss = np.append(loss,float(values[1]))
    return (freq,loss)

def average_loss_list(current: float) -> tuple:
    filenames = []

    loss = np.array([])

    address = "./%.2fA" % (current)
    # address = "./0A"
    os.chdir(address)

    # Read data lines
    for file in filenames:
        with open(file, "r") as f:
            data_lines = f.readlines()

        freq = np.array([])
        for data in data_lines:
            values = data.split(",")
            freq = np.append(freq,float(values[0]) / GHz)
            loss = np.append(loss,float(values[1]))
    
    loss = np.reshape(loss,(3,-1))
    loss = loss.transpose()

    os.chdir("../")
    loss = np.average(loss,axis=1)
    return (freq,loss)

def esrcontour(magnet_name, fitting = False, xlim = (0,0), ylim = (0,0)):
    current = current_list()
    current = np.array(current)
    # print(current[0])
    freq, loss_0 = loss_list(current[0])
    # magnetic = 19.713 * current[1:] + 224.92
    magnetic = current_mag(current[1:],magnet_name)
    B, F = np.meshgrid(magnetic,freq)
    lossmesh = np.array([])
    for i in current[1:]:
        freq, loss = loss_list(i)
        loss = loss_0 - loss
        lossmesh = np.append(lossmesh,loss)
    lossmesh = np.reshape(lossmesh,(-1,freq.shape[-1]))

    fig, ax = plt.subplots()
    if fitting == True:
        with open("./fitting_params.json","r") as f:
            data = json.load(f)
        
        magnetic_field = np.ndarray([])
        resonance_freq = np.ndarray([])
        for current, obj in data.items():
            mag = current_mag(float(current), magnet_name)
            magnetic_field = np.append(magnetic_field,mag)
        
            frequency = obj["resonance-frequency"]
            resonance_freq = np.append(resonance_freq,frequency)

        resonance_freq = np.delete(resonance_freq,[0])
        magnetic_field = np.delete(magnetic_field,[0])

        m,c = fit_linear(resonance_freq[1:],magnetic_field[1:])

        freq_pts = np.arange(9,11)
        mag_pts = freq_pts * m + c
        # print(magnetic_field.size)
        # print(resonance_freq.size)
        ax.plot(magnetic_field,resonance_freq,"ko")
        ax.plot(mag_pts, freq_pts, "k--", lw=2)


    cp = ax.contourf(B, F, lossmesh.transpose(), cmap='rainbow', levels=100, zorder=1)
    cb = plt.colorbar(cp,orientation = 'vertical')
    cb.ax.tick_params(labelsize = 16)
    cb.set_label(label="absorption (dB)", fontsize=20)
    if xlim != (0,0):
        ax.set_xlim(xlim)
    if ylim != (0,0):
        ax.set_ylim(ylim)
    ax.set_xlabel("magnetic field (mT)",fontsize=20)
    ax.set_ylabel("frequency (GHz)",fontsize=20)
    ax.tick_params(axis='both',which='major',labelsize=13)
    ax.set_title("Contour plot of ESR signal", fontsize = 20)

    plt.tight_layout()
    magnet_name = magnet_name.replace(magnet_name[-4:],"")
    plt.savefig("./figs/ESR_contour" + magnet_name + ".png")
    pass

def current_list():
    currents = np.arange(0,600) / 100
    current = []
    for i in tqdm(currents):
        finding = find("%.2fA.csv"%i,"./")
        if finding is True:
            current.append(i)
        else:
            pass
    return current

def find_all(name: str, path: str):
  """
  Finds all folders containing the substring 'name' within the given path.

  Args:
      name: The substring to search for in folder names.
      path: The starting directory to search from.

  Returns:
      A list of full paths to folders containing the substring 'name'.
  """
  result = []
  for root, dirs, files in os.walk(path):
    for file_name in files:
      if name in file_name:
        result.append(file_name)

  return result

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
        else:
            return False
    pass
        
def lorentzian_fit(freq:np.ndarray, absorption:np.ndarray):
    index = np.where(absorption == np.max(absorption))[0][0]
    max_freq = freq[index]
    # plt.figure()
    # plt.scatter(freq,absorption)
    # plt.show()
    #curve fitting
    popt,_ = curve_fit(lorentz, freq, absorption,p0=(.5,.001,max_freq,-.2))
    Al,b,a,offsetl = popt
    return (Al,b,a,offsetl)

def lorentz(x: np.ndarray, Al:float, b:float, a:float, offsetl:float) -> np.ndarray:
    return Al / np.pi * (b / ((x - a)**2 + b**2)) + offsetl

def UTM_2D_plot(x:np.ndarray, y:np.ndarray, title:str, xlabel:str, ylabel:str, filename:str, canvas:tuple = None):
    plt.title(title, fontsize = 20)
    plt.ylabel(ylabel, fontsize=20)
    plt.xlabel(xlabel, fontsize=20)
    plt.xticks(fontsize = 13)
    plt.yticks(fontsize = 13)
    plt.plot(x,y)
    plt.subplots_adjust(bottom=0.2,left=0.2)
    plt.savefig("./figs/" + filename)

def current_mag(current, magnet_name):
    with open('./Analyse_data/current.json', 'r') as f:
        fitted_current = json.load(f)

        m = fitted_current[magnet_name].get('m')[0]
        c = fitted_current[magnet_name].get('c')[0]
    
    return m * current + c 

def mag_current(mag,magnet_name):
    with open('./Analyse_data/current.json', 'r') as f:
        fitted_current = json.load(f)

        m = fitted_current[magnet_name].get('m')[0]
        c = fitted_current[magnet_name].get('c')[0]
    
    return (mag - c)/m 

def fit_linear(x: np.ndarray, y: np.ndarray) -> tuple:
    gradient, intercept, r, p, se = linregress(x, y)
    return (gradient, intercept)

def get_g(parameter_address: str, magnet_name):
    with open(parameter_address,"r") as f:
        data = json.load(f)
    
    magnetic_field = np.ndarray([])
    resonance_freq = np.ndarray([])
    for current, obj in data.items():
        mag = current_mag(float(current), magnet_name)
        magnetic_field = np.append(magnetic_field,mag)
    
        frequency = obj["resonance-frequency"]
        resonance_freq = np.append(resonance_freq,frequency)
    
    resonance_freq = np.delete(resonance_freq,[0])
    magnetic_field = np.delete(magnetic_field,[0])
    
    m,c = fit_linear(resonance_freq,magnetic_field)
    g = m / PLANK_CONSTANT * BOHR_MAGNETON /GHz*mT
    return (1 / g ,m, c)
    
def absortion_magnetic_plot(current: float, resonance_freq:float, loss_0:float):
    
    try: freq, loss_ave = loss_list(current)
    except: print("failed")
    loss_ave = loss_ave - loss_0
    # print(freq)
    index_resonant = np.where(freq==resonance_freq)[0][0]
    current_out = np.append(current_out,current)
    transmission = np.append(transmission,loss_ave[index_resonant])
    return (current_out, transmission)
    
def resonator_fit(address: str):
    with open(address) as f:
        data = f.read()
    
    pass

def current_fit():
    pass

def get_resonator_params(filenames: list, loss_0):
    dict_list = {}

    for name in filenames:
        try:
            freq, loss_ave = loss_list(name)
        except:
            continue
        absorption = loss_0 - loss_ave

        try:
            params = sp.lorentzian_fit(freq, absorption)
        except:
            print(str(name) + " unable to fit")
            continue
        dict_list.update({"%.2f" % (name): {
                            "amplitude"           : params[0],
                            "bandwidth"           : params[1],
                            "resonance-frequency" : params[2],
                            "offset"              : params[3]
                            }
                        })
        
        l = lorentz(freq,*params)
        plt.figure()
        # fig[filenames.index(name)], ax[filenames.index(name)] = plt.subplots()
        plt.scatter(freq,absorption)
        
        sp.UTM_2D_plot(freq,l,
                    title = "signal fitting",
                    xlabel = "frequency, GHz",
                    ylabel = "absorption",
                    filename = "fitting %.2fA.png" % (name),
                    )
        
    with open("fitting_params.json", "w") as outfile:
        json.dump(dict_list,outfile)
    pass

def get_fitting_params(names, params: list ,values: list, output=False, out_name=None):
    dict_list = {}
    i = 0
    for name in names:
        while i < len(list)+1:
            dict_list.update({str(name): {params[i]: values[i]}})
            i = i +1
    
    if output is True:
        with open("fitting_params.json", "w") as outfile:
            json.dump(dict_list,outfile)
        
        pass
    else:
        return dict_list

def get_current_params(filenames: list):
    dict_list = {}
    for file in filenames:
        current = np.array([])
        mag = np.array([])
        name = file.replace(file[-4:],"")

        with open(file, "r") as f:
            data_lines = f.readlines()

        for data in data_lines:
            values = data.split()
            current = np.append(current,float(values[0]))
            mag = np.append(mag,float(values[1]))
        
        params = fit_linear(current,mag)
        dict_list.update({file: {
                    "m"           : [params[0]],
                    "c"           : [params[1]],
                    }
                })
        
        y = params[0] * current + params[1]
        plt.figure()
        plt.scatter(current,mag)
        UTM_2D_plot(current,y,
                    title=  name + " calibration",
                    xlabel= "current, A",
                    ylabel= "magnetic field, mT",
                    filename= "fitting " + name + ".png")
        
    with open("fitting_params.json", "w") as outfile:
        json.dump(dict_list,outfile)





# print(find("5.24.csv",'./'))
# for root,dirs,files in os.walk("./"):
#     print(files)
# print(current_list())
# current = current_list()
# current = np.array(current)
# freq, loss_0 = loss_list(current[0])
# print(freq.shape[-1])

# x = np.linspace(8.5,10,100)
# y = lorentz(x,10,.1,9.5,1)
# rng = np.random.default_rng()
# y_noise = 0.2 * rng.normal(size=x.size) * 0
# y = y + y_noise
# # params = lorentzian_fit(x,y)
# params,_ = curve_fit(lorentz, x, y,p0=(10,.1,9.5,1))
# fit_y = lorentz(x, *params)

# plt.scatter(x,y)
# plt.plot(x,fit_y)

# plt.show()
# print(get_g("./fitting_params.json", ' double-magnet '))

# esrcontour(' double-magnet ', True, xlim=(322,328), ylim=(9.25,9.6))