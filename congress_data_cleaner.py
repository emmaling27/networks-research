import pandas as pd
import os
from os.path import join
from congress_data_helpers import last_name, get_last_name

class CongressDataCleaner():

    def __init__(self, raw_path, clean_path, party_affiliation_path):
        self.raw_path = raw_path
        self.clean_path = clean_path
        self.party_affiliation_path = party_affiliation_path
        self.party_affiliations = self.get_party_affiliations()

    def get_party_affiliations(self):
        house_affil = pd.read_csv(join(self.party_affiliation_path,'house.csv'))
        senate_affil = pd.read_csv(join(self.party_affiliation_path, 'senate.csv'))
        party_affiliations = house_affil.append(senate_affil)
        party_affiliations = party_affiliations.apply(get_last_name, axis=1)
        party_affil_dict = {}
        for name, party in party_affiliations.unique():
            if party == 100:
                party_affil_dict[name] = "Democrat"
            elif party == 200:
                party_affil_dict[name] = "Republican"
        return party_affil_dict

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
        new_data = {'unit': [], 'u': [], 'u_type': [], 'v_type': [], 'v': [], 'time': []}
        for _, sponsor_row in df[df.sponsor].iterrows():
            sponsor = last_name(sponsor_row['name'])
            for _, cosponsor_row in df[df.bill_number == sponsor_row.bill_number].iterrows():
                cosponsor = last_name(cosponsor_row['name'])
                if sponsor != cosponsor and sponsor in self.party_affiliations.keys() and cosponsor in self.party_affiliations.keys():
                    new_data['unit'].append(cosponsor_row.bill_number)
                    new_data['u'].append(sponsor)
                    new_data['u_type'].append(self.party_affiliations[sponsor])
                    new_data['v'].append(cosponsor)
                    new_data['v_type'].append(self.party_affiliations[cosponsor])
                    new_data['time'].append(sponsor_row.date_signed)
        new_df = pd.DataFrame(new_data)
        new_df = new_df.sort_values('time')
        return new_df

    def clean_all_data(self, t=None):
        """Creates and saves bill dfs of all congresses, optionally below threshold t"""
        if t:
            path = join(self.clean_path, 'below_' + str(t) + '_cosponsors/')
        else:
            path = join(self.clean_path, 'full/')
        os.mkdir(path)
        for congress in range(93, 115):
            congress_df = pd.read_csv(join(self.raw_path, 'govtrack_cosponsor_data_' + str(congress) + '_congress.csv'))
            if t:
                congress_df = self.below_threshold_df(congress_df, t)
            self.clean_df(congress_df, True).to_csv(join(path, 'congress_' + str(congress) + '_house.csv'), index=False)
            self.clean_df(congress_df, False).to_csv(join(path, 'congress_' + str(congress) + '_senate.csv'), index=False)
