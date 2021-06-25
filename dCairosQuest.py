# -*- coding: utf-8 -*-
import os
from Analysislib import DataAnalysis
from dCairosFilelib import DataToProcess
from dCairosFilelib import DataUnpack
from dCairosFilelib import FindDataFiles
from dCairosFilelib import Initialize
from dCairoslib import dCairos
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='dCairosQuest argument')
parser.add_argument("-v", "--version", dest="version", action="store_true")
parser.add_argument("-s", "--dSetting", dest="dSetting", action="append")
parser.add_argument("-p", "--dProcess", dest="dProcess", action="store_true")
# __init__#####################################################################
basedir = os.path.abspath(os.path.dirname(__file__))
init = Initialize(basedir)
init.dirCheck()
location = init.run()
args = parser.parse_args()
###############################################################################
if args.version:
    ver = '1.0.0'
    print('version :', ver)
###############################################################################
if args.dSetting:
    div = args.dSetting[0]
    dpach = os.path.join(location['conf'], 'xlsx')
    if div.upper() == 'BL':
        for name in tqdm(os.listdir(os.path.join(dpach, 'BaseLine')), desc='데이터설정[DataSetting]'):
            print(name)
            DataAnalysis(location['conf']).xlsxTOcsv(name, 'BaseLine')
    elif div.upper() == 'BR':
        for name in tqdm(os.listdir(os.path.join(dpach, 'BaseReport')), desc='데이터설정[DataSetting]'):
            DataAnalysis(location['conf']).xlsxTOcsv(name, 'BaseReport')
    elif div.upper() == 'BA':
        for name in tqdm(os.listdir(os.path.join(location['conf'], 'xlsx')), desc='데이터설정[DataSetting]'):
            DataAnalysis(location['conf']).xlsxTOcsvAll(name)
    else:
        temp = '-' in div
        if temp:
            data = div.split('-')
            if data[0].upper() == 'BL':
                if data[1] == 'Windows' or data[1] == 'IIS' or data[1] == 'PC' or data[1] == 'Linux':
                    cName = data[1]+'.xlsx'
                    for name in tqdm(range(1), desc='데이터설정[DataSetting]'):
                        DataAnalysis(location['conf']).xlsxTOcsv(cName, 'BaseLine')
                else:
                    print('Not Windows OR IIS OR PC OR Linux')
            elif data[0].upper() == 'BR':
                if data[1] == 'Windows' or data[1] == 'IIS' or data[1] == 'PC' or data[1] == 'Linux':
                    cName = data[1]+'.xlsx'
                    for name in tqdm(range(1), desc='데이터설정[DataSetting]'):
                        DataAnalysis(location['conf']).xlsxTOcsv(cName, 'BaseReport')
                else:
                    print('Not Windows OR IIS OR PC OR Linux')
            else:
                print('bl OR br and [ClassificationName] ex) bl-PC OR br-PC')
        else:
            print('bl OR br OR ba OR bf-[ClassificationName] ex) bf-PC')
###############################################################################
if args.dProcess:
    for name in tqdm(os.listdir(location['input']), desc='데이터마이닝[DataMining]'):
        DataToProcess(location).DataMining(name)
###############################################################################
    for dataname in tqdm(FindDataFiles(location['project'], 'zip').keys(), desc='데이터분석[DataAnalysis]'):
        Criterion = DataAnalysis(location['conf']).BaseLine(dataname)
        Object = DataUnpack(location['project']).UnpackExtract(dataname)
        Proto = DataAnalysis(location['conf']).BaseReport(dataname)
        dCairos(Criterion, Object, Proto).dWorkerRun(location['output']+'/' + dataname)
