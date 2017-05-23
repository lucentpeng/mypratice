#!/bin/bash
. ./00_Env.sh

#Run sensor collection funtion
while read -r item
do
    device=$(echo $item | awk -F ',' '{print $1}')
    ip=$(echo $item | awk -F ',' '{print $2}')

    printf 'Create run file'
    ssh -n ubuntu@$ip "touch $DEV_DEST/RUN"
    printf 'Execute sensor collection device ip is %s\n' "$ip"
    ssh -n ubuntu@$ip $DEV_DEST/sensor-collection.py -t 0 -c 1200 & >/dev/null 2>&1
done <"$DATA/DEVICELIST_from_lan.txt"

#After few minutes after , stop it
#Get collection data from devices
sleep $SENSOR_TEST_PERIOD

while read -r item
do
    ip=$(echo $item | awk -F ',' '{print $2}')
    dev="$(ssh -n ubuntu@$ip hostname)"
    printf 'Device Hostname is %s\n' "$dev"
    printf 'Stop sensor collection %s\n' "$dev"
    ssh -n ubuntu@$ip "rm $DEV_DEST/RUN"
    printf 'Copy data from device %s\n' "$dev"
    scp ubuntu@$ip:$DEV_DEST/*.csv $DATA/
done <"$DATA/DEVICELIST_from_lan.txt"

#Run sensor analysis function to calculate delta value
while read -r item
do
    ip=$(echo $item | awk -F ',' '{print $2}')
    device=$(echo $item | awk -F ',' '{print $1}')
    echo $device >> /tmp/list.txt
done <"$DATA/DEVICELIST_from_lan.txt"

$HOST_SRC/sensor-analysis.py -s $SENSOR -o /tmp/list.txt

#Push back to each device
while read -r item
do
    item=$(echo $item | awk -F ',' '{print $2}')
    dev="$(ssh -n ubuntu@$ip hostname)"
    scp $DATA/$dev.def ubuntu@$ip:~/Calibration.def
done <"$DATA/DEVICELIST_from_lan.txt"

rm /tmp/list.txt
#var="$(ssh ubuntu@$ip test -e /home/ubuntu/run && echo "Exist" || echo "Not exist")"
#
#if [ "$var"=="Exist" ]; then
#	echo "OK, continue"
#	exit 0
#fi
