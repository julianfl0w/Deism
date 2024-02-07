import requests
import json

# Endpoint of the Flask app to test
flask_endpoint = "http://localhost:5000/verify"
flask_endpoint = "http://23.20.174.7:5000/verify"

# JSON payload with the URL to test
json_payload = {
    "urls": ["https://www.coursera.org/account/accomplishments/verify/GA668424ZUQH"]
}

# Send a POST request to the Flask app
response = requests.post(flask_endpoint, json=json_payload)

# Check the status code of the response
if response.status_code == 200:
    print("Request was successful.")
else:
    print(f"Request failed with status code: {response.status_code}")

# Print the output received from the Flask app
print("Output received:", response.text)

# Optionally, parse the JSON response and perform further checks
# response_data = response.json()
# print(response_data)
# Here you can add more specific checks based on the structure of your response data
