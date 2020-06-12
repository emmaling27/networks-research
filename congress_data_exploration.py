import numpy as np
import modin.pandas as pd
import matplotlib.pyplot as plt


def plot_histogram(congress_df, suppress_plot=False):
    num_of_cosponsors_per_bill = {}
    for bill in congress_df.bill_number.unique():
        num_of_cosponsors_per_bill[bill] = 0
    for bill in congress_df.bill_number:
        num_of_cosponsors_per_bill[bill] += 1
    max_cosponsors = max(num_of_cosponsors_per_bill.values())
    counts_of_bills_with_x_cosponsors = np.zeros(max_cosponsors + 1)
    for i in num_of_cosponsors_per_bill.values():
        counts_of_bills_with_x_cosponsors[i] += 1
    if not suppress_plot:
        plt.plot(range(2,50), counts_of_bills_with_x_cosponsors[2:50])
        plt.xlabel("Number of Cosponsors")
        plt.ylabel("Number of Bills")
        plt.show()
    return counts_of_bills_with_x_cosponsors.astype(int)

def find_num_of_cosponsors(t, arr): 
    i = 0
    while t > 0:
        t -= arr[i]
        i += 1
    return i

def plot_fraction_of_bills_by_cosponsors():
    for i in range(93, 115):
        df = pd.read_csv("data/govtrack_cosponsor_data/govtrack_cosponsor_data_" + str(i) + "_congress.csv")
        cosponsors_for_threshold = []
        threshold_range = np.arange(.5, 1, .05)
        for t in threshold_range:
            cosponsors_for_threshold.append(find_num_of_cosponsors(t * df.bill_number.unique().shape[0], plot_histogram(df, True)))
        plt.plot(threshold_range, cosponsors_for_threshold, label=i)
    plt.xlabel("Fraction of Bills")
    plt.ylabel("Number of Cosponsors")
    plt.title("Fraction of Bills by Cosponsor Number")
    plt.savefig("plots/fraction_of_bills_by_cosponsors")
    plt.show()