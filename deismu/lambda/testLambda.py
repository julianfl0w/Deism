import requests
import json

# Define your URLs array in Python
urls = ["https://www.coursera.org/account/accomplishments/verify/GA668424ZUQH", "google.com"]

# API endpoint
url = "https://hwi6tlzmzk.execute-api.us-east-1.amazonaws.com/verifyCertificate"

# Create the payload with the URLs array
payload = {
    "urls": urls
}

# Convert the payload to a JSON-formatted string
data = json.dumps(payload)

# Make a POST request with JSON data
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})

# Check the status code and print the response
if response.status_code == 200:
    print("Success:")
    print(response.json())  # Assuming the response is JSON-formatted
else:
    print("Error:", response.status_code, response.text)
