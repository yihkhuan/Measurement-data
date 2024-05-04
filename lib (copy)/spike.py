import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from scipy.optimize import curve_fit
from scipy.stats import linregress
import json

GHZ_UNIT = 1e9

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

def UTM_3D_plot(x: np.ndarray, y: np.ndarray, lossmesh: np.ndarray, ax: plt.Axes, *,
                cmap: str = 'rainbow',  # Colormap for the contour plot
                levels: int = 100,  # Number of contour levels
                vmin: float = None, vmax: float = None,  # Value range for colormap
                cblabel: str = None,  # Label for the colorbar
                xlabel: str = None, ylabel: str = None, title: str = None,  # Axis and title labels
                fontsize: int = 20,  # Font size for labels and title
                ticksize: int = 13,  # Font size for major ticks
                xlim: tuple[float, float] = None, ylim: tuple[float, float] = None,  # Axis limits
                x2label: str = None, y2label: str = None,  # Labels for secondary axes
                x2secx: callable = None, secx2x: callable = None,  # Functions for x2 axis conversion
                y2secy: callable = None, secy2y: callable = None  # Functions for y2 axis conversion
                ):
    """
    This function creates a 3D contour plot with optional customizations and secondary axes.

    Args:
        x: A numpy array of x-coordinates.
        y: A numpy array of y-coordinates.
        lossmesh: A numpy array of loss values.
        ax: A matplotlib axes object.

    Kwargs:
        cmap (str, optional): Colormap for the contour plot (default: 'rainbow').
        levels (int, optional): Number of contour levels (default: 100).
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