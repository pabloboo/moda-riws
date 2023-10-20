import scrapy
import json
from bs4 import BeautifulSoup
from modariws.items import Producto
from elasticsearch import Elasticsearch
from scrapy import Request
from scrapy.linkextractors import LinkExtractor


class SheinSpider(scrapy.Spider):
    name = "shein"
    allowed_domains = ['shein.com']
    start_urls = ['https://www.shein.com']
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

    def parse(self, response):
        producto = Producto()

        # Use Beautiful Soup to parse the response content
        soup = BeautifulSoup(response.text, 'html.parser')

        links = LinkExtractor(
            allow_domains=['shein.com'],
        ).extract_links(response)

        # Extract product links using Beautiful Soup
        outlinks = []  # List to store all links
        for link in links:
            url = link.url
            outlinks.append(url)  # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse)

        # Check if the page contains product information
        product_details = soup.find('div', class_='product-intro__description')
        if product_details:
            # Extract product URL and description
            producto['url'] = response.url

            # Extract the product name
            product_name = soup.find('h1', class_='product-intro__head-name')
            if product_name:
                name = product_name.get_text()
                print(f'Nombre: {name}')
                producto['nombre'] = name

            # Extract the price
            price_div = soup.find('div', class_='product-intro__head-mainprice')
            if price_div:
                price = price_div.find('span').get_text()
                print(f'Precio: {price}')
                producto['precio'] = price





            # Add more attribute extraction and printing as needed

            producto['links'] = outlinks

            def custom_serialize(producto):
                # Create a dictionary with product data
                serialized_producto = {
                    'url': producto['url'],
                    'nombre': producto['nombre'],
                    'precio': producto['precio'],
                    # 'color': producto['color']

                }

                # Convert the dictionary to a JSON string
                return json.dumps(serialized_producto)

            self.es.index(index='shein_prod', body=custom_serialize(producto))

            yield producto
