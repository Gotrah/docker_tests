import csv
import io
import os
from pathlib import Path
import urllib.request
import zipfile

from datetime import datetime

from enum import Enum

import matplotlib
import matplotlib.pyplot as plt
import base64


matplotlib.use('agg')


class WeatherData:
    WEATHER_DATA_DIR = "weather_app/weather_data/"
    WEATHER_DATA_FILE = "etmgeg_240.txt"
    WEATHER_DATA_URL = "https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_240.zip"

    def __init__(self, data_type, field, y_label):
        self.data_type = data_type
        self.field = field
        self.y_label = y_label

        self.columns = None
        self.reader = None

    @staticmethod
    def open_file():
        path = Path(os.path.join(WeatherData.WEATHER_DATA_DIR, WeatherData.WEATHER_DATA_FILE))

        if not WeatherData.check_file_updated():
            WeatherData.download_weather_data()

        try:
            lines = path.read_text().splitlines()
        except FileNotFoundError as e:
            print("File not found:", e)
            exit()

        return csv.reader(lines)

    @staticmethod
    def check_file_updated():
        """Check if the file has been updated today."""
        try:
            modified_timestamp = os.path.getmtime("weather_app/weather_data/etmgeg_240.txt")
            modified_date = datetime.fromtimestamp(modified_timestamp).date()
            if modified_date < datetime.now().date():
                return False
            else:
                return True
        except FileNotFoundError as e:
            return False

    @staticmethod
    def download_weather_data():
        """Download the file from the given url, extract it and remove the zip file."""
        try:
            filename = os.path.basename(WeatherData.WEATHER_DATA_URL)
            save_path = os.path.join(WeatherData.WEATHER_DATA_DIR, filename)
            urllib.request.urlretrieve(WeatherData.WEATHER_DATA_URL, save_path)
            print(f"File downloaded successfully from url {WeatherData.WEATHER_DATA_URL}.")

            with zipfile.ZipFile(save_path, 'r') as zip_ref:
                zip_ref.extractall(WeatherData.WEATHER_DATA_DIR)

            os.remove(save_path)
            print("Done downloading and extracting.")

        except urllib.error.URLError as e:
            print("An error occurred while downloading the file:", e)
        except FileNotFoundError as e:
            print("The specified directory does not exist:", e)
            print("Currently it is:", os.getcwd())
        except PermissionError as e:
            print("Permission denied for the specified directory:", e)
        except ValueError as e:
            print("Invalid URL provided:", e)

    def read_txt_file(self):
        reader = self.open_file()

        header_found = False
        counter = 0
        # Go through lines until an empty row is found. The next row is the header row.
        while not header_found and counter < 100:
            current_row = next(reader)
            if not current_row:
                header_found = True
            counter += 1

        header_row = next(reader)
        next(reader)

        columns = {column_header.strip(): index for index, column_header in enumerate(header_row)}

        self.columns = columns
        self.reader = reader

    def load_period_data(self, start, end):
        self.read_txt_file()

        loaded_data = []
        dates = []
        data_value = None
        total = 0
        count = 0

        for row in self.reader:
            date = datetime.strptime(row[self.columns['YYYYMMDD']], '%Y%m%d')

            if start <= date <= end:
                value = float(row[self.columns[self.field]])/10
                total += value
                count += 1
                if self.data_type == WeatherData.DataType.CUMULATIVE:
                    data_value = total
                elif self.data_type == WeatherData.DataType.AVERAGE:
                    data_value = total / count
                loaded_data.append(data_value)
                dates.append(datetime.strptime(row[self.columns['YYYYMMDD']], '%Y%m%d'))

        return dates, loaded_data

    def create_graph(self):
        fig, ax = plt.subplots()
        dates, data22 = self.load_period_data(datetime(2022, 3, 1), datetime(2022, 5, 30))
        ax.plot(data22, color='blue', alpha=0.5, label="2022")

        dates, data23 = self.load_period_data(datetime(2023, 3, 1), datetime(2023, 5, 30))
        ax.plot(data23, color='red', alpha=0.5, label="2023")

        ax.set_xlabel('Date', fontsize=16)
        fig.autofmt_xdate()
        plt.legend(loc="upper left")
        ax.set_ylabel(self.y_label, fontsize=16)
        ax.tick_params(labelsize=16)

        # encode the plot image as a base64 string
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)

        return base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')

    class DataType(Enum):
        AVERAGE = 1
        CUMULATIVE = 2
        MOVING_AVERAGE = 3

