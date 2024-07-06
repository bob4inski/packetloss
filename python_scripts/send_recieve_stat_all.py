
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Define the path to the directory containing the CSV files
directory = 'converted'

# Define the client and server IP addresses
client_ip = '10.10.10.20'
server_ip = '10.10.10.10'

# Define a pattern to extract parameters from filenames
pattern = r"tcpdump-s_(?P<sender>[a-zA-Z0-9]+)_c_(?P<receiver>[a-zA-Z0-9]+)_loss(?P<loss>\d+)\.pcap\.csv"

# Initialize a dictionary to store data for each combination
data_dict = {}

# Loop through the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        match = re.match(pattern, filename)
        if match:
            sender = match.group('sender')
            receiver = match.group('receiver')
            loss = match.group('loss')

            # Read the CSV file
            csv_file = os.path.join(directory, filename)
            df = pd.read_csv(csv_file, delimiter=";")

            # Rename columns for easier reference
            df.columns = ['No', 'Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info']

            # Filter client-to-server and server-to-client packets
            client_to_server = df[(df['Source'] == client_ip) & (df['Destination'] == server_ip)]
            server_to_client = df[(df['Source'] == server_ip) & (df['Destination'] == client_ip)]

            # Calculate the bytes sent and received over time
            client_to_server['time'] = pd.to_datetime(client_to_server['Time'])
            server_to_client['time'] = pd.to_datetime(server_to_client['Time'])

            client_to_server['bytes_sent'] = client_to_server['Length']
            server_to_client['bytes_received'] = server_to_client['Length']

            bytes_sent_over_time = client_to_server.groupby('time')['bytes_sent'].sum()
            bytes_received_over_time = server_to_client.groupby('time')['bytes_received'].sum()
            
            # Combine sender and receiver to a single key
            key = f"s_{sender}_c_{receiver}"

            # Initialize if the key does not exist
            if key not in data_dict:
                data_dict[key] = []

            # Store the results with their respective loss values
            data_dict[key].append((loss, bytes_sent_over_time, bytes_received_over_time))

# Plot the results
for key, values in data_dict.items():
    fig, axs = plt.subplots(2, 1, figsize=(12, 12), sharex=True)
    
    for loss, bytes_sent_over_time, bytes_received_over_time in values:
        # Plot bytes sent on the first subplot
        axs[0].plot(bytes_sent_over_time.index, bytes_sent_over_time.values, label=f'Loss {loss}% Bytes Sent (Client to Server)')
        
        # Plot bytes received on the second subplot
        axs[1].plot(bytes_received_over_time.index, bytes_received_over_time.values, label=f'Loss {loss}% Bytes Received (Server to Client)')
    
    # Set labels, titles, legends, and grid
    axs[0].set_ylabel('Bytes Sent')
    axs[0].set_title(f'Bytes Sent Over Time for {key}')
    axs[0].legend()
    axs[0].grid()

    axs[1].set_ylabel('Bytes Received')
    axs[1].set_xlabel('Time')
    axs[1].set_title(f'Bytes Received Over Time for {key}')
    axs[1].legend()
    axs[1].grid()

    # Adjust layout
    plt.tight_layout()

    # Show the plots
    plt.show()
