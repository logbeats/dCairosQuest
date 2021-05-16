import numpy as np


###############################################################################
class CodeItemClassify:
    def __init__(self, df):
        self.item = {}
        CodeItems = df['ItemCode'].unique()
        for term in CodeItems:
            amnt_sum = df.loc[df['ItemCode'] == term]
            self.item[term] = amnt_sum

###############################################################################
    def CodeItemList(self, code):
        name = []
        data = []
        result = []
        for i, j in enumerate(self.item[code]['ItemCode']):
            name.append(self.item[code].iloc[i]['Name'])
            data.append(self.item[code].iloc[i]['Data'])
            result.append(str(self.item[code].iloc[i]['Result']))
        name = "\n".join(name)
        data = "\n".join(data)
        result = "\n".join(result)
        return name, data, result


###############################################################################
class DataWorker:
    def __init__(self, df):
        self.df = df

###############################################################################
    def run(self, Proto, ostype):
        num = self.df['ItemCode'].unique()
        for Term in np.sort(num, axis=None):
            self.SheetTerm(self.df, Term, Proto)
        if ostype == 'PC':
            self.ConvertPC(Proto)
        elif ostype == 'Windows':
            self.DataFtpNA(Proto)
            self.ConvertWindows(Proto)
        elif ostype == 'IIS':
            self.ConvertIIS(Proto)
        elif ostype == 'Linux':
            self.ConvertLinux(Proto)
        else:
            pass

###############################################################################
    def SheetTerm(self, df, Term, Proto):
        Data = CodeItemClassify(df).CodeItemList(Term)
        Nanoom = Term.split('-')
        try:
            Number = int(Nanoom[1])
            Proto.iat[Number, 3] = Data[0]
            Proto.iat[Number, 4] = Data[1]
            Proto.iat[Number, 5] = Data[2]
        except IndexError:
            pass

###############################################################################
    def ConvertPC(self, Proto):
        indexCount = list(Proto.index)
        for Number in indexCount:
            Convert = str(Proto.iloc[Number, 5])

            if Convert != 'None':
                Convert = Convert.replace('0', '양호')
                Convert = Convert.replace('1', '취약')
                if Number == 4 or Number == 9:
                    Convert = Convert.replace('2', '양호')
                else:
                    Convert = Convert.replace('2', '취약')
                Proto.iloc[Number, 5] = Convert
            else:
                pass

###############################################################################
    def ConvertWindows(self, Proto):
        indexCount = list(Proto.index)
        for Number in indexCount:
            Convert = str(Proto.iloc[Number, 5])

            if Convert != 'None':
                Convert = Convert.replace('0', '양호')
                Convert = Convert.replace('1', '취약')
                Convert = Convert.replace('3', 'N/A')
                if Number == 2 or Number == 10 or Number == 26:
                    Convert = Convert.replace('2', '취약')
                else:
                    Convert = Convert.replace('2', '양호')
                Proto.iloc[Number, 5] = Convert
            else:
                pass

    def DataFtpNA(self, Proto):
        Convert = str(Proto.iloc[13, 5])
        if Convert != '1':
            for Number in range(14, 17):
                Proto.iat[Number, 3] = 'FTP Service'
                Proto.iat[Number, 4] = '미사용'
                Proto.iat[Number, 5] = '3'
        else:
            pass

###############################################################################
    def ConvertIIS(self, Proto):
        indexCount = list(Proto.index)
        for Number in indexCount:
            Convert = str(Proto.iloc[Number, 5])

            if Convert != 'None':
                Convert = Convert.replace('0', '양호')
                Convert = Convert.replace('1', '취약')
                Convert = Convert.replace('2', '양호')
                Proto.iloc[Number, 5] = Convert
            else:
                pass

    def ConvertLinux(self, Proto):
        indexCount = list(Proto.index)
        for Number in indexCount:
            Convert = str(Proto.iloc[Number, 5])

            if Convert != 'None':
                Convert = Convert.replace('0', '양호')
                Convert = Convert.replace('1', '취약')
                Convert = Convert.replace('3', 'N/A')
                if Number == 3:
                    Convert = Convert.replace('2', '취약')
                else:
                    Convert = Convert.replace('2', '양호')
                Proto.iloc[Number, 5] = Convert
            else:
                pass
