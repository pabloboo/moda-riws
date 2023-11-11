# -*- coding: utf-8 -*-
import scrapy
import json
from elasticsearch import Elasticsearch
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from bs4 import BeautifulSoup
from modariws.items import Producto


class BrownieSpider(scrapy.Spider):
    # Nombre de la araña
    name = "brownie"

    # Dominios permitidos
    allowed_domains = ['browniespain.com']

    # URLs para comenzar a rastrear
    # Url real https://www.browniespain.com/es/es/
    # Url para testear https://www.browniespain.com/es/es/jerseis/99695-jersey-trenzas-cuello-redondo.html
    start_urls = [
        'https://www.browniespain.com/es/es/'
    ]

    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

    def parse(self, response):
        exists = False
        producto = Producto()
        soup = BeautifulSoup(response.body, 'html.parser')

        # Extraemos los enlaces
        links = LinkExtractor(
            allow_domains=['browniespain.com']
        ).extract_links(response)

        outlinks = []  # Lista con todos los enlaces
        for link in links:
            url = link.url
            outlinks.append(url)  # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse)  # Generamos la petición

        title = soup.find('h1', class_='h1 product_title')
        if title:
            name = title.get_text()
            exists = True
            producto['nombre'] = name

        price = soup.find('span', class_='current-price-display')
        if price:
            precio = price.get_text()
            exists = True
            producto['precio'] = precio

        imagen = soup.find('a', class_='prodmini fancyimg visib')
        if imagen:
            url_imagen = imagen['href']
            exists = True
            producto['imagen'] = url_imagen

        description = soup.find('div', class_='product_descr')
        if description:
            descripcion = description.get_text()
            exists = True
            producto['descripcion'] = descripcion        

        sizes = soup.find_all('div', class_='custom-control custom-radio')
        tallas = ''
        if sizes:
            for size in sizes:
                label = size.find('label')
                if label:
                    size_text = label.get_text()
                    tallas += size_text
                    tallas += ', '
            exists = True
            if len(tallas) > 2:
                tallas = tallas[0:len(tallas)-2]
            producto['tallas'] = tallas          

        if exists:
            color = soup.find('span', class_='sr-only')
            if color:
                color_text = color.get_text()
                color_parsed = color_text.replace('Color mostrado: ', '')
                exists = True
                producto['color'] = color_parsed

            producto['url'] = response.url

            producto['marca'] = "Brownie"

            producto['links'] = outlinks

            def custom_serialize(producto):
                serialized_producto = {}
                # Create a dictionary with product data
                if 'nombre' in producto:
                    serialized_producto['nombre'] = producto['nombre']
                if 'precio' in producto:
                    serialized_producto['precio'] = producto['precio']
                if 'descripcion' in producto:
                    serialized_producto['descripcion'] = producto['descripcion']
                if 'color' in producto:
                    serialized_producto['color'] = producto['color']
                if 'imagen' in producto:
                    serialized_producto['imagen'] = producto['imagen']
                if 'url' in producto:
                    serialized_producto['url'] = producto['url']
                if 'tallas' in producto:
                    serialized_producto['tallas'] = producto['tallas']

                serialized_producto['marca'] = producto['marca']

                # Convert the dictionary to a JSON string
                return json.dumps(serialized_producto)

            self.es.index(index='productos', body=custom_serialize(producto))

            yield producto
