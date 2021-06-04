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
parser.add_argument("-f", "--dfile", dest="dfile", action="store")
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
    if div == 'BaseLine':
        for name in tqdm(os.listdir(os.path.join(dpach, 'BaseLine')), desc='데이터설정[DataSetting]'):
            DataAnalysis(location['conf']).xlsxTOcsv(name, 'BaseLine')
    elif div == 'BaseReport':
        for name in tqdm(os.listdir(os.path.join(dpach, 'BaseReport')), desc='데이터설정[DataSetting]'):
            DataAnalysis(location['conf']).xlsxTOcsv(name, 'BaseReport')
    elif div == 'All':
        for name in tqdm(os.listdir(os.path.join(location['conf'], 'xlsx')), desc='데이터설정[DataSetting]'):
            DataAnalysis(location['conf']).xlsxTOcsvAll(name)
    else:
        pass

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
