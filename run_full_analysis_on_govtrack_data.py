from congress_data_cleaner import CongressDataCleaner
from grapher import Grapher
from plotter import Plotter

'''
Example script for running full analysis on govtrack cosponsor dataset
'''

congress_data_cleaner = CongressDataCleaner('data/govtrack_cosponsor_data/raw', 'data/govtrack_cosponsor_data/clean/', 'data/party_affiliation/')
congress_data_cleaner.clean_all_data()

grapher = Grapher('data/govtrack_cosponsor_data/clean/full/', 'analysis/govtrack_cosponsor_data')
grapher.get_all_counts()

plotter = Plotter('analysis/govtrack_cosponsor_data/counts', 'plots/govtrack_cosponsor_data', 100, 20)
plotter.plot_all()