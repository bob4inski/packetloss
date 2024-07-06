
import pandas as pd
import matplotlib.pyplot as plt
import os

file_names = os.listdir('comparse')  # Assuming all files in 'comparse' should be plotted
num_files = len(file_names)  # Count the number of files

# Prepare a figure
fig, ax = plt.subplots(figsize=(15, 10))

# Data structure to store the data from all files
all_data = {}

for file_name in file_names:
    # Prepare data structures
    data = {
        'delay': [],
        'packet_loss': [],
        'http_version': [],
        'time': []
    }
    
    # Read file and parse data
    with open(f'comparse/{file_name}', 'r') as file:
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

    # Store the processed data
    all_data[file_name] = pivot_df

# Get the list of unique files
file1, file2 = file_names[:2]

# Ensure that we have exactly two files for comparison
if len(file_names) >= 2:
    # Get the data for the two files
    df1 = all_data[file1]
    df2 = all_data[file2]

    # Align the indices by reindexing
    common_packet_loss = df1.index.intersection(df2.index)
    df1 = df1.reindex(common_packet_loss)
    df2 = df2.reindex(common_packet_loss)

    # Calculate the percentage differences and plot
    for column in df1.columns:
        if column in df2.columns:
            percentage_diff = (df2[column] - df1[column]) / df1[column] * 100
            ax.plot(common_packet_loss, percentage_diff, marker='o', label=f'{column} ({file2} vs {file1})')

    ax.set_xlabel('Packet Loss (%)')
    ax.set_ylabel('Percentage Difference (%)')
    ax.set_title('Percentage Difference in Time for Various Packet Loss Rates')
    ax.legend(title='HTTP Version')
    ax.grid(True)
else:
    print("Insufficient files for comparison. Please ensure there are at least two files in the 'comparse' directory.")

# Adjust the layout so the plots do not overlap each other
plt.tight_layout()
plt.show()
