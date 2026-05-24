from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route('/sub4unlock', methods=['GET'])
def bypass_endpoint():
    url = request.args.get('url')
    start_time = time.time()
    
    if not url:
        return jsonify({
            'status': 'error',
            'error': 'Missing url parameter',
            'Discord': 'https://discord.gg/jEaY4etBTY',
            'Made By': 'LATstudio'
        }), 400
    
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        
        link_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.linky.buttonpanel.buttonpanel-block.btn-lg.get-link"))
        )
        
        Sub4Unlock_Result = link_element.get_attribute("href")
        
        driver.quit()
        
        elapsed = time.time() - start_time
        
        return jsonify({
            'status': 'success',
            'result': Sub4Unlock_Result,
            'time': f"{elapsed:.12f}",
            'Discord': 'https://discord.gg/jEaY4etBTY',
            'Made By': 'LATstudio'
        })
        
    except Exception as e:
        elapsed = time.time() - start_time
        return jsonify({
            'status': 'error',
            'error': str(e),
            'time': f"{elapsed:.12f}",
            'Discord': 'https://discord.gg/jEaY4etBTY',
            'Made By': 'LATstudio'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)