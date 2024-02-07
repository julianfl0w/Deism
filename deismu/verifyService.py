from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def scrape_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Update your CSS selectors according to the actual HTML structure
            name_element = soup.select_one("h3.cds-119 strong")
            name = name_element.text if name_element else "Name not found"

            course_name_element = soup.select_one("h2.course-name")
            course_name = course_name_element.text if course_name_element else "Course name not found"

            return {'name': name, 'course_name': course_name}
        else:
            return {'error': 'Failed to fetch the URL'}
    except Exception as e:
        return {'error': str(e)}

@app.route('/verify', methods=['POST'])
def scrape():
    data = request.json
    urls = data.get('urls')

    if not urls or not isinstance(urls, list):
        return jsonify({'error': 'Missing or invalid URL list'}), 400

    results = []
    for url in urls:
        result = scrape_url(url)
        results.append(result)

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
