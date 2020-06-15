import matplotlib.pyplot as plt
from os import listdir, mkdir
from os.path import isfile, join
import pickle
import numpy as np

class Plotter():

    def __init__(self, count_path, plots_path, start):
        self.count_path = count_path
        self.plots_path = plots_path
        self.start = start

    def get_marginal_counts(self, arr):
        marginal_counts = []
        for i in range(1, len(arr)):
            marginal_counts.append(arr[i] - arr[i-1])
        return np.array(marginal_counts)

    def plot_f_w_over_time(self, counts, name):
        """Plot cumulative bichromatic fraction of edges added via triadic closure over time"""
        plt.plot(range(self.start, len(counts['f(w)'])), (counts['f(w_b)'] / counts['f(w)'])[self.start:])
        plt.xlabel("Time")
        plt.ylabel("f(w)")
        plt.title(name + " f(w)")
        plt.savefig(join(self.plots_path, name, 'f_t(w).png'))
        plt.show()

    def plot_bichromatic_fraction_f_w_diff_over_time(self, counts, name):
        plt.plot(range(self.start, len(counts['f(w)'])), (counts['f(w_b)'] / counts['f(w)'])[self.start:] - counts['bi_fraction'][self.start:-1])
        plt.xlabel("Time")
        plt.ylabel("f_t(w) - b_(t-1)")
        plt.title(name + " f_t(w) - b_(t-1)")
        plt.savefig(join(self.plots_path, name, 'f_t(w)-b_t-1.png'))
        plt.show()

    def plot_f_w_f_b_ratios_over_time(self, counts, name):
        plt.plot(range(self.start, len(counts['f(w)'])), ((counts['f(w_b)'] / counts['f(w)']) / (counts['f(b_b)'] / counts['f(b)']))[self.start:])
        plt.xlabel("Time")
        plt.ylabel("f(w) / f(b)")
        plt.title(name + " f(w) / f(b)")
        plt.savefig(join(self.plots_path, name, 'f(w)_over_f(b).png'))
        plt.show()

    def plot_f_b_over_time(self, counts, name):
        plt.plot(range(self.start, len(counts['f(b)'])), (counts['f(b_b)'] / counts['f(b)'])[self.start:])
        plt.xlabel("Time")
        plt.ylabel("f(b)")
        plt.title(name + " f(b)")
        plt.savefig(join(self.plots_path, name, 'f(b).png'))
        plt.show()

    def plot_f_w_f_b_separately_over_time(self, counts, name):
        plt.plot(range(self.start, len(counts['f(b)'])), (counts['f(w_b)'] / counts['f(w)'])[self.start:], label="f(w)")
        plt.plot(range(self.start, len(counts['f(b)'])), (counts['f(b_b)'] / counts['f(b)'])[self.start:], label="f(b)")
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Cumulative Bichromatic Ratio")
        plt.title(name + " f(w) and f(b)")
        plt.savefig(join(self.plots_path, name, 'f(b)_and_f(w).png'))
        plt.show()
    
    def plot_marginal_w_b_over_time(self, counts, name):
        plt.plot(range(self.start, len(counts['f(b)'])-1), (self.get_marginal_counts(counts['f(w_b)']) / self.get_marginal_counts(counts['f(w)']))[self.start:], label="w_b/w")
        plt.plot(range(self.start, len(counts['f(b)'])-1), (self.get_marginal_counts(counts['f(b_b)']) / self.get_marginal_counts(counts['f(b)']))[self.start:], label="b_b/b")
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Marginal Bichromatic Ratio")
        plt.title(name + " w_b/w and b_b/b")
        plt.savefig(join(self.plots_path, name, 'bichromatic_fractions_w_and_b.png'))
        plt.show()

    def plot_all(self):
        """Plot all the above"""
        files = [f for f in listdir(self.count_path) if isfile(join(self.count_path, f))]
        try:
            mkdir(self.plots_path)
        except:
            print('plots directory already exists')
        for file_name in files:
            with open(join(self.count_path, file_name), 'rb') as f:
                counts = pickle.load(f)
            file_name = file_name[:-4]
            try:
                mkdir(join(self.plots_path, file_name))
            except:
                print('plots ' + file_name + ' directory already exists')
            self.plot_f_w_over_time(counts, file_name)
            self.plot_bichromatic_fraction_f_w_diff_over_time(counts, file_name)
            self.plot_f_b_over_time(counts, file_name)
            self.plot_f_w_f_b_ratios_over_time(counts, file_name)
            self.plot_f_w_f_b_separately_over_time(counts, file_name)
            self.plot_marginal_w_b_over_time(counts, file_name)