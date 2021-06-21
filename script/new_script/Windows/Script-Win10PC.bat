@echo Off
CLS
:_admin
openfiles >nul 2>&1 ||(
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%~0", "", "", "runas",1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs" >nul 2>&1
goto:eof
)
del /f /q "%temp%\getadmin.vbs" >nul 2>&1
setlocal
pushd %~dp0
chcp 437
CLS

color 1f

TITLE Cloud Windows PC Security Check by logbeats

for /f "delims=[] tokens=2" %%a in ('ping -4 -n 1 %ComputerName% ^| findstr [') do (set ipaddress=%%a)
del %COMPUTERNAME%-%ipaddress%-PC.zip
echo Off
reg query "HKCU\Control Panel\Desktop" | findstr /I "Screen" >> RegistryData.csv
reg query "HKLM\Software\Policies\Microsoft\Messenger\Client" | findstr /I "PreventRun" >> RegistryData.csv
reg query "HKLM\SYSTEM\CurrentControlSet\Services\lanmanserver\parameters" | findstr /I "AutoShare" >> RegistryData.csv
reg query "HKLM\Software\Policies\Microsoft\Messenger\Client" | findstr /I "PreventRun">> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" | findstr /I "ProductName">> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" | findstr /I "BuildLab">> RegistryData.csv
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" | findstr /I "NoAutoUpdate">> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate" | findstr /I "LastDownloadsPurgeTime">> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" | findstr /I "AutoLogin">> RegistryData.csv
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" | findstr /I "LimitBlankPasswordUse">> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows Defender" | findstr /i "DisableAntiVirus" >> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows Defender" | findstr /i "DisableAntiSpyware" >> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows Defender\Signature Updates" | findstr /i "ASSignatureVersion" >> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows Defender\Real-Time Protection" | findstr /i "DisableRealtimeMonitoring" >> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows Defender\Signature Updates" | findstr /I "SignatureUpdateInterval">> RegistryData.csv
reg query "HKLM\SOFTWARE\Ahnlab\V3Lite4" | findstr /I "AscVersion">> RegistryData.csv
reg query "HKLM\SOFTWARE\Ahnlab\V3Lite4\ServiceStatus" | findstr /I "AvMon">> RegistryData.csv
reg query "HKLM\SOFTWARE\Ahnlab\V3Lite4\Option\UPDATE" | findstr /I "autoupdateuse">> RegistryData.csv
reg query "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile" | findstr /i "EnableFirewall" >> RegistryData.csv
reg query "HKLM\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile" | findstr /i "EnableFirewall" >> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Setup\RecoveryConsole" | find /i "SecurityLevel"  >> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" | findstr /i "NoDriveTypeAutoRun" >> RegistryData.csv
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\Cache" | findstr /i "Persistent" >> RegistryData.csv
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services" | findstr "fAllowUnsolicited" >> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Internet Explorer" | findstr -I "svcVersion" >> RegistryData.csv

bcdedit /v | findstr -I "Loader" >> temp.txt
SET "count=0"
FOR /f "tokens=*" %%G IN (temp.txt) DO (
set /a "count+=1"
)
echo BootLoader REG_SZ %count% >> RegistryData.csv
del temp.txt

echo On
Secedit /export /cfg SecurityPolicy.csv
rem [Share]
wmic Share get Description, Name, Path, Status /format:csv   > Share.csv
rem [Service]
wmic service where (state="running") get Caption,Name,StartMode,State /format:csv > Service.csv
rem [QFE]
wmic QFE get Description, HotFixID, InstalledOn /format:csv > QFEInformation.csv
rem [Logicaldisk]
wmic logicaldisk get Name, FileSystem, VolumeName /format:csv > LogicalDisk.csv

.\bin\7za a -tzip %COMPUTERNAME%-%ipaddress%-PC.zip *.csv -scsUTF-8

del *.csv

EXIT
