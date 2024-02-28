import os
import numpy as np

def list_txt_files():
   """Lists all .txt files in the same directory as the script."""
   script_dir = os.path.dirname(__file__)  # Get the current script's directory
   txt_files = [file for file in os.listdir(script_dir) if file.endswith(".csv")]
   return txt_files



plots = {}
txt_files = list_txt_files()

for file in txt_files:
    with open(file, "r") as f:
        data_lines = f.readlines()     

    
    x_axis = []
    y_axis = []
    for line in data_lines:
        # print(line)
        data = line.strip().split(", ")
        x_axis.append(float(data[0]))
        y_axis.append(float(data[1]))

    plots[file] = {}
    plots[file]['x_axis'] = np.array(x_axis)
    plots[file]['y_axis'] = np.array(y_axis)
import matplotlib.pyplot as plt
fig,axs = plt.subplots(4,1,figsize=(10,8))

# x = plots['before_magnet.csv']['x_axis'] * 1e-9
# y = plots['before_magnet.csv']['y_axis']
# axs[0].plot(x,y,label='before magnet')
# axs[0].xaxis.set_label_coords(1.05, -0.025)
# axs[0].set(xlabel = ("Frequency, GHz"), ylabel =('Signal power, dB'))
# axs[0].legend()

# x = plots['after_magnet_1.csv']['x_axis']* 1e-9
# y = plots['after_magnet_1.csv']['y_axis']
# axs[1].plot(x,y,label='after magnet 1')
# axs[1].xaxis.set_label_coords(1.05, -0.025)
# axs[1].set(xlabel = ("Frequency, GHz"), ylabel =('Signal power, dB'))
# axs[1].legend()

# x = plots['after_magnet_2.csv']['x_axis']* 1e-9
# y = plots['after_magnet_2.csv']['y_axis']
# axs[2].plot(x,y,label='after magnet 2')
# axs[2].xaxis.set_label_coords(1.05, -0.025)
# axs[2].set(xlabel = ("Frequency, GHz"), ylabel =('Signal power, dB'))
# axs[2].legend()

# x = plots['after_magnet_2.csv']['x_axis']* 1e-9
# y = plots['after_magnet_2.csv']['y_axis'] - plots['after_magnet_1.csv']['y_axis']
# axs[3].plot(x,y,label='after magnet 2')
# axs[3].xaxis.set_label_coords(1.05, -0.025)
# axs[3].set(xlabel = ("Frequency, GHz"), ylabel =('Signal power, dB'))
# axs[3].legend()
# plt.savefig("results")
# plt.show()
reference_data = ["finger.csv", "no magnet.csv","1mm between.csv", "big magnet.csv"]
txt_files = list(set(txt_files) - set(reference_data) - {"nothing.csv"})
print(txt_files)
index = 0
for file in txt_files:
    index = txt_files.index(file)
    reference = reference_data[3]
    

    x = plots[reference]['x_axis'] * 1e-9
    y = plots[file]['y_axis'] - plots[reference]['y_axis']
    
    axs[index].plot(x,y,label=file)
    axs[index].set(xlabel = ("Frequency, GHz"), ylabel =('Signal power'))
    axs[index].xaxis.set_label_coords(1.05, -0.025)
    axs[index].legend()
    index = index + 1


plt.show()
