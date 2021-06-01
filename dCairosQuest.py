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
parser.add_argument("-m", "--dMining", dest="dMining", action="store_true")
parser.add_argument("-a", "--dAnalysis", dest="dAnalysis", action="store_true")
parser.add_argument("-c", "--aControl", dest="aControl", action="store_true")
# __init__#####################################################################
basedir = os.path.abspath(os.path.dirname(__file__))
init = Initialize(basedir)
init.dirCheck()
location = init.run()
args = parser.parse_args()
###############################################################################
if args.dMining:
    for name in tqdm(os.listdir(location['input']), desc='데이터마이닝[DataMining]'):
        DataToProcess(location).DataMining(name)
###############################################################################
if args.dAnalysis:
    for dataname in tqdm(FindDataFiles(location['project'], 'zip').keys(), desc='데이터분석[DataAnalysis]'):
        Criterion = DataAnalysis(location['conf']).BaseLine(dataname)
        Object = DataUnpack(location['project']).UnpackExtract(dataname)
        Proto = DataAnalysis(location['conf']).BaseReport(dataname)
        dCairos(Criterion, Object, Proto).dWorkerRun(location['output']+'/'+ dataname)
###############################################################################
if args.aControl:
    for name in tqdm(os.listdir(location['input']), desc='데이터마이닝[DataMining]'):
        DataToProcess(location).DataMining(name)
    for dataname in tqdm(FindDataFiles(location['project'], 'zip').keys(), desc='데이터분석[DataAnalysis]'):
        Criterion = DataAnalysis(location['conf']).BaseLine(dataname)
        Object = DataUnpack(location['project']).UnpackExtract(dataname)
        Proto = DataAnalysis(location['conf']).BaseReport(dataname)
        dCairos(Criterion, Object, Proto).dWorkerRun(location['output']+'/' + dataname)
