# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Producto(scrapy.Item):
    url = scrapy.Field()
    nombre = scrapy.Field()
    precio = scrapy.Field()
    color = scrapy.Field()
    links = scrapy.Field()
    
class ProductoNike(scrapy.Item):
    nombre = scrapy.Field()
    subtitulo = scrapy.Field()
    precio = scrapy.Field()
    imagen = scrapy.Field()
    color = scrapy.Field()
    descripcion = scrapy.Field()
    url = scrapy.Field()
    links = scrapy.Field()
    
