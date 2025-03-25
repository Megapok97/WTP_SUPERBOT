from datetime import datetime

from app import config, interface, pokemons
from app.database import Game
from app.events import Event
from app.logger import logger
from app.superbot import SkipHandler
from app.superbot.superbot import Superbot

superbot = Superbot({
    'vkontakte': {'token': config.VKONTAKTE_TOKEN},
    'telegram': {'token': config.TELEGRAM_TOKEN}
}, 10, logger, Event)

pokemons_data_cache = {}


def start_game(event: Event):
    if event.account.keyboard not in [None, interface.WAITING_KEYBOARD.name]:
        raise SkipHandler()

    pokemon_data = pokemons.generate_pokemon(*config.POKEMONS_RANGE)
    pokemons_data_cache[f'{event.account.platform}.{event.account.platform_id}'] = pokemon_data

    Game.create(
        account=event.account, status='active',
        pokemon_number=pokemon_data['number'],
        start_date=datetime.now()
    )

    event.account.update_one(keyboard=interface.INGAME_KEYBOARD.name)
    event.reply('Это что за покемон?', [pokemon_data['image_secret']], interface.INGAME_KEYBOARD)


def settings(event: Event):
    event.reply('(ﾉ>ω<)ﾉ :｡･:*:･ﾟ’★,｡･:*:･ﾟ’☆')


def process_answer(event: Event):
    if event.account.keyboard != interface.INGAME_KEYBOARD.name:
        raise SkipHandler()

    try:
        pokemon_data = pokemons_data_cache.pop(f'{event.account.platform}.{event.account.platform_id}')
    except KeyError:
        pokemon_data = pokemons.get_pokemon_data(event.account.pokemon_number)

    pokemon_name, pokemon_image = pokemon_data['name_ru'], pokemon_data['image']
    is_answer_correct = event.message.lower() in [s.lower() for s in [pokemon_data['name_en'], pokemon_data['name_ru']]]

    game_status = 'completed' if is_answer_correct else 'failed'
    event.game.update_one(status=game_status, end_date=datetime.now(), answer=event.message)
    event.account.update_one(keyboard=interface.WAITING_KEYBOARD.name)

    message = f'Верно, это был {pokemon_name}!' if is_answer_correct else f'Нет, это был {pokemon_name}!'
    event.reply(message, [pokemon_image], interface.WAITING_KEYBOARD)


def show_answer(event: Event):
    if event.account.keyboard != interface.INGAME_KEYBOARD.name:
        raise SkipHandler()

    try:
        pokemon_data = pokemons_data_cache.pop(f'{event.account.platform}.{event.account.platform_id}')
    except KeyError:
        pokemon_data = pokemons.get_pokemon_data(event.game.pokemon_number)

    event.game.update_one(status='failed', end_date=datetime.now())
    event.account.update_one(keyboard=interface.WAITING_KEYBOARD.name)

    pokemon_name, pokemon_image = pokemon_data['name_ru'], pokemon_data['image']
    event.reply(f'Это был {pokemon_name}!', [pokemon_image], interface.WAITING_KEYBOARD)


def show_rating(event: Event):
    games_query = event.account.games.select()

    total_games = games_query.where(Game.status != 'active').count()
    won_games = games_query.where(Game.status == 'completed').count()

    event.reply(f'Верно угадано: {won_games}\nВсего было сыграно: {total_games}')


def show_info(event: Event):
    event.reply(' '.join([
        'Ваша задача угадать имя покемона. Ответы',
        'принимаются как на английском языке, так и на русском!'
    ]))


superbot.register_handler(start_game, None, interface.WAITING_KEYBOARD.messages - interface.START_GAME_BUTTON.messages)
superbot.register_handler(settings, interface.SETTINGS_BUTTON.messages)

superbot.register_handler(process_answer, message_ne=interface.INGAME_KEYBOARD.messages)
superbot.register_handler(show_answer, interface.UNKNOWN_BUTTON.messages)

superbot.register_handler(show_rating, interface.RATING_BUTTON.messages)
superbot.register_handler(show_info, interface.INFO_BUTTON.messages)
