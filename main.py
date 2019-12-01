from selenium import webdriver
from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def test():
    print("test")
    return 'Hello World'

if __name__ == '__main__':
    app.run()

# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
