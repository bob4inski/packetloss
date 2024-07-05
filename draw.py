import pandas as pd
import matplotlib.pyplot as plt

import os

file_names = os.listdir('result')  # Assuming all files in 'result' should be plotted
num_files = len(file_names)  # Count the number of files

fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Create a 2x2 grid of subplots
axs = axs.ravel()  # Flatten the array of axes for easy iteration

for i, file_name in enumerate(file_names):
    data = {
        'delay': [],
        'packet_loss': [],
        'http_version': [],
        'time': []
    }

    with open(f'result/{file_name}', 'r') as file:
        lines = file.readlines()
    # Parse file content
        current_delay = 0
        current_packet_loss = 0
        for line in lines:
            if "delay" in line and "packet loss" in line:
                parts = line.split()
                print(parts)
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

        # Convert to Pandas DataFrame
        df = pd.DataFrame(data)
        # df = df.reset_index()
        ax = axs[i]
        pivot_df = df.pivot(columns='http_version', values='time')
       

        for http_version in pivot_df.columns:
            ax.plot(pivot_df[http_version], marker='o',label=http_version)
            ax.set_title(f'Response Time vs Network Delay {file_name}')
            ax.set_xlabel('')
            ax.set_ylabel('Average Response Time (seconds)')
            ax.legend(title='HTTP Version')
            # plt.grid(True)

        vertical_lines = {}
        packet_losses = [0, 2, 6, 8, 12]

        for i in range(5):
            vertical_lines[i*18] = packet_losses[i]

        for x_pos, label in vertical_lines.items():
            ax.axvline(x=x_pos, color='red', linestyle='dashed')  # Разделяющая линия
          #  ax.text(x_pos, 12, label, color='black', horizontalalignment='left')  # Текстовая подпись

plt.tight_layout()
plt.show()
    # # Plotting the DataFrame  
    # plt.figure(figsize=(12, 6))
    # for http_version in pivot_df.columns:
    #     plt.plot(pivot_df.index, pivot_df[http_version], marker='o', label=http_version)
