# networks-research

The architecture of this network analysis has three stages: data cleaning, generating graphs, and plotting counts of interest. Each file ending in `cleaner.py` creates pandas dataframes with columns: 'u', 'v', 'time', 'u_type', 'v_type', sorted by 'time'. The `Grapher` generates graphs from these dataframes by iteratively going through each row with edge information and counting if the edge is bichromatic or closes a wedge, saving the graphs and counts. The  `Plotter` plots the counts saved by the `Grapher`. The script in `run_full_analysis_on_govtrack_data.py` shows an example of how to run this analysis on the govtrack bill cosponsorship dataset.

Centrality analysis is in both `bill_cosponsorship_analysis.ipynb` and `stochastic_block_model.ipynb`. `SBM` verifies theoretical counts against actual counts from a sample stochastic block model.

The variable names are consistent with the mathematical notation [here](https://www.overleaf.com/project/5ec801258534650001e98c8a) and [here](https://www.overleaf.com/project/5e7caff7fbc31000017c64ea).