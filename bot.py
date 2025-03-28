import logging  
import requests  
import asyncio  
import os  
from aiogram import Bot, Dispatcher  
from aiogram.types import ParseMode  
from apscheduler.schedulers.asyncio import AsyncIOScheduler  

# Токен бота и ID группы  
BOT_TOKEN = os.getenv("BOT_TOKEN")  
CHAT_ID = os.getenv("CHAT_ID")  

# URL API НБУ  
NBU_API_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"  

# Настройка логирования  
logging.basicConfig(level=logging.INFO)  
bot = Bot(token=BOT_TOKEN)  
dp = Dispatcher()  

async def fetch_exchange_rates():  
    try:  
        response = requests.get(NBU_API_URL).json()  
        rates = {item["cc"]: item["rate"] for item in response}  

        text = f"""📢 Курс валют на сегодня:  
🇺🇸 1 USD = {rates.get('USD', 'N/A')} грн  
🇪🇺 1 EUR = {rates.get('EUR', 'N/A')} грн  
🇬🇧 1 GBP = {rates.get('GBP', 'N/A')} грн  
🇵🇱 1 PLN = {rates.get('PLN', 'N/A')} грн"""  

        await bot.send_message(CHAT_ID, text, parse_mode=ParseMode.MARKDOWN)  
    except Exception as e:  
        logging.error(f"Ошибка получения курса валют: {e}")  

# Планировщик задач  
scheduler = AsyncIOScheduler()  
scheduler.add_job(fetch_exchange_rates, "cron", hour=7, minute=0)  

async def main():  
    scheduler.start()  
    await dp.start_polling(bot)  

if name == "main":  
    asyncio.run(main())