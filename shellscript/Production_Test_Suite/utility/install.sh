#!/bin/bash

file="ip"

#Read IP from file
while read ip; do
    echo $ip
    echo "copy id"
    sshpass -p "uno@1" ssh-copy-id ubuntu@$ip
done <"$file"
