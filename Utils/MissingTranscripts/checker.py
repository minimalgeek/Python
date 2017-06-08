from pymongo import MongoClient
import json
from datetime import datetime, timedelta
from pprint import pprint

if __name__ == "__main__":
    database = MongoClient(host='localhost', port=27017).get_database('python_import')

    collection_transcripts = database.get_collection('earnings_transcript')
    collection_dates = database.get_collection('zacks_earnings_call_dates')

    missing_transcripts = []
    found_transcripts = []

    tickers = json.loads(open('NAS_ALL.json', encoding='utf-8').read())
    for ticker in tickers:
        symbol = ticker['Symbol']
        dates_for_ticker = collection_dates.find({'ticker': symbol},
                                                 projection={'nextReportDate': True})
        for date_for_ticker in list(dates_for_ticker):

            start = date_for_ticker['nextReportDate']
            end = date_for_ticker['nextReportDate'] + timedelta(days=2)

            transcript = collection_transcripts.find_one(
                {'tradingSymbol': symbol,
                 'publishDate': {'$gte': start, '$lte': end}}
            )

            transcript_blueprint = {'ticker': symbol, 'date': start}
            if transcript is None:
                missing_transcripts.append(transcript_blueprint)
            else:
                found_transcripts.append(transcript_blueprint)
    print('Missing transcripts > ', len(missing_transcripts))
    pprint(missing_transcripts)
    print('Found transcripts > ', len(found_transcripts))
    pprint(found_transcripts)
