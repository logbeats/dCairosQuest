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

del %COMPUTERNAME%-%ipaddress%-IIS.zip

TITLE Cloud Windows Server IIS Security Check by logbeats
copy %systemroot%\system32\inetsrv\config\applicationHost.config applicationHost.config
copy %systemroot%\system32\inetsrv\MetaBase.xml Metabase.xml

echo Name,Data>> ResultData.csv
echo %DATETIME%>> ResultData.csv
for /f "delims=[] tokens=2" %%a in ('ping -4 -n 1 %ComputerName% ^| findstr [') do (set ipaddress=%%a)
echo ipaddress,%ipaddress%>> ResultData.csv
@echo On

DIR /s/b c:\Inetpub\*.lnk >> lnk.txt
type lnk.txt | findstr /I "lnk" > nul
IF ERRORLEVEL 1 echo IISlnk,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 echo IISlnk,1 >> ResultData.csv
del lnk.txt

cacls C:\Inetpub\wwwroot > Home-Acl.txt
type Home-Acl.txt | findstr /I "everyone" > nul
IF ERRORLEVEL 1 echo EveryoneAcl,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 echo EveryoneAcl,1 >> ResultData.csv

type Home-Acl.txt | findstr /I "Users:(ID)F" > nul
IF ERRORLEVEL 1 echo UserseAcl,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 echo UserseAcl,1 >> ResultData.csv

type Home-Acl.txt | findstr /I "IUSR_" > nul
IF ERRORLEVEL 1 echo IUSR_Acl,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 echo IUSR_Acl,1 >> ResultData.csv
del Home-Acl.txt

type applicationHost.config | findstr /I "notListedIsapisAllowed=\"true\"" > checkISAPI.txt
IF ERRORLEVEL 1 GOTO CONFIG-ABSENCE
IF NOT ERRORLEVEL 1 GOTO CONFIG-PRESENCE
:CONFIG-ABSENCE
echo checkISAPI,0 >> ResultData.csv
del checkISAPI.txt
goto QUIT
:CONFIG-PRESENCE
type checkISAPI.txt | findstr /I "false" > nul
IF ERRORLEVEL 1 echo checkISAPI,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 echo checkISAPI,1 >> ResultData.csv
del checkISAPI.txt
:QUIT

type applicationHost.config | findstr /I "notListedCgisAllowed=\"true\"" > checkCGI.txt
IF ERRORLEVEL 1 GOTO CONFIG-ABSENCE
IF NOT ERRORLEVEL 1 GOTO CONFIG-PRESENCE
:CONFIG-ABSENCE
echo checkCGI,0 >> ResultData.csv
del checkCGI.txt
goto QUIT
:CONFIG-PRESENCE
type checkCGI.txt | findstr /I "false" > nul
IF ERRORLEVEL 1 echo checkCGI,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 echo checkCGI,1 >> ResultData.csv
del checkCGI.txt
:QUIT

type applicationHost.config | findstr /I "directoryBrowse enabled" > DirBrowse.txt 
type DirBrowse.txt | find "true" > nul
IF ERRORLEVEL 1 ECHO DirBrowse,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 ECHO DirBrowse,1 >> ResultData.csv
del DirBrowse.txt 

type applicationHost.config  | findstr /I "enableParentPaths" > ParentPaths.txt 
type ParentPaths.txt | find "true" > nul
IF ERRORLEVEL 1 ECHO ParentPaths,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 ECHO ParentPaths,1 >> ResultData.csv 
del ParentPaths.txt

type Metabase.xml | findstr /I "AspEnableParentPaths" > AspEnableParentPaths.txt
type AspEnableParentPaths.txt | find "true" > nul
IF ERRORLEVEL 1 ECHO AspEnableParentPaths,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 ECHO AspEnableParentPaths,1 >> ResultData.csv
del AspEnableParentPaths.txt 

type Metabase.xml | findstr /I "ip security" > IPsecurity.txt
IF ERRORLEVEL 1 echo IPsecurity,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 ECHO IPsecurity,1 >> ResultData.csv
del IPsecurity.txt

type applicationHost.config | findstr /I "accesstype users ipaddress" > AcctypeUsersIP.txt
IF ERRORLEVEL 1 echo AcctypeUsersIP,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 ECHO AcctypeUsersIP,1 >> ResultData.csv
del AcctypeUsersIP.txt

cacls c:\inetpub\ftproot >   ftproot.txt
type ftproot.txt | find /i "everyone" > nul
IF ERRORLEVEL 1 echo FtpDirEveryone,0 >> ResultData.csv 
IF NOT ERRORLEVEL 1 echo FtpDirEveryone,1 >> ResultData.csv
del ftproot.txt

reg query "HKLM\SYSTEM\CurrentControlSet\Service\MSFtpsv\Parameters" | find "AllowAnonymous" > nul
IF ERRORLEVEL 1 echo AnonymousFTP,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 echo AnonymousFTP,1 >> ResultData.csv

type applicationHost.config | findstr /I "processModel identityType" >> identityType.txt
type identityType.txt | find /I "LocalSystem" > nul
IF ERRORLEVEL 1 echo identityType,0 >> ResultData.csv
IF NOT ERRORLEVEL 1 ECHO identityType,1 >> ResultData.csv
del identityType.txt

del applicationHost.config
del Metabase.xml
del Service.txt
.\bin\7za a -tzip %COMPUTERNAME%-%ipaddress%-IIS.zip *.csv -scsUTF-8
del *.csv 2>nul

EXIT
