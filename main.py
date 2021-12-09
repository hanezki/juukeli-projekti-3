import requests
import random
import os
import json

from dotenv import load_dotenv

from random_movie import random_movie_id
from check_where_movie import check_where_movie

load_dotenv()

#API_KEY=os.environ.get('API_KEY')

API_KEY=os.getenv('API_KEY')

# funktio etsii top 250 listasta annettuun pituuteen sopivaa elokuvaa
def check_movie_length(request):

    request_json = request.get_json()
    
    if request.args and 'length' in request.args:
        pituus = int(request.args.get('length'))
    elif request_json and 'length' in request_json:
        pituus = int(request_json['length'])
    else:
        pituus = 120
    
    pituus = 120

    lista = random_movie_id()

    laskuri = 50

    # hakee laskurin määrän verran, löytyykö sopiva elokuvia listasta
    while laskuri > 0:
        leffa_id = random.choice(lista) 
        string = requests.get(f"https://imdb-api.com/en/API/Title/{API_KEY}/{leffa_id}")
        data = string.json()
        
        elokuvan_pituus = int(data["runtimeMins"])
        elokuvan_pituus_tunteina = data["runtimeStr"]

        imdb_rating = data["imDbRating"]

        elokuva_title = data["title"]
        #elokuva_fulltitle = data["fullTitle"]

        elokuva_kuva_url = data["image"]

        #tämä palauttaisi että missä palvelussa olisi saatavilla TAI että onko saatavilla netflixissä
        saatavuus = check_where_movie(leffa_id)

        # jos valittu satunnainen elokuva on pidempi kuin annettu pituus, 
        # laskuria vähennetään ja palataan silmukan alkuun hakemaan uusi satunnainen elokuva
        if pituus < elokuvan_pituus:                    
            laskuri-=1

        # jos valittu satunnainen elokuva mahtuu annetun pituuden välille,
        # tulostetaan elokuvan nimi, pituus ja imdb-pisteet
        elif pituus >= elokuvan_pituus:

            #print(f"Katso elokuva: {elokuva_fulltitle}\nPituus: {elokuvan_pituus} minuuttia, eli {elokuvan_pituus_tunteina}\nIMDB-pisteet: {imdb_rating}/10")

            #print(saatavuus)
            
            elokuva_dict = {"imdb_id": leffa_id, "title": elokuva_title, "lenInMin": elokuvan_pituus, "lenInHrs": elokuvan_pituus_tunteina, "imdb_rating": f"{imdb_rating}/10", "image_url": elokuva_kuva_url, "availibility": saatavuus}

            elokuva_json = json.dumps(elokuva_dict)

            return print(elokuva_json)
    
    # jos laskuri menee nollaan, eikä sopivan pituista elokuvaa löydy    
    return print("Ei löydy noin lyhyttä elokuvaa, mene vaikka ulos!")        


check_movie_length()