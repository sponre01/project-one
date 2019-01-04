# Brewerydb 
# package setup for brewery exploration

import requests
key = "db2208bcd8a86d5b3a817f122e6ef489"
endpoint = "beers"
page = "1"


def get_data(endpoint="beers", page='1', key="db2208bcd8a86d5b3a817f122e6ef489"):
    url = f"http://api.brewerydb.com/v2/{endpoint}/?key={key}&p={page}"
    response = requests.get(url).json()
    return response

