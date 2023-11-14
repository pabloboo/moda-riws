import scrapy
import json
from bs4 import BeautifulSoup
from modariws.items import Producto
from elasticsearch import Elasticsearch
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import re


class hymSpider(scrapy.Spider):
    name = "hym"
    allowed_domains = ['hm.com']
    start_urls = ['https://www2.hm.com/es_es/']
    es = Elasticsearch([{'host': '172.24.0.2', 'port': 9200, 'scheme': 'http'}])

    def parse(self, response):
        producto = Producto()

        # Use Beautiful Soup to parse the response content
        soup = BeautifulSoup(response.text, 'html.parser')

        links = LinkExtractor(
            allow_domains=['hm.com'],
        ).extract_links(response)

        # Extract product links using Beautiful Soup
        outlinks = []  # List to store all links
        for link in links:
            url = link.url
            outlinks.append(url)  # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse)

        # Check if the page contains product information
        product_details = soup.find('div', class_='sub-content product-detail-info product-detail-meta inner sticky-on-scroll semi-sticky sticky-candidate')
        if product_details:
            # Extract product URL and description
            producto['url'] = response.url

            # Extract the product name
            product_name = soup.select_one('hm-product-name > div > h1')
            if product_name:
                name = product_name.get_text()
                print(f'Nombre: {name}')
                producto['nombre'] = name

            # Extract the color
            price_div = soup.select('div.primary-row.product-item-price')
            if price_div:
                price_element = price_div[0].find('span', class_='price-value')
                if price_element:
                    price = price_element.get_text().replace('\r', '').replace('\t', '').strip()
                    price = ''.join(c for c in price if c.isdigit() or c == ',') #delete €
                    price = float(price.replace(',', '.'))
                    print(f'Precio: {price}')
                    producto['precio'] = price

            # Extract the color
            color_div = soup.find('a', class_='filter-option')
            if color_div:
                img_tag = color_div.find('img')
                if img_tag:
                    color = img_tag['alt']
                    print(f'Color: {color}')
                    producto['color'] = color

            # Extract the image
            figure_tag = soup.find('figure', class_='pdp-image product-detail-images product-detail-main-image')         
            if figure_tag:
                img_tag = figure_tag.find('img')
                if img_tag:
                    url_imagen = img_tag['srcset']
                    # Completar la URL con el esquema "https:"
                    if url_imagen.startswith('//'):
                        url_imagen = 'https:' + url_imagen
                        # Buscar la primera URL que comienza con "https" utilizando una expresión regular
                        urls = re.findall(r'https://[^,\s]+', url_imagen)
                        # Obtener la primera URL
                        if urls:
                            url_imagen = urls[0]
                            print(f'Url imagen: {url_imagen}')
                            producto['imagen'] = url_imagen

            producto['links'] = outlinks
            producto['marca'] = "HyM"

            def custom_serialize(producto):
                # Create a dictionary with product data
                serialized_producto = {
                    'url': producto['url'],
                    'nombre': producto['nombre'],
                    'precio': producto['precio'],
                    'color': producto['color'],
                    'imagen': producto['imagen'],
                    'tallas': "NA",
                    'marca': producto['marca']
                }

                # Convert the dictionary to a JSON string
                return json.dumps(serialized_producto)

            self.es.index(index='productos', body=custom_serialize(producto))

            yield producto
