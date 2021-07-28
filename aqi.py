import datetime
import requests
from bs4 import BeautifulSoup
from time import time

DATA_EXPIRATION_SECS = 3600
DATE_FORMAT = '%A, %b %d %Y %H'
URL = 'https://www.iqair.com/us/usa/california/truckee'


def get_date_from_cells(cells):
    date_cell_text = cells[0].text

    now = datetime.datetime.now()

    date_obj = None

    # putting the data point at noon because the forcast is supposed to span the whole day (I think)
    if (date_cell_text.lower() == 'today'):
        date_obj = datetime.datetime(now.year, now.month, now.day, 12)
    else:
        # WARNING: guessing year as now.year will get weird around January 1
        date_string = '{day} {year} 12'.format(
            day=date_cell_text, year=now.year)

        date_obj = datetime.datetime.strptime(date_string, DATE_FORMAT)

    return date_obj.isoformat() if date_obj > now else None


def get_row_date_and_aqi(row):
    cells = row.find_all('td')

    aqi = int(cells[1].div.p.span.b.text)

    return {"date": get_date_from_cells(cells), "aqi": aqi}


def fetch_aqi_html():
    page = requests.get(URL)

    return BeautifulSoup(page.content, 'html.parser')


def parse_aqi_data(soup):
    now_aqi = int(soup.find(class_="aqi-value__value").text)

    table = soup.find('table', 'aqi-forecast__weekly-forecast-table')
    rows = table.tbody.find_all('tr')

    all_forecasts = list(map(get_row_date_and_aqi, rows))

    future_forecasts = list(
        filter(lambda forecast: forecast["date"], all_forecasts))

    now_forecast = {"date": datetime.datetime.now().isoformat(),
                    "aqi": now_aqi}

    future_forecasts.insert(0, now_forecast)

    return future_forecasts


class AQI:
    def __init__(self):
        self.aqi_data = None
        self.last_updated = {"aqi": 0}

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
