# import scrapy
# import json
# from modariws.items import Producto
# from scrapy.linkextractors import LinkExtractor
# from elasticsearch import Elasticsearch
# from scrapy import Request
# from bs4 import BeautifulSoup
#
# class ZaraSpider(scrapy.Spider):
#     # Nombre de la araña
#   name = "zara"
#
#     # Dominios permitidos
#     allowed_domains = ['zara.com']
#
#     # URLs para comenzar a rastrear
#     start_urls = [
#         'https://www.zara.com/es/'
#     ]
#
#     es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
#
#     # Extraer información de cada URL mediante BeautifulSoup
#     def parse(self, response):
#         producto = ProductoZara()
#
#         # Extraemos los enlaces
#         links = LinkExtractor(
#             allow_domains=['zara.com'],
#             restrict_xpaths=["//a"],
#             allow="/es/"
#         ).extract_links(response)
#
#         outlinks = []  # Lista con todos los enlaces
#         for link in links:
#             url = link.url
#             outlinks.append(url)  # Añadimos el enlace en la lista
#             yield Request(url, callback=self.parse)  # Generamos la petición
#
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         product_tag = soup.find('meta', {'content': 'product'})
#         if product_tag:
#             # Extraemos la URL, el nombre del producto, la descripción y su precio
#             producto['url'] = response.request.url
#             producto['nombre'] = soup.find('h1', {'class': 'product-detail-info__header-name'}).text
#             producto['precio'] = soup.find('span', {'class': 'money-amount__main'}).text
#             descripcion = soup.find('div', class_='product-detail-description').find('p').text
#             producto['descripcion'] = descripcion
#             imagen_url = soup.find('img', class_='media-image__image')['src']
#             if imagen_url:
#                 producto['imagen'] = imagen_url
#
#             def custom_serialize(producto):
#                 # Crear un diccionario con los datos del producto
#                 serialized_producto = {
#                     'url': producto['url'],
#                     'nombre': producto['nombre'],
#                     'precio': producto['precio'],
#                     'descripcion': producto['descripcion'],
#                     'imagen': producto['imagen']
#                 }
#
#                 # Convertir el diccionario en una cadena JSON
#                 return json.dumps(serialized_producto)
#
#             self.es.index(index='zara_products2', body=custom_serialize(producto))
#
#             yield producto
