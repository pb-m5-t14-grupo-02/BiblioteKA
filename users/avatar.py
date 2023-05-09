from random import choice
import os
import dotenv

pixel_art_lits = [
    "Max_ctzin7",
    "Oreo_bglowz",
    "Bailey_ofiegc",
    "Misty_pzvdaz",
    "Molly_ot1egr",
    "Scooter_v0dcjl",
    "Garfield_sqmmim",
    "Chester_hifwo7",
    "Kiki_guacg9",
    "Gracie_vmx7fg",
    "Daisy_zsx4gp",
    "George_uhyhyt"
]

dotenv.load_dotenv()
BASE_URL_AVATAR = os.getenv("CLOUDINARY_URL") + "/defaults/avatar/" 


def get_random_avatar() -> str:
    return BASE_URL_AVATAR + choice(pixel_art_lits) + ".svg"
