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
    browser.get("https://listingcenter.nasdaq.com/noncompliantcompanylist.aspx")
    expand = browser.find_element_by_class_name("rgExpand")
    expand.click()
    time.sleep(1)
    data = []
    rows = browser.find_elements_by_xpath('//table[contains(@class, "rgMasterTable")]/tbody/tr')
    header = ""
    for row in rows:
        className = row.get_attribute('class')
        if className == "rgGroupHeader":
            header = row.find_element_by_xpath(".//td[last()]/p")
        else:
            company = {
                "name": header.text,
                "tickers": [],
                "deficiency": "",
                "market": "",
                "date": ""
            }
            tickerContainer = row.find_element_by_xpath('.//*[contains(@class, "LeftPadding")]')
            tickers = tickerContainer.find_elements_by_xpath(('.//a'))
            for t in tickers:
                company["tickers"].append(t.text)
            categories = tickerContainer.find_elements_by_xpath('.//following-sibling::td')
            i = 0
            for category in categories: 
                if i == 0: 
                    company["deficiency"] = category.text
                elif i == 1:
                    company["market"] = category.text
                elif i == 2: 
                    company["date"] = category.text
                i += 1
            data.append(company)
    return jsonify(data)

if __name__ == '__main__':
    app.run()
