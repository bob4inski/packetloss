FILES="tcpdumps/*"
for f in $FILES
do
   tshark -N n -r "$f" -T fields \
    -e frame.number -e _ws.col.Time -e _ws.col.Source \
    -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -e _ws.col.Info -E header=y \
    -E separator=';' > converted/"$f".csv
  
  # take action on each file. $f store current file name
  echo "$f"
done