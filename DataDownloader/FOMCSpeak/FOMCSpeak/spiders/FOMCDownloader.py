# -*- coding: utf-8 -*-
import scrapy
import json
import logging
from scrapy import FormRequest

class FomcdownloaderSpider(scrapy.Spider):
    name = "FOMCDownloader"
    allowed_domains = ["https://www.stlouisfed.org"]
    headers_map = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'hu-HU,hu;q=0.8,en-US;q=0.6,en;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        for year in range(2013, 2018):
            for page_index in range(10):
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
        self.log(response.body)
        json_response = json.loads(response.body_as_unicode(), encoding="utf-8")
        results = json_response['Results']
        if len(results) > 0:
            for result in results:
                yield scrapy.Request(url=result['RemarkLink'], callback=self.article_parse)

    def article_parse(self, response):
        pass
        