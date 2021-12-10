from logging import error
from dotenv.main import dotenv_values
import requests
import os
from dotenv import load_dotenv
import json
from google.cloud import storage
import time

storage_client = storage.Client()

load_dotenv()

stored_ids = "stored_ids.json"
bucket_name = os.environ.get("BUCKET_NAME")
API_KEY=os.environ.get("API_KEY2")

def check_where_movie(leffa_id):
    
    #Etsi watchmode API:sta tietyllä imdb id:llä elokuva
    
    search_request = requests.get(f"https://api.watchmode.com/v1/search/?apiKey={API_KEY}&search_field=imdb_id&search_value={leffa_id}")

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
    
    return find_sources_from_bucket(sources_list)
    

def find_sources_from_bucket(ids_to_find):
    source_names = []

    print("for loop alkaa")
    read = True
    for i in range(len(ids_to_find)):
        
        if read:
            data = read_from_bucket(ids_to_find)
            read = False

        # with open(stored_ids, "r") as content:
        #     data2 = json.loads(content.read())

        
        # data = json.load(f)

        # f.close()
        if str(ids_to_find[i]) in data:
            source_names.append(data.get(str(ids_to_find[i])))
        else:
            add_sources_to_bucket(ids_to_find)
            read = True

        # if str(ids_to_find[i]) in data2:
        #     source_names.append(data2.get(str(ids_to_find[i])))

        # else:
        #     print("for loopin else")
        #     add_sources_to_bucket(ids_to_find)                
                
    return source_names
    


#etsi source idllä jsonista sourcejen nimiä.
# def find_sources_from_file(ids_to_find):

#     source_names = []

#     try:
#         f = open(stored_ids)

#         data = json.load(f)

#         f.close()

        

#         print("for loop alkaa")
#         for i in range(len(ids_to_find)):

#             with open(stored_ids, "r") as content:
#                 data2 = json.loads(content.read())

#             # if ids_to_find[i] in data:
#             #     source_names.append(data.get(str(ids_to_find[i])))

#             # else:
#             #     print("for loopin else")
#             #     add_sources_to_file(ids_to_find)

#             if str(ids_to_find[i]) in data2:
#                 source_names.append(data2.get(str(ids_to_find[i])))

#             else:
#                 print("for loopin else")
#                 add_sources_to_file(ids_to_find)                
                    
#         return source_names
#     except FileNotFoundError:
#         create_new_file(ids_to_find)


#luo uusi json tiedosto
# def create_new_file(ids_to_find):
#     f = open(stored_ids, "w")
#     f.close()
#     add_sources_to_file(ids_to_find)




def add_sources_to_bucket(ids_to_find):
    sources = {}
    sources_request = requests.get(f"https://api.watchmode.com/v1/sources/?apiKey={API_KEY}")
    data = sources_request.json()
    for i in range(len(data)):
        id = data[i]["id"]
        name = data[i]["name"]
        sources[id] = name

    
    json_object = json.dumps(sources, indent=2)

    write_to_bucket(json_object)


#lisää json tiedostoon key value pareina kaikkien mahdollisten sourcejen id ja nimi
# def add_sources_to_file(ids_to_find):
#     sources = {}
#     sources_request = requests.get(f"https://api.watchmode.com/v1/sources/?apiKey={API_KEY}")
#     data = sources_request.json()
#     for i in range(len(data)):
#         id = data[i]["id"]
#         name = data[i]["name"]
#         sources[id] = name

    
#     json_object = json.dumps(sources, indent=2)

#     try:
#         with open(stored_ids, "w") as outfile:
#             outfile.write(json_object)
        
#     except FileNotFoundError as e:
#         create_new_file(ids_to_find)


def read_from_bucket(ids_to_find):
    bucket = storage_client.get_bucket(bucket_name)
    file = bucket.blob(stored_ids)
    while True:

        if file.exists():
            blob = bucket.get_blob(stored_ids)
            downloaded_file = json.loads(blob.download_as_text(encoding="utf-8"))
            break
            
        else:
            add_sources_to_bucket(ids_to_find)
    return downloaded_file
    

def write_to_bucket(json_to_write):
    bucket = storage_client.get_bucket(bucket_name)
    file = stored_ids
    file = bucket.blob(file)
    file.upload_from_string(str(json_to_write))
    while True:
        if file.exists:
            print("file on olemassa")
            break
        else:
            print("fileä ei ole olemassa vielä")
            time.sleep(1)


