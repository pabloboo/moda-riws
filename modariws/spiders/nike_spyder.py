# -*- coding: utf-8 -*-
import scrapy
import json
from elasticsearch import Elasticsearch
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from bs4 import BeautifulSoup
from modariws.items import ProductoNike

class NikeSpider(scrapy.Spider):
    # Nombre de la araña
    name = "nike"

    # Dominios permitidos
    allowed_domains = ['nike.com']
    
    # URLs para comenzar a rastrear
    #Url real https://www.nike.com/es/
    #Url para testear https://www.nike.com/es/t/sportswear-phoenix-fleece-pantalon-de-chandal-de-talle-alto-oversize-7h49M3/DQ5887-063
    start_urls = [
        'https://www.nike.com/es/'
    ]
    
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
    
    def parse(self, response):
        exists = False
        producto = ProductoNike()
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
            
        titles = soup.find(id='pdp_product_title')
        if titles:
            name = titles.get_text()
            print(f'Nombre: {name}')
            exists = True
            producto['nombre'] = name
        
        subtitles = soup.find('h2', class_='headline-5 pb1-sm d-sm-ib')
        if subtitles:
            subtitulo = subtitles.get_text()
            print(f'Subtitulo: {subtitulo}')
            exists = True
            producto['subtitulo'] = subtitulo
            
        prices = soup.find('div', class_='product-price css-11s12ax is--current-price css-tpaepq')
        if prices:
            precio = prices.get_text()
            print(f'Precio: {precio}')
            exists = True
            producto['precio'] = precio
            
        if exists:
            producto['url'] = response.url
            
        producto['links'] = outlinks
        
        def custom_serialize(producto):
            serialized_producto = {}
            # Create a dictionary with product data
            if 'nombre' in producto:
                serialized_producto['nombre'] = producto['nombre']
            if 'subtitulo' in producto:
                serialized_producto['subtitulo'] = producto['subtitulo']
            if 'precio' in producto:
                serialized_producto['precio'] = producto['precio']
            if 'url' in producto:
                serialized_producto['url'] = producto['url']

            # Convert the dictionary to a JSON string
            return json.dumps(serialized_producto)

        self.es.index(index='nike_prod', body=custom_serialize(producto))

        yield producto