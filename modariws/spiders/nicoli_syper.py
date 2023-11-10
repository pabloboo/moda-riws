# -*- coding: utf-8 -*-
import json

import scrapy
from elasticsearch import Elasticsearch
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from bs4 import BeautifulSoup
from modariws.items import Producto


class NicolishopSpider(scrapy.Spider):
    name = "nicoli"
    allowed_domains = ['nicolishop.com']
    start_urls = ['https://www.nicolishop.com/es/es/abrigo-oversize-cuadros/232M505304-35.html']

    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

    def parse(self, response):
        producto = Producto()
        soup = BeautifulSoup(response.text, 'html.parser')

        links = LinkExtractor(
            allow_domains=['nicolishop.com']
        ).extract_links(response)

        outlinks = []  # Lista con todos los enlaces
        for link in links:
            url = link.url
            outlinks.append(url)  # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse)  # Generamos la petición

        # Nombre del producto
        name_element = soup.find('h1', class_='product-name')
        if name_element:
            name = name_element.get_text(strip=True)
            producto['nombre'] = name
            print(f'Nombre: {name}')

        # Precio del producto
        price_element = soup.find('span', class_='price-sales')
        if price_element:
            price = price_element.get_text(strip=True)
            producto['precio'] = price
            print(f'Precio: {price}')

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

        # Tallas disponibles
        sizes_set = set()
        size_elements = soup.select('div.product-variation-sizes li')
        for size_element in size_elements:
            size = size_element.get_text(strip=True)
            sizes_set.add(size)  # Agregar al conjunto para evitar duplicados

        # Convertir el conjunto en una lista
        sizes = list(sizes_set)

        producto['tallas'] = sizes
        print(f'Tallas: {sizes}')

        # Descripción del producto
        description_element = soup.find('div', class_='product-description')
        if description_element:
            description = description_element.get_text(strip=True)
            producto['descripcion'] = description
            print(f'Descripción: {description}')

        producto['url'] = response.url

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
            if 'url' in producto:
                serialized_producto['url'] = producto['url']
            if 'color' in producto:
                serialized_producto['color'] = producto['color']
            if 'imagen' in producto:
                serialized_producto['imagen'] = producto['imagen']
            if 'tallas' in producto:
                serialized_producto['tallas'] = producto['tallas']

            # Convert the dictionary to a JSON string
            return json.dumps(serialized_producto)

        self.es.index(index='productos', body=custom_serialize(producto))

        yield producto
