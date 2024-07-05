import csv
import pandas as pd
import matplotlib.pyplot as plt
from scapy.all import rdpcap
from scapy.layers.inet import TCP

def extract_window_size(info):
    if isinstance(info, str) and "Win=" in info:
        start = info.index("Win=") + len("Win=")
        end = info[start:].find(" ")
        if end == -1:  
            return int(info[start:])
        else:
            return int(info[start:start+end])
    return None

csv_file = 'csv/s_bbr_c_bbr_loss0.csv'

df = pd.read_csv(csv_file)
filtered_df = df[df['Protocol'] == "TCP"]
print(filtered_df)

filtered_df = filtered_df.reset_index()  # make sure indexes pair with number of rows
filtered_df['window_size'] = filtered_df['Info'].apply(extract_window_size)
filtered_df = filtered_df.dropna(subset=['window_size'])

timestamps = filtered_df['Time']
window_sizes = filtered_df['window_size']

# # Make timestamps relative to the first timestamp
initial_time = timestamps.min()
relative_timestamps = timestamps - initial_time

plt.figure(figsize=(12, 6))
plt.plot(relative_timestamps, window_sizes, marker='o', linestyle='-')
plt.xlabel('Time (seconds)')
plt.ylabel('TCP Window Size')
plt.title('TCP Window Scaling over Time')
plt.grid(True)
plt.savefig('tcp_window_scaling_plot.png')
plt.show()