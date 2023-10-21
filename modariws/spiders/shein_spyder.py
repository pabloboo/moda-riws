import scrapy
import json
from bs4 import BeautifulSoup
from modariws.items import Producto
from elasticsearch import Elasticsearch
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy_splash import SplashRequest

click_script = """
  function main(splash, args)
      local detalles = splash:select('h2.product-intro__description-head')
      detalles:mouse_click()
      splash:wait(2)
      return splash:html()
  end
  """


class SheinSpider(scrapy.Spider):
    name = "shein"
    allowed_domains = ['shein.com']
    start_urls = ['https://es.shein.com']
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
            yield SplashRequest(
                url,
                callback=self.parse,
                endpoint='execute',
                args={'wait': 2, 'lua_source': click_script, url: url}
            )
           # self.logger.info(response.text)

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

            color_element = response.css('div.color-block')

            # Extraer el texto del elemento
            color = color_element.css('span.color-999::text').get()
            print(f'Color: {color}')
            producto['color'] = color

            producto['links'] = outlinks

            def custom_serialize(producto):
                # Create a dictionary with product data
                serialized_producto = {
                    'url': producto['url'],
                    'nombre': producto['nombre'],
                    'precio': producto['precio'],
                    'color': producto['color']
                }

                # Convert the dictionary to a JSON string
                return json.dumps(serialized_producto)

            self.es.index(index='shein_prod', body=custom_serialize(producto))

            yield producto
