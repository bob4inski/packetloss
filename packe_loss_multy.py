import pandas as pd
import matplotlib.pyplot as plt
import os

file_names = os.listdir('result')  # Assuming all files in 'result' should be plotted
num_files = len(file_names)  # Count the number of files

fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Create a 2x2 grid of subplots
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
    with open(f'result/{file_name}', 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "delay" in line and "packet loss" in line:
            parts = line.split()
            current_delay = int(parts[1].replace('ms', ''))
            current_packet_loss = int(parts[3].replace('%', ''))
        elif "HTTP" in line:
            parts = line.split()
            version = parts[1]
            time = float(parts[3].replace('seconds', ''))
            data['delay'].append(current_delay)
            data['packet_loss'].append(current_packet_loss)
            data['http_version'].append(f"HTTP {version}")
            data['time'].append(time)

    # Convert to Pandas DataFrame and process data
    df = pd.DataFrame(data)
    avg_packet_loss = df.groupby(['http_version', 'packet_loss']).mean()  # Note: Use .mean() for average
    avg_packet_loss = avg_packet_loss.reset_index()
    pivot_df = avg_packet_loss.pivot(index='packet_loss', columns='http_version', values='time')

    # Plot on the current subplot axis
    ax = axs[i]
    for column in pivot_df.columns:
        ax.plot(pivot_df.index, pivot_df[column], marker='o', label=column)
    
    ax.set_xlabel('Packet Loss (%)')
    ax.set_ylabel('Time')
    ax.set_title(f'Time vs. Packet Loss ({file_name})')
    ax.legend(title='HTTP Version')
    ax.grid(True)

# Adjust the layout so the plots do not overlap each other
plt.tight_layout()
plt.show()