import pandas as pd
import os
from congress_data_helpers import last_name

class CongressDataCleaner():

    def __init__(self, raw_path, clean_path):
        self.raw_path = self._proper_path(raw_path)
        self.clean_path = self._proper_path(clean_path)
    
    def _proper_path(self, path):
        if path[-1] != '/':
            return path + '/'
        else:
            return path

    def below_threshold_df(self, df, t):
        """Returns df with only bills with <= t cosponsors"""
        num_of_cosponsors_per_bill = {}
        for bill in df.bill_number.unique():
            num_of_cosponsors_per_bill[bill] = 0
        for bill in df.bill_number:
            num_of_cosponsors_per_bill[bill] += 1
        df = df.set_index('bill_number')
        for bill in num_of_cosponsors_per_bill:
            if num_of_cosponsors_per_bill[bill] > t:
                df = df.drop(bill)
        return df.reset_index()
    
    def clean_df(self, df, house):
        """Returns cleaned df in standard format"""
        if house:
            df = df[df.district.notnull()]
        else:
            df = df[df.district.isnull()]
        new_data = {'unit': [], 'u': [], 'v': [], 'time': []}
        for _, sponsor_row in df[df.sponsor].iterrows():
            for _, cosponsor_row in df[df.bill_number == sponsor_row.bill_number].iterrows():
                if sponsor_row['name'] != cosponsor_row['name']:
                    new_data['unit'].append(cosponsor_row.bill_number)
                    new_data['u'].append(last_name(sponsor_row['name']))
                    new_data['v'].append(last_name(cosponsor_row['name']))
                    new_data['time'].append(sponsor_row.date_signed)
        new_df = pd.DataFrame(new_data)
        new_df = new_df.sort_values('time')
        return new_df

    def clean_all_data(self, t=None):
        """Creates and saves bill dfs of all congresses, optionally below threshold t"""
        if t:
            path = self.clean_path + 'below_' + str(t) + '_cosponsors/'
        else:
            path = self.clean_path + 'full/'
        os.mkdir(path)
        for congress in range(93, 115):
            congress_df = pd.read_csv(self.raw_path + 'govtrack_cosponsor_data_' + str(congress) + '_congress.csv')
            if t:
                congress_df = self.below_threshold_df(congress_df, t)
            self.clean_df(congress_df, True).to_csv(path + 'congress_' + str(congress) + '_house.csv', index=False)
            self.clean_df(congress_df, False).to_csv(path + 'congress_' + str(congress) + '_senate.csv', index=False)
