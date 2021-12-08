import requests
#import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

#suoritetaan kerran
def random_movie_id():
    #payload = {}
    #headers= {}

    #alla oleva kommentoitu pois. Käytetään ympäristömuuttujia cloud functionissa
    API_KEY=os.getenv("API_KEY")
    
    #API_KEY=os.environ.get('API_KEY')

    string = requests.get(f"https://imdb-api.com/en/API/Top250Movies/{API_KEY}")

    data = string.json()

    item_data = data["items"] 

    lista = []

    for i in range(len(item_data)):
        idt = item_data[i]["title"]
        
        lista.append(idt)

    leffa = random.choice(lista)
    print(leffa)
    return leffa

#testiä varten:
if __name__=="__main__":
    random_movie_id()