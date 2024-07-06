import subprocess
import time

delays = [0, 10, 20, 30, 50, 100]
packet_losses = [0, 2, 6, 8, 12]
network_interface = "ens37"
ssh_target = "root@10.10.10.10"
url_base = "https://10.10.10.10:443/static/file-10.txt"
tftp_url = "tftp://10.10.10.10/file-10.txt"
versions = ["1.1", "2", "3"]

# Adding base tc rule
subprocess.run(f"ssh {ssh_target} 'tc qdisc delete dev ens37 root'", shell=True)
subprocess.run(f"ssh {ssh_target} 'tc qdisc add dev {network_interface} root netem delay 0ms loss 0%'", shell=True)
time.sleep(1)

results_file = 'result/avg_cubic_cubic_output.txt'

subprocess.run(['mkdir', '-p', 'result'])
with open(results_file, 'w') as f:
    f.write("start testing cubic-cubic\n")

for packet_loss in packet_losses:
    tcpdump_file = f"tcpdumps/tcpdump-s_cubic_c_cubic_loss{packet_loss}.pcap"
    tcpdump_process = subprocess.Popen(["sudo", "tcpdump", "-i", network_interface, "-v", "-w", tcpdump_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for delay in delays:
        with open(results_file, 'a') as f:
            f.write(f"--------- {delay}ms delay, {packet_loss}% packet loss-------------\n")
        command = f"ssh {ssh_target} 'tc qdisc replace dev {network_interface} root netem delay {delay}ms loss {packet_loss}%'"
        subprocess.run(command, shell=True)

        for version in versions:
            total_time = 0.0
            for _ in range(3):
                proc = subprocess.run([f"./curl -w '%{{time_total}}' --http{version} -o /dev/null --insecure -s {url_base}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                time_taken = float(proc.stdout.strip())
                total_time += time_taken

            avg_time = total_time / 3.0

            with open(results_file, 'a') as f:
                f.write(f"HTTP {version} : {avg_time} seconds\n")
        time.sleep(1)
        
    tcpdump_process.send_signal(subprocess.signal.SIGINT)
    tcpdump_process.wait()
