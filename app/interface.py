from app.superbot import Button, Keyboard

START_GAME_BUTTON = Button('Начать', '✅', '/start')
SETTINGS_BUTTON = Button('Настройки', '⚙', '/settings')
UNKNOWN_BUTTON = Button('Не знаю', '🤔', '/pass')

RATING_BUTTON = Button('Рейтинг', '🏆', '/rating')
INFO_BUTTON = Button('Справка', '📄', '/info')

WAITING_KEYBOARD = Keyboard('waiting', [[START_GAME_BUTTON, RATING_BUTTON], [SETTINGS_BUTTON, INFO_BUTTON]])
INGAME_KEYBOARD = Keyboard('ingame', [[UNKNOWN_BUTTON, RATING_BUTTON], [SETTINGS_BUTTON, INFO_BUTTON]])
