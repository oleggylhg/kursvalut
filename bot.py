import requests
import telebot
import logging
import time
from datetime import datetime

# Настройки
BOT_TOKEN = "7619596787:AAFZuMNKjBFSY8fnKxY1ckIfB7kEdPH2GnI"
CHAT_ID = "-1001521182831"
PRIVAT_API_URL = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=5"

# Логирование
logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)

def fetch_exchange_rates():
    """Получает курс валют (покупка и продажа) и отправляет в Telegram"""
    try:
        response = requests.get(PRIVAT_API_URL).json()
        rates = {item["ccy"]: item for item in response}

        text = f"""📢 Курс валют (ПриватБанк) на сегодня:  
🇺🇸 USD  
➖ Покупка: {rates['USD']['buy']} грн  
➕ Продажа: {rates['USD']['sale']} грн  

🇪🇺 EUR  
➖ Покупка: {rates['EUR']['buy']} грн  
➕ Продажа: {rates['EUR']['sale']} грн  

🇵🇱 PLN  
➖ Покупка: {rates['PLN']['buy']} грн  
➕ Продажа: {rates['PLN']['sale']} грн"""

        bot.send_message(CHAT_ID, text, parse_mode="Markdown")
        logging.info("Курс валют отправлен")
    except Exception as e:
        logging.error(f"Ошибка получения курса: {e}")

# Запуск отправки сообщений по расписанию
while True:
    now = datetime.now()
    if now.hour == 7 and now.minute == 0:
        fetch_exchange_rates()
        time.sleep(60)  # Ждём 1 минуту, чтобы не отправлять несколько раз
    time.sleep(30)  # Проверяем время каждые 30 секунд
