# -*- coding: utf-8 -*-
from scrapy import Spider, Request

class RiwsSpider(Spider):
    name = "prueba"
    
    def start_requests(self):
        urls = ['https://www.fic.udc.es']
        print("test")
        print(urls)
        for url in urls:
            yield Request(url=url, callback=self.parse)
            
    def parse(self, response, **kwargs):
        page = response.url
        print(page)
        
        
def main():
    print("Moda-RIWS")

if __name__ == "__main__":
    main()
    spider = RiwsSpider()
    spider.start_requests()
    