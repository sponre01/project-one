# Brewerydb 
# package setup for brewery exploration

import requests
import json
import pprint
from config import api_key

key = api_key
endpoint = "beers"
page = "1"
pp = pprint.PrettyPrinter(indent=1)


def get_data(endpoint="beers", page='1', key=api_key):
    url = f"http://api.brewerydb.com/v2/{endpoint}/?key={key}&p={page}"
    response = requests.get(url).json()
    return response

def navigate_json(data):
    
    pp.pprint(data)
    print("--------------------------------------------------------------------------")
    next_step = ''
    order = 'data'
    while next_step != 'stop':
        print("Here are the current values you may select: ")
        if type(data) == list:
            print([i for i in range(len(data))])
        elif type(data) == dict:
            print(data.keys())
        next_step = input("Please input a valid selection or type 'stop' to break: ")
        if next_step == 'stop':
            break
        if type(data) == list:
            next_step = int(next_step)
            order = f"{order}[{next_step}]"
        else:
            order = f"{order}['{next_step}']"
        data = data[next_step]
        
        print("--------------------------------------------------------------------------")
        pp.pprint(data)
        print("--------------------------------------------------------------------------")
        print(f"Your current query is: {order}")
        print()
