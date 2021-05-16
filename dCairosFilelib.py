# -*- coding: utf-8 -*-
import re
import os
import shutil
import pandas as pd
import zipfile
from Classifylib import Extraction
from chardet.universaldetector import UniversalDetector
from io import StringIO
import configparser
import tarfile
import subprocess


###############################################################################
class Initialize:
    def __init__(self, basedir):
        self.basedir = basedir
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.edit = int(config['logbeats']['edit'])
        self.dataPath = {}
        if self.edit:
            self.conf = config['logbeats']['conf']
            self.input = config['logbeats']['input']
            self.output = config['logbeats']['output']
            self.project = config['logbeats']['project']
        else:
            self.conf = os.path.join(self.basedir, 'conf')
            self.workspace = os.path.join(self.basedir, 'workspace')
            self.input = os.path.join(self.basedir, 'workspace', 'input')
            self.output = os.path.join(self.basedir, 'workspace', 'output')
            self.project = os.path.join(self.basedir, 'workspace', 'project')

    def run(self):
        self.dataPath['conf'] = self.conf
        self.dataPath['input'] = self.input
        self.dataPath['output'] = self.output
        self.dataPath['project'] = self.project

        return self.dataPath

    def dirCheck(self):
        if not os.path.isdir(self.workspace):
            try:
                os.mkdir(self.workspace)
            except FileExistsError:
                pass

        if not os.path.isdir(self.input):
            try:
                os.mkdir(self.input)
            except FileExistsError:
                pass

        if not os.path.isdir(self.output):
            try:
                os.mkdir(self.output)
            except FileExistsError:
                pass

        if not os.path.isdir(self.project):
            try:
                os.mkdir(self.project)
            except FileExistsError:
                pass


###############################################################################
def FindDataFiles(Path, ext):
    filefind = DirFiles(Path, ext)
    zipName = filefind.FileNames()
    return zipName


###############################################################################
def get_encoding_type(pathname):  # 인코딩을 확인한다.
    detector = UniversalDetector()
    detector.reset()
    try:
        with open(pathname, 'rb') as fp:
            for line in fp:
                detector.feed(line)
                if detector.done:
                    break
    except FileNotFoundError:
        return str('FileNotFoundError')
    detector.close()
    return detector.result['encoding']


###############################################################################
def convert_encoding_type(pathname):  # utf-8로 변환한다.
    encode_type = get_encoding_type(pathname)

    with open(pathname, 'r', encoding=encode_type) as fp:
        content = fp.read()

    with open(pathname, 'w', encoding='utf-8', newline='\n') as fp:
        fp.write(content)

    return content


###############################################################################
class DataToZipfile:  # 패스워드로 압축된 파일의 내용을 읽어온다.
    def __init__(self, zName, password=None):
        self._pItem = False
        self._zName = zName
        self._password = password
        self.NameDict = {}

        if password is not None:
            self._pItem = True
        self._archive = zipfile.ZipFile(zName, 'r')

###############################################################################
    def Get_InfoList(self):  # 아직 필수적인 함수 아님
        return self._archive.infolist()

###############################################################################
    def Get_PrintDir(self):  # 아직 필수적인 함수 아님
        return self._archive.printdir()  # 필요시 커스텀 작업 필요함

###############################################################################
    def Get_InfoFile(self, fName):
        return self._archive.getinfo(fName)

###############################################################################
    def Get_FileList(self, reverse=True):  # 확장자 제거 : True 앞, False 뒤
        files = self._archive.namelist()
        for file in files:
            fileName = file.split('.')
            if reverse:
                self.NameDict[fileName[0]] = file
            else:
                self.NameDict[file] = fileName[0]
        return self.NameDict

###############################################################################
    def FileToPd(self, fName):  # 인코딩 UTF-8로 pandas형식으로 불러온다.
        if self._pItem:
            self._archive.setpassword(self._password.encode())
        try:
            data = self._archive.read(fName)
            data = str(data, 'utf-8')
            data = StringIO(data)
        except IOError:
            return str('암호가 다름 & 다른문제???')

        return pd.read_csv(data)


###############################################################################
class strToInt:

    def __init__(self):

        self.lDiv = {'d': 'Dir', '-': 'File', 's': 'Socket', 'b': 'Block',
                     'l': 'Link', 'c': 'IO'}
        self.lChmod = {'r': 4, 'w': 2, 'x': 1, '-': 0, 's': 1, 't': 1}
        self.lClass = {'r': 'Read', 'w': 'Write', 'x': 'Execute', '-': 'None',
                       's': 'Set', 't': 'Bit', 'S': 'NoBit', 'T': 'NoBit'}

    def div(self, data):
        if data is None:
            raise Exception("Need to data")

        return self.lDiv[data[0:1]]

    def special(self, data):
        if data is None:
            raise Exception("Need to data")
        temp = []
        temp.append(self.lClass[data[3]])
        temp.append(self.lClass[data[6]])
        temp.append(self.lClass[data[9]])

        return temp

    def permission(self, data):
        if data is None:
            raise Exception("Need to data")
        temp = []
        temp.append(self.chmodToInt(data[1:4]))
        temp.append(self.chmodToInt(data[4:7]))
        temp.append(self.chmodToInt(data[7:10]))

        return int(''.join(temp))

    def chmodToInt(self, data):
        if data is None:
            raise Exception("Need to data")
        result = 0
        for key in data:
            result += self.lChmod[key.lower()]  # 대소문자 구분 X

        return str(result)


###############################################################################
class DirFiles:   # 특정 디렉터리에서 파일 이름만 추출함
    def __init__(self, path, ext=None):
        if ext is None:
            ext = 'zip'
        self._ext = ext.lower()
        self.path = path
        self.NameDict = {}

###############################################################################
    def FileNames(self, reverse=True):  # 확장자 제거 : True 앞, False 뒤
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file[-len(self._ext):].lower() == self._ext:
                    fileName = file[:file.rfind('.')]
                    if reverse:
                        self.NameDict[fileName] = file
                    else:
                        self.NameDict[file] = fileName
        return self.NameDict

###############################################################################
    def DirNames(self, reverse=True):  # 특정 디렉터리에서 디렉터리 이름만 추출함
        for root, dirs, files in os.walk(self.path):
            for Dir in dirs:
                DirPath = os.path.join(self.path, Dir)
                if reverse:
                    self.NameDict[Dir] = DirPath
                else:
                    self.NameDict[DirPath] = Dir
        return self.NameDict


###############################################################################
class DataToProcess:
    def __init__(self, location):
        self.location = location
        self.dPath = location['input']
        self.dirFind = DirFiles(self.dPath)

###############################################################################
    def DataMining(self, name):
        if os.path.splitext(name)[1] == '.tar':
            self.tarToZip(self.location['input']+'/'+name)
            if os.path.isfile(self.location['input']+'/'+name):
                os.remove(self.location['input']+'/'+name)
        if os.path.splitext(name)[1] == '.zip':
            self.read_input(self.location['input']+'/'+name,
                            self.location['input']+'/'+os.path.splitext(name)[0],
                            None)
        name = os.path.splitext(name)[0]
        csvfind = DirFiles(self.location['input']+'/'+name, '.csv')
        csvName = csvfind.FileNames()

        for cName in csvName:
            self.dataArrange(self.location['input']+'/'+name, csvName[cName])
        f = zipfile.ZipFile(self.location['input']+'/'+name+'.zip', 'w')
        for file in os.listdir(self.location['input']+'/'+name):
            f.write(self.location['input']+'/'+name+'/'+file,
                    file, compress_type=zipfile.ZIP_DEFLATED)
        f.close()
        shutil.rmtree(self.location['input']+'/'+name)
        EaN = os.path.exists(self.location['project']+'/'+name+'.zip')
        if EaN:
            os.remove(self.location['project']+'/'+name+'.zip')
            shutil.move(self.location['input']+'/'+name+'.zip',
                        self.location['project'])
        else:
            shutil.move(self.location['input']+'/'+name+'.zip',
                        self.location['project'])

###############################################################################
    def DataExtract(self, pw=None):
        zipName = self.dirFind.FileNames()
        for name in zipName:  # 특정폴더에서 압축파일을 찾고 해제한다.
            self.read_input(self.dPath+zipName[name], self.dPath+name, pw)

###############################################################################
    def DataConvert(self):
        dirName = self.dirFind.DirNames()

        for dName in dirName:  # 특정폴더에서 압축파일을 찾고 해제한다.
            csvfind = DirFiles(dirName[dName], '.csv')
            csvName = csvfind.FileNames()
            for cName in csvName:
                self.dataArrange(dirName[dName], csvName[cName])

