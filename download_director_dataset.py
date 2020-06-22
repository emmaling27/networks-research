import wget

"""
Downloads the director dataset from http://www.boardsandgender.com/data
"""

for year in range(2002, 2012):
    for month in range(1, 13):
        month_str = str(month)
        if len(month_str) == 1:
            month_str = '0' + month_str
        url = 'http://www.boardsandgender.com/data/net1m/net1m_' + str(year) + '-' + month_str + '-01.txt'
        try:
            wget.download(url, '/Users/emmaling/Documents/networks-research/data/directors/directors_' + str(year) + '-' + month_str + '.tsv')
        except:
            print('could not download dataset for ' + str(year) + ' ' + month_str)