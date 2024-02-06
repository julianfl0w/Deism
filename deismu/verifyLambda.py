import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options for headless operation
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def scrape_url(driver, url):
    driver.get(url)
    name_element = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h3.cds-119 strong"))
    )
    name = name_element.text if name_element else "Name not found"

    course_name_element = driver.find_element(By.CSS_SELECTOR, "h2.course-name")
    course_name = course_name_element.text if course_name_element else "Course name not found"

    return {'name': name, 'course_name': course_name}

def lambda_handler(event, context):
    results = []
    urls = event.get('urls')
    if not urls or not isinstance(urls, list):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing or invalid URL list'})
        }

    # Initialize the headless browser
    with webdriver.Chrome(options=chrome_options) as driver:
        for url in urls:
            try:
                result = scrape_url(driver, url)
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})

    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }

# Main execution for direct run
if __name__ == '__main__':
    # Get URL from environment variable
    test_url = os.environ.get('TEST_URL')

    if test_url:
        # Simulate the event structure for direct invocation
        event = {'urls': [test_url]}
        result = lambda_handler(event, context=None)
        print(json.dumps(result, indent=4))
    else:
        print("No URL provided.")
