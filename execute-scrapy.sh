#!/bin/bash

# Give permissions to write the file
chmod +w productos.json

# Execute Scrapy crawl
scrapy crawl hym -s CLOSESPIDER_ITEMCOUNT=10