import requests
from pathlib import Path


def get_summary_of_category(category, country):
    path = "http://localhost:5001/" + category + "/" + country
    content = requests.get(path).json()[0]
    count = sum(content["data"].values())
    return count

