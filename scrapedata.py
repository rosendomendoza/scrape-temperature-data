import time
import requests
import selectorlib
from datetime import datetime

URL = "https://programmer100.pythonanywhere.com/"


def scrape(url):
    response = requests.get(url)
    return response.text


def extract(scraped):
    extractor = selectorlib.Extractor.from_yaml_file("home.yaml")
    value = extractor.extract(scraped)['home']
    return value


def store(date, temperature):
    with open("data.txt", "a") as file:
        to_store = f"{date},{temperature}\n"
        file.write(to_store)

def scrapedata(amount_lectura=10, time_cicle=60):
    count = 0
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        now = datetime.now()
        timestamp = now.strftime("%y-%m-%d-%H-%M-%S")
        store(timestamp, str(extracted))
        count = count + 1
        if count > amount_lectura:
            break
        else:
            time.sleep(time_cicle)



if __name__ == "__main__":
    count = 0
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        now = datetime.now()
        timestamp = now.strftime("%y-%m-%d-%H-%M-%S")
        store(timestamp, str(extracted))
        count = count + 1
        if count > 10:
            break
        else:
            time.sleep(60)
