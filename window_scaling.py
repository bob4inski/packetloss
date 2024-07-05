
import matplotlib.pyplot as plt
from scapy.all import rdpcap
from scapy.layers.inet import TCP

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) 
# Path to the pcap file
pcap_file = 'tcpdumps/tcpdump-s_bbr_c_bbr_loss0.pcap'

# Read packets from the pcap file
packets = rdpcap(pcap_file)

# Lists to store the captured data
timestamps = []
window_sizes = []

# Parse packets to extract TCP window sizes and their respective timestamps
for packet in packets:
    print("im alive dont kill me")
    if TCP in packet:
        tcp_layer = packet[TCP]
        if hasattr(tcp_layer, 'window'):
            window_size = tcp_layer.window
            timestamp = packet.time
            timestamps.append(timestamp)
            window_sizes.append(window_size)    

# Ensure timestamps are relative, starting from zero
initial_time = min(timestamps)
relative_timestamps = [ts - initial_time for ts in timestamps]

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(relative_timestamps, window_sizes, marker='o', linestyle='-')
plt.xlabel('Time (seconds)')
plt.ylabel('TCP Window Size')
plt.title('TCP Window Scaling over Time')
plt.grid(True)

# Save the plot to a file and display it
plt.savefig('tcp_window_scaling.png')
plt.show()
