import os
from unittest import TestCase, skip

from PIL.Image import Image

from app import pokemons


class TempFolderMixin:
    @classmethod
    def setUpClass(cls):
        cls.temp_folder_path = os.path.join(os.path.dirname(__file__), 'temp')

    def clear_temp_folder(self):
        pass
        # shutil.rmtree(self.temp_folder_path)
        # os.mkdir(self.temp_folder_path)


class PokemonsTestCase(TempFolderMixin, TestCase):
    def test_generate_pokemon_number(self):
        pokemon_number = pokemons.generate_pokemon_number(1, 151)
        self.assertIsInstance(pokemon_number, int)

        for _ in range(1000):
            pokemon_number = pokemons.generate_pokemon_number(1, 151)

            self.assertGreaterEqual(pokemon_number, 1)
            self.assertLessEqual(pokemon_number, 151)

        for _ in range(1000):
            pokemon_number = pokemons.generate_pokemon_number(200, 300)

            self.assertGreaterEqual(pokemon_number, 200)
            self.assertLessEqual(pokemon_number, 300)

    def test_format_pokemon_number(self):
        formatted_number = pokemons.format_pokemon_number(1)
        self.assertEqual(formatted_number, '001')

        formatted_number = pokemons.format_pokemon_number(11)
        self.assertEqual(formatted_number, '011')

        formatted_number = pokemons.format_pokemon_number(151)
        self.assertEqual(formatted_number, '151')

    def test_get_pokemon_names(self):
        pokemon_names = pokemons.get_pokemon_names('001')

        self.assertIsInstance(pokemon_names, tuple)
        self.assertIsInstance(pokemon_names[0], str)
        self.assertIsInstance(pokemon_names[1], str)

        en_name, ru_name = pokemons.get_pokemon_names('001')

        self.assertEqual(en_name, 'Bulbasaur')
        self.assertEqual(ru_name, 'Бульбазавр')

        en_name, ru_name = pokemons.get_pokemon_names('453')

        self.assertEqual(en_name, 'Croagunk')
        self.assertEqual(ru_name, 'Кроганк')

    @skip('Для ручного тестирования')
    def test_get_pokemon_image(self):
        self.clear_temp_folder()

        for pokemon_number in [1, 151, 300]:
            number_formatted = pokemons.format_pokemon_number(pokemon_number)
            file_path = os.path.join(self.temp_folder_path, f'{number_formatted}.png')

            image = pokemons.get_pokemon_image(pokemon_number)
            image.save(file_path, format='PNG')

    @skip('Для ручного тестирования')
    def test_generate_pokemon_background_image(self):
        self.clear_temp_folder()

        for pokemon_number in [1, 151, 300]:
            number_formatted = pokemons.format_pokemon_number(pokemon_number)
            pokemon_image = pokemons.get_pokemon_image(pokemon_number)

            file_path = os.path.join(self.temp_folder_path, f'{number_formatted}_bg.png')
            image = pokemons.generate_pokemon_background_image(pokemon_image)
            image.save(file_path, format='PNG')

            file_path = os.path.join(self.temp_folder_path, f'{number_formatted}_bgs.png')
            image = pokemons.generate_pokemon_background_image(pokemon_image, True)
            image.save(file_path, format='PNG')

    def test_get_pokemon_data(self):
        pokemon_data = pokemons.get_pokemon_data(1)
        self.assertIsInstance(pokemon_data, dict)

        self.assertEqual(pokemon_data['number'], 1)
        self.assertEqual(pokemon_data['number_formatted'], '001')

        self.assertEqual(pokemon_data['name_en'], 'Bulbasaur')
        self.assertEqual(pokemon_data['name_ru'], 'Бульбазавр')

        self.assertIsInstance(pokemon_data['image'], Image)
        self.assertIsInstance(pokemon_data['image_secret'], Image)

    def test_generate_pokemon(self):
        for _ in range(3):
            pokemon_data = pokemons.generate_pokemon(1, 500)
            self.assertIsInstance(pokemon_data, dict)

            self.assertIsInstance(pokemon_data['number'], int)
            self.assertIsInstance(pokemon_data['number_formatted'], str)

            self.assertIsInstance(pokemon_data['name_en'], str)
            self.assertIsInstance(pokemon_data['name_ru'], str)

            self.assertIsInstance(pokemon_data['image'], Image)
            self.assertIsInstance(pokemon_data['image_secret'], Image)
