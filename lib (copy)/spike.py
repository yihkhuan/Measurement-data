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
