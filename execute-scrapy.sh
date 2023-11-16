#!/bin/bash

# Give permissions to write the file
chmod +w productos.json

# Configure Elasticsearch for fields
curl -X PUT "http://172.24.0.2:9200/productos/_mapping" -H "Content-Type: application/json" -d '{
  "properties": {
    "color": {
      "type": "text",
      "fielddata": true
    },
    "tallas": {
      "type": "text",
      "fielddata": true
    },
    "marca": {
      "type": "text",
      "fielddata": true
    }
  }
}'

# Execute Scrapy crawl
scrapy crawl hym -s CLOSESPIDER_ITEMCOUNT=10
scrapy crawl nicoli -s CLOSESPIDER_ITEMCOUNT=10
scrapy crawl brownie -s CLOSESPIDER_ITEMCOUNT=10
scrapy crawl nike -s CLOSESPIDER_ITEMCOUNT=10