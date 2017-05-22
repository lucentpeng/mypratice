#!/bin/bash
#確認Test Suite所需軟體套件都已經安裝
#To confirm all needed packages have be installed in the PC
. ./00_Env.sh

bash $UTIL/install_needed_package.sh $PACKAGE_LIST
