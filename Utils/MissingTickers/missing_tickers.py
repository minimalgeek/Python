from pprint import pprint
import json


def open_and_read(name):
    with open(name) as f:
        tickers = f.readlines()
        return tickers


tickers_A = open_and_read('tickers_A.csv')
tickers_B = open_and_read('tickers_B.csv')

diff = list(set(tickers_A) - set(tickers_B))
jsondiff = [{'Symbol': x.split('\n')[0]} for x in diff]

diff = json.dump(jsondiff, open('NAS_Missing.json', mode='w', encoding='utf-8'))