#!/bin/bash
nmap -sP 172.16.78.* | grep "Nmap scan report" | awk {'print $5'} > ip
