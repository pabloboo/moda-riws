# -*- coding: utf-8 -*-
import scrapy
import json
from elasticsearch import Elasticsearch
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from bs4 import BeautifulSoup
from modariws.items import ProductoGucci


class GucciSpider(scrapy.Spider):
    # Nombre de la araña
    name = "gucci"

    # Dominios permitidos
    allowed_domains = ['gucci.com']

    # URLs para comenzar a rastrear
    # Url real https://www.nike.com/es/
    # Url para testear https://www.nike.com/es/t/sportswear-phoenix-fleece-pantalon-de-chandal-de-talle-alto-oversize-7h49M3/DQ5887-063
    start_urls = [
        'https://www.gucci.com/es/'
    ]

    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

    def parse(self, response):
        exists = False
        producto = ProductoGucci()
        soup = BeautifulSoup(response.body, 'html.parser')

        # Extraemos los enlaces
        links = LinkExtractor(
            allow_domains=['gucci.com']
        ).extract_links(response)

        outlinks = []  # Lista con todos los enlaces
        for link in links:
            url = link.url
            outlinks.append(url)  # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse)  # Generamos la petición

        name_div = soup.find(class_='product-name product-detail-product-name')
        if name_div:
            name = name_div.get_text()
            print(f'Nombre: {name}')
            exists = True
            producto['nombre'] = name

        color_div = soup.find(class_='color-material-name')
        if color_div:
            color = color_div.get_text()
            print(f'Color: {color}')
            exists = True
            producto['color'] = color

        prices = soup.find(id='markedDown_full_Price')
        if prices:
            precio = prices.get_text()
            print(f'Precio: {precio}')
            exists = True
            producto['precio'] = precio
        # description_div = soup.find(id='product-details')
        description=soup.find('p')
        print(description)
        if exists:
            producto['url'] = response.url

        producto['links'] = outlinks

        def custom_serialize(producto):
            serialized_producto = {}
            if 'precio' not in producto:
                return
            # Create a dictionary with product data
            if 'nombre' in producto:
                serialized_producto['nombre'] = producto['nombre']
            if 'color' in producto:
                serialized_producto['color'] = producto['color']
            if 'precio' in producto:
                serialized_producto['precio'] = producto['precio']
            if 'url' in producto:
                serialized_producto['url'] = producto['url']

            # Convert the dictionary to a JSON string
            return json.dumps(serialized_producto)

        self.es.index(index='gucci_prod', body=custom_serialize(producto))

        yield producto