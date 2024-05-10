import spike as sp
import os

def find_all(subname: str, path = './') -> list:
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

# filenames = find_all(".csv")

# magnet_name = ' 0mm '
# for name in filenames:
#    mag = name.replace(name[-6:], "")
#    current = sp.mag_current(float(mag), magnet_name)
#    current = "%.2f" % current
# #    os.system("cd")
#    os.system(f"copy .\{name} .\{current}A.txt")
#    os.system(f"move .\{name} .\ori\{name}")
filenames = find_all("A.txt")

for name in filenames:
   new_name =  name.replace(name[-3:], "csv")
   os.system(f"move .\{name} .\ori\{new_name}")