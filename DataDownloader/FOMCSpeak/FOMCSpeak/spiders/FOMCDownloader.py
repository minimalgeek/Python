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
        'MONGO_COLLECTION': 'fomc_articles',
        'DOWNLOAD_DELAY': 1
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
        json_response = json.loads(response.body_as_unicode(), encoding="utf-8")
        results = json_response['Results']
        if len(results) > 0:
            for result in results:
                yield scrapy.Request(url=result['RemarkLink'],
                                     callback=self.article_parse,
                                     meta={'date': result['RemarkDate']})

    def article_parse(self, response):
        # Jan. 09, 2017 (12:45 PM ET)
        datetime_object = None
        try:
            datetime_object = datetime.strptime(response.meta['date'], '%b. %d, %Y (%H:%M %p ET)')
        except ValueError:
            try:
                datetime_object = datetime.strptime(response.meta['date'], '%b. %d, %Y')
            except ValueError as err2:
                self.log(err2, level=logging.ERROR)
        except Exception as ex:
            self.log(ex, level=logging.ERROR)

        yield {
            'date' : datetime_object,
            'url' : response.url,
            'content' : ' '.join(response.css('p *::text').extract())
        }
