from dotenv import dotenv_values
from aiogram import Bot

ENV = dotenv_values(".env")

TOKEN = ENV["TOKEN"]
ADMIN = ENV["ADMIN"]
GROUP_ID = ENV["GROUP_ID"]

bot = Bot(token=TOKEN)
