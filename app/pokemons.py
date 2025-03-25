import json
import os
import random

import requests
from PIL import Image


def generate_pokemon_number(number_from: int, number_to: int) -> int:
    return random.randint(number_from, number_to)


def format_pokemon_number(pokemon_number: int) -> str:
    if pokemon_number <= 9:
        pokemon_number = '00' + str(pokemon_number)
    elif pokemon_number <= 99:
        pokemon_number = '0' + str(pokemon_number)
    else:
        pokemon_number = str(pokemon_number)
    return pokemon_number


def get_pokemon_names(pokemon_number_formatted: str) -> tuple[str, str]:
    file_path = os.path.join(os.path.dirname(__file__), '../data/pokemon-names.json')

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return tuple(data[pokemon_number_formatted])


def get_pokemon_image(pokemon_number: int) -> Image:
    pokemon_number = format_pokemon_number(pokemon_number)
    url = f'https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{pokemon_number}.png'
    return Image.open(requests.get(url, stream=True).raw)


def generate_pokemon_background_image(pokemon_image: Image, is_secret: bool = False) -> Image:
    file_path = os.path.join(os.path.dirname(__file__), '../assets/background.png')
    background_image = Image.open(file_path)

    if is_secret:
        pixels_data = pokemon_image.load()
        for y in range(pokemon_image.size[1]):
            for x in range(pokemon_image.size[0]):
                if pixels_data[x, y][3] != 0:
                    pixels_data[x, y] = (0, 0, 0, 255)

    pokemon_image = pokemon_image.resize((800, 800), Image.LANCZOS)
    background_image.paste(pokemon_image, (160, 140), pokemon_image)

    return background_image


def get_pokemon_data(pokemon_number: int) -> dict:
    number_formatted = format_pokemon_number(pokemon_number)
    name_en, name_ru = get_pokemon_names(number_formatted)
    image = get_pokemon_image(pokemon_number)

    return {
        'number': pokemon_number,
        'number_formatted': number_formatted,
        'name_en': name_en,
        'name_ru': name_ru,
        'image': generate_pokemon_background_image(image),
        'image_secret': generate_pokemon_background_image(image, True),
    }


def generate_pokemon(number_from: int, number_to: int) -> dict:
    return get_pokemon_data(generate_pokemon_number(number_from, number_to))
