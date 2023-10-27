# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from bs4 import BeautifulSoup

class NikeSpider(scrapy.Spider):
    # Nombre de la araña
    name = "nike"

    # Dominios permitidos
    allowed_domains = ['nike.com']
    
    # URLs para comenzar a rastrear
    #Url para testear https://www.nike.com/es/t/sportswear-phoenix-fleece-pantalon-de-chandal-de-talle-alto-oversize-7h49M3/DQ5887-063
    start_urls = [
        'https://www.nike.com/es/'
    ]
    
    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')

        # Extraemos los enlaces
        links = LinkExtractor(
            allow_domains=['nike.com']
            ).extract_links(response)
        
        outlinks = []  # Lista con todos los enlaces
        for link in links:
            url = link.url
            outlinks.append(url) # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse) # Generamos la petición
            
        # Iterar a través de los elementos y obtener la 
        titles = soup.find(id='pdp_product_title')
        subtitles = soup.find_all('h2', class_='headline-5 pb1-sm d-sm-ib')
        prices = soup.find_all('div', class_='product-price css-11s12ax is--current-price css-tpaepq')
        
        print(titles)
        print(subtitles)
        print(prices)
