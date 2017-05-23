#!/bin/bash

file="ip"
path=/home/ubuntu/factory
execute_time=185
to_test="T H C V P D L"

#IP list must need exist, we will
[ ! -f "ip" ] && echo "Need IP list" && exit 0

#Create data folder, data folder is working dir
if [ ! -d "./data" ]; then
    mkdir data
else
    [ -f "./data/DEVICELIST.txt" ] && rm "./data/DEVICELIST.txt"
fi

#Check "run" file exist or not, create it if file not exist
#Run sensor collection funtion
while read ip; do
    echo $ip
    ssh -n ubuntu@$ip touch $path/run
done < ip

while read -r line
do
        # display $line or do somthing with $line
    ip=$line
    printf 'Execute sensor collection device ip is %s\n' "$ip"
    ssh -n ubuntu@$ip $path/sensor-collection.py -t 0 -c 1200 & >/dev/null 2>&1
done <"$file"

#After few minutes after , stop it
#Get collection data from devices
sleep $execute_time

while read -r line
do
        # display $line or do somthing with $line
    printf 'Device IP is %s\n' "$line"
    ip=$line
    dev="$(ssh -n ubuntu@$ip hostname)"
    printf 'Device Hostname is %s\n' "$dev"
    echo "$dev" >> ./data/DEVICELIST.txt
    printf 'Stop sensor collection %s\n' "$dev"
    ssh -n ubuntu@$ip rm $path/run
    printf 'Copy data from device %s\n' "$dev"
    scp ubuntu@$ip:$path/*.csv data/
done <"$file"

#Run sensor analysis function to calculate delta value
../python/sensor-analysis.py -s $to_test -o DEVICELIST.txt

#Push back to each device
while read -r line
do
    printf '%s\n' "$line"
    ip=$line
    dev="$(ssh -n ubuntu@$ip hostname)"
#    scp data/$dev.def ubuntu@$ip:/opt/ironman/Calibration.def
    scp data/$dev.def ubuntu@$ip:$path/Calibration.def
#    ssh -n ubuntu@$ip sudo su;cp $path/Calibration.def $path/Calibration.def
done <"$file"
#

#var="$(ssh ubuntu@$ip test -e /home/ubuntu/run && echo "Exist" || echo "Not exist")"
#
#if [ "$var"=="Exist" ]; then
#	echo "OK, continue"
#	exit 0
#fi
