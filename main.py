from selenium import webdriver
from flask import Flask, request
from flask import jsonify
from lxml import html
import requests
import time
import os

app = Flask(__name__)
def makeRequestAndGetTree(URL):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Accept-Language': 'en-gb',
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    try:
        r = requests.get(URL, headers=headers, timeout=5)
        tree = html.fromstring(r.content)
        return tree
    except Exception as e:
        print(e)
        return None

def scrapeCalendar(URL):
    tree = makeRequestAndGetTree(URL)
    if tree is None:
        return None
    eventContainers = tree.xpath("//tr[@item-type='http://schema.org/Event']")
    print(len(eventContainers))
    print(tree)

@app.route("/sherdog/events")
def scrape():
    URL = 'http://www.sherdog.com/events/upcoming'
    events = scrapeCalendar(URL)
    events = jsonify(events)
    return events

@app.route("/brwlrz/getFavorites")
def getFavorites():
    token = 'api1575404422oY4rNBhdTW9JjgfyulEi78894'
    calendar = '1576110713243225' 
    url = 'https://www.addevent.com/api/v1/me/calendars/events/list/?token=' + token + '&calendar_id=' + calendar
    events = []
    while True:
        old = requests.get(url)
        old = old.json()
        past = old['events']
        events += past
        if old['paging']['next'] is '':
            break
        else:
            url = old['paging']['next']
    return jsonify(events)

@app.route("/brwlrz/setFavorites", methods=['POST'])
def setFavorites():
    req_data = request.get_json()
    token = 'api1575404422oY4rNBhdTW9JjgfyulEi78894'
    calendar = '1576110713243225' 
    for row in req_data:
        i = row[0]
        favorite = row[1]
        URL = 'https://www.addevent.com/api/v1/me/calendars/events/save/?token=' + token +'&calendar_id=' + calendar +'&event_id='+ i + '&organizer_email=' + favorite
         r = requests.get(URL)
    return jsonify(req_data)

def scrapeCalendar(URL):
    tree = makeRequestAndGetTree(URL)
    if tree is None:
        return None
    events = []
    containers = tree.xpath("//tr[@itemtype='http://schema.org/Event']")
    for container in containers:
        date = container.xpath(".//meta[@itemprop='startDate']")
        date = date[0].attrib.get("content") if len(date) is not 0 else None
        name = container.xpath(".//meta[@itemprop='name']")
        name = name[0].attrib.get("content") if len(name) is not 0 else None
        org = None
        if (name is not None):
            name = name.split("-")
            title = name[1].strip()
            org = name[0].strip()
        location = container.xpath(".//span[@itemprop='location']")
        location = location[0].text_content() if len(location) is not 0 else None
        link = container.xpath(".//a[@itemprop='url']")
        link = 'https://www.sherdog.com/' + link[0].attrib.get("href") if len(link) is not 0 else None
        event = {
            "date": date,
            "name": title,
            "location": location,
            "link": link,
            "org": org
        }
        print(event)
        events.append(event)
    return events

@app.route("/")
def test():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser= webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    browser.get("https://listingcenter.nasdaq.com/noncompliantcompanylist.aspx")
    expand = browser.find_element_by_class_name("rgExpand")
    expand.click()
    time.sleep(1)
    table = browser.find_element_by_xpath('//table[contains(@class, "rgMasterTable")]')
    table = table.get_attribute('innerHTML')
    browser.quit()
    table = html.fromstring(table)
    rows = table.xpath('.//tbody/tr')
    data = []
    header = ""
    for row in rows:
        className = row.get('class')
        if className == "rgGroupHeader":
            header = row.xpath(".//td[last()]/p")[0].text_content()
        else:
            company = {
                "name": header,
                "tickers": [],
                "exchange": "NASDAQ",
            }
            tickerContainer = row.xpath('.//*[contains(@class, "LeftPadding")]')[0]
            tickers = tickerContainer.xpath(('.//a'))
            for t in tickers:
                company["tickers"].append(t.text_content())
            categories = tickerContainer.xpath('.//following-sibling::td')
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
            print(company)
    return jsonify(data)

if __name__ == '__main__':
    app.run()
