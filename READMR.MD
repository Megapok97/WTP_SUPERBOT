![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

![Blabla](https://archives.bulbagarden.net/media/upload/thumb/8/84/WTP_EP001_before.png/300px-WTP_EP001_before.png)
# 💡 Идея 
Проект "Who’s That Pokémon?" вдохновлён моей любовью к покемонам и написан в 2021 году. Я решил разработать бота, способного одновременно работать с Telegram и ВКонтакте через универсальный интерфейс, чтобы исследовать возможности интеграции с несколькими платформами.
# Who’s That Pokémon? 🐾

**Who’s That Pokémon?** — это интерактивный бот для Telegram и ВКонтакте, который позволяет играть в игру "Кто этот покемон?". Бот показывает затемнённое изображение покемона, а задача игрока — угадать его имя на русском или английском языке.


## 🛠️ Технологии

- `Python 3.11`
- `threading` (для многопоточности)
- `requests` (для HTTP-запросов)
- `vk-api` (для ВКонтакте)
- `pyTelegramBotAPI` (для Telegram)
- `peewee` (ORM для SQLite)
- `Pillow` (обработка изображений)
- `Docker` 

## 🏗️ О ядре

Ядро проекта, реализованное в модуле `app.superbot`. Оно позволяет одновременно обрабатывать сообщения из Telegram и ВКонтакте, используя единый интерфейс для обработки событий. Основные преимущества:
- **Универсальность**: один код для двух платформ.
- **Многопоточность**: интеграции (VK, Telegram) и обработка событий работают параллельно.

## 📦 Развёртывание в Docker

### Требования

- Docker и Docker Compose.
- Токены для ВКонтакте и Telegram.

### 1. Клонируй репозиторий

```sh
git clone https://github.com/<your-username>/wtp-bot.git
cd wtp-bot
```

### 2. Создай файл .env в корне проекта

```sh
VKONTAKTE_TOKEN=your_vk_token
TELEGRAM_TOKEN=your_telegram_token
```

### 4. Создай папку data
```sh
mkdir -p data
```

### 5. Запусти контейнер
```sh
docker-compose up --build
```
