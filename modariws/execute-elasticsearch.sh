#!/bin/bash

chmod +x /app/elasticsearch-8.10.2/jdk/bin/java
chmod +x /app/execute-elasticsearch.sh
chmod +x /app/elasticsearch-8.10.2/bin/elasticsearch
# Start Elasticsearch in the background
/app/elasticsearch-8.10.2/bin/elasticsearch

# Print Elasticsearch logs for troubleshooting
# tail -f /app/elasticsearch/elasticsearch-8.10.2/logs/*.log

# Wait for Elasticsearch to fully start
while ! curl -s http://localhost:9200; do
    echo "Waiting for Elasticsearch to start..."
    sleep 5
done

# Configure Elasticsearch for "color" field
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

# Check if Elasticsearch is available
# curl -X GET "localhost:9200"
