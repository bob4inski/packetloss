
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file into a DataFrame
# Assuming the CSV file has columns: frame.number, ip.src, ip.dst, frame.len, frame.time_relative, etc.
csv_file = 'converted/tcpdump-s_bbr_c_cubic_loss0.pcap.csv'
df = pd.read_csv(csv_file,delimiter=";")

# Define client and server IP addresses
client_ip = '10.10.10.20'
server_ip = '10.10.10.10'

# Filter client-to-server and server-to-client packets
df.columns = ['No', 'Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info']
# Filter client-to-server and server-to-client packets
client_to_server = df[(df['Source'] == client_ip) & (df['Destination'] == server_ip)]
server_to_client = df[(df['Source'] == server_ip) & (df['Destination'] == client_ip)]

# Convert 'frame.time_relative' to datetime
client_to_server['time'] = pd.to_datetime(client_to_server['Time'], unit='s')
server_to_client['time'] = pd.to_datetime(server_to_client['Time'], unit='s')

# Calculate bytes sent and received over time intervals
time_interval = '1S'  # 1 second intervals - adjust as needed
client_to_server['bytes_sent'] = client_to_server['Length']
server_to_client['bytes_received'] = server_to_client['Length']

bytes_sent_over_time = client_to_server.set_index('time').resample(time_interval)['bytes_sent'].sum()
bytes_received_over_time = server_to_client.set_index('time').resample(time_interval)['bytes_received'].sum()

# Compute the upload and download speeds (in bytes per second)
upload_speed = bytes_sent_over_time / pd.to_timedelta(time_interval).total_seconds()
download_speed = bytes_received_over_time / pd.to_timedelta(time_interval).total_seconds()

# Plot the results using subplots in matplotlib
fig, ax = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

# Plot upload speed on the first subplot
ax[0].plot(upload_speed.index, upload_speed.values, label='Upload Speed (Bytes/sec)')
ax[0].set_ylabel('Upload Speed (Bytes/sec)')
ax[0].set_title('Upload Speed Over Time')
ax[0].legend()
ax[0].grid()

# Plot download speed on the second subplot
ax[1].plot(download_speed.index, download_speed.values, label='Download Speed (Bytes/sec)', color='orange')
ax[1].set_ylabel('Download Speed (Bytes/sec)')
ax[1].set_xlabel('Time')
ax[1].set_title('Download Speed Over Time')
ax[1].legend()
ax[1].grid()

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
