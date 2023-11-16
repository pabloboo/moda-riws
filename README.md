# moda-riws
Web sobre recuperación de información sobre moda

## Ejecución con Docker

Los siguientes comandos es necesario ejecutarlos en una terminal Ubuntu (si se dispone de Windows se pueden ejecutar en la terminal wsl de Ubuntu).

Ejecutar contenedor de elasticsearch:
```bash
cd modariws/
docker-compose up
```

En caso de que ese comando no funcione se puede usar: docker compose up

Comprobar que el contenedor de elasticsearch se encuentra en la dirección ipv4 172.24.0.2. Si no lo está es necesario cambiar la ip de la conexión con elasticsearch (variable ES_HOST del fichero modariws/spiders/elasticsearch_connection.py) y la ip de la petición curl del archivo execute-scrapy.sh, línea 7.

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' elasticsearch
```

También se debe comprobar que el contenedor elasticsearch se está ejecutando en el network 'modariws_moda-riws-network' con el siguiente comando:

```bash
docker inspect -f '{{json .NetworkSettings.Networks}}' elasticsearch
```

Si no está en esa red se debe cambiar el parámetro --network en los siguientes comandos por el valor de network obtenido.

Si elasticsearch se está ejecutando correctamente y escuchando en el puerto 9200 se puede proseguir ejecutando scrapy.
Ejecutar contenedor de scrapy:
```bash
docker build -f DockerfileScrapy -t scrapy-image .
docker run --name scrapy --network modariws_moda-riws-network scrapy-image
```

En cuanto se recuperen los primeros elementos ya se puede ejecutar el contenedor del frontend y poco a poco se irán recuperando más productos.
Ejecutar contenedor del frontend:
```bash
cd frontend/
docker build -f DockerfileReact -t react-image .
docker run --name react -p 3000:3000 --network modariws_moda-riws-network react-image
```

Si al desplegar la web no se muestran los filtros de color,talla y marca es necesario ejecutar en una terminal el siguiente comando cambiando la ip por la ip en la que se está ejecutando el contenedor de elastic:
```bash
curl -X PUT "http://172.20.0.2:9200/productos/_mapping" -H "Content-Type: application/json" -d '{
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

## Estructura de los ficheros

En el directorio principal se pueden encontrar los archivos necesarios para la configuración en Docker de Scrapy, la carpeta frontend/ con el código de React y la carpeta modariws/ con el código del back-end.

En la carpeta modariws/ se encuentra el archivo de configuración en docker-compose de ElasticSearch además de los ficheros necesarios para scrapear las webs. Los spiders de las distintas webs de moda se encuentran en el directorio spiders/

Por último, en el directorio frontend/ se encuentra todo el código de react. Además en este directorio también se pueden encontrar los archivos de configuración de Docker para el frontend en React.