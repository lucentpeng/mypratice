#!/bin/bash
nmap -sP 192.168.0.* | grep "Nmap scan report" | awk {'print $5'} > ip
