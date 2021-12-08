import requests
import random
import os
from flask import jsonify
from dotenv import load_dotenv
from requests.api import request

load_dotenv()
API_KEY=os.getenv("API_KEY")    

# kysyy elokuvan pituuden
def select_length(request):
    request_json = request.get_json() 
    output = request_json['input']   
    print(jsonify(output))
 
# funktio tekee listan top250 elokuvan id:istä   
def random_movie_id(): 
    string = requests.get(f"https://imdb-api.com/en/API/Top250Movies/{API_KEY}")
    data = string.json()
    item_data = data["items"] 
    lista = []

    for i in range(len(item_data)):
        idt = item_data[i]["id"]        
        lista.append(idt)
    return lista

# funktio etsii listasta annettuun pituuteen sopivaa elokuvaa    
def check_movie_length():
    lista = random_movie_id()
    pituus = select_length('12')

    laskuri = 25

    # hakee laskurin määrän verran, löytyykö sopiva elokuvia listasta
    while laskuri > 0:
        leffa_id = random.choice(lista) 
        string = requests.get(f"https://imdb-api.com/en/API/Title/{API_KEY}/{leffa_id}")
        data = string.json()
        
        elokuvan_pituus = int(data["runtimeMins"])   
        elokuvan_pituus_tunteina = data["runtimeStr"]

        imdb_rating = data["imDbRating"]

        elokuva_title = data["title"]
        elokuva_fulltitle = data["fullTitle"]

        # jos valittu satunnainen elokuva on pidempi kuin annettu pituus, 
        # laskuria vähennetään ja palataan silmukan alkuun hakemaan uusi satunnainen elokuva
        if pituus < elokuvan_pituus:                    
            laskuri-=1

        # jos valittu satunnainen elokuva mahtuu annetun pituuden välille,
        # tulostetaan elokuvan nimi, pituus ja imdb-pisteet
        elif pituus >= elokuvan_pituus:
            print(f"Katso elokuva: {elokuva_fulltitle}\nPituus: {elokuvan_pituus} minuuttia, eli {elokuvan_pituus_tunteina}\nIMDB-pisteet: {imdb_rating}/10")
            return elokuva_title
    
    # jos laskuri menee nollaan, eikä sopivan pituista elokuvaa löydy    
    print("Ei löydy noin lyhyttä elokuvaa, mene vaikka ulos!")           

check_movie_length()