# -*- coding: utf-8 -*-
import pandas as pd


###############################################################################
class Extraction:
    def __init__(self, FileName):
        self.FileName = FileName

###############################################################################
    def Analysis(self, DataFrame):
        df = DataFrame
        if self.FileName == 'RegistryData':
            df = df[['Name', 'Data']].rename(
                    columns={'Name': 'Name', 'Data': 'Data'})
            df['Data'] = df['Data'].astype(str)

        elif self.FileName == 'Product':
            df = df[['Name', 'Version']].rename(
                    columns={'Name': 'Name', 'Version': 'Data'})

        elif self.FileName == 'LogicalDisk':
            df = df[['Name', 'FileSystem']].rename(
                    columns={'Name': 'Name', 'FileSystem': 'Data'})

        elif self.FileName == 'QFEInformation':
            df = df[['Description', 'InstalledOn']].rename(
                    columns={'Description': 'Name', 'InstalledOn': 'Data'})
            df = df[df['Name'] == 'Security Update'].sort_values(
                    by='Data',
                    ascending=[False]).iloc[0]['Data'].replace('/', '.')
            ToData = {
                     'Name': ['SecurityUpdate'],
                     'Data': [str(df)]
                     }
            df = pd.DataFrame(ToData)

        elif self.FileName == 'Service':
            df = df[['Caption', 'State']].rename(
                    columns={'Caption': 'Name', 'State': 'Data'})

        elif self.FileName == 'StartUp':
            try:
                df = df[['Caption', 'Command']].rename(
                        columns={'Caption': 'Name', 'Command': 'Data'})
                ToData = {
                         'Name': ['StartUpCount'],
                         'Data': [str(df.index.size)]
                         }
                df = pd.DataFrame(ToData)
            except Exception:
                ToData = {
                         'Name': ['StartUpCount'],
                         'Data': [str(0)]
                         }
                df = pd.DataFrame(ToData)

        elif self.FileName == 'UserAccount':
            df = df[['Name', 'Status']].rename(
                    columns={'Name': 'Name', 'Status': 'Data'})
            UserAccount = list(df['Data']).count('OK')
            df.loc[df.index.size] = ['UserAccount', str(UserAccount)]

        elif self.FileName == 'UserResult':
            Administrators = list(
                    df['Local Group Memberships']).count('*Administrators')
            ToData = {
                     'Name': ['Administrators'],
                     'Data': [str(Administrators)]
                     }
            df = pd.DataFrame(ToData)

        elif self.FileName == 'NteventLog':

            df = df[['FileName', 'MaxFileSize']].rename(
                    columns={'FileName': 'Name', 'MaxFileSize': 'Data'})
            df['Data'] = df['Data'].astype(str)

        elif self.FileName == 'TaskList':
            df = df[['Image Name', 'Status']].rename(
                    columns={'Image Name': 'Name', 'Status': 'Data'})

        elif self.FileName == 'Share':
            df = df[['Name', 'Description']].rename(
                    columns={'Name': 'Name', 'Description': 'Data'})
##############################################################################
        elif self.FileName == 'ResultData':
            df = df[['Name', 'Data']].rename(
                    columns={'Name': 'Name', 'Data': 'Data'})
            df['Data'] = df['Data'].astype(str)

        elif self.FileName == 'ProcessState':
            df = df[['Name', 'Cmd']].rename(
                columns={'Cmd': 'Name', 'Name': 'Data'})

        elif self.FileName == 'Permission':
            df = df[['Name', 'Data']].rename(
                columns={'Name': 'Name', 'Data': 'Data'})
            df['Data'] = df['Data'].astype(str)

        else:
            df = DataFrame

        return df
###############################################################################
