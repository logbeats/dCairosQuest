# -*- coding: utf-8 -*-
import os
from Analysislib import DataAnalysis
from dCairosFilelib import DataToProcess
from dCairosFilelib import DataUnpack
from dCairosFilelib import FindDataFiles
from dCairosFilelib import Initialize
from dCairoslib import dCairos
from tqdm import tqdm


# __init__#####################################################################
basedir = os.path.abspath(os.path.dirname(__file__))
init = Initialize(basedir)
init.dirCheck()
location = init.run()
for name in tqdm(os.listdir(location['input']), desc='데이터마이닝[DataMining]'):
    DataToProcess(location).DataMining(name)
###############################################################################
for dataname in tqdm(FindDataFiles(location['project'], 'zip').keys(),
                     desc='데이터분석[DataAnalysis]'):
    Criterion = DataAnalysis(location['conf']).BaseLine(dataname)
    Object = DataUnpack(location['project']).UnpackExtract(dataname)
    Proto = DataAnalysis(location['conf']).BaseReport(dataname)
    dCairos(Criterion, Object, Proto).dWorkerRun(location['output']+'/'
                                                 + dataname)
