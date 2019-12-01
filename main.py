from selenium import webdriver
from flask import Flask
from flask import jsonify
import time
import os

app = Flask(__name__)

@app.route("/")
def test():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get("https://listingcenter.nasdaq.com/noncompliantcompanylist.aspx")
    expand = driver.find_element_by_class_name("rgExpand")
    expand.click()
    time.sleep(.2)
    headers = driver.find_elements_by_xpath('//*[contains(@class, "rgGroupHeader")]//p')
    details = driver.find_elements_by_xpath('//*[contains(@title, "Quote")]/parent::*/following-sibling::td')
    data = []

    for x in headers:
        company = {
            "name": "",
            "ticker": "",
            "deficiency": "",
            "market": "",
            "date": ""
        }
        company["name"] = x.text
        data.append(company)
    i = 1
    counter = 0
    for x in details:
        if (i == 1):
            data[counter]["ticker"] = x.text
        elif (i == 2):
            data[counter]["deficiency"] = x.text
        elif (i == 3):
            data[counter]["market"] = x.text
        elif (i == 4):
            data[counter]["date"] = x.text
            i = 0
            counter += 1
        i += 1
    return jsonify(data)

if __name__ == '__main__':
    app.run()
