from pprint import pprint

def open_and_read(name):
    with open(name) as f:
        tickers = f.readlines()
        return tickers

tickers_A = open_and_read('tickers_A.csv')
tickers_B = open_and_read('tickers_B.csv')

diff = list(set(tickers_A) - set(tickers_B))
pprint(diff)

with open('diff.csv', mode='w', encoding='utf-8') as f:
    f.writelines(diff)