###############################################################################
    def DataUnite(self):
        dirName = self.dirFind.DirNames()
        for name in dirName:
            f = zipfile.ZipFile(dirName[name]+'.zip', 'w')

            for file in os.listdir(dirName[name]):
                f.write(dirName[name]+'/'+file, file,
                        compress_type=zipfile.ZIP_DEFLATED)
            f.close()

###############################################################################
    def DelandMove(self, ProjectPath):
        dirName = self.dirFind.DirNames()
        for name in dirName:
            shutil.rmtree(dirName[name])

        moveName = self.dirFind.FileNames()
        for name in moveName:
            EaN = os.path.exists(ProjectPath+moveName[name])
            if EaN:
                os.remove(ProjectPath+moveName[name])
                shutil.move(self.dPath+moveName[name], ProjectPath)
            else:
                shutil.move(self.dPath+moveName[name], ProjectPath)

###############################################################################
    def read_input(self, zDataName, unzipName, password):
        zf = zipfile.ZipFile(zDataName)
        if password is not None:
            zf.setpassword(password.encode())
        try:
            for name in zf.namelist():
                zf.extract(name, unzipName)
            zf.close()
        except Exception:
            pass

###############################################################################
    def tarToZip(self, fname):
        if tarfile.is_tarfile(fname):
            dpath = os.path.split(fname)[0]
            dname = os.path.split(fname)[1].split('.tar')
            zipdir = os.path.join(dpath, dname[0])
            if not os.path.isdir(zipdir):
                try:
                    os.mkdir(zipdir)
                except FileExistsError:
                    pass

            tar = tarfile.open(fname)
            # 전체 압축 해제
            tar.extractall(zipdir)
            filelist = tar.getnames()
            tar.close()

            basedir = os.path.abspath(os.path.dirname(__file__))
            cli = os.path.join(basedir, 'conf', 'Linux.cli')
            df = self.ResultDATA(zipdir, cli)
            df.to_csv(os.path.join(zipdir, 'ResultData.csv'), mode='w',
                      index=False)

            for dName in filelist:
                if dName.split('.')[1] == 'csv':
                    df = self.EtcToFile(os.path.join(zipdir, dName))
                    df.to_csv(os.path.join(zipdir, dName), mode='w',
                              index=False)
                    self.PdFileDir(os.path.join(zipdir, dName))
                else:
                    pass

###############################################################################
    def ResultDATA(self, dirname, filename):
        encode_type = get_encoding_type(filename)
        ProcessState = os.path.join(dirname, 'ProcessState.csv')
        ExtractResult = os.path.join(dirname, 'ExtractResult.txt')

        DataResult = []
        with open(filename, 'r', encoding=encode_type) as file:
            contents = file.readlines()
            contents = [x.strip() for x in contents]

            for line in contents:
                DataLine = line.split(',')
                Data = DataLine[0]
                DataLine[1] = DataLine[1].replace('ProcessState.csv',
                                                  ProcessState)
                DataLine[1] = DataLine[1].replace('ExtractResult.txt',
                                                  ExtractResult)
                sysMsg = subprocess.getstatusoutput(DataLine[1])
                print(sysMsg)
                if sysMsg[1]:  # 데이터 있음
                    Resul = Data, sysMsg[1].strip()
                    DataResult.append(Resul)

                else:  # 데이터 없음
                    Resul = Data, 'NoData'
                    DataResult.append(Resul)

        return pd.DataFrame(DataResult, columns=('Name', 'Data'))

###############################################################################
    def dataArrange(self, PathDir, PathFile):  # 선택된 파일 추출
        PathDirFile = os.path.join(PathDir, PathFile)
        try:
            if PathFile == 'SecurityPolicy.csv':
                df = self.SeceditFile(PathDirFile)
                df.to_csv(PathDirFile, mode='w', index=False)
            elif PathFile == 'RegistryData.csv':
                df = self.RegistryFile(PathDirFile)
                df.to_csv(PathDirFile, mode='w', index=False)
            elif PathFile == 'UserResult.csv':
                df = self.UserResult(PathDirFile)
                df.to_csv(PathDirFile, mode='w', index=False)
            else:
                self.PdFileDir(PathDirFile)
        except Exception:
            self.PdFileDir(PathDirFile)

###############################################################################
    def EtcToFile(self, file):

        filename = os.path.split(os.path.splitext(file)[0])
        encode_type = get_encoding_type(file)
        try:
            ToData = []
            pattern = re.compile(r'\s+')
            with open(file, 'r', encoding=encode_type) as file:
                contents = file.readlines()
            contents = [x.strip() for x in contents]
            for line in contents:
                if filename[1] == 'passwd' or filename[1] == 'shadow':
                    line = re.sub(pattern, '', line)  # 공백 제거
                    splitLine = line.split(':')
                elif filename[1] == 'Permission':
                    if not line.startswith('ls:'):
                        splitLine = line.split()
                        psn = strToInt().permission(splitLine[0])
                        splitLine.append(int(psn))
                elif (filename[1] == 'WorldWritable'
                      or filename[1] == 'StickBit'
                      or filename[1] == 'RootOrUser'):
                    splitLine = line.split()
                elif filename[1] == 'ProcessState':
                    splitLine = line.split(',')
                ToData.append(splitLine)
        except FileNotFoundError:
            return str('FileNotFoundError')

        if filename[1] == 'passwd':
            return pd.DataFrame(ToData, columns=('Name', 'Pwd', 'Uid', 'Gid',
                                                 'Info', 'Home', 'Login'))
        elif filename[1] == 'shadow':
            return pd.DataFrame(ToData, columns=('Name', 'Pwd', 'Last', 'Min',
                                                 'Max', 'Expiration',
                                                 'Destruction', 'Expiration',
                                                 'reserved'))
        elif filename[1] == 'Permission':
            return pd.DataFrame(ToData, columns=('Permission', 'Link', 'Owner',
                                                 'Group', 'Size', 'Month',
                                                 'Day', 'Year', 'Name',
                                                 'Data'))
        elif filename[1] == 'StickBit' or filename[1] == 'RootOrUser':
            return pd.DataFrame(ToData, columns=('Permission', 'Link', 'Owner',
                                                 'Group', 'Size', 'Month',
                                                 'Day', 'Year', 'Name'))
        elif filename[1] == 'WorldWritable':
            return pd.DataFrame(ToData, columns=('Inode', 'BlockCount',
                                                 'Permission', 'Link', 'Owner',
                                                 'Group', 'Size', 'Month',
                                                 'Day', 'Year', 'Name'))
        elif filename[1] == 'ProcessState':
            return pd.DataFrame(ToData, columns=('Name', 'Started',
                                                 'Cmd')).drop([0])
        else:
            return pd.DataFrame(ToData)

###############################################################################
    def SeceditFile(self, filename):  # SeceditFile를 pandas형식으로 불러온다.
        encode_type = get_encoding_type(filename)
        try:
            ToData = []
            pattern = re.compile(r'\s+')
            with open(filename, 'r', encoding=encode_type) as file:
                contents = file.readlines()
            contents = [x.strip() for x in contents]
            for line in contents:
                line = line.replace('"', '')
                line = line.replace(',', '')
                line = re.sub(pattern, '', line)  # 공백 제거
                splitLine = line.split('=')
                ToData.append(splitLine)
        except FileNotFoundError:
            return str('FileNotFoundError')
        return pd.DataFrame(ToData, columns=('Name', 'Data')).dropna()

###############################################################################
    def RegistryFile(self, filename):
        encode_type = get_encoding_type(filename)
        try:
            ToData = []
            pattern = re.compile(r'\s+')
            with open(filename, 'r', encoding=encode_type) as file:
                contents = file.readlines()
            contents = [x.strip() for x in contents]
            for line in contents:
                line = re.sub(pattern, '', line)  # 공백 제거
                line = line.replace('0x', '')
                line = line.replace('REG_SZ', '=')
                line = line.replace('REG_DWORD', '=')
                line = line.replace('REG_BINARY', '=')
                splitLine = line.split('=')

                ToData.append(splitLine)
        except FileNotFoundError:
            return str('FileNotFoundError')

        return pd.DataFrame(ToData, columns=('Name', 'Data'))

###############################################################################
    def EtcInfoFile(self, filename):  # EtcInfoFile를 pandas형식으로 불러온다.
        encode_type = get_encoding_type(filename)
        try:
            ToData = []
            pattern = re.compile(r'\s+')
            with open(filename, 'r', encoding=encode_type) as file:
                contents = file.readlines()
            contents = [x.strip() for x in contents]
            for line in contents:
                line = re.sub(pattern, '', line)  # 공백 제거
                splitLine = line.split(':')
                ToData.append(splitLine)
        except FileNotFoundError:
            return str('FileNotFoundError')
        return pd.DataFrame(ToData, columns=('Name', 'Data'))

###############################################################################
    def UserResult(self, filename):  # NetStatFile pandas형식으로 불러온다.
        NameInfo = []
        UserInfo = {'User name': [],
                    'Account active': [],
                    'Account expires': [],
                    'Last logon': [],
                    'Password expires': [],
                    'Password changeable': [],
                    'Password required': [],
                    'Password last set': [],
                    'Local Group Memberships': []}
        encode_type = get_encoding_type(filename)
        try:
            with open(filename, 'r', encoding=encode_type) as file:
                contents = file.readlines()
            contents = [x.strip() for x in contents]
            for line in UserInfo.keys():
                NameInfo.append(line)
            for line in contents:
                line = line.rstrip()
                if line.startswith(NameInfo[0]):
                    Product = line.split()
                    result = ' '.join(Product[2:])
                    UserInfo[NameInfo[0]].append(result)

                if line.startswith(NameInfo[1]):
                    Product = line.split()
                    result = ' '.join(Product[2:])
                    UserInfo[NameInfo[1]].append(result)

                if line.startswith(NameInfo[2]):
                    Product = line.split()
                    result = ' '.join(Product[2:])
                    UserInfo[NameInfo[2]].append(result)

                if line.startswith(NameInfo[3]):
                    Product = line.split()
                    result = ' '.join(Product[2:])
                    UserInfo[NameInfo[3]].append(result)

                if line.startswith(NameInfo[4]):
                    Product = line.split()
                    result = ' '.join(Product[2:])
                    UserInfo[NameInfo[4]].append(result)

                if line.startswith(NameInfo[5]):
                    Product = line.split()
                    result = ' '.join(Product[2:])
                    UserInfo[NameInfo[5]].append(result)

                if line.startswith(NameInfo[6]):
                    Product = line.split()
                    result = ' '.join(Product[2:])
                    UserInfo[NameInfo[6]].append(result)

                if line.startswith(NameInfo[7]):
                    Product = line.split()
                    result = ' '.join(Product[3:])
                    UserInfo[NameInfo[7]].append(result)

                if line.startswith(NameInfo[8]):
                    Product = line.split()
                    result = ' '.join(Product[3:])
                    UserInfo[NameInfo[8]].append(result)

        except FileNotFoundError:
            return str('FileNotFoundError')
        return pd.DataFrame(UserInfo)

###############################################################################
    def PdFileDir(self, filename):  # 인코딩 UTF-8로 pandas형식으로 불러온다.
        encode_type = get_encoding_type(filename)
        try:
            with open(filename, 'r', encoding=encode_type) as file:
                contents = file.readlines()
            contents = [x.strip(', ') for x in contents]

            ToData = []
            for line in contents:
                text = re.sub(', ', ' ', line)
                ToData.append(text)

            with open(filename, 'w', encoding='utf-8', newline='\n') as file:
                for line in ToData:
                    file.write(line)
        except FileNotFoundError:
            return str('FileNotFoundError')
        return filename

###############################################################################
    def NetStatFile(self, filename):  # NetStatFile pandas형식으로 불러온다.
        encode_type = get_encoding_type(filename)
        try:
            ToData = []
            with open(filename, 'r', encoding=encode_type) as file:
                for i, line in enumerate(file):
                    if i >= 4:
                        splitLine = line.split()
                        ToData.append(splitLine)
        except FileNotFoundError:
            return str('FileNotFoundError')
        return pd.DataFrame(ToData, columns=('Proto', 'LocalAddress',
                                             'ForeignAddress',
                                             'State', 'PID'))


###############################################################################
class DataUnpack:
    def __init__(self, ProjectPath):
        self.ProjectPath = ProjectPath
        self.zipName = FindDataFiles(self.ProjectPath, 'zip')

###############################################################################
    def UnpackExtract(self, zID):
        archive = DataToZipfile(self.ProjectPath+'/'+self.zipName.get(zID))
        csvName = archive.Get_FileList()

        try:
            RegistryData = archive.FileToPd(
                csvName['RegistryData']).dropna(axis=1, how='all')
            RegistryData = Extraction('RegistryData').Analysis(RegistryData)
        except Exception:
            ToData = {'Name': ['RegistryData'], 'Data': [str(0)]}
            RegistryData = pd.DataFrame(ToData)

        try:
            result = archive.FileToPd(
                csvName['ExtractResult']).dropna(axis=1, how='all')
            result = Extraction(zID).Analysis(result)
            result = result.replace(' ', '', regex=True)

        except Exception:
            ToData = {'Name': ['result'], 'Data': [str(0)]}
            result = pd.DataFrame(ToData)

        try:
            LogicalDisk = archive.FileToPd(
                csvName['LogicalDisk']).dropna(axis=1, how='all')
            LogicalDisk = Extraction('LogicalDisk').Analysis(LogicalDisk)

        except Exception:
            ToData = {'Name': ['LogicalDisk'], 'Data': [str(0)]}
            LogicalDisk = pd.DataFrame(ToData)

        try:
            NteventLog = archive.FileToPd(
                csvName['NteventLog']).dropna(axis=1, how='all')
            NteventLog = Extraction('NteventLog').Analysis(NteventLog)

        except Exception:
            ToData = {'Name': ['NteventLog'], 'Data': [str(0)]}
            NteventLog = pd.DataFrame(ToData)

        try:
            QFEInformation = archive.FileToPd(
                csvName['QFEInformation']).dropna(axis=1, how='all')
            QFEInformation = Extraction('QFEInformation').Analysis(
                QFEInformation)

        except Exception:
            ToData = {'Name': ['QFEInformation'], 'Data': [str(0)]}
            QFEInformation = pd.DataFrame(ToData)

        try:
            SecurityPolicy = archive.FileToPd(
                csvName['SecurityPolicy']).dropna(axis=1, how='all')
            SecurityPolicy = Extraction('SecurityPolicy').Analysis(
                SecurityPolicy)

        except Exception:
            ToData = {'Name': ['SecurityPolicy'], 'Data': [str(0)]}
            SecurityPolicy = pd.DataFrame(ToData)

        try:
            Service = archive.FileToPd(
                csvName['Service']).dropna(axis=1, how='all')
            Service = Extraction('Service').Analysis(Service)

        except Exception:
            ToData = {'Name': ['Service'], 'Data': [str(0)]}
            Service = pd.DataFrame(ToData)

        try:
            StartUp = archive.FileToPd(
                csvName['StartUp']).dropna(axis=1, how='all')
            StartUp = Extraction('StartUp').Analysis(StartUp)

        except Exception:
            ToData = {'Name': ['StartUp'], 'Data': [str(0)]}
            StartUp = pd.DataFrame(ToData)

        try:
            UserAccount = archive.FileToPd(
                csvName['UserAccount']).dropna(axis=1, how='all')
            UserAccount = Extraction('UserAccount').Analysis(UserAccount)

        except Exception:
            ToData = {'Name': ['UserAccount'], 'Data': [str(0)]}
            UserAccount = pd.DataFrame(ToData)

        try:
            UserResult = archive.FileToPd(
                csvName['UserResult']).dropna(axis=1, how='all')
            UserResult = Extraction('UserResult').Analysis(UserResult)

        except Exception:
            ToData = {'Name': ['UserResult'], 'Data': [str(0)]}
            UserResult = pd.DataFrame(ToData)

        try:
            ResultData = archive.FileToPd(
                csvName['ResultData']).dropna(axis=1, how='all')
            ResultData = Extraction('ResultData').Analysis(ResultData)

        except Exception:
            ToData = {'Name': ['ResultData'], 'Data': [str(0)]}
            ResultData = pd.DataFrame(ToData)

        try:
            ProcessState = archive.FileToPd(
                csvName['ProcessState']).dropna(axis=1, how='all')
            ProcessState = Extraction('ProcessState').Analysis(ProcessState)

        except Exception:
            ToData = {'Name': ['ProcessState'], 'Data': [str(0)]}
            ProcessState = pd.DataFrame(ToData)

        try:
            Permission = archive.FileToPd(
                csvName['Permission']).dropna(axis=1, how='all')
            Permission = Extraction('Permission').Analysis(Permission)

        except Exception:
            ToData = {'Name': ['Permission'], 'Data': [str(0)]}
            Permission = pd.DataFrame(ToData)

        frames = [RegistryData, result, LogicalDisk, NteventLog,
                  QFEInformation, SecurityPolicy, Service, StartUp,
                  UserAccount, UserResult, ResultData, ProcessState,
                  Permission]

        return pd.concat(frames, sort=True).fillna('NoData')
###############################################################################


def DataTravel(project, input):
    Data = DataToProcess(project)
    Data.DataExtract()
    Data.DataConvert()
    Data.DataUnite()
    Data.DelandMove(input)
