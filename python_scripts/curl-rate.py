import subprocess
import time


limits = [100, 500, 1024, 10240]
versions = ["1.1", "2", "3"]

url_base = "https://10.10.10.10:443/static/file-10.txt"
results_file = 'result/curl_reate-limit.txt'

subprocess.run(['mkdir', '-p', 'result'])
with open(results_file, 'w') as f:
    f.write("start testing rate-limit\n")


tcpdump_file = f"tcpdumps/curl-rate-limit.pcap"
tcpdump_process = subprocess.Popen(["sudo", "tcpdump", "-i", "ens37", "-v", "-w", tcpdump_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

for limit in limits:
    with open(results_file, 'a') as f:
        f.write(f"--------- {limit} rate limit-------------\n")

    with open(results_file, 'a') as f:
        for version in versions:
            total_time = 0.0
            for _ in range(3):
                proc = subprocess.run([f"./curl  --http{version} -o /dev/null --limit-rate {limit}k --insecure -s {url_base}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                time_taken = float(proc.stdout.strip())
                total_time += time_taken

            avg_time = total_time / 3.0

            with open(results_file, 'a') as f:
                f.write(f"HTTP {version} : {avg_time} seconds\n")
    time.sleep(1)
    
tcpdump_process.send_signal(subprocess.signal.SIGINT)
tcpdump_process.wait()
