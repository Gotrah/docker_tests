import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the URL for the OpenWeatherMap API
url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine'

# Define the API key and location for the rainfall data
api_key = '06c5764cda669cfdcd9fd4f107136c71'
lat = '52.3784'
lon = '4.9007'

# Define the date range for the rainfall data
start_date = datetime(2022, 1, 1)
end_date = datetime.today()

# Make a request to the OpenWeatherMap API to get the rainfall data
rainfall_data = []
current_date = start_date
while current_date <= end_date:
    timestamp = int(current_date.timestamp())
    params = {
        'lat': lat,
        'lon': lon,
        'dt': timestamp,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("Data: ", data)
    rainfall = data['hourly'][0].get('rain', {}).get('1h', 0)
    rainfall_data.append((current_date, rainfall))
    current_date += timedelta(days=1)

# Generate a line graph of the rainfall data using Matplotlib
dates = [data[0] for data in rainfall_data]
rainfall = [data[1] for data in rainfall_data]

fig, ax = plt.subplots()
ax.plot(dates, rainfall)
ax.set_xlabel('Date')
ax.set_ylabel('Rainfall (mm)')
ax.set_title('Daily rainfall in Amsterdam')
plt.show()
