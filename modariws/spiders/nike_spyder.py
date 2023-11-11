# -*- coding: utf-8 -*-
import scrapy
import json
from elasticsearch import Elasticsearch
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from bs4 import BeautifulSoup
from modariws.items import Producto


class NikeSpider(scrapy.Spider):
    # Nombre de la araña
    name = "nike"

    # Dominios permitidos
    allowed_domains = ['nike.com']

    # URLs para comenzar a rastrear
    # Url real 
    # Url para testear https://www.nike.com/es/t/sportswear-phoenix-fleece-pantalon-de-chandal-de-talle-alto-oversize-7h49M3/DQ5887-063
    start_urls = [
        'https://www.nike.com/es/'
    ]

    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

    def parse(self, response):
        exists = False
        producto = Producto()
        soup = BeautifulSoup(response.body, 'html.parser')

        # Extraemos los enlaces
        links = LinkExtractor(
            allow_domains=['nike.com']
        ).extract_links(response)

        outlinks = []  # Lista con todos los enlaces
        for link in links:
            url = link.url
            outlinks.append(url)  # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse)  # Generamos la petición

        title = soup.find(id='pdp_product_title')
        if title:
            name = title.get_text()
            exists = True
            producto['nombre'] = name

        subtitle = soup.find('h2', class_='headline-5 pb1-sm d-sm-ib')
        if subtitle:
            subtitulo = subtitle.get_text()
            exists = True
            if 'nombre' in producto:
                producto['nombre'] = f'{producto["nombre"]} - {subtitulo}'
            else:
                producto['nombre'] = subtitulo

        price = soup.find('div', class_='product-price css-11s12ax is--current-price css-tpaepq')
        if price:
            precio = price.get_text()
            exists = True
            producto['precio'] = precio
        else:
            discounted_price = soup.find('div', class_='product-price is--current-price css-s56yt7 css-xq7tty')
            if discounted_price:
                precio_descuento = discounted_price.get_text()
                exists = True
                producto['precio'] = precio_descuento

        imagen = soup.find('img', class_='css-viwop1 u-full-width u-full-height css-m5dkrx')
        if imagen:
            url_imagen = imagen['src']
            exists = True
            producto['imagen'] = url_imagen

        description = soup.find('div', class_='description-preview body-2 css-1pbvugb')
        if description:
            descripcion = description.get_text()
            exists = True
            producto['descripcion'] = descripcion

        color = soup.find('li', class_='description-preview__color-description ncss-li')
        if color:
            color_text = color.get_text()
            color_parsed = color_text.replace('Color mostrado: ', '')
            exists = True
            producto['color'] = color_parsed

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
                if 'descripcion' in producto:
                    serialized_producto['descripcion'] = producto['descripcion']
                if 'color' in producto:
                    serialized_producto['color'] = producto['color']
                if 'imagen' in producto:
                    serialized_producto['imagen'] = producto['imagen']
                if 'url' in producto:
                    serialized_producto['url'] = producto['url']
                serialized_producto['tallas'] = "NA"

                # Convert the dictionary to a JSON string
                return json.dumps(serialized_producto)

            self.es.index(index='productos', body=custom_serialize(producto))

            yield producto
