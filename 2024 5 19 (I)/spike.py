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
EXPECTED_GRADIENT = 2.0036* BOHR_MAGNETON / PLANK_CONSTANT * mT / GHz

def loss_list(current: float) -> tuple: 
    freq = np.array([])
    loss = np.array([])
    file = "%.3fA.csv" % current
    with open(file, "r") as f:
        data_lines = f.readlines()

    for data in data_lines:
        values = data.split(",")
        freq = np.append(freq,float(values[0]) / GHz)
        loss = np.append(loss,float(values[1]))
    return (freq,loss)

## General control functions
def find_all(subname: str, path = './') -> list:

    result = []
    for root, dirs, files in os.walk(path):
        if root == './':
            for file_name in files:
                if subname in file_name:
                    result.append(file_name)

    return result

def find(name: str, path: str = './'):

    for root, dirs, files in os.walk(path):
        if root == './':
            if name in files:
                return True
            else:
                return False
    pass

def average_loss_list(current: float) -> tuple:
    filenames = []

    loss = np.array([])

    address = "./%.3fA" % (current)
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

def esrcontour(magnet_name, loss_0: np.ndarray, current_list, fitting = False, xlim = (0,0), ylim = (0,0)):
    
    current = np.array(current_list)
    print(current)
    freq = loss_list(current[0])[0]
    # magnetic = 19.713 * current[1:] + 224.92
    magnetic = current_mag(current,magnet_name)
    B, F = np.meshgrid(magnetic,freq)
    lossmesh = np.array([])
    for i in current:
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

        ax.plot(magnetic_field,resonance_freq,"ko", label = "absorption")
        ax.plot(mag_pts, freq_pts, "k--", lw=2)

    cp = ax.contourf(B, F, lossmesh.transpose(), cmap='rainbow', levels=100, zorder=1)
    cb = plt.colorbar(cp,orientation = 'vertical')
    cb.ax.tick_params(labelsize = 16)
    cb.set_label(label="absorption (dB)", fontsize=20)
    if xlim != (0,0):
        ax.set_xlim(xlim)
    else:
        ax.set_xlim(magnetic[0], magnetic[-1])
    if ylim != (0,0):
        ax.set_ylim(ylim)
    else:
        ax.set_ylim(freq[0], freq[-1])
    ax.set_xlabel("magnetic field (mT)",fontsize=20)
    ax.set_ylabel("frequency (GHz)",fontsize=20)
    ax.tick_params(axis='both',which='major',labelsize=13)
    ax.set_title("Contour plot of ESR signal", fontsize = 25)

    xmax, ymax = np.unravel_index(np.argmax(lossmesh), lossmesh.shape)
    ax.plot(magnetic[xmax],freq[ymax],"g+", label = "maximum absorption")
    # print(magnet_name)
    mag2current = lambda x: mag_current(x, magnet_name)
    current2mag = lambda x: current_mag(x , magnet_name)
    # print(magnet_name)
    secax = ax.secondary_xaxis('top', functions=(mag2current,current2mag))
    secax.set_xlabel('current (A)',fontsize=20)
    secax.tick_params(axis='x',which='major',labelsize=13)

    # m = fitted_current[magnet_name].get('m')[0]
    # m,c,*r = fit_linear(magnetic_field, resonance_freq)

    mag_pts = np.arange(300,400)
    # freq_pts = mag_pts * m + c

    # ax.plot(magnetic_field,resonance_freq,"ko")
    # ax.plot(mag_pts, freq_pts, "k--", lw=2, label = "data points")

    ###True Values
    with open("./Analyse_data/fitted.json","r") as g:
        resonator = json.load(g)
    
    resonator_freq = resonator["fitted_data"][0].get('a')[0]

    
    expected_freq = lambda mag: mag * 2.0036 * BOHR_MAGNETON / PLANK_CONSTANT * mT / GHz
    expected_mag = lambda freq: freq / (2.0036 * BOHR_MAGNETON / PLANK_CONSTANT * mT / GHz)
    ax.plot(mag_pts, np.ones(mag_pts.shape[-1]) * resonator_freq, "r--", lw=2, label = "resonance frequency")
    # ax.plot(expected_mag(resonator_freq),resonator_freq,"ro", label = "expected maximum absorption")

    plt.legend()
    plt.tight_layout()
    # magnet_name = magnet_name.replace(magnet_name[-4:],"")
    plt.savefig("./figs/ESR_contour_full_" + magnet_name + ".png")
    pass

def current_list(start: float = 0, end: float = 12):
    currents = np.arange(start*1000,end*1000) / 1000
    current = []
    for i in tqdm(currents):
        finding = find("%.3fA.csv"%i,"./")
        if finding is True:
            current.append(i)
        else:
            pass
    return current
        
def lorentzian_fit(freq:np.ndarray, absorption:np.ndarray, freq_expected: float = None):
    if freq_expected:
        diff_array = np.abs(freq - freq_expected)
        index = np.where(diff_array == np.abs(freq - freq_expected).min())[0][0]
    else:
        index = np.where(absorption == absorption.max())[0][0]
    max_freq = freq[index]
    # print(max_freq)
    # plt.figure()
    # plt.scatter(freq,absorption)
    # plt.show()
    #curve fitting
    dw = 200
    popt,_ = curve_fit(lorentz, freq[index - dw:index + dw + 1], absorption[index - dw:index + dw + 1],
                       p0=(2,.02,max_freq,-0.1))
    plt.figure()
    plt.plot(freq[index:index], absorption[index:index], marker = "+")
    print(absorption[index])
    Al,b,a,offsetl = popt
    return (Al,b,a,offsetl)

def lorentz(x: np.ndarray, Al:float, b:float, a:float, offset:float) -> np.ndarray:
    return Al / np.pi * (b / ((x - a)**2 + b**2))

def UTM_2D_plot(x:np.ndarray, y:np.ndarray, title:str, xlabel:str, ylabel:str, filename:str, canvas:tuple = None):
    plt.title(title, fontsize = 20)
    plt.ylabel(ylabel, fontsize=20)
    plt.xlabel(xlabel, fontsize=20)
    plt.xticks(fontsize = 13)
    plt.yticks(fontsize = 13)
    plt.plot(x,y)
    plt.subplots_adjust(bottom=0.2,left=0.2)
    plt.savefig("./figs/" + filename)
    # plt.show()

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
            resonance_freq = current_mag(name, magnet_name) * EXPECTED_GRADIENT


            params = lorentzian_fit(freq, absorption)

            plt.scatter(freq,absorption)
        except:
            print("fitting failed for " + str(name))
            continue

        dict_list.update({"%.3f" % (name): {
                            "amplitude"           : params[0],
                            "bandwidth"           : params[1],
                            "resonance-frequency" : params[2],
                            "offset"              : params[3]  
                            }
                        })
        
        l = lorentz(freq,*params)

        # fig[filenames.index(name)], ax[filenames.index(name)] = plt.subplots()
        UTM_2D_plot(freq,l,
            title = "signal fitting, B = %.3f mT" % current_mag(name, magnet_name),
            xlabel = "frequency, GHz",
            ylabel = "absorption",
            filename = "fitting %.3fA.png" % (name),
            )

        plt.show()
        
    with open("fitting_params.json", "w") as outfile:
        json.dump(dict_list,outfile)

def current_decider(magnet_name):
    
    with open("./Analyse_data/fitted.json","r") as g:
        resonator = json.load(g)

    resonator_freq = resonator["fitted_data"][0].get('a')[0]

    # print((resonator_freq * 1e-3)/ EXPECTED_GRADIENT)
    output = (mag_current((resonator_freq - 50 * 1e-3)/ (EXPECTED_GRADIENT), magnet_name), mag_current((resonator_freq + 50 * 1e-3)/ (EXPECTED_GRADIENT), magnet_name))

    return output

def current_diff(magnet_name):
    with open('./Analyse_data/current.json', 'r') as f:
        fitted_current = json.load(f)

        m = fitted_current[magnet_name].get('m')[0]
        
    return (50 * 1e-3)/ EXPECTED_GRADIENT/m