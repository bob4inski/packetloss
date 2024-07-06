import csv
import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'converted/tcpdump-s_bbr_c_bbr_loss6.pcap.csv'

df = pd.read_csv(csv_file,delimiter=";")
print(df)
df.rename(columns={'_ws.col.Time': 'Time', '_ws.col.Source': 'SRC',"_ws.col.Info":"Info","_ws.col.Length":"Length",'_ws.col.Protocol': 'Protocol'}, inplace=True)
filtered_df = df[(df['Protocol'] == "TCP") | (df['Protocol'] == "QUIC") | (df['Protocol'] == "TLSv1.3")]



out_df = filtered_df[filtered_df['SRC'] == "10.10.10.10"]
in_df = filtered_df[filtered_df['SRC'] == "10.10.10.20"]
fig, axs = plt.subplots(1, 2, figsize=(15, 10))  # Create a 2x2 grid of subplots
axs = axs.ravel()

for i, df in enumerate([out_df,in_df]):
    df = df.reset_index()
    timestamps = df['Time']
    window_sizes = df['Length']
    initial_time = timestamps.min()
    relative_timestamps = timestamps - initial_time
    ax = axs[i]
    df = df.reset_index()
    pivot_df = df.pivot(columns='Protocol', values='Length')
    for column in pivot_df.columns:
        ax.plot(pivot_df.index, pivot_df[column], marker='o', label=column)

    ax.plot(relative_timestamps,window_sizes, marker='o', linestyle='-')
    ax.set_xlabel('Time')
    ax.set_ylabel('Packet lenght')
    ax.set_title(f'aboba')
    ax.legend(title='Protocol')
    ax.grid(True)
plt.show()