import pandas as pd
import os
from os.path import join

class HighSchoolDataCleaner():

    def __init__(self, raw_path, clean_path):
        self.raw_path = raw_path
        self.clean_path = clean_path

    def clean_df(self, hs_df, type_df):
        """Returns cleaned df in standard format"""
        hs_df.columns = ['time', 'u', 'v', 'class1', 'c2']
        type_df.columns = ['id', 'class', 'gender']
        type_df = type_df.set_index('id')
        df = hs_df.join(type_df, on='u')
        df.columns = ['time', 'u', 'v', 'c', 'c1', 'c2', 'u_type']
        df = df.join(type_df, on='v')
        df.columns = ['time', 'u', 'v', 'c', 'c1', 'c2', 'u_type', 'c2', 'v_type']
        df = df.drop(['c', 'c1', 'c2', 'c2'], axis=1)
        return df

    def clean_all_data(self, t=None):
        """Creates and saves network dfs for high schools in 2011 and 2012"""
        for year in range(2011, 2013):
            hs_df = pd.read_csv(join(self.raw_path, 'highschool_' + str(year) + '.tsv'), sep='\t')
            type_df = pd.read_csv(join(self.raw_path, 'metadata_' + str(year) + '.tsv'), sep='\t')
            self.clean_df(hs_df, type_df).to_csv(join(self.clean_path, 'highschool_' + str(year) + '.csv'), index=False)
