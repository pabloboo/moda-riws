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

## Ejecución del spider de hym

Instalación de dependencias:
```bash
pip install Scrapy
pip install --upgrade --force-reinstall Scrapy Twisted
pip install attrs
pip install service_identity
pip install elasticsearch
pip install beautifulsoup4
```

Ejecución del spider: `scrapy crawl hym`

## Comprobar que los productos se indexan bien en elasticSearch

Petición GET de postman: localhost:9200/hym_prod/_search?size=600

## Configuración frontend
```bash
curl -X PUT "http://localhost:9200/hym_prod/_mapping" -H "Content-Type: application/json" -d '{
  "properties": {
    "precio": {
      "type": "text",
      "fielddata": true
    }
  }
}'
```

```bash
cd frontend
npm i @appbaseio/reactivesearch@3.45.0 --legacy-peer-deps
npm start
```