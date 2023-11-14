#!/bin/bash

# Give permissions to write the file
chmod +w productos.json

# Execute Scrapy crawl
scrapy crawl hym -s CLOSESPIDER_ITEMCOUNT=10
scrapy crawl nicoli -s CLOSESPIDER_ITEMCOUNT=10
scrapy crawl brownie -s CLOSESPIDER_ITEMCOUNT=10
scrapy crawl nike -s CLOSESPIDER_ITEMCOUNT=10