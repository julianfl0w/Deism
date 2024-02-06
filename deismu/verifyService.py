from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
CORS(app)

def get_chrome_options():

    chrome_prefs = {}
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')  # Only if GPU is not used
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.experimental_options["prefs"] = chrome_prefs


    return chrome_options

def get_webdriver():
    chrome_service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=chrome_service, options=get_chrome_options())

def scrape_url(driver, url):
    try:
        driver.get(url)
        name_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h3.cds-119 strong"))
        )
        name = name_element.text if name_element else "Name not found"

        course_name_element = driver.find_element(By.CSS_SELECTOR, "h2.course-name")
        course_name = course_name_element.text if course_name_element else "Course name not found"

        return {'name': name, 'course_name': course_name}
    except Exception as e:
        return {'error': str(e)}

driver = get_webdriver() 
@app.route('/verify', methods=['POST'])
def scrape():
    data = request.json
    urls = data.get('urls')

    if not urls or not isinstance(urls, list):
        return jsonify({'error': 'Missing or invalid URL list'}), 400

    results = []
    for url in urls:
        result = scrape_url(driver, url)
        results.append(result)

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
