# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import xlsxwriter
from Analysislib import dPAPERsAnalysis
from dWorkerlib import DataWorker


###############################################################################
class dCairos:
    def __init__(self, Criterion, Object, Proto):
        dAnalysis = np.array(
            dPAPERsAnalysis().SeceditAnalysis(Criterion, Object))
        pdDict = {'Name': dAnalysis[0].astype(str).tolist(),
                  'Data': dAnalysis[1].astype(str).tolist(),
                  'Result': dAnalysis[2].astype(str).tolist(),
                  'ItemCode': dAnalysis[3].astype(str).tolist(), }
        self.df = pd.DataFrame(pdDict)
        self.Proto = Proto

###############################################################################
    def dWorkerRun(self, outfile):
        ostype = outfile[outfile.rfind('-')+1:]
        DataWorker(self.df).run(self.Proto, ostype)
        data = self.Proto.values
        data = data.astype(str).tolist()
        workbook = xlsxwriter.Workbook(outfile+'.xlsx')
        worksheet = workbook.add_worksheet()
###############################################################################
        cell_format = workbook.add_format()
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
        cell_format.set_text_wrap()
###############################################################################
        if ostype == 'PC':
            worksheet.set_column('A:A', 10, cell_format)
            worksheet.set_column('B:B', 70, cell_format)
            worksheet.set_column('C:C', 10, cell_format)
            worksheet.set_column('D:D', 32, cell_format)
            worksheet.set_column('E:E', 12, cell_format)
            worksheet.set_column('F:F', 10, cell_format)
            worksheet.set_column('G:G', 32, cell_format)
        elif ostype == 'Windows':
            worksheet.set_column('A:A', 10, cell_format)
            worksheet.set_column('B:B', 48, cell_format)
            worksheet.set_column('C:C', 10, cell_format)
            worksheet.set_column('D:D', 32, cell_format)
            worksheet.set_column('E:E', 28, cell_format)
            worksheet.set_column('F:F', 10, cell_format)
            worksheet.set_column('G:G', 32, cell_format)
        elif ostype == 'IIS':
            worksheet.set_column('A:A', 10, cell_format)
            worksheet.set_column('B:B', 30, cell_format)
            worksheet.set_column('C:C', 10, cell_format)
            worksheet.set_column('D:D', 20, cell_format)
            worksheet.set_column('E:E', 20, cell_format)
            worksheet.set_column('F:F', 10, cell_format)
            worksheet.set_column('G:G', 30, cell_format)
        elif ostype == 'Linux':
            worksheet.set_column('A:A', 10, cell_format)
            worksheet.set_column('B:B', 50, cell_format)
            worksheet.set_column('C:C', 10, cell_format)
            worksheet.set_column('D:D', 15, cell_format)
            worksheet.set_column('E:E', 15, cell_format)
            worksheet.set_column('F:F', 10, cell_format)
            worksheet.set_column('G:G', 50, cell_format)
###############################################################################
        for count in range(0, len(data)):
            for idx, val in enumerate(data[count]):
                worksheet.write(count+1, idx, val)
        workbook.close()
###############################################################################
