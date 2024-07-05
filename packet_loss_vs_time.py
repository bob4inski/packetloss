import pandas as pd
import matplotlib.pyplot as plt

with open('result/avg_bbr_bbr_output.txt', 'r') as file:
    lines = file.readlines()

# Prepare data structures
data = {
    'delay': [],
    'packet_loss': [],
    'http_version': [],
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

avg_packet_loss = df.groupby(['http_version','packet_loss']).sum()
# print(avg_packet_loss)
avg_packet_loss = avg_packet_loss.reset_index()
pivot_df = avg_packet_loss.pivot(index='packet_loss', columns='http_version', values='time')

for column in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[column], marker='o', label=column)

plt.xlabel('Packet Loss (%)')
plt.ylabel('Time')
plt.title('Time vs. Packet Loss')
plt.legend(title='HTTP Version')
plt.grid(True)
plt.show()