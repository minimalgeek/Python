from datetime import datetime, timedelta
import pymongo
import pandas as pd
import os.path
from nltk import word_tokenize
import logging

class ToneCalc(object):

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['python_import']
        self.collection = self.db['earnings_transcript']
        self.initialize_positive_negative_words()
        
    def initialize_positive_negative_words(self):
        scriptpath = os.path.dirname(__file__)
        filename = os.path.join(scriptpath, 'henry_wordlist.xlsx')
        henry_words = pd.read_excel(open(filename, 'rb'), sheetname=0)
        self.positive = henry_words[henry_words['Positive tone'] == 1]['Word'].str.lower()
        self.negative = henry_words[henry_words['Negative tone'] == 1]['Word'].str.lower()

    def get_words(self, transcript, prop):
        return word_tokenize(transcript[prop])

    def process_words(self, words):
        pos_count, neg_count = 0, 0
        for word in words:
            if (self.negative == word.lower()).any():
                neg_count += 1
            elif (self.positive == word.lower()).any():
                pos_count += 1
        return {'positiveCount' : pos_count, 'negativeCount' : neg_count}

    def process_tone(self, transcript):
        words = self.get_words(transcript, 'rawText')
        q_and_a_words = self.get_words(transcript, 'qAndAText')

        h_tone = self.process_words(words)
        q_and_a_h_tone = self.process_words(q_and_a_words)
        return (h_tone, q_and_a_h_tone, len(words), len(q_and_a_words))

    def process_all_and_save(self):
        transcripts = self.collection.find()
        for transcript in transcripts:
            if 'h_tone' in transcript:
                logging.info(transcript['url'] + ' already calculated')
                continue
            h_tone, q_and_a_h_tone, wordSize, qAndAWordSize = self.process_tone(transcript)
            if isinstance(transcript['publishDate'], str):
                dt = datetime.strptime(transcript['publishDate'], '%Y-%m-%dT%H:%M:%SZ')
            else:
                dt = transcript['publishDate']
            date_number = (dt.year - 1900)*10000 + (dt.month)*100 + (dt.day)
            time_number = (dt.hour)*10000 + (dt.minute)*100 + (dt.second)
            self.collection.update_one(
                {'_id': transcript['_id']},
                {'$set': {'h_tone': h_tone,
                          'q_and_a_h_tone' : q_and_a_h_tone,
                          'wordSize' : wordSize,
                          'q_and_a_wordSize' : qAndAWordSize,
                          'date_number' : date_number,
                          'time_number' : time_number}})
            logging.info(transcript['url'] + ' updated')


if __name__ == '__main__':
    logging.basicConfig(filename='tone_calc.log',level=logging.DEBUG)
    tone_calc = ToneCalc()
    tone_calc.process_all_and_save()
