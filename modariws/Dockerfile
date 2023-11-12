FROM python:3.9-slim-bullseye

# Install Python and other dependencies as needed
RUN apt-get update && apt-get install -y python3 python3-pip
# Install necessary dependencies for Elasticsearch
RUN apt update && apt install -y wget tar
# Install curl
RUN apt-get install -y curl

# Create a non-root user (needed to be able to execute elasticsearch)
RUN useradd -m nonrootuser
# Set the working directory and change ownership to the non-root user
WORKDIR /app
RUN chown -R nonrootuser /app
# Give the non-root user all permissions on the /app directory
RUN chmod -R 777 /app
# Switch to the non-root user
USER nonrootuser

# Create a directory to install Elasticsearch
# RUN mkdir -p /app/elasticsearch
# WORKDIR /app/elasticsearch
# # Install Elasticsearch
# RUN curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.2-linux-x86_64.tar.gz
# RUN tar -xvf elasticsearch-8.10.2-linux-x86_64.tar.gz

# # Clear the existing content of elasticsearch.yml
# RUN echo "" > /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml

# # Copy the content of your local elasticsearch.yml to the container
# COPY elasticsearch.yml /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml

# USER root
# # Adjust file permissions
# RUN chown -R nonrootuser /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml \
#     && chmod 644 /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml
# USER nonrootuser

# RUN echo "xpack.security.enabled: false" >> /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml
# RUN echo "http.cors.enabled: true" >> /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml
# RUN echo "http.cors.allow-origin: '*'" >> /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml
# RUN echo "http.cors.allow-credentials: true" >> /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml
# RUN echo "http.cors.allow-headers: 'X-Requested-With, Content-Type, Content-Length, Authorization'" >> /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml
# RUN echo "network.host: 0.0.0.0" >> /app/elasticsearch/elasticsearch-8.10.2/config/elasticsearch.yml

# Create a working directory for your Scrapy project
WORKDIR /app

# Copy your Scrapy project into the container
COPY . /app

USER root
# Adjust file permissions
RUN chown -R nonrootuser /app/elasticsearch-8.10.2/ \
    && chmod 777 /app/elasticsearch-8.10.2/
RUN chmod 777 /app/elasticsearch-8.10.2/jdk/bin/java
RUN chmod 777 /app/execute-elasticsearch.sh
RUN chmod 777 /app/elasticsearch-8.10.2/bin/elasticsearch
USER nonrootuser

# Expose port 9200 for Elasticsearch
EXPOSE 9200

# Start Elasticsearch and run Scrapy using a shell script
CMD /bin/sh /app/execute-elasticsearch.sh