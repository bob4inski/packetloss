
#!/bin/bash

delays=(0 10 20 30 50 100)

# Packet loss percentages
packet_losses=(0 2 6 8 12)
network_interface="ens37"
ssh root@10.10.10.10 'tc qdisc add dev ens37 root netem delay 0ms loss 0%'
#sudo tcpdump -i ens37 -v -w downloads/tcpdumps/tcp/s_cubic-c_cubic_all&
sleep 1
versions=(1.1 2 3)
#mkdir results
#touch results/output.xtx
echo "start testing cubic-cubic" > result/output.txt
for packet_loss in "${packet_losses[@]}"; do
    for delay in "${delays[@]}"; do
        echo "--------- ${delay}ms delay, ${packet_loss}% packet loss-------------" >> result/output.txt
        command="tc qdisc replace dev ens37 root netem delay ${delay}ms loss ${packet_loss}%"
        ssh root@10.10.10.10 $command
        url=https://10.10.10.10:443/static/file-10.txt
        for version in "${versions[@]}"; do
           for number in 1 2 3
                do
                        time=$(./curl -w "%{time_total}" --http"$version" -o /dev/null --insecure -s $url)
                        total_time=$(echo "$total_time + $time" | bc -l)
                done
           avg_time=$(( $total_time / 3 ))
           echo "HTTP $version : $avg_time seconds" >>  result/avg_cubic_cubic_output.txt
        done
        for number in 1 2 3
        do
                time=$(./curl -w "%{time_total}" -o /dev/null  -s tftp://10.10.10.10/file-10.txt)
                total_time=$(echo "$total_time + $time" | bc -l)
        done
        avg_time=$(( $total_time / 3 ))
        echo "TFTP 1 : $avg_time seconds" >>  result/avg_cubic_cubic_output.txt
    done
sleep 1
done

# pid=$(ps -e | pgrep tcpdump)
# sleep 1
# kill -2 $pid

ssh root@10.10.10.10 "tc qdisc delete dev ens37 root"
