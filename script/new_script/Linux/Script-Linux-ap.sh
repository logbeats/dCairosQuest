#!/bin/bash -

LANG=C
export LANG
OS=`uname -s | tr -d ' '`
YEAR=`date +%Y | tr -d ' '`
DATE=`date +%m%d | tr -d ' '`
HMS=`date +%H:%M:%S | tr -d ' '`
HOST_NAME=`hostname | tr -d ' '`
VERSION=`uname -r | tr -d ' '`
IPADDRESS=`hostname -I | tr -d '[:space:]'`

RESULT_FILE=${HOSTNAME}-${IPADDRESS}-${OS}

#if [ -f ExtractResult.txt ]
#  then
rm -rf ./$RESULT_FILE
#fi
mkdir $RESULT_FILE
cd $RESULT_FILE
echo "=============================================================================="
echo "Cloud Linux Apache CCE(Common Configuration Enumeration) Check by logbeats"
echo "Copyright (c) $YEAR logbeats Co. Ltd. All rights Reserved. "
echo "=============================================================================="
echo "[Start Intelligence]=========================================================="
HTTPD_ROOT=`httpd -V | grep HTTPD_ROOT | awk -F'"' '{printf $2"\n"}'`
SERVER_CONFIG_FILE=`httpd -V | grep SERVER_CONFIG_FILE | awk -F'"' '{printf $2"\n"}'`

ACONF=$HTTPD_ROOT/$SERVER_CONFIG_FILE
cat $HTTPD_ROOT/$SERVER_CONFIG_FILE >> ExtractResult.txt

tar -cvf $RESULT_FILE.tar ExtractResult.txt

mv $RESULT_FILE.tar ../

rm -rf ../$RESULT_FILE
rm -rf ../dCairoScript-Linux.sh

echo "[Complete]"