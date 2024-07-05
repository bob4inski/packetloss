import csv
import pandas as pd
import matplotlib.pyplot as plt

def extract_window_size(info):
    if isinstance(info, str) and "Win=" in info:
        start = info.index("Win=") + len("Win=")
        end = info[start:].find(" ")
        if end == -1:  
            return int(info[start:])
        else:
            return int(info[start:start+end])
    return None

csv_file = '../converted/tcpdump-s_bbr_c_bbr_loss6.pcap.csv'

df = pd.read_csv(csv_file,delimiter=";")
df.rename(columns={'_ws.col.Time': 'Time', '_ws.col.Source': 'SRC',"_ws.col.Info":"Info",'_ws.col.Protocol': 'Protocol'}, inplace=True)
filtered_df = df[df['Protocol'] == "TCP"]

out_df = filtered_df[filtered_df['SRC'] == "10.10.10.10"]
in_df = filtered_df[filtered_df['SRC'] == "10.10.10.20"]
fig, axs = plt.subplots(1, 2, figsize=(15, 10))  # Create a 2x2 grid of subplots
axs = axs.ravel()  # Flatten the array of axes for easy iteration

for i, df in enumerate([out_df,in_df]):
    df = df.reset_index()  # make sure indexes pair with number of rows
    df['window_size'] = filtered_df['Info'].apply(extract_window_size)
    df = df.dropna(subset=['window_size'])

    timestamps = df['Time']
    window_sizes = df['window_size']
    # # Make timestamps relative to the first timestamp
    initial_time = timestamps.min()
    relative_timestamps = timestamps - initial_time
    ax = axs[i]

    ax.plot(relative_timestamps,window_sizes, marker='o', linestyle='-')
    ax.set_xlabel('X')
    ax.set_ylabel('Time')
    ax.set_title(f'Time')
plt.show()