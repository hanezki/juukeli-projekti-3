import requests
import random
#import json

#suoritetaan kerran
def random_movie_id():
    #payload = {}
    #headers= {}

    API_KEY="ei-api-keyta-githubiin"

    string = requests.get(f"https://imdb-api.com/en/API/Top250Movies/{API_KEY}")

    data = string.json()

    item_data = data["items"]

    lista = []

    for i in range(len(item_data)):
        idt = item_data[i]["id"]
        
        lista.append(idt)

    leffa = random.choice(lista)

    return leffa