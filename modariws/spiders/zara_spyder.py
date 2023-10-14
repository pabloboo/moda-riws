import scrapy
from modariws.items import Producto
from scrapy.linkextractors import LinkExtractor
from scrapy import Request

class ZaraSpider(scrapy.Spider):
    # Nombre de la araña
    name = "zara"
    
    # Dominios permitidos
    allowed_domains = ['zara.com']
    
    # URLs para comenzar a rastrear
    start_urls = [
        'https://www.zara.com/es/es/man-new-in-collection-l6164.html?v1=2297656'
    ]
    
    # Extraer información de cada url mediante expresiones
    def parse(self, response):
        producto = Producto()

        # Extraemos los enlaces
        links = LinkExtractor(
            allow_domains=['zara.com'],
            restrict_xpaths=["//a"],
            allow="/es/"
            ).extract_links(response)

        outlinks = []  # Lista con todos los enlaces
        for link in links:
            url = link.url
            outlinks.append(url) # Añadimos el enlace en la lista
            yield Request(url, callback=self.parse) # Generamos la petición
                
        product = response.xpath('//meta[@content="product"]').extract()
        if product:
            # Extraemos la url, el nombre del producto, la descripcion y su precio
            producto['url'] = response.request.url
            producto['nombre'] = response.xpath('//h1[@class="product-detail-info__header-name"]/text()').extract_first()
            producto['precio'] = response.xpath('//span[@class="money-amount__main"]/text()').extract_first()
            producto['descripcion'] = response.xpath('//div[@class="product-detail-description product-detail-info__description"]//text()').extract_first()
            producto['links'] = outlinks
                
            yield producto