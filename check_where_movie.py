#import requests
from logging import error
from dotenv.main import dotenv_values
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

stored_ids = "stored_ids.json"
API_KEY = os.getenv("API_KEY2")

def check_where_movie():
    
    #Etsi watchmode API:sta tietyllä imdb id:llä elokuva
    
    search_request = requests.get(f"https://api.watchmode.com/v1/search/?apiKey={API_KEY}&search_field=imdb_id&search_value=tt0076759")

    data = search_request.json()

    item_data = data["title_results"] 
    #Ota talteen kyseisen elokuvan ID (eri kuin imdb id)
    title = item_data[0]["id"]

    #Etsi elokuvan sourcet ID:llä
    title_request = requests.get(f"https://api.watchmode.com/v1/title/{title}/sources/?apiKey={API_KEY}")

    data = title_request.json()
    sources_list = []

    #Lisää sourcet listaan
    for i in range(len(data)):
        idt = data[i]["source_id"]
        
        sources_list.append(idt)

    sources_list = list(dict.fromkeys(sources_list))
    
    find_sources_from_file(sources_list)
    

#etsi source idllä jsonista sourcejen nimiä.
def find_sources_from_file(ids_to_find):

    source_names = []

    try:
        f = open(stored_ids)

        data = json.load(f)

        f.close()

        for i in range(len(ids_to_find)):
            if data.get(str(ids_to_find[i])):
                source_names.append(data.get(str(ids_to_find[i])))
                
            else:
                add_sources_to_file(ids_to_find)
            return source_names
    except FileNotFoundError:
        create_new_file(ids_to_find)



#luo uusi json tiedosto
def create_new_file(ids_to_find):
    f = open(stored_ids, "w")
    f.close()
    add_sources_to_file(ids_to_find)
    

#lisää json tiedostoon key value pareina kaikkien mahdollisten sourcejen id ja nimi
def add_sources_to_file(ids_to_find):
    sources = {}
    sources_request = requests.get(f"https://api.watchmode.com/v1/sources/?apiKey={API_KEY}")
    data = sources_request.json()

    for i in range(len(data)):
        id = data[i]["id"]
        name = data[i]["name"]
        sources[id] = name

    
    json_object = json.dumps(sources, indent=2)

    

    try:
        with open(stored_ids, "w") as outfile:
            outfile.write(json_object)
        
        find_sources_from_file(ids_to_find)
    except FileNotFoundError as e:
        create_new_file(ids_to_find)



check_where_movie()