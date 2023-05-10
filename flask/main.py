import io
import sys
from pathlib import Path
import csv
from datetime import datetime
from copy import deepcopy
from enum import Enum
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64


class DataType(Enum):
    AVERAGE = 1
    CUMULATIVE = 2
    MOVING_AVERAGE = 3


app = Flask(__name__)
Bootstrap(app)
app.debug = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rainfall')
def rainfall():
    return render_template('rainfall.html')


@app.route('/sunhours')
def sunhours():
    return render_template('sunhours.html')


@app.route('/hello_world')
def hello_world():
    fig, _ = create_graph({"field": "SQ", "data_type": DataType.CUMULATIVE, "y_label": "Total sun hours"})

    # encode the plot image as a base64 string
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    print("In hello world")

    # render the HTML template with the plot image
    return render_template('index.html', image_base64=image_base64)

    # # Plot the statistics.
    # # create_graph({"field": "TX", "data_type": DataType.AVERAGE, "y_label": "Average Temperature (C)"})
    # # create_graph({"field": "RH", "data_type": DataType.CUMULATIVE, "y_label": "Total rainfall (mm)"})
    #
    # output = io.BytesIO()
    # plt.show()
    # return Response(output.getvalue(), mimetype='image/png')
    # # return 'Hello, World!'


def open_file():
    path = Path('weather_data/etmgeg_260.txt')
    lines = path.read_text().splitlines()
    return csv.reader(lines)


def read_txt_file():
    reader = open_file()

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

    return columns, reader


def load_period_data(start, end, data_config):
    columns, data = read_txt_file()

    loaded_data = []
    dates = []
    data_value = None
    total = 0
    count = 0
    for row in data:
        date = datetime.strptime(row[columns['YYYYMMDD']], '%Y%m%d')

        if start <= date <= end:
            value = float(row[columns[data_config["field"]]])/10
            total += value
            count += 1
            if data_config["data_type"] == DataType.CUMULATIVE:
                data_value = total
            elif data_config["data_type"] == DataType.AVERAGE:
                data_value = total / count
            loaded_data.append(data_value)
            dates.append(datetime.strptime(row[columns['YYYYMMDD']], '%Y%m%d'))

    return dates, loaded_data


def create_graph(data_config):
    fig, ax = plt.subplots()
    dates, data22 = load_period_data(datetime(2022, 3, 1), datetime(2022, 4, 30), data_config)
    ax.plot(data22, color='blue', alpha=0.5, label="2022")

    dates, data23 = load_period_data(datetime(2023, 3, 1), datetime(2023, 4, 30), data_config)
    ax.plot(data23, color='red', alpha=0.5, label="2023")

    ax.set_xlabel('', fontsize=16)
    fig.autofmt_xdate()
    plt.legend(loc="upper left")
    ax.set_ylabel(data_config["y_label"], fontsize=16)
    ax.tick_params(labelsize=16)

    return fig, ax


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)