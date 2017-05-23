#!/bin/bash
# 確認Device上Test Suite的軟體版本與IPCS的軟體版本
# 必須符合本次測試的版本
# 強制更新至產測電腦版本
# To confirm SW version is compatiable between IPCS and Test Suite
. ./00_Env.sh


#IP list must need exist, we will
#[ ! -f "ip" ] && echo "Need IP list" && exit 0

while read -r item
do
    device=$(echo $item | awk -F ',' '{print $1}')
    ip=$(echo $item | awk -F ',' '{print $2}')
    sshpass -p "uno@1" ssh-copy-id ubuntu@$ip
    ssh -n ubuntu@$ip "mkdir $DEV_DEST"
    if [ $? -eq 0 ] ;then
	echo "$device don't have factory code, install it"
	scp -r $DEV_SRC/* ubuntu@$ip:$DEV_DEST/
	ssh -n ubuntu@$ip "echo $TEST_SUITE_VERSION > $DEV_DEST/version"
    else
	echo "$device have factory code, check version"
	old_ver=$(ssh -n ubuntu@$ip "cat $DEV_DEST/version")

	if [ "$TEST_SUITE_VERSION" != "$old_version" ] ; then
	    echo "Remove facotry code from device"
	    ssh -n ubuntu@$ip "rm -rf $DEV_DEST"
	    echo "Upload current version to device"
	    ssh -n ubuntu@$ip "mkdir $DEV_DEST"
	    scp -r $DEV_SRC/* ubuntu@$ip:$DEV_DEST/
	    ssh -n ubuntu@$ip "echo $TEST_SUITE_VERSION > $DEV_DEST/version"
	else
	    echo "Nothing need to do"
	fi
    fi


done <"$DATA/DEVICELIST_from_lan.txt"
