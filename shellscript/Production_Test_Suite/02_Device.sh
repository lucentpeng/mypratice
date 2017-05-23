#!/bin/bash
#確認區網可以偵測到IPCS,並且數量及序號與Barcode掃到的一致
#To confirm Test Suite can detect IPCS devices and serial number and amount of numbers should be the same that scaned by bar code
. ./00_Env.sh

nmap -sP $LAN | grep "Nmap scan report" | awk {'print $5'} > $DATA/iptable

#IP list must need exist, we will
[ ! -f "$DATA/iptable" ] && echo "No any device in the LAN network" && exit 0

#Delete old device list from network
[ -f "$DATA/DEVICELIST_from_lan.txt" ] && rm "$DATA/DEVICELIST_from_lan.txt"

#Search device by IP
while read -r ip
do
    value="$(avahi-resolve-address $ip)"
    echo "$value" | grep "$SN_FORMAT"
    if [ $? -eq 0 ] ;then
	echo "match found, write to list"
	printf 'Device IP is %s\n' "$ip"
	dev=$(echo $value | awk '{print $2}')
	device_name=$(echo "$dev" | awk -F '.' {'print $1'})
	echo "$device_name,$ip" >> $DATA/DEVICELIST_from_lan.txt
    else
	echo "match not found"
    fi

done <"$DATA/iptable"

#Compare device list between LAN and Barcode
#TBD

