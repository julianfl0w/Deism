#!/bin/bash

# To create the layers
# docker run --rm --entrypoint /bin/bash -v "$(pwd):/workdir" -w /workdir python:3.12-slim -c "bash createLayer.sh" > layer.zip

# Create a directory for Python packages that mimics the AWS Lambda structure
mkdir -p /opt/python/lib/python3.12/site-packages

# Install the required Python packages
pip install beautifulsoup4 requests -t /opt/python/lib/python3.12/site-packages

# Update package lists and install zip (Debian/Ubuntu)
apt-get update
apt-get install -y zip

# Package the installed packages into a ZIP file
cd /opt 
zip -r lambda_layer.zip .

# Output the zip file to stdout
cat lambda_layer.zip
