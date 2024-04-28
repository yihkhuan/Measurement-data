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
    ##Plotting
    fig, ax = plt.subplots()
    if fitting == True:
        with open("./fitting_params.json","r") as f:
            data = json.load(f)
        
        magnetic_field = np.array([])
        resonance_freq = np.array([])
        for current, obj in data.items():
            mag = current_mag(float(current), magnet_name)
            magnetic_field = np.append(magnetic_field,mag)
        
            frequency = obj["resonance-frequency"]
            resonance_freq = np.append(resonance_freq,frequency)


        m,c,*r = fit_linear(magnetic_field, resonance_freq)

        mag_pts = np.arange(300,400)
        freq_pts = mag_pts * m + c

        ax.plot(magnetic_field,resonance_freq,"ko")
        ax.plot(mag_pts, freq_pts, "k--", lw=2)

    cp = ax.contourf(B, F, lossmesh.transpose(), cmap='rainbow', levels=100, zorder=1, vmin = 0)
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
    ax.set_title("Contour plot of ESR signal", fontsize = 25)
    # print(magnet_name)
    mag2current = lambda x: mag_current(x, magnet_name)
    current2mag = lambda x: current_mag(x , magnet_name)
    # print(magnet_name)
    secax = ax.secondary_xaxis('top', functions=(mag2current,current2mag))
    secax.set_xlabel('current (A)',fontsize=20)
    secax.tick_params(axis='x',which='major',labelsize=13)

    # m = fitted_current[magnet_name].get('m')[0]
    m,c,*r = fit_linear(magnetic_field, resonance_freq)

    mag_pts = np.arange(300,400)
    freq_pts = mag_pts * m + c

    ax.plot(magnetic_field,resonance_freq,"ko")
    ax.plot(mag_pts, freq_pts, "k--", lw=2)

    ###True Values
    with open("./Analyse_data/fitted.json","r") as g:
        resonator = json.load(g)
    
    resonator_freq = resonator["fitted_data"][0].get('a')[0]

    
    expected_freq = lambda mag: mag * 2.0036 * BOHR_MAGNETON / PLANK_CONSTANT * mT / GHz
    expected_mag = lambda freq: freq / (2.0036 * BOHR_MAGNETON / PLANK_CONSTANT * mT / GHz)
    ax.plot(mag_pts, expected_freq(mag_pts), "r--", lw=2)
    ax.plot(expected_mag(resonator_freq),resonator_freq,"ro")

    plt.tight_layout()
    # magnet_name = magnet_name.replace(magnet_name[-4:],"")
    plt.savefig("./figs/ESR_contour_full_" + magnet_name + ".png")
    pass

def current_list(start: float = 0, end: float = 6):
    currents = np.arange(start*100,end*100) / 100
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
    dw = 5
    popt,_ = curve_fit(lorentz, freq[index-5:index+5], absorption[index-5:index+5],p0=(.5,.001,max_freq,-.2))
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
    result = linregress(x, y)
    return (result.slope, result.intercept, result.stderr, result.intercept_stderr)

def get_g(magnet_name, parameter_address: str = './fitting_params.json'):
    with open(parameter_address,"r") as f:
        data = json.load(f)
    
    magnetic_field = np.array([])
    resonance_freq = np.array([])
    for current, obj in data.items():
        mag = current_mag(float(current), magnet_name)
        magnetic_field = np.append(magnetic_field,mag)
    
        frequency = obj["resonance-frequency"]
        resonance_freq = np.append(resonance_freq,frequency)

    m,c,err,serr = fit_linear(magnetic_field, resonance_freq)
    print(err)
    print(serr)

    g = m * GHz / mT * PLANK_CONSTANT / BOHR_MAGNETON
    dg = err * GHz / mT * PLANK_CONSTANT / BOHR_MAGNETON
    print("y-intercept at",end=" ")
    print(c)
    print("x-intercept at",end=" ")
    print(-c/m)
    return g, dg
    
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

def get_resonator_params(filenames: list, loss_0, magnet_name):
    dict_list = {}

    for name in filenames:
        freq, loss_ave = loss_list(name)
        absorption = loss_0 - loss_ave
        try:
            params = lorentzian_fit(freq, absorption)
        except:
            print("fitting failed for " + str(name))
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
        
        UTM_2D_plot(freq,l,
                    title = "signal fitting, B = %.2f mT" % current_mag(name, magnet_name),
                    xlabel = "frequency, GHz",
                    ylabel = "absorption",
                    filename = "fitting %.2fA.png" % (name),
                    )
        
    with open("fitting_params.json", "w") as outfile:
        json.dump(dict_list,outfile)

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
# print(get_g("./fitting_params.json"))
magnet = ' double-magnet '
# esrcontour(' double-magnet ')
esrcontour(magnet, True, xlim = (320,340), ylim=(9,10.4))
# print(mag_current(331,' double-magnet '))
# freq, loss0 = loss_list(0.41)
# filename = current_list(4.6,5)
# filename.append(5.15)
# get_resonator_params(filename, loss0, magnet)
print(get_g(magnet))

print(current_mag(6, magnet))