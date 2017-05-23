#!/bin/bash
#載入script所需的環境變數
#To load environment variable what we need.
IMAGE=$PWD/flash_image
OUT=$PWD/out
DATA=$PWD/data
UTIL=$PWD/utility
DEV_SRC=$PWD/src/device
DEV_DEST=/home/ubuntu/production_test_suite
HOST_SRC=$PWD/src/host
TEST_SUITE_VERSION=0.1

#Ubuntu Package to install
PACKAGE_LIST="python-pandas sshpass"
#LAN domain address
LAN=172.16.78.*
#Serial Number Pattern
SN_FORMAT="16[A-Z0-9]\+\.local$"

#37_Sensor_Test.sh
SENSOR="T H C V P D L"
SENSOR_TEST_PERIOD="60" #seconds
