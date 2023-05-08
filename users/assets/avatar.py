from random import choice
import dotenv
import os

pixel_art_lits = [
    "Max",
    "Oreo",
    "Bailey",
    "Misty",
    "Molly",
    "Scooter",
    "Garfield",
    "Chester",
    "Kiki",
    "Gracie",
    "Daisy",
    "George"
]

dotenv.load_dotenv()
BASE_URL = "https://api.dicebear.com/6.x/pixel-art/svg?seed="

def get_random_avatar():
    return BASE_URL + choice(pixel_art_lits)

import requests

urls = pixel_art_lits

for url in urls:
    response = requests.get(BASE_URL + url)
    content = response.content
    print(content)
    with open(url + '.svg', 'wb') as f:
        f.write(content)
