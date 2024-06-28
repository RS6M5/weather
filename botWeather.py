import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from googletrans import Translator
import os

API_TOKEN = '7234232452:AAHzYMJe7GtlBYUa0Z4q_b8p3VY5tpwMPzg'
WEATHER_API_KEY = 'ваш_ключ_погоды'
CITY_NAME = 'Moscow'
URL = f'http://api.openweathermap.org/data/2.5/weather?id=524901&appid={WEATHER_API_KEY}'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота, диспетчера и роутера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

# Создание папки img, если не существует
if not os.path.exists('img'):
    os.makedirs('img')

# Инициализация переводчика
translator = Translator()

# Команда /start
@router.message(CommandStart())
async def send_welcome(message: Message):
    await message.reply("Добро пожаловать! Я бот, который предоставляет прогноз погоды и переводит текст на английский.\n"
                        "Используйте /help для получения списка доступных команд.")

# Команда /help
@router.message(Command(commands=['help']))
async def send_help(message: Message):
    await message.reply("/start - Начать работу с ботом\n"
                        "/help - Получить список доступных команд\n"
                        "/weather - Получить прогноз погоды")

# Команда /weather
@router.message(Command(commands=['weather']))
async def send_weather(message: Message):
    weather_data = get_weather(CITY_NAME, WEATHER_API_KEY)
    if weather_data:
        response = (f"Прогноз погоды для {CITY_NAME}:\n"
                    f"Температура: {weather_data['temp']}°C\n"
                    f"Описание: {weather_data['description'].capitalize()}")
        await message.reply(response)
    else:
        await message.reply("Не удалось получить данные о погоде. Попробуйте позже.")

def get_weather(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temp": data['main']['temp'],
            "description": data['weather'][0]['description']
        }
        return weather
    else:
        return None

# Обработчик текстовых сообщений для перевода на английский
# @router.message()
# async def translate_to_english(message: Message):
#     translated = translator.translate(message.text, src='auto', dest='en')
#     await message.reply(f"Перевод на английский: {translated.text}")
#
# async def main():
#     dp.include_router(router)
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)
#
# if __name__ == '__main__':
#     asyncio.run(main())