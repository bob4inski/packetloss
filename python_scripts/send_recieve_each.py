
import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'converted/tcpdump-s_bbr_c_cubic_loss0.pcap.csv'
df = pd.read_csv(csv_file,delimiter=";")

# Define client and server IP addresses
client_ip = '10.10.10.20'
server_ip = '10.10.10.10'
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

# Plot the results using matplotlib
ig, ax = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

# Plot bytes sent on the first subplot
ax[0].plot(bytes_sent_over_time.index, bytes_sent_over_time.values, label='Bytes Sent (Client to Server)')
ax[0].set_ylabel('Bytes Sent')
ax[0].set_title('Bytes Sent Over Time')
ax[0].legend()
ax[0].grid()

# Plot bytes received on the second subplot
ax[1].plot(bytes_received_over_time.index, bytes_received_over_time.values, label='Bytes Received (Server to Client)', color='orange')
ax[1].set_ylabel('Bytes Received')
ax[1].set_xlabel('Time')
ax[1].set_title('Bytes Received Over Time')
ax[1].legend()
ax[1].grid()

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()
