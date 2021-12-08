import requests
import random
import os
from dotenv import load_dotenv
from random_movie import random_movie_id
load_dotenv()
API_KEY=os.getenv("API_KEY")

# funktio-kysely, minkä pituisen elokuvan haluaa katsoa
def select_length():
    pituus = 120 #input("Minkä pituisen elokuvan maksimissaan haluat katsoa? Anna vastaus minuutteina: ")
    return pituus    

# funktio etsii top 250 listasta annettuun pituuteen sopivaa elokuvaa
def check_movie_length(request):

    request_json = request.get_json()
    
    if request.args and 'length' in request.args:
        pituus = int(request.args.get('length'))
    elif request_json and 'length' in request_json:
        pituus = int(request_json['length'])
    else:
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
        elokuva_fulltitle = data["fullTitle"]

        elokuva_kuva_url = data["image"]

        # jos valittu satunnainen elokuva on pidempi kuin annettu pituus, 
        # laskuria vähennetään ja palataan silmukan alkuun hakemaan uusi satunnainen elokuva
        if pituus < elokuvan_pituus:                    
            laskuri-=1

        # jos valittu satunnainen elokuva mahtuu annetun pituuden välille,
        # tulostetaan elokuvan nimi, pituus ja imdb-pisteet
        elif pituus >= elokuvan_pituus:

            print(f"Katso elokuva: {elokuva_fulltitle}\nPituus: {elokuvan_pituus} minuuttia, eli {elokuvan_pituus_tunteina}\nIMDB-pisteet: {imdb_rating}/10")
            return f"{{ imdb_id: {leffa_id}, title: {elokuva_title}, lenInMin: {elokuvan_pituus}, lenInHrs: {elokuvan_pituus_tunteina}, imdb_rating: {imdb_rating}/10, image: {elokuva_kuva_url} }} "
    
    # jos laskuri menee nollaan, eikä sopivan pituista elokuvaa löydy    
    return "Ei löydy noin lyhyttä elokuvaa, mene vaikka ulos!"           
