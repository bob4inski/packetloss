#!/bin/bash

sudo tcpdump -i ens37 -v -w tcpdump-server-tc&
sleep 1
tftp 10.10.10.10 -c get file new-file-zero


#без задержек;
#10 ms delay, 0% packet loss;
#100 ms delay, 0% packet loss;
#10 ms delay, 2% packet loss;
#30 ms delay, 2% packet loss;P
#100 ms delay, 2% packet loss;
#20 ms delay, 6% packet loss.

ssh root@10.10.10.10 "tc qdisc add dev ens37 root netem delay 10ms loss 0%"
tftp 10.10.10.10 -c get file new-file-10-delay

ssh root@10.10.10.10 "tc qdisc replace dev ens37 root netem delay 100ms loss 0%"
tftp 10.10.10.10 -c get file new-file-100-delay

ssh root@10.10.10.10 "tc qdisc replace dev ens37 root netem delay 10ms loss 2%"
tftp 10.10.10.10 -c get file new-file-10-2-delay

ssh root@10.10.10.10 "tc qdisc replace dev ens37 root netem delay 30ms loss 2%"
tftp 10.10.10.10 -c get file new-file-30-2-delay
# делаем тесты ...
#

ssh root@10.10.10.10 "tc qdisc replace dev ens37 root netem delay 100ms loss 2%"
tftp 10.10.10.10 -c get file new-file-10-2-delay

ssh root@10.10.10.10 "tc qdisc replace dev ens37 root netem delay 20ms loss 6%"
tftp 10.10.10.10 -c get file new-file-30-2-delay


ssh root@10.10.10.10 "tc qdisc delete dev ens37 root"

sleep 1

#now interrupt the process.  get its PID:
pid=$(ps -e | pgrep tcpdump)
echo $pid

#interrupt it:
sleep 5
kill -2 $pid
