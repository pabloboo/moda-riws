# moda-riws
Web sobre recuperación de información sobre moda

## Ejecución con Docker

Mover la carpeta elasticsearch-8.10.2/ a modariws/ (próxima actualización bajarla directamente en el docker)

Ejecutar contenedor de elasticsearch
```bash
cd modariws/
docker build -f DockerfileElasticsearch -t elasticsearch-image .
docker run --name elasticsearch -p 9200:9200 --network moda-riws-network elasticsearch-image
```

Comprobar que el contenedor de elasticsearch se encuentra en la dirección ipv4 172.24.0.2. Si no lo está es necesario cambiar la conexión en los spyders (es = Elasticsearch([{'host': '172.24.0.2', 'port': 9200, 'scheme': 'http'}]) en los ficheros xxx_spyder.py).

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' elasticsearch
```

Ejecutar contenedor de scrapy
```bash
docker build -f DockerfileScrapy -t scrapy-image .
docker run --name scrapy --network moda-riws-network scrapy-image
```

Ejecutar contenedor del frontend
```bash
cd frontend/
docker build -f DockerfileReact -t react-image .
docker run --name react -p 3000:3000 --network moda-riws-network react-image
```

## Ejecución sin Docker

### Instalación y ejecución elasticSearch

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

### Ejecución del spider de hym

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

### Comprobar que los productos se indexan bien en elasticSearch

Petición GET de postman: localhost:9200/productos/_search?size=600

### Configuración frontend
Enable color and tallas field data:
```bash
curl -X PUT "http://localhost:9200/productos/_mapping" -H "Content-Type: application/json" -d '{
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
```

```bash
cd frontend
npm i @appbaseio/reactivesearch@3.45.0 --legacy-peer-deps
npm start
```

### Alternative to enable color and tallas field data. 
Create a postman PUT petition with: http://localhost:9200/productos/_mapping
Body -> raw -> JSON:
```bash
{
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
}
```

## Ejecutar con Docker compose

NO funciona porque el contenedor de elasticsearch no se ejecuta siempre en la misma ip

```bash
docker-compose up
```