import pandas as pd
import os
from os.path import join

class DirectorDataCleaner():

    def __init__(self, raw_path, clean_path):
        self.raw_path = raw_path
        self.clean_path = clean_path

    def clean_df(self, month_df, type_df):
        """Returns cleaned df in standard format"""
        month_df.columns = ['u', 'v']
        type_df = type_df.set_index('id')
        df = month_df.join(type_df, on='u').drop('name', axis=1)
        df.columns = ['u', 'v', 'u_type']
        df = df.join(type_df, on='v').drop('name', axis=1)
        df.columns = ['u', 'v', 'u_type', 'v_type']
        return df

    def clean_all_data(self, t=None):
        """Creates and saves bill dfs of all congresses, optionally below threshold t"""
        type_df = pd.read_csv(join(self.raw_path, 'data_people2.tsv'), sep=' ')
        df = pd.DataFrame()
        for year in range(2002, 2012):
            for month in range(1, 13):
                month_str = str(month)
                if len(month_str) == 1:
                    month_str = '0' + month_str
                try:
                    month_df = pd.read_csv(join(self.raw_path, 'directors_' + str(year) + '-' + month_str + '.tsv'), sep=' ')
                    clean_month_df = self.clean_df(month_df, type_df)
                    clean_month_df['time'] = str(year) + '-' + month_str
                    df = df.append(clean_month_df)
                except:
                    print('no dataset for ' + str(year) + ' ' + month_str)
        df.to_csv(join(self.clean_path, 'directors.csv'), index=False)
