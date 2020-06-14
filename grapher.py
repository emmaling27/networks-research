import networkx as nx
import numpy as np
from os import listdir, mkdir
from os.path import isfile, join
import pickle
import pandas as pd
from networkx.readwrite.gpickle import write_gpickle, read_gpickle

class Grapher():

    def __init__(self, clean_path, grapher_path):
        self.clean_path = clean_path
        self.grapher_path = grapher_path
    
    def get_counts_over_time(self, df):
        """Output graph and count object with bichromatic fractions, f(w), f(b), f(w_b), f(b_b)"""
        g = nx.Graph()
        counts = {'f(w)': [], 'f(w_b)': [],'f(b)': [], 'f(b_b)': [], 'bi_fraction':[0]}
        w, w_b, b, b_b = 0, 0, 0, 0
        last_time = 0
        for _, row in df.iterrows():
            g.add_nodes_from([row['u'], row['v']])
            if not g.has_edge(row['u'], row['v']):
                if set(g.neighbors(row['u'])).intersection(set(g.neighbors(row['v']))):
                    if row['u_type'] != row['v_type']:
                        w_b += 1
                    w += 1
                else:
                    if row['u_type'] != row['v_type']:
                        b_b += 1
                    b += 1
                g.add_edge(row['u'], row['v'])
            this_time = row['time']
            if this_time != last_time:
                counts['f(w_b)'].append(w_b)
                counts['f(w)'].append(w)
                counts['bi_fraction'].append((w_b + b_b) / (w + b))
                counts['f(b_b)'].append(b_b)
                counts['f(b)'].append(b)
                last_time = this_time
        counts['f(w_b)'].append(w_b)
        counts['f(w)'].append(w)
        counts['bi_fraction'].append((w_b + b_b) / (w + b))
        counts['f(b_b)'].append(b_b)
        counts['f(b)'].append(b)
        for item in counts:
            counts[item] = np.array(counts[item])
        return g, counts
    
    def get_all_counts(self):
        files = [f for f in listdir(self.clean_path) if isfile(join(self.clean_path, f))]
        mkdir(self.grapher_path)
        mkdir(join(self.grapher_path, 'graphs'))
        mkdir(join(self.grapher_path, 'counts'))
        for f in files:
            df = pd.read_csv(join(self.clean_path, f))
            g, counts = self.get_counts_over_time(df)
            write_gpickle(g, join(self.grapher_path, 'graphs', f[:-4] + '.pkl'))
            count_file = open(join(self.grapher_path, 'counts', f[:-4] + '.pkl'), 'wb')
            pickle.dump(counts, count_file)
            count_file.close()

