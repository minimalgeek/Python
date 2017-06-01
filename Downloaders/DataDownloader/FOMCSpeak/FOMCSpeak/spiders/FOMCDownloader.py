# -*- coding: utf-8 -*-
import scrapy
import json
import logging
from scrapy import FormRequest
from datetime import datetime


class FomcdownloaderSpider(scrapy.Spider):
    name = "FOMCDownloader"
    headers_map = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'hu-HU,hu;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    custom_settings = {
        'ITEM_PIPELINES': {
            'FOMCSpeak.pipelines.MongoPipeline': 100,
        },
        'MONGO_COLLECTION': 'fomc_articles'
    }
    url_to_selector = {
        'www.richmondfed.org': '.pi_footnote p , .pi_speech_content p',
        'www.federalreserve.gov': 'p',
        'www.dallasfed.org': 'p+ p , .separator-red+ p , h1',
        'www.chicagofed.org': 'h1 , p+ p , h3 , h3+ .cfedContent__text p',
        'www.minneapolisfed.org': 'section > p , section div h2 , section h2 , section div p',  # this is shit :(
        'video.cnbc.com': '#video-title , #video-desc', # it contains some information
        'www.frbatlanta.org': 'p , .listBulleted li , strong',
        'www.bostonfed.org': '.clearfix p , .speeches_subtitle , .title',
        'www.frbsf.org': '.clear-both~ p , h1',
        'clevelandfed.org': 'h2+ p , p+ h2 , p+ p , hr+ p , .articletext',
        'www.philadelphiafed.org': 'h3~ p , h3 , h2',
        'www.c-span.org': 'p , .video-page-title',
        'www.newyorkfed.org': '.ts-article-title , .ts-article-subhead , p',
        'www.stlouisfed.org': '.wrapper p , #pageTitleHeader',
        #'www.wsj.com': 'p', # registration needed
        'economix.blogs.nytimes.com': '.story-body-text , .entry-title',
        #'link.brightcove.com': 'p', # only one article, irrelevant content
        'www.washingtonpost.com': 'h1 , article > p',
        'www.phil.frb.org': 'p+ ul li , p+ h3 , h3~ p , blockquote , h3+ p , blockquote+ h3 , h2',
        #'www.bloomberg.com': 'p', # only video
        #'comments.cftc.gov': 'p', # only one article, irrelevant content
        'www.eastbaytimes.com': '.body-copy p , .headlines',
        'www.marketwatch.com': '#article-body p , #article-subhead p , #article-headline',
        'www.sacbee.com': '.story div div p , p+ h1',
        'www.nytimes.com': '.story-body-text , #headline',
        # 'blogs.wsj.com': 'p', # registration needed
        # 'www.mprnews.org': 'p', # only radio interviews
        'www.cnbc.com': 'p , .title',
        #'www.americanbanker.com': 'p', # registration needed
        #'www.ft.com': 'p', # registration needed
        'www.cfr.org': '#transcript p , #description h5 , #description p , .title',
        'www.dallasnews.com': '#art-title , .art-story__text p',
        'asia.nikkei.com': '.article-box .title , .selection p',
    }

    def start_requests(self):
        for year in range(2013, 2018):
            for page_index in range(30):
                body_map = {"ContentType": "",
                            "Options": {"PageSize": 20,
                                        "PageIndex": str(page_index),
                                        "ResultsType": "FOMCRemarks"},
                            "BeginDate": "01/01/" + str(year),
                            "EndDate": "12/31/" + str(year),
                            "Filters": [],
                            "EventRange": "upcoming",
                            "GetFilterCounts": "false"}
                yield scrapy.Request("https://www.stlouisfed.org/API/FacetedSearch/SearchFOMCRemarks",
                                     method="POST",
                                     dont_filter=True,
                                     headers=self.headers_map,
                                     body=str(body_map))

    def parse(self, response):
        '''from scrapy.shell import inspect_response
        inspect_response(response, self)'''

        json_response = json.loads(
            response.body_as_unicode(), encoding="utf-8")
        results = json_response['Results']
        if len(results) > 0:
            for result in results:
                yield scrapy.Request(url=result['RemarkLink'],
                                     callback=self.article_parse,
                                     meta={'result': result})

    def article_parse(self, response):
        result = response.meta['result']
        # Jan. 09, 2017 (12:45 PM ET)
        datetime_object = None
        try:
            datetime_object = datetime.strptime(
                result['RemarkDate'], '%b. %d, %Y (%H:%M %p ET)')
        except ValueError:
            try:
                datetime_object = datetime.strptime(
                    result['RemarkDate'], '%b. %d, %Y')
            except ValueError as err2:
                self.log(err2, level=logging.ERROR)
        except Exception as ex:
            self.log(ex, level=logging.ERROR)

        url = response.url
        url_root = self.find_between(url, '://', '/')

        if url_root in self.url_to_selector:
            extractor = self.url_to_selector[url_root]
            real_extractor = '::text, '.join(extractor.split(' , ')) + '::text'
            extracted_content = '\n '.join(response.css(real_extractor).extract())
            
            self.log("Real extractor: " + real_extractor)
            self.log("Extracted content: " + extracted_content)

            yield {
                'date': datetime_object,
                'url': url,
                'content': extracted_content,

                'ParticipantJobTitle': result['ParticipantJobTitle'],
                'ParticipantLocation': result['ParticipantLocation'],
                'ParticipantName': result['ParticipantName'],
                'ParticipantTitleLastName': result['ParticipantTitleLastName'],
                'ParticipantUrl': result['ParticipantUrl'],
                'RemarkDate': result['RemarkDate'],
                'RemarkDescription': result['RemarkDescription'],
                'RemarkType': result['RemarkType']
            }

    def find_between(self, string, first, last):
        try:
            start = string.index(first) + len(first)
            end = string.index(last, start)
            return string[start:end]
        except ValueError:
            return ""
