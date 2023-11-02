# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProductoZara(scrapy.Item):
    url = scrapy.Field()
    nombre = scrapy.Field()
    precio = scrapy.Field()
    descripcion = scrapy.Field()
    color = scrapy.Field()
    imagen = scrapy.Field()
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

class ProductoGucci(scrapy.Item):
    nombre = scrapy.Field()
    color = scrapy.Field()
    precio = scrapy.Field()
    description = scrapy.Field()
    more_data=scrapy.Field()
    url = scrapy.Field()
    links = scrapy.Field()
    

class ProductoShein(scrapy.Item):
    url = scrapy.Field()
    nombre = scrapy.Field()
    precio = scrapy.Field()
    color = scrapy.Field()
    links = scrapy.Field()