#!/bin/bash

# URL to test
TEST_URL="https://www.coursera.org/account/accomplishments/verify/GA668424ZUQH"

# Name of your Docker image
DOCKER_IMAGE="selenium"

# Run the Docker container and capture the output
output=$(docker run --rm -e TEST_URL="$TEST_URL" "$DOCKER_IMAGE")

# Check the output
echo "Output received: $output"

# Parse and check the output here
# Example: using jq to check a JSON output
# echo $output | jq 'Your conditions here'
