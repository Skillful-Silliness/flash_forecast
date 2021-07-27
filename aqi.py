import requests
from bs4 import BeautifulSoup
from time import time

DATA_EXPIRATION_SECS = 3600

URL = 'https://www.iqair.com/us/usa/california/truckee'


def get_row_date_and_aqi(row):
    cells = row.find_all('td')

    return {"date": cells[0].text, "aqi": cells[1].div.p.span.b.text}


def fetch_aqi_html():
    page = requests.get(URL)

    return BeautifulSoup(page.content, 'html.parser')


def parse_aqi_data(soup):
    table = soup.find('table', 'aqi-forecast__weekly-forecast-table')
    rows = table.tbody.find_all('tr')

    return list(map(get_row_date_and_aqi, rows))


class AQI:
    def __init__(self):
        self.aqi_data = None
        self.last_updated = {}

    # TODO: dedupe these with the weather forcast class
    def is_data_expired(self, key):
        return time() - self.last_updated[key] > DATA_EXPIRATION_SECS

    def set_last_updated(self, key):
        self.last_updated[key] = time()

    def get_aqi_data(self):
        if self.aqi_data == None or self.is_data_expired("aqi"):
            self.aqi_data = parse_aqi_data(fetch_aqi_html())

        return self.aqi_data


def demo():
    forcaster = AQI()
    aqi_data = forcaster.get_aqi_data()

    print(aqi_data)
