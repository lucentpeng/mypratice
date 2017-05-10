#!/bin/bassh

file="ip"

#Read IP from file
while read ip; do
    echo $ip
    echo "copy id"
    ssh -n ubuntu@$ip 'mkdir /home/ubuntu/factory'
    scp ../python/sensor-collection.py ubuntu@$ip:~/factory
done <"$file"

