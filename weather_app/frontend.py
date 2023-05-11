# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

from .weather_data import WeatherData
from .nav import nav

frontend = Blueprint('frontend', __name__)

# We're adding a navbar as well through weather_app-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
nav.register_element('frontend_top', Navbar(
    View('Home', '.index'),
    View('Rainfall', '.rainfall'),
    View('Sun Hours', '.sun_hours'),
    View('Temperature', '.temperature'),
))


# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@frontend.route('/')
def index():
    return render_template('index.html')


@frontend.route('/rainfall')
def rainfall():
    weather_data = WeatherData(WeatherData.DataType.CUMULATIVE, "RH", "Total rainfall")
    image_base64 = weather_data.create_graph()

    # render the HTML template with the plot image
    return render_template('rainfall.html', image_base64=image_base64)


@frontend.route('/sun_hours')
def sun_hours():
    weather_data = WeatherData(WeatherData.DataType.CUMULATIVE, "SQ", "Sun Hours")
    image_base64 = weather_data.create_graph()

    # render the HTML template with the plot image
    return render_template('sun_hours.html', image_base64=image_base64)


@frontend.route('/temperature')
def temperature():
    weather_data = WeatherData(WeatherData.DataType.AVERAGE, "TX", "Average Temperature")
    image_base64 = weather_data.create_graph()

    # render the HTML template with the plot image
    return render_template('temperature.html', image_base64=image_base64)
