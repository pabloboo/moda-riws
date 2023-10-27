# moda-riws
Web sobre recuperación de información sobre moda

## Instalación y ejecución elasticSearch

Instalación: https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html

En el archivo elasticsearch/config/elasticsearch.yml

Cambiar la línea:
`xpack.security.enabled: false`

Añadir las líneas:
```bash
http.cors.enabled: true
http.cors.allow-origin: "*"
http.cors.allow-credentials: true
http.cors.allow-headers: "X-Requested-With, Content-Type, Content-Length, Authorization"
```

Ejecución:
```bash
cd elasticsearch/
./bin/elasticsearch
```

Comprobar funcionamiento: `curl -X GET "localhost:9200"`

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

## Configuración frontend
```bash
cd frontend
npm start
```