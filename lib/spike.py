import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from scipy.optimize import curve_fit
from scipy.stats import linregress
import json

GHZ_UNIT = 1e9
MT_UNIT = 1e-3
PLANK_CONSTANT = 6.626e-34
BOHR_MAGNETON = 9.27e-24


## General control functions
def find_all(subname: str, path: str = "./") -> list:
  """
  Finds all folders containing the substring 'subname' at the given path.

  Args:
      name: The substring to search for in folder names.
      path: The directory to search at.

  Returns:
      A list of full paths to folders containing the substring 'name'.
  """
  result = []
  for root, dirs, files in os.walk(path):
    if root == './':
        for file_name in files:
            if subname in file_name:
                result.append(file_name)

  return result

def find(name: str, path: str = './'):
    """
    Find if folders having a particular 'name' at the given path exists.

    Args:
        name: The substring to search for in folder names.
        path: The directory to search at.

    Returns:
        Boolean logic of the the search result.
    """
    for root, dirs, files in os.walk(path):
        if root == './':
            if name in files:
                return True
            else:
                return False
    pass

def split_data(filename: str, delimiter: str = ""):
    # Read data lines
    with open(filename, "r") as f:
        data_lines = f.readlines()

    # Separate data blocks
    data_blocks = []
    current_block = []
    for line in data_lines:
        if line.strip() == "":  # Check for empty line
            # print(current_block)
            if current_block:
                data_blocks.append(current_block)
            current_block = []
        else:
            current_block.append(line.strip())  # Strip trailing newline
    if current_block:
        data_blocks.append(current_block)
    name = []
    x = np.array([])
    y = np.array([])
    #Converting data block into Ndarray format
    for i in range(len(data_blocks)):
        # Choose block to plot (modify index for different blocks)
        chosen_block = data_blocks[i]

        # Extract data points (adapt based on your actual data format)
        
        x_data = np.array([])
        y_data = np.array([])
        for line in chosen_block:
            if delimiter != "":
                values = line.split(delimiter)
            else:
                values = line.split()# Assuming data is space-separated
            try:
                x_data = np.append(x_data, float(values[0]))
                y_data = np.append(y_data, float(values[1]))
            except:
                continue

        name.append(chosen_block[0])
        x = np.append(x, x_data)
        x = np.reshape(x,(len(data_blocks),-1))
        y = np.append(y, y_data)
        y = np.reshape(y,(len(data_blocks),-1))

    return (name, x, y)

def split_datablock(filename: str, delimiter: str = "") -> tuple[list, np.ndarray, np.ndarray]:
  """
  This function reads a data file containing multiple data blocks, 
  separated by empty lines. It extracts data points (assuming two values 
  per line, first being x and second being y) and stores them in separate 
  NumPy arrays for each block. Additionally, it retrieves the names 
  (assumed to be from the first line of each block) and stores them in a list.

  Args:
      filename: Path to the data file.
      delimiter: Optional delimiter used to separate values within a line 
                 (defaults to empty string, assuming space-separated data).

  Returns:
      A tuple containing three elements:
          - name: List of names for each data block.
          - x: NumPy array containing the x-data points for each block.
          - y: NumPy array containing the y-data points for each block.
  """

  # Read data lines
  with open(filename, "r") as f:
    data_lines = f.readlines()

  # Separate data blocks
  data_blocks = []
  current_block = []
  for line in data_lines:
    if not line.strip():  # Check for empty line (more efficient)
      if current_block:
        data_blocks.append(current_block)
      current_block = []
    else:
      current_block.append(line.strip())

  if current_block:
    data_blocks.append(current_block)

  # Extract data points and names
  name, x_all, y_all = [], [], []
  for block in data_blocks:
    x_data, y_data = [], []
    for line in block:
      values = line.split(delimiter) if delimiter else line.split()
      try:
        x_data.append(float(values[0]))
        y_data.append(float(values[1]))
      except:
        pass  # Skip lines with conversion errors

    name.append(block[0])
    x_all.append(x_data)
    y_all.append(y_data)

  # Convert data lists to NumPy arrays
  x = np.array(x_all)
  y = np.array(y_all)

  return name, x, y

## ESR control functions
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

def current_list(start: float = 0, end: float = 15):

    currents = np.arange(start*100,end*100) / 100
    current = []
    for i in tqdm(currents):
        finding = find("%.2fA.csv"%i,"./")
        if finding is True:
            current.append(i)
        else:
            pass
    return current

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

def lorentz(x: np.ndarray, Al:float, b:float, a:float, offsetl:float) -> np.ndarray:
    return Al / np.pi * (b / ((x - a)**2 + b**2)) + offsetl

lorentz = lambda x, Al, b, a, offsetl: Al / np.pi * (b / ((x - a)**2 + b**2)) + offsetl

def UTM_3D_plot(x: np.ndarray, y: np.ndarray, lossmesh: np.ndarray, ax, 
                colourbar_label: str, xlabel: str, ylabel: str, title: str,
                sec_xlabel: str, x2secx, secx2x, 
                sec_ylabel: str, y2secy, secy2y,
                ):
    cp = ax.contourf(x, y, lossmesh.transpose(), cmap='rainbow', levels=100, zorder=1, vmin = 0)
    cb = plt.colorbar(cp,orientation = 'vertical')
    cb.ax.tick_params(labelsize = 16)
    cb.set_label(label= colourbar_label, fontsize=20)

    ax.set_xlabel(xlabel,fontsize=20)
    ax.set_ylabel(ylabel,fontsize=20)
    ax.tick_params(axis='both',which='major',labelsize=13)
    ax.set_title(title, fontsize = 25)
    


    secax = ax.secondary_xaxis('top', functions=(x2secx,secx2x))
    secax.set_xlabel('',fontsize=20)
    secax.tick_params(axis='x',which='major',labelsize=13)

    secay = ax.secondary_xaxis('right', functions=(y2secy,secy2y))
    secax.set_xlabel('current (A)',fontsize=20)
    secax.tick_params(axis='x',which='major',labelsize=13)

def line_on_3D(fig, ax) -> tuple: 

    pass

self.magnet()
self.mag_min()
self.mag_max()
self.freq_min()
self.freq_max()