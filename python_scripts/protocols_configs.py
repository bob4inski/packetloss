
import pandas as pd
import matplotlib.pyplot as plt
import os

# Directory containing result files
directory = 'result'

# List of files in the directory
file_names = os.listdir(directory)  

# Data structures to store processed data
data_frames = {
    'HTTP1.1': pd.DataFrame(columns=['configuration', 'packet_loss', 'value']),
    'HTTP2': pd.DataFrame(columns=['configuration', 'packet_loss', 'value']),
    'HTTP3': pd.DataFrame(columns=['configuration', 'packet_loss', 'value'])
}

# Process each file
for file_name in file_names:
    # Prepare data structures
    data = {
        'delay': [],
        'packet_loss': [],
        'http_version': [],
        'time': []
    }
    
    # Read file and parse data
    with open(os.path.join(directory, file_name), 'r') as file:
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
            data['http_version'].append(version)
            data['time'].append(time)
    
    # Convert to Pandas DataFrame and process data
    df = pd.DataFrame(data)
    avg_packet_loss = df.groupby(['http_version', 'packet_loss']).mean().reset_index()
    
    # Append data to corresponding DataFrame
    for http_version in ['1.1', '2', '3']:
        version_key = f"HTTP{http_version}"
        filtered_data = avg_packet_loss[avg_packet_loss['http_version'] == http_version]
        for _, row in filtered_data.iterrows():
            data_frames[version_key] = data_frames[version_key]._append({
                'configuration': file_name,
                'packet_loss': row['packet_loss'],
                'value': row['time']
            }, ignore_index=True)

# Plotting
fig, axs = plt.subplots(3, 1, figsize=(15, 15), sharex=True)

for i, (protocol, df) in enumerate(data_frames.items()):
    ax = axs[i]
    for config in df['configuration'].unique():
        config_data = df[df['configuration'] == config]
        ax.plot(config_data['packet_loss'], config_data['value'], marker='o', label=config)
    
    ax.set_title(f'Time vs. Packet Loss for {protocol}')
    ax.set_xlabel('Packet Loss (%)')
    ax.set_ylabel('Time (s)')
    ax.legend(title='Configuration')
    ax.grid(True)

# Adjust layout
plt.tight_layout()
plt.show()
