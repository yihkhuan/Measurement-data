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

def esrcontour():
    current = current_list()
    current = np.array(current)
    # print(current[0])
    freq, loss_0 = loss_list(current[0])
    magnetic = 19.713 * current[1:] + 224.92
    B, F = np.meshgrid(magnetic,freq)
    lossmesh = np.array([])
    for i in current[1:]:
        freq, loss = loss_list(i)
        loss = loss_0 - loss
        lossmesh = np.append(lossmesh,loss)
    lossmesh = np.reshape(lossmesh,(-1,freq.shape[-1]))

    fig, ax = plt.subplots()
    cp = ax.contourf(B, F, lossmesh.transpose(), cmap='rainbow', levels=100, zorder=1,vmax=0.15)
    cb = plt.colorbar(cp,orientation = 'vertical')
    cb.ax.tick_params(labelsize = 16)
    cb.set_label(label="absorption (dB)", fontsize=20)
    ax.set_xlim((325,340))
    ax.set_ylim((9.35,9.6))
    ax.set_xlabel("magnetic field (mT)",fontsize=20)
    ax.set_ylabel("frequency (GHz)",fontsize=20)
    ax.tick_params(axis='both',which='major',labelsize=13)
    ax.set_title("Contour plot of ESR signal", fontsize = 20)

    plt.tight_layout()
    plt.savefig("./figs/ESR_contour.png")
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
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
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

def current_mag(current:float) -> float:
    with open('./Analyse_data/fitted_current.json', 'r') as f:
        fitted_current = json.load(f)

        m = fitted_current[' small-magnet '].get('m')[0]
        c = fitted_current[' small-magnet '].get('c')[0]
    
    return m * current + c 

def mag_current(mag:float) -> float:
    with open('./Analyse_data/fitted_current.json', 'r') as f:
        fitted_current = json.load(f)

        m = fitted_current[' small-magnet '].get('m')[0]
        c = fitted_current[' small-magnet '].get('c')[0]
    
    return (mag - c)/m 

def fit_linear(x: np.ndarray, y: np.ndarray) -> tuple:
    gradient, intercept, r, p, se = linregress(x, y)
    return (gradient, intercept)

def get_g(parameter_address: str):
    with open(parameter_address,"r") as f:
        data = json.load(f)
    
    magnetic_field = np.ndarray([])
    resonance_freq = np.ndarray([])
    for current, obj in data.items():
        mag = current_mag(float(current))
        magnetic_field = np.append(magnetic_field,mag)
    
        frequency = obj["resonance-frequency"]
        resonance_freq = np.append(resonance_freq,frequency)
    
    m,c = fit_linear(resonance_freq,magnetic_field)
    g = m / PLANK_CONSTANT * BOHR_MAGNETON /GHz*mT
    return 1 / g
    

    

# print(find("5.24.csv",'./'))
# for root,dirs,files in os.walk("./"):
#     print(files)
# print(current_list())
# current = current_list()
# current = np.array(current)
# freq, loss_0 = loss(current[0])
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
print(get_g("./fitting_params.json"))