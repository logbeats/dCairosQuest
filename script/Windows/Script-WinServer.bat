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
SET HOUR=%TIME:~0,2%
IF "%HOUR:~0,1%" == " " SET HOUR=0%HOUR:~1,1%
SET T=%HOUR%%TIME:~3,2%%TIME:~6,2%
SET D=%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%
SET DATETIME=%D%,%T%
color 1f

TITLE Cloud Windows Server Security Check by logbeats

echo Name,Data>> ExtractResult.csv
echo %DATETIME% >> ExtractResult.csv
for /f "delims=[] tokens=2" %%a in ('ping -4 -n 1 %ComputerName% ^| findstr [') do (set ipaddress=%%a)
echo ipaddress,%ipaddress%>> ExtractResult.csv
del %COMPUTERNAME%-%ipaddress%-Windows.zip

FOR /F "tokens=1 skip=4" %%j IN ('net user') DO net user %%j >> ./UserResult.csv  2>nul
FOR /F "tokens=2 skip=4" %%j IN ('net user') DO net user %%j >> ./UserResult.csv  2>nul
FOR /F "tokens=3 skip=4" %%j IN ('net user') DO net user %%j >> ./UserResult.csv  2>nul

@echo Off
net share | findstr /v "$" | findstr /v "command"                                          > netsharelist.txt                              
FOR /F "tokens=2 skip=4" %%j IN ('type netsharelist.txt') DO cacls %%j > nul
IF ERRORLEVEL 1 echo shareEveryone,0 >> ExtractResult.csv
IF NOT ERRORLEVEL 1 echo shareEveryone,1 >> ExtractResult.csv
del netsharelist.txt

reg query "HKLM\SYSTEM\CurrentControlSet\Services\NetBT\Parameters\Interfaces" /s |find "NetbiosOptions" > NetbiosOptions.txt
type NetbiosOptions.txt | findstr /I "0x2" > nul
IF ERRORLEVEL 1 echo NetbiosOptions,1 >> ExtractResult.csv
IF NOT ERRORLEVEL 1 echo NetbiosOptions,0 >> ExtractResult.csv
del NetbiosOptions.txt

cacls c:\inetpub\ftproot > ftproot.txt
type ftproot.txt | find /i "everyone" > nul
IF ERRORLEVEL 1 echo FtpDirEveryone,0 >> ExtractResult.csv 
IF NOT ERRORLEVEL 1 echo FtpDirEveryone,1 >> ExtractResult.csv
del ftproot.txt

reg query "HKLM\SYSTEM\CurrentControlSet\Service\MSFtpsv\Parameters" | find "AllowAnonymous" > nul
IF ERRORLEVEL 1 echo AnonymousFTP,0 >> ExtractResult.csv
IF NOT ERRORLEVEL 1 echo AnonymousFTP,1 >> ExtractResult.csv

type applicationHost.config | findstr /I "accesstype users ipaddress" > AcctypeUsersIP.txt
IF ERRORLEVEL 1 echo AcctypeUsersIP,0 >> ExtractResult.csv
IF NOT ERRORLEVEL 1 ECHO AcctypeUsersIP,1 >> ExtractResult.csv
del AcctypeUsersIP.txt

reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\DNS Server\Zones" /s | find "SecureSecondaries"  | findstr "x0 x1" > nul
IF ERRORLEVEL 1 echo DNSZoneTransfer,0 >> ExtractResult.csv
IF NOT ERRORLEVEL 1 ECHO DNSZoneTransfer,1 >> ExtractResult.csv


cacls %systemroot%\system32\config\SAM | findstr /v "Administrator SYSTEM" | findstr "\ :" >nul
IF ERRORLEVEL 1 echo SamFile,0 >> ExtractResult.csv
IF NOT ERRORLEVEL 1 echo SamFile,1 >> ExtractResult.csv

SET /A STATUS=0
cacls %systemroot%\system32\logfiles |find /I "Everyone" > nul
IF NOT ERRORLEVEL 1 SET /A STATUS+=1
IF ERRORLEVEL 1 SET /A STATUS+=0
cacls %systemroot%\system32\config |find /I "Everyone" > nul
IF NOT ERRORLEVEL 1 SET /A STATUS+=1
IF ERRORLEVEL 1 SET /A STATUS+=0
echo LogEveryone,%STATUS% >> ExtractResult.csv



reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows Defender" | findstr /I "DisableAntiVirus" >> RegistryData.csv
reg query "HKCU\Control Panel\Desktop" | findstr /I "ScreenSaveActive" >> RegistryData.csv
reg query "HKCU\Control Panel\Desktop" | findstr /I "ScreenSaverIsSecure" >> RegistryData.csv
reg query "HKCU\Control Panel\Desktop" | findstr /I "ScreenSaveTimeout" >> RegistryData.csv
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" | findstr "shutdownwithoutlogon" >> RegistryData.csv
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" | findstr /I "AllocateDASD" >> RegistryData.csv
reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon" | findstr /I  "AutoAdminLogon" >> RegistryData.csv
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" | findstr /I "crashonaudit" >> RegistryData.csv
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "restrictanonymous" | findstr /I "restrict" >> RegistryData.csv
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "restrictanonymoussam" | findstr /I "restrict" >> RegistryData.csv
reg query "HKLM\System\CurrentControlSet\Services\LanmanServer\Parameters" | findstr /I "autoshare" >> RegistryData.csv
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows Defender\Signature Updates" | findstr /I "ASSignatureVersion" >> RegistryData.csv

@echo On
Secedit /export /cfg SecurityPolicy.csv
rem [UserAccount]
wmic useraccount list full /format:csv                       > UserAccount.csv 
rem [OS]
wmic OS get /format:csv                                      > OSInformation.csv
rem [Share]
wmic Share get Description, Name, Path, Status /format:csv   > Share.csv
rem [Service]
wmic service where (state="running") get Caption,Name,StartMode,State /format:csv > Service.csv
rem [QFE]
wmic QFE get Description, HotFixID, InstalledOn /format:csv > QFEInformation.csv
rem [Logicaldisk]
wmic logicaldisk get Name, FileSystem, VolumeName /format:csv > LogicalDisk.csv
rem [NicConfig]
wmic NicConfig list full /format:csv                         > NicConfig.csv
rem [Product]
wmic product get name,version /format:csv                    > Product.csv

.\bin\7za a -tzip %COMPUTERNAME%-%ipaddress%-Windows.zip *.csv -scsUTF-8

del *.csv
wmic service where (state="running") get name > Service.txt

type Service.txt | findstr /I "iis"  >nul
IF NOT ERRORLEVEL 1 GOTO QUIT
IF ERRORLEVEL 1 call dCairoScript-IIS.bat
:QUIT
del Service.txt

EXIT
