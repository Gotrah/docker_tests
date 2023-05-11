import csv
import io
from pathlib import Path

from datetime import datetime

from enum import Enum

import matplotlib
import matplotlib.pyplot as plt
import base64


matplotlib.use('agg')


class WeatherData:

    def __init__(self, data_type, field, y_label):
        self.data_type = data_type
        self.field = field
        self.y_label = y_label

        self.columns = None
        self.reader = None

    @staticmethod
    def open_file():
        path = Path('weather_app/weather_data/etmgeg_260.txt')
        lines = path.read_text().splitlines()
        return csv.reader(lines)

    def read_txt_file(self):
        reader = self.open_file()

        header_found = False
        counter = 0
        while not header_found and counter < 100:
            current_row = next(reader)
            if not current_row:
                header_found = True
            counter += 1

        header_row = next(reader)

        columns = {}

        for index, column_header in enumerate(header_row):
            columns[column_header.strip()] = index

        next(reader)

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

