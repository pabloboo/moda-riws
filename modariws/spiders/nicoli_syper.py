# -*- coding: utf-8 -*-
import json
import re

import scrapy
from elasticsearch import Elasticsearch
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from bs4 import BeautifulSoup
from modariws.items import Producto
from . import elasticsearch_connection


class NicolishopSpider(scrapy.Spider):
    name = "nicoli"
    allowed_domains = ['nicolishop.com']
    start_urls = ['https://www.nicolishop.com']

    es = Elasticsearch([{'host': elasticsearch_connection.ES_HOST, 'port': elasticsearch_connection.ES_PORT, 'scheme': elasticsearch_connection.ES_SCHEME}])

    def parse(self, response):
        producto = Producto()
        soup = BeautifulSoup(response.text, 'html.parser')

        exclude_pattern = re.compile(
            r'^https://www\.nicolishop\.com/es/es/bebe|'
            r'^https://www\.nicolishop\.com/es/es/tweena|'
            r'^https://www\.nicolishop\.com/es/es/tweeno|'
            r'https://www\.nicolishop\.com/es/es/tarjeta-regalo'
        )
        links = LinkExtractor(
            allow_domains=['nicolishop.com'],
            deny=exclude_pattern
        ).extract_links(response)

        outlinks = []  # Lista con todos los enlaces
        for link in links:
            url = link.url
            outlinks.append(url)  # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse)  # Generamos la petición

        # Nombre del producto
        name_element = soup.find('h1', class_='product-name')
        if name_element and 'tarjeta regalo' not in name_element.get_text(strip=True).lower():
            name = name_element.get_text(strip=True)
            producto['nombre'] = name
            print(f'Nombre: {name}')

        else:
            return

        # Precio del producto
        price_element = soup.find('span', class_='price-sales')
        if price_element:
            price = price_element.get_text().replace('\r', '').replace('\t', '').strip()
            price = ''.join(c for c in price if c.isdigit() or c == ',')  # delete €
            price = float(price.replace(',', '.'))
            print(f'Precio: {price}')
            producto['precio'] = price

        color_element = soup.select_one('div.product-color-selection-swatches .swatch-color-wrapper.active span')
        if color_element:
            color = color_element['title']
            print(f'Color: {color}')
            producto['color'] = color

        image_element = soup.select_one('div.product-thumbnails .thumbnail-image-wrapper.active img')
        if image_element:
            image_url = image_element['src']
            print(f'URL de la imagen: {image_url}')
            producto['imagen'] = image_url
        else:
            return

        # Tallas disponibles
        size_elements = soup.select('div.product-variation-sizes li')
        tallas = set()
        for size_element in size_elements:
            size = size_element.get_text(strip=True)
            tallas.add(size)  # Agregar al conjunto para evitar duplicados
        tallas_str = ', '.join(sorted(tallas))  # Ordenar tallas y unirlas con comas
        producto['tallas'] = tallas_str
        print(f'Tallas: {tallas_str}')

        # Descripción del producto
        description_element = soup.find('div', class_='product-description')
        if description_element:
            description = description_element.get_text(strip=True)
            producto['descripcion'] = description
            print(f'Descripción: {description}')

        producto['url'] = response.url

        producto['links'] = outlinks

        producto['marca'] = "Nicoli"

        def custom_serialize(producto):
            serialized_producto = {}
            # Create a dictionary with product data
            if 'nombre' in producto:
                serialized_producto['nombre'] = producto['nombre']
            if 'precio' in producto:
                serialized_producto['precio'] = producto['precio']
            if 'descripcion' in producto:
                serialized_producto['descripcion'] = producto['descripcion']
            if 'url' in producto:
                serialized_producto['url'] = producto['url']
            if 'color' in producto:
                serialized_producto['color'] = producto['color']
            if 'imagen' in producto:
                serialized_producto['imagen'] = producto['imagen']
            if 'tallas' in producto:
                serialized_producto['tallas'] = producto['tallas']

            serialized_producto['marca'] = producto['marca']

            # Convert the dictionary to a JSON string
            return json.dumps(serialized_producto)

        self.es.index(index='productos', body=custom_serialize(producto))

        yield producto
