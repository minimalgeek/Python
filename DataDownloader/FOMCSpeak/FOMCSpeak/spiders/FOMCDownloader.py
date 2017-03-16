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
        'MONGO_COLLECTION': 'fomc_articles_new'
    }
    url_to_selector = {
        'www.richmondfed.org': 'p',
        'www.federalreserve.gov': 'p',
        'www.bloomberg.com': 'p',
        'www.dallasfed.org': 'p',
        'www.chicagofed.org': 'p',
        'www.minneapolisfed.org': 'p',
        'video.cnbc.com': 'p',
        'www.frbatlanta.org': 'p',
        'www.bostonfed.org': 'p',
        'www.frbsf.org': 'p',
        'www.clevelandfed.org': 'p',
        'www.philadelphiafed.org': 'p',
        'www.stlouisfed.org': 'p',
        'www.c-span.org': 'p',
        'www.newyorkfed.org': 'p',
        'www.reuters.com': 'p',
        'video.foxbusiness.com': 'p',
        'www.wsj.com': 'p',
        'www.cnbc.com': 'p',
        'economix.blogs.nytimes.com': 'p',
        'www.bnn.ca': 'p',
        'nbr.com': 'p',
        'link.brightcove.com': 'p',
        'www.washingtonpost.com': 'p',
        'www.phil.frb.org': 'p',
        'comments.cftc.gov': 'p',
        'www.econtalk.org': 'p',
        'clevelandfed.org': 'p',
        'www.foxbusiness.com': 'p',
        'www.marketplace.org': 'p',
        'www.eastbaytimes.com': 'p',
        'www.marketwatch.com': 'p',
        'www.sacbee.com': 'p',
        'video.foxnews.com': 'p',
        'www.nytimes.com': 'p',
        'blogs.wsj.com': 'p',
        'www.mprnews.org': 'p',
        'www.americanbanker.com': 'p',
        'www.ft.com': 'p',
        'www.bizjournals.com': 'p',
        'www.cfr.org': 'p',
        'www.dallasnews.com': 'p',
        'www.npr.org': 'p',
        'charlierose.com': 'p',
        'asia.nikkei.com': 'p',
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
                url_to_open = result['RemarkLink']
                if "richmondfed.org" in url_to_open:
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

        yield {
            'date': datetime_object,
            'url': response.url,
            'content': ' '.join(response.css('p *::text').extract()),

            'ParticipantJobTitle': result['ParticipantJobTitle'],
            'ParticipantLocation': result['ParticipantLocation'],
            'ParticipantName': result['ParticipantName'],
            'ParticipantTitleLastName': result['ParticipantTitleLastName'],
            'ParticipantUrl': result['ParticipantUrl'],
            'RemarkDate': result['RemarkDate'],
            'RemarkDescription': result['RemarkDescription'],
            'RemarkType': result['RemarkType']
        }
