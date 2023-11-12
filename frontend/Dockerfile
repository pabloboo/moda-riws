# Use a base image with OpenJDK 8
FROM openjdk:8-jre

# Install Node.js and npm
# replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# update the repository sources list
# and install dependencies
RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y autoclean
# create nvm directory
RUN mkdir /usr/local/nvm
# nvm environment variables
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 14.17.0
# install nvm
# https://github.com/nvm-sh/nvm#install-script
RUN curl --silent -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default
# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
# confirm installation
RUN node -v
RUN npm -v
RUN npm install @appbaseio/reactivesearch@3.45.0 --legacy-peer-deps

# Create a working directory for your Scrapy project
WORKDIR /app

# Copy your Scrapy project into the container
COPY . /app

# Expose port 3000 for the web application
EXPOSE 3000

# Change ownership of ESLint cache directory
# RUN chown -R nonrootuser /app/frontend/node_modules/.cache

# Start Elasticsearch and run Scrapy using a shell script
CMD ["/bin/sh", "/app/execute-frontend.sh"]