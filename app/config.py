import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Определяем окружение
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')

env_file = f"{ENVIRONMENT}.env"
env_file_path = os.path.join(BASE_DIR, 'envs', env_file)
if os.path.exists(env_file_path):
    load_dotenv(env_file_path)

VKONTAKTE_TOKEN = os.environ.get('VKONTAKTE_TOKEN')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

if not VKONTAKTE_TOKEN:
    raise ValueError("VKONTAKTE_TOKEN is not set")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set")

POKEMONS_RANGE = (1, 151)
