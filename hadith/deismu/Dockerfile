# Use Python with Alpine Linux base image
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /

# Install dependencies for headless operation
RUN apk add --no-cache \
    chromium \
    chromium-chromedriver \
    && pip install --no-cache-dir selenium==4.0.0 webdriver_manager

# Copy the script into the container
COPY verifyCert.py /verifyCert.py

# Command to run the script
CMD ["python", "/verifyCert.py"]
