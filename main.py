from flask import Flask, render_template, request, make_response, jsonify, redirect, flash, send_from_directory
# from flask_jwt import JWT, jwt_required, current_identity
import json, os
import time
from flask_cors import CORS, cross_origin
from seleniumwire import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import collections

SECRET_KEY = "5713q3E#@f4h"
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, support_credentials=True)

def workBrowser(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument("--user-agent=" + user_agent)
    # service = ChromeService(executable_path=ChromeDriverManager().install())
    # chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
    chrome_driver = webdriver.Chrome(options=chrome_options)
    
    stealth(
        chrome_driver,
        # user_agent=user_agent,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        run_on_insecure_origins=False
    )
    chrome_driver.maximize_window()
    try:
        chrome_driver.get(url)
        # chrome_driver.implicitly_wait(10)
    except Exception as ex:
        chrome_driver.quit()
        print(ex)
        return
    link_video = "No link"
    print(chrome_driver.requests.count)
    for request in chrome_driver.requests:
        if str(request.url).find('ainakwalajeen.com:999/') != -1:
            link_video = request.url
            print(link_video)
            break
    chrome_driver.quit()
    return link_video

@app.route('/api/video_stream', methods=['GET'])
@cross_origin(supports_credentials=True)
def process_image_api():
    video_url = request.args.get('url')
    print(video_url)
    stream_Link = workBrowser(video_url)
    return stream_Link

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)