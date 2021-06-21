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
echo "Cloud Linux Server CCE(Common Configuration Enumeration) Check by logbeats"
echo "Copyright (c) $YEAR logbeats Co. Ltd. All rights Reserved. "
echo "=============================================================================="
echo "[Start Intelligence]=========================================================="
echo "[shadow]==>==================================================================="
cat /etc/shadow                                                            >> shadow.csv 2>&1
echo "=============================================================================="

echo "[passwd]==========>==========================================================="
cat /etc/passwd                                                            >> passwd.csv 2>&1
echo "=============================================================================="

echo "[login]============================================================" >> ExtractResult.txt 2>&1
cat /etc/pam.d/login                                                       >> ExtractResult.txt 2>&1
echo "[sshd_config]======================================================" >> ExtractResult.txt 2>&1
cat /etc/ssh/sshd_config                                                   >> ExtractResult.txt 2>&1
echo "[securetty]========================================================" >> ExtractResult.txt 2>&1
cat /etc/securetty                                                         >> ExtractResult.txt 2>&1
echo "[system-auth]======================================================" >> ExtractResult.txt 2>&1
cat /etc/pam.d/system-auth                                                 >> ExtractResult.txt 2>&1
echo "[login.defs]=======================================================" >> ExtractResult.txt 2>&1
cat /etc/login.defs                                                        >> ExtractResult.txt 2>&1
echo "[pwquality.conf]===================================================" >> ExtractResult.txt 2>&1
cat /etc/security/pwquality.conf                                           >> ExtractResult.txt 2>&1
echo "[password-auth]====================================================" >> ExtractResult.txt 2>&1
cat /etc/pam.d/password-auth                                               >> ExtractResult.txt 2>&1
echo "[common-password]==================================================" >> ExtractResult.txt 2>&1
cat /etc/pam.d/common-password                                             >> ExtractResult.txt 2>&1
echo "[common-auth]======================================================" >> ExtractResult.txt 2>&1
cat /etc/pam.d/common-auth                                                 >> ExtractResult.txt 2>&1
echo "[hosts.allow]======================================================" >> ExtractResult.txt 2>&1
cat /etc/hosts.allow                                                       >> ExtractResult.txt 2>&1
echo "[hosts.deny]=======================================================" >> ExtractResult.txt 2>&1
cat /etc/hosts.deny                                                        >> ExtractResult.txt 2>&1
echo "[finger]===========================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/finger                                                   >> ExtractResult.txt 2>&1
echo "[inetd.conf]=======================================================" >> ExtractResult.txt 2>&1
cat /etc/inetd.conf                                                        >> ExtractResult.txt 2>&1
echo "[vsftpd/vsftpd.con]================================================" >> ExtractResult.txt 2>&1
cat /etc/vsftpd/vsftpd.conf                                                >> ExtractResult.txt 2>&1
echo "[vsftpd.conf]======================================================" >> ExtractResult.txt 2>&1
cat /etc/vsftpd.conf                                                       >> ExtractResult.txt 2>&1
echo "[rsh]==============================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/rsh                                                      >> ExtractResult.txt 2>&1
echo "[rlogin]===========================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/rlogin                                                   >> ExtractResult.txt 2>&1
echo "[rexec]============================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/rexec                                                    >> ExtractResult.txt 2>&1
echo "[echo-dgram]=======================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/echo-dgram                                               >> ExtractResult.txt 2>&1
echo "[echo-stream]======================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/echo-stream                                              >> ExtractResult.txt 2>&1
echo "[discard-dgram]====================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/discard-dgram                                            >> ExtractResult.txt 2>&1
echo "[discard-stream]===================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/discard-stream                                           >> ExtractResult.txt 2>&1
echo "[daytime-dgram]====================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/daytime-dgram                                            >> ExtractResult.txt 2>&1
echo "[daytime-stream]===================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/daytime-stream                                           >> ExtractResult.txt 2>&1
echo "[chargen-dgram]====================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/chargen-dgram                                            >> ExtractResult.txt 2>&1
echo "[chargen-stream]===================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/chargen-stream                                           >> ExtractResult.txt 2>&1
echo "[echo]=============================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/echo                                                     >> ExtractResult.txt 2>&1
echo "[chargen]==========================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/chargen                                                  >> ExtractResult.txt 2>&1
echo "[daytime]==========================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/daytime                                                  >> ExtractResult.txt 2>&1
echo "[discard]==========================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/discard                                                  >> ExtractResult.txt 2>&1
echo "[exports]==========================================================" >> ExtractResult.txt 2>&1
cat /etc/exports                                                           >> ExtractResult.txt 2>&1
echo "[tftp]=============================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/tftp                                                     >> ExtractResult.txt 2>&1
echo "[talk]=============================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/talk                                                     >> ExtractResult.txt 2>&1
echo "[ntalk]============================================================" >> ExtractResult.txt 2>&1
cat /etc/xinetd.d/ntalk                                                    >> ExtractResult.txt 2>&1
echo "[sendmail.cf]======================================================" >> ExtractResult.txt 2>&1
cat /etc/mail/sendmail.cf                                                  >> ExtractResult.txt 2>&1
echo "[access]===========================================================" >> ExtractResult.txt 2>&1
cat /etc/mail/access                                                       >> ExtractResult.txt 2>&1
echo "[named.conf]=======================================================" >> ExtractResult.txt 2>&1
cat /etc/named.conf                                                        >> ExtractResult.txt 2>&1
echo "[named.boot]=======================================================" >> ExtractResult.txt 2>&1
cat /etc/named.boot                                                        >> ExtractResult.txt 2>&1
echo "[version]==========================================================" >> ExtractResult.txt 2>&1
cat /etc/*release                                                          >> ExtractResult.txt 2>&1
echo "[debian_version]===================================================" >> ExtractResult.txt 2>&1
cat /etc/debian_version                                                    >> ExtractResult.txt 2>&1
echo "[profile]==========================================================" >> ExtractResult.txt 2>&1
cat /etc/profile                                                           >> ExtractResult.txt 2>&1
echo "[named]============================================================" >> ExtractResult.txt 2>&1
strings /usr/sbin/named                                                    >> ExtractResult.txt 2>&1
echo "[named8]===========================================================" >> ExtractResult.txt 2>&1
strings /usr/sbin/named8                                                   >> ExtractResult.txt 2>&1
echo "===================================================================" >> ExtractResult.txt 2>&1
echo "[OS Bit Check]=====================================================" >> ExtractResult.txt 2>&1
uname -m                                                                   >> ExtractResult.txt 2>&1
echo "[IP  Check]========================================================" >> ExtractResult.txt 2>&1
ifconfig -a                                                                >> ExtractResult.txt 2>&1
echo "[TCP PORT Check]===================================================" >> ExtractResult.txt 2>&1
netstat -tnlp                                                              >> ExtractResult.txt 2>&1
echo "[UDP PORT Check]===================================================" >> ExtractResult.txt 2>&1
netstat -unlp                                                              >> ExtractResult.txt 2>&1
echo "[netstat-an]=======================================================" >> ExtractResult.txt 2>&1
netstat -an                                                                >> ExtractResult.txt 2>&1
echo "===================================================================" >> ExtractResult.txt 2>&1
echo "[Start Time]=======================================================" >> ExtractResult.txt 2>&1
echo "`date +%Y-%m-%d` `date +%X`"                                         >> ExtractResult.txt 2>&1
echo "[Kernel-Name]======================================================" >> ExtractResult.txt 2>&1
uname -s | tr -d ' '                                                       >> ExtractResult.txt 2>&1
echo "[Kernel-Release]===================================================" >> ExtractResult.txt 2>&1
uname -r | tr -d ' '                                                       >> ExtractResult.txt 2>&1
echo "[uname-All]========================================================" >> ExtractResult.txt 2>&1
uname -a  | tr -d ' '                                                      >> ExtractResult.txt 2>&1
echo "[Time]=============================================================" >> ExtractResult.txt 2>&1
date +%Y | tr -d ' '                                                       >> ExtractResult.txt 2>&1
date +%m%d | tr -d ' '                                                     >> ExtractResult.txt 2>&1
date +%H:%M:%S | tr -d ' '                                                 >> ExtractResult.txt 2>&1
echo "[Hostname]=========================================================" >> ExtractResult.txt 2>&1
hostname | tr -d ' '                                                       >> ExtractResult.txt 2>&1
echo "[/proc/version]====================================================" >> ExtractResult.txt 2>&1
cat /proc/version                                                          >> ExtractResult.txt 2>&1
echo "[/etc/lsb-release]=================================================" >> ExtractResult.txt 2>&1
cat /etc/lsb-release                                                       >> ExtractResult.txt 2>&1
echo "[/etc/redhat-release]==============================================" >> ExtractResult.txt 2>&1
cat /etc/redhat-release                                                    >> ExtractResult.txt 2>&1
echo "[PATH]=============================================================" >> ExtractResult.txt 2>&1
echo $PATH                                                                 >> ExtractResult.txt 2>&1
echo "===================================================================" >> ExtractResult.txt 2>&1

echo "[Linux ls -alL]=============>================================================="
ls -alL /etc/passwd                                                        >> Permission.csv 2>&1
ls -alL /etc/shadow                                                        >> Permission.csv 2>&1
ls -alL /etc/hosts                                                         >> Permission.csv 2>&1
ls -alL /etc/inetd.conf                                                    >> Permission.csv 2>&1
ls -alL /etc/xinetd.conf                                                   >> Permission.csv 2>&1
ls -alL /etc/syslog.conf                                                   >> Permission.csv 2>&1
ls -alL /etc/rsyslog.conf                                                  >> Permission.csv 2>&1
ls -alL /etc/services                                                      >> Permission.csv 2>&1
ls -alL /etc/hosts.allow                                                   >> Permission.csv 2>&1
ls -alL /etc/hosts.deny                                                    >> Permission.csv 2>&1
ls -alL /etc/cron.allow                                                    >> Permission.csv 2>&1
ls -alL /etc/cron.deny                                                     >> Permission.csv 2>&1
ls -alL /usr/sbin/named                                                    >> Permission.csv 2>&1
ls -alL /usr/sbin/named8                                                   >> Permission.csv 2>&1
ls -alL /sbin/dump                                                         >> Permission.csv 2>&1
ls -alL /usr/bin/lpq-lpd                                                   >> Permission.csv 2>&1
ls -alL /usr/bin/newgrp                                                    >> Permission.csv 2>&1
ls -alL /sbin/restore                                                      >> Permission.csv 2>&1
ls -alL /usr/bin/lpr                                                       >> Permission.csv 2>&1
ls -alL /usr/sbin/lpc                                                      >> Permission.csv 2>&1
ls -alL /sbin/unix_chkpwd                                                  >> Permission.csv 2>&1
ls -alL /usr/bin/lpr-lpd                                                   >> Permission.csv 2>&1
ls -alL /usr/sbin/lpc-lpd                                                  >> Permission.csv 2>&1
ls -alL /usr/bin/at                                                        >> Permission.csv 2>&1
ls -alL /usr/bin/lprm                                                      >> Permission.csv 2>&1
ls -alL /usr/sbin/traceroute                                               >> Permission.csv 2>&1
ls -alL /usr/bin/lpq                                                       >> Permission.csv 2>&1
ls -alL /usr/bin/lprm-lpd                                                  >> Permission.csv 2>&1
ls -alL /etc/profile                                                       >> Permission.csv 2>&1
ls -alL /.profile                                                          >> Permission.csv 2>&1
echo "=============================================================================="

echo "[NouserGroup]=========================>======================================="
find /etc /tmp /bin /sbin -nouser -o -nogroup                              >> Permission.csv 2>&1
echo "=============================================================================="

echo "[WorldWritable]==================================>============================"
find /home /tmp /etc /var -xdev -xdev -perm -2 -ls | grep -v "\l"          >> WorldWritable.csv 2>&1
echo "=============================================================================="

echo "[StickBit]================================================>==================="
find / -xdev -user root -type f \( -perm -04000 -o -perm -02000 \) -exec ls -al {} \; >> StickBit.csv 2>&1
echo "=============================================================================="

echo "[process]=========================================================>==========="
ps -e -o %u, -o lstart -o ,%c                             >> ProcessState.csv 2>&1
echo "=============================================================================="

echo "[UserPasswd]=============================================================>===="
echo "[UserPasswd]=======================================================" >> ExtractResult.txt 2>&1
chage -l root >> UserPasswd.csv 2>&1

awk -F: '$3 >= 500' /etc/passwd >> tmp_passwd 2>&1 
cat tmp_passwd | awk 'BEGIN {FS=":";OFS="-"} {print $1, $3}' >> tmp_user 2>&1
for check_uid in $(cat tmp_user)
	do
		echo "[$check_uid]" >> ExtractResult.txt 2>&1
		uid=$(echo $check_uid | awk 'BEGIN {FS="-"} {print $1}')
		echo $uid >> ExtractResult.txt 2>&1
		chage -l $uid >> ExtractResult.txt 2>&1
		echo "" >> ExtractResult.txt 2>&1

	done
rm -rf tmp_passwd
rm -rf tmp_user
echo "===================================================================" >> ExtractResult.txt 2>&1
echo "[RootOrUser]=================================================================>"
HOMEDIRS=`cat /etc/passwd | awk -F":" 'length($6) > 0 {print $6}' | sort -u | grep -v "#" | grep -v "/tmp" | grep -v "uucppublic" | uniq`
for dir in $HOMEDIRS
	do
		ls -dal $dir | grep '\d.........' >> RootOrUser.csv 2>&1
	done
HOMEDIRS=`cat /etc/passwd | awk -F":" 'length($6) > 0 {print $6}' | sort -u | grep -v '/bin/false' | grep -v 'nologin' | grep -v "#"`
FILES=".profile .cshrc .kshrc .login .bash_profile .bashrc .bash_login .exrc .netrc .history .sh_history .bash_history .dtprofile .Xdefaults"
for file in $FILES
	do
		FILE=/$file
		if [ -f $FILE ]
			then
			ls -al $FILE >> RootOrUser.csv 2>&1
		fi
	done

for dir in $HOMEDIRS
	do
		for file in $FILES
			do
				FILE=$dir/$file
				if [ -f $FILE ]
					then
						ls -al $FILE >> RootOrUser.csv 2>&1
				fi
			done
	done
unset HOMEDIRS
unset FILES
echo "[End intelligence]"


tar -cvf $RESULT_FILE.tar shadow.csv passwd.csv ExtractResult.txt Permission.csv WorldWritable.csv ProcessState.csv StickBit.csv RootOrUser.csv

mv $RESULT_FILE.tar ../

rm -rf ../$RESULT_FILE
rm -rf ../dCairoScript-Linux.sh

echo "[Complete]"