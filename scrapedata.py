import time
import requests
import selectorlib
from datetime import datetime
import sqlite3

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

def initDB():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM temp_stamp")

    connection.commit()
    cursor.close()
    connection.close()


def storeDB(date, temperature):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO temp_stamp VALUES(?,?)", (date, temperature))

    connection.commit()
    cursor.close()
    connection.close()


def scrapedata(amount_data=5, time_cycle=1):
    initDB()
    count = 0
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        now = datetime.now()
        timestamp = now.strftime("%y-%m-%d-%H-%M-%S")
        storeDB(timestamp, extracted)
        count = count + 1
        if count >= amount_data:
            break
        else:
            time.sleep(time_cycle)


if __name__ == "__main__":
    count = 0

    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        now = datetime.now()
        timestamp = now.strftime("%y-%m-%d-%H-%M-%S")
        storeDB(timestamp, extracted)
        count = count + 1
        if count >= 5:
            break
        else:
            time.sleep(2)
