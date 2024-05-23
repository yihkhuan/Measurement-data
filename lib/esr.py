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
EXPECTED_GRADIENT = 2.0036 * BOHR_MAGNETON / PLANK_CONSTANT * MT_UNIT / GHZ_UNIT


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
        if root == "./":
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
    # os.chdir(path)

    for root, dirs, files in os.walk(path):
        if root == "./":
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
#   print(len(x_all[0]))
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
    find_all("A.csv")
    currents = np.arange(start*100,end*100) / 100
    current = []
    for i in tqdm(currents):
        finding = find("%.2fA.csv"%i,"./")
        if finding is True:
            current.append(i)
        else:
            pass
    return current

def esr_contour(magnetic_field, freq, lossmesh, fitting = False, xlim = (0,0), ylim = (0,0)):
    """
        This function turns the data into a 3D plot to locate the ESR signal.

        Args:
            filename: Path to the data file.
            delimiter: Optional delimiter used to separate values within a line 
                        (defaults to empty string, assuming space-separated data).
            lossmesh: B- rows and F- columns

        Returns:
            A tuple containing three elements:
                - name: List of names for each data block.
                - x: NumPy array containing the x-data points for each block.
                - y: NumPy array containing the y-data points for each block.
    """

    B, F = np.meshgrid(magnetic_field,freq)
    # lossmesh = np.reshape(lossmesh,(-1,freq.shape[-1]))
    ##Plotting
    fig, ax = plt.subplots()
    try:
        with open("./fitting_params.json","r") as f:
            data = json.load(f)
        
        magnetic_field = np.array([])
        resonance_freq = np.array([])
        for current, obj in data.items():
            mag = current_mag(float(current), magnet_name)
            magnetic_field = np.append(magnetic_field,mag)
        
            frequency = obj["resonance-frequency"]
            resonance_freq = np.append(resonance_freq,frequency)


        parameters = fit_linear(magnetic_field, resonance_freq)

        ax = line_on_3D(ax, linear, parameters,
                    label = "line of resonance",colour="black")
        ax = pts_on_3D(ax, magnetic_field, resonance_freq, 
                    label = "expected highest absorption", colour = "black")
    except:
        pass


    UTM_3D_plot(B, F, lossmesh, ax, esr_lib, secx2x = current_mag, x2secx = mag_current)

    ###True Values
    with open("./Analyse_data/fitted.json","r") as g:
        resonator = json.load(g)
    
    resonator_freq = resonator["fitted_data"][0].get('a')[0]

    ax = line_on_3D(ax, linear, (EXPECTED_GRADIENT,0),
                    label = "expected resonance belt",colour="red")
    ax = pts_on_3D(ax, expected_mag(resonator_freq), resonator_freq, 
                   label = "expected highest absorption", colour = "red")
    
    plt.tight_layout()
    # magnet_name = magnet_name.replace(magnet_name[-4:],"")
    plt.savefig("./figs/ESR_contour_full_" + magnet_name + ".png")
    plt.close()
    pass

# def lorentz(x: np.ndarray, Al:float, b:float, a:float, offsetl:float) -> np.ndarray:
#     return Al / np.pi * (b / ((x - a)**2 + b**2)) + offsetl

def UTM_3D_plot(x: np.ndarray, y: np.ndarray, lossmesh: np.ndarray, ax: plt.Axes, *,
                cmap: str = 'rainbow',  # Colormap for the contour plot
                levels: int = 100,  # Number of contour levels
                fontsize: int = 20,  # Font size for labels and title
                ticksize: int = 13,  # Font size for major ticks
                **kwargs
                ):
    """
    This function creates a 3D contour plot with optional customizations and secondary axes.

    Args:
        x: A numpy array of x-coordinates.
        y: A numpy array of y-coordinates.
        lossmesh: A numpy array of loss values.
        ax: A matplotlib axes object.
        cmap (str, optional): Colormap for the contour plot (default: 'rainbow').
        levels (int, optional): Number of contour levels (default: 100).

    Kwargs:
        vmin (float, optional): Minimum value for the colormap.
        vmax (float, optional): Maximum value for the colormap.
        cblabel (str, optional): Label for the colorbar.
        xlabel (str, optional): Label for the x-axis.
        ylabel (str, optional): Label for the y-axis.
        title (str, optional): Title for the plot.
        fontsize (int, optional): Font size for labels and title (default: 20).
        ticksize (int, optional): Font size for major ticks (default: 13).
        xlim (tuple[float, float], optional): Limits for the x-axis.
        ylim (tuple[float, float], optional): Limits for the y-axis.
        x2label (str, optional): Label for the secondary x-axis.
        y2label (str, optional): Label for the secondary y-axis.
        x2secx (callable, optional): Function to convert primary x-values to secondary x-values.
        secx2x (callable, optional): Function to convert secondary x-values to primary x-values (for interactive panning/zooming).
        y2secy (callable, optional): Function to convert primary y-values to secondary y-values.
        secy2y (callable, optional): Function to convert secondary y-values to primary y-values (for interactive panning/zooming).

    Returns:
        The matplotlib axes object with the plot.
    """

    # Value range for colormap
    vmin = kwargs.get('vmin')
    vmax = kwargs.get('vmin')  

    # Label for the colorbar
    cblabel = kwargs.get('cblabel')

    # Axis and title labels
    xlabel = kwargs.get('xlabel') 
    ylabel = kwargs.get('ylabel')
    title = kwargs.get('title')

    # Axis limits
    xlim = kwargs.get('xlim')
    ylim = kwargs.get('ylim')

    # Labels for secondary axes
    x2label = kwargs.get('x2label')
    y2label = kwargs.get('y2label')

    # Functions for x2 axis conversion
    x2secx = kwargs.get('x2secx')
    secx2x = kwargs.get('secx2x')

    # Functions for y2 axis conversion
    y2secy = kwargs.get('y2secy')
    secy2y = kwargs.get('secy2y')

    # Create the contour plot
    cp = ax.contourf(x, y, lossmesh.transpose(), cmap=cmap, levels=levels, zorder=1,
                    vmin=vmin, vmax=vmax)

    # Set up the colorbar
    if cblabel:
        cb = plt.colorbar(cp, orientation='vertical')
        cb.ax.tick_params(labelsize=16)
        cb.set_label(label=cblabel, fontsize=fontsize)

    # Set up axis labels and title
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=fontsize)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=fontsize)
    if title:
        ax.set_title(title, fontsize=fontsize)
        ax.tick_params(axis='both', which='major', labelsize=ticksize)

    # Set axis limits
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    # Set up secondary x-axis
    if x2label:
        try:
            secax = ax.secondary_xaxis('top', functions=(x2secx, secx2x))
        except:
            secax = ax.secondary_xaxis('top', functions=None)
        secax.set_xlabel(x2label, fontsize=fontsize)
        secax.tick_params(axis='x', which='major', labelsize=ticksize)

    if y2label:
        try:
            secay = ax.secondary_yaxis('right', functions=(y2secy, secy2y))
        except:
            secay = ax.secondary_yaxis('right', functions=None)
        secay.set_xlabel(y2label, fontsize=fontsize)
        secay.tick_params(axis='y', which='major', labelsize=ticksize)

    return ax
    
def line_on_3D(ax, fx, parameters: tuple, start: float =0, stop: float =500, label: str = None, colour: str = None): 

    x = np.arange(start= start, stop= stop)
    y = fx(x, *parameters)
    ax.plot(x, y, marker = "--", lw=2, label = label, color= colour)
    
    return ax

def pts_on_3D(ax, x: np.ndarray, y: np.ndarray, label: str = None, colour: str = None): 

    ax.plot(x, y, marker = "o", lw=2, label = label, color= colour)

    return ax

# def saveData(data, dictionary, keyword):

    
    # dictionary.update({"%.3f" % (name): {
    #                 "amplitude"           : params[0],
    #                 "bandwidth"           : params[1],
    #                 "resonance-frequency" : params[2],
    #                 "offset"              : params[3]  
    #                 }
    #             })
    # pass

#lambda functions
expected_freq   = lambda mag                    : mag * 2.0036 * BOHR_MAGNETON / PLANK_CONSTANT * MT_UNIT / GHZ_UNIT
expected_mag    = lambda freq                   : freq / (2.0036 * BOHR_MAGNETON / PLANK_CONSTANT * MT_UNIT / GHZ_UNIT)
lorentz         = lambda x, Al, b, a, offsetl   : Al / np.pi * (b / ((x - a)**2 + b**2)) + offsetl
linear          = lambda x, m, c                : m * x + c

esr_lib = {
    "vmin"      : 0,
    "cblabel"   : "absorbtion",
    "xlabel"    : "magnetic field strength, mT",
    "ylabel"    : "frequency, GHz",
    "title"     : "Absortion spectra of DPPH",
    "x2label"   : "current, A"
}

# lib = {
#     "variable"  : "current",
#     "description": "teflon",
#     "resonator" :   "UR-4",
#     "magnet"    :   "double-magnet",
#     "data"      :      {{12 :   [4,5,6]},
#                         {13 :   [4,5,6]},
#                         }
# }
# self.magnet()
# self.mag_min()
# self.mag_max()
# self.freq_min()
# self.freq_max()