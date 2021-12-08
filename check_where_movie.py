#import requests
import urllib.request
import json
import os
from dotenv import load_dotenv

load_dotenv()


def check_where_movie():
    API_KEY = os.getenv("API_KEY2")

    with urllib.request.urlopen(
            f"https://api.watchmode.com/v1/search/?apiKey={API_KEY}&search_field=name&search_value=tt0119488") as url:
        data = json.loads(url.read().decode())
        print(data)


check_where_movie()