# moda-riws
Web sobre recuperación de información sobre moda

## Instalación y ejecución elasticSearch

Instalación: https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html
elasticsearch.yml → enabled: false.

Ejecución:
cd elasticsearch/
./bin/elasticsearch

Comprobar funcionamiento:
curl -X GET "localhost:9200"

## Configuración scrapy splash

Descargar docker
Descargar imagen de Scrapy Splash: `docker pull scrapinghub/splash`
Ejecutar Scrapy Splash: `docker run -it -p 8050:8050 --rm scrapinghub/splash`
Entrar en la url http://localhost:8050/ para comprobar que ha funcionado correctamente.

## Ejecución del spider de shein

Instalación de dependencias:
```bash
pip install Scrapy
pip install --upgrade --force-reinstall Scrapy Twisted
pip install attrs
pip install service_identity
pip install elasticsearch
pip install beautifulsoup4
pip install scrapy-splash
```

Ejecución del spider: `scrapy crawl shein`

## Comprobar que los productos se indexan bien en elasticSearch

Petición GET de postman: localhost:9200/shein_prod/_search?size=600
