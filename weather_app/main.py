import io
import logging
import sys
from pathlib import Path
import csv
from datetime import datetime
from copy import deepcopy
from enum import Enum
from weather_app import Blueprint, render_template
from flask_bootstrap import Bootstrap

import matplotlib
import matplotlib.pyplot as plt
import base64

from weather_data import WeatherData
from .nav import nav

# matplotlib.use('Agg')

app = Flask(__name__)
Bootstrap(app)
# app.debug = True


class DataType(Enum):
    AVERAGE = 1
    CUMULATIVE = 2
    MOVING_AVERAGE = 3


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rainfall')
def rainfall():
    weather_data = WeatherData(WeatherData.DataType.CUMULATIVE, "RH", "Total rainfall")
    image_base64 = weather_data.create_graph()

    # render the HTML template with the plot image
    return render_template('rainfall.html', image_base64=image_base64)


@app.route('/sun_hours')
def sun_hours():
    weather_data = WeatherData(WeatherData.DataType.CUMULATIVE, "SQ", "Total sun hours")
    image_base64 = weather_data.create_graph()

    # render the HTML template with the plot image
    return render_template('sun_hours.html', image_base64=image_base64)


@app.route('/temperature')
def temperature():
    weather_data = WeatherData(WeatherData.DataType.AVERAGE, "TX", "Average temperature")
    image_base64 = weather_data.create_graph()

    # render the HTML template with the plot image
    return render_template('temperature.html', image_base64=image_base64)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)