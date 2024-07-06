import pandas as pd
import matplotlib.pyplot as plt
import os

file_names = os.listdir('tftp')  # Assuming all files in 'result' should be plotted
num_files = len(file_names)  # Count the number of files

fig, axs = plt.subplots(2, 2, figsize=(10, 10))  # Create a 2x2 grid of subplots
axs = axs.ravel()  # Flatten the array of axes for easy iteration

for i, file_name in enumerate(file_names):
    # Prepare data structures
    data = {
        'delay': [],
        'packet_loss': [],
        'http_version': [],
        'time': []
    }
    
    # Read file and parse data
    with open(f'tftp/{file_name}', 'r') as file:
        lines = file.readlines()

# Prepare data structures
    data = {
        'delay': [],
        'packet_loss': [],
        'protocol': [],
        'time': []
    }

# Parse file content
    current_delay = 0
    current_packet_loss = 0
    for line in lines:
        if "delay" in line and "packet loss" in line:
            parts = line.split()
            print(parts)
            current_delay = int(parts[1].replace('ms', ''))
            current_packet_loss = int(parts[3].replace('%', ''))

        elif "TFTP" in line:
            parts = line.split()
            
            time = float(parts[2].replace('seconds', ''))
            data['delay'].append(current_delay)
            data['packet_loss'].append(current_packet_loss)
            data['protocol'].append(f"TFTP")
            data['time'].append(time)

# Convert to Pandas DataFrame
    df = pd.DataFrame(data)
    print(df)
    avg_packet_loss = df.groupby(['protocol','packet_loss']).mean()
    print(avg_packet_loss)
    avg_packet_loss = avg_packet_loss.reset_index()
    pivot_df = avg_packet_loss.pivot(index='packet_loss', columns='protocol', values='time')
    ax = axs[i]
    for column in pivot_df.columns:
        ax.plot(pivot_df.index, pivot_df[column], marker='o', label=column)

    ax.set_xlabel('Packet Loss (%)')
    ax.set_ylabel('Time')
    ax.set_title(f'Time vs. Packet Loss ({file_name})')
    ax.legend(title='TFTP')
    ax.grid(True)
    # ax.set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()