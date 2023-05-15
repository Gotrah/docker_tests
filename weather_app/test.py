import urllib.request
import os
import datetime
import zipfile


def check_file_updated():
    try:
        modified_timestamp = os.path.getmtime("weather_data/etmgeg_240.txt")
        modified_datetime = datetime.datetime.fromtimestamp(modified_timestamp)
        if modified_datetime < datetime.datetime.now() - datetime.timedelta(days=1):
            return False
        else:
            return True
    except Exception as e:
        return False


def download_file(url, save_path):
    try:
        urllib.request.urlretrieve(url, save_path)
        print("File downloaded successfully.")

        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            zip_ref.extractall("weather_data/")

        os.remove(save_path)

    except Exception as e:
        print("An error occurred while downloading the file:", e)


if not check_file_updated():
    download_file("https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_240.zip",
                  "weather_data/etmgeg_240.zip")
