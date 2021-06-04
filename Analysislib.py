# -*- coding: utf-8 -*-
import os
import pandas as pd


###############################################################################
class ComparingOperator:
    Comparison = {'==': 'eq',
                  '!=': 'ne',
                  '>=': 'gte',
                  '<=': 'lte',
                  '>': 'gt',
                  '<': 'lt',
                  'in': 'in',
                  'nin': 'nin'}

    Logic = {'And': 'and',
             'Or': 'or',
             'Nor': 'nor',
             'Not': 'not'}

###############################################################################
    def __init__(self, argument, a, b, option=False):
        self.iData = []

        method = getattr(self, self.Comparison[argument])
        return method(a, b, option)

###############################################################################
    def eq(self, a, b, option):
        if option:
            if a == b and a != 0:
                self.iData = 1
            else:
                self.iData = 0
        else:
            if a == b:
                self.iData = 1
            else:
                self.iData = 0

###############################################################################
    def ne(self, a, b, option):
        if option:
            if a != b and a != 0:
                self.iData = 1
            else:
                self.iData = 0
        else:
            if a != b:
                self.iData = 1
            else:
                self.iData = 0

###############################################################################
    def gte(self, a, b, option):
        if option:
            if a >= b and a != 0:
                self.iData = 1
            else:
                self.iData = 0
        else:
            if a >= b:
                self.iData = 1
            else:
                self.iData = 0

###############################################################################
    def lte(self, a, b, option):
        if option:
            if a <= b and a != 0:
                self.iData = 1
            else:
                self.iData = 0
        else:
            if a <= b:
                self.iData = 1
            else:
                self.iData = 0

###############################################################################
    def gt(self, a, b, option):
        if option:
            if a > b and a != 0:
                self.iData = 1
            else:
                self.iData = 0
        else:
            if a > b:
                self.iData = 1
            else:
                self.iData = 0

###############################################################################
    def lt(self, a, b, option):
        if option:
            if a < b and a != 0:
                self.iData = 1
            else:
                self.iData = 0
        else:
            if a < b:
                self.iData = 1
            else:
                self.iData = 0

###############################################################################
    def result(self, reverse=True):
        if reverse:
            if self.iData:
                return self.iData - 1
            else:
                return self.iData + 1
        else:
            return self.iData


###############################################################################
class dPAPERsAnalysis:

    def __init__(self):
        self.Name = []
        self.Data = []
        self.Result = []
        self.Collect = []
        self.Explanatory = []
###############################################################################

    def SeceditAnalysis(self, df, df2):

        for dfresult in df.values:
            temp = df2[(df2.Name.str.lower() == dfresult[0].lower())]
            df = pd.Series(dfresult, index=['Name', 'Compare', 'Data',
                                            'Explanatory', 'ItemCode'])

            if temp.empty:
                self.Explanatory.append(df['ItemCode'])
                self.Name.append(df['Name'])
                self.Data.append('NoData')
                self.Result.append(2)
            else:
                self.Explanatory.append(df['ItemCode'])
                self.Name.append(df['Name'])
                self.Data.append(temp.iloc[0]['Data'])

                if temp.iloc[0]['Data'] == 'NoData':
                    self.Result.append(ComparingOperator(df['Compare'],
                                                         'NoData',
                                                         df['Data']).result())
                else:
                    self.Result.append(ComparingOperator(df['Compare'],
                                                         temp.iloc[0]['Data'],
                                                         df['Data']).result())

        return self.Name, self.Data, self.Result, self.Explanatory
###############################################################################

    def AnalysisCollect(self, df, df2):

        for dfresult in df.values:
            temp = df2[(df2.Name.str.lower() == dfresult[0].lower())]

            df = pd.Series(dfresult, index=['Name', 'Compare', 'Data',
                                            'Explanatory', 'ItemCode'])

            if temp.empty:
                self.Name.append(df['Name'])
                self.Collect.append(0)
                self.Explanatory.append(df['Explanatory'])
            else:
                self.Name.append(df['Name'])
                self.Collect.append(1)
                self.Explanatory.append(df['Explanatory'])
        return self.Name, self.Collect, self.Explanatory
###############################################################################


class DataAnalysis:
    def __init__(self, ConfPath):
        self.ConfPath = ConfPath

    def xlsxTOcsv(self, file, Name):
        iPath = os.path.join(self.ConfPath, 'xlsx', Name, file)
        if iPath.split('.')[1] == 'xlsx':
            df = pd.read_excel(iPath, header=None)
            if Name == 'BaseLine':
                df = df.loc[:,[0,1,2,3,4]]
            elif Name == 'BaseReport':
                df = df.loc[:,[0,1,2,3,4,5,6]]
            oPath = os.path.join(self.ConfPath, 'csv', Name)
            cfile = os.path.join(oPath, file.split('.')[0]+'.csv')
            df.to_csv(cfile, mode='w', index=False)

    def xlsxTOcsvAll(self, path):
        iPath = os.path.join(self.ConfPath, 'xlsx', path)

        for file in os.listdir(iPath):
            if file.split('.')[1] == 'xlsx':
                
                efile = os.path.join(iPath, file)
                df = pd.read_excel(efile, header=None)
                if path == 'BaseLine':
                    df = df.loc[:,[0,1,2,3,4]]
                elif path == 'BaseReport':
                    df = df.loc[:,[0,1,2,3,4,5,6]]
                oPath = os.path.join(self.ConfPath, 'csv', path)
                cfile = os.path.join(oPath, file.split('.')[0]+'.csv')
                df.to_csv(cfile, mode='w', index=False)
    
    def BaseLine(self, targetFile):
        dPath = os.path.join(self.ConfPath, 'csv')
        os_type = targetFile[targetFile.rfind('-')+1:]
        lfile = os.path.join(dPath, 'BaseLine', os_type+'.csv')
        df = pd.read_csv(lfile)

        return df

    def BaseReport(self, targetFile):
        dPath = os.path.join(self.ConfPath, 'csv')
        os_type = targetFile[targetFile.rfind('-')+1:]
        rfile = os.path.join(dPath, 'BaseReport', os_type+'.csv')
        df = pd.read_csv(rfile)

        return df
###############################################################################
