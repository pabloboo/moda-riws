# -*- coding: utf-8 -*-
from scrapy import Spider, Request

class RiwsSpider(Spider):
    name = "spiderRiws"
    
    def start_requests(self):
        urls = ['https://www.fic.udc.es']
        for url in urls:
            yield Request(url=url, callback=self.parse)
            
    def parse(self, response, **kwargs):
        page = response.url
        print(page)
        
