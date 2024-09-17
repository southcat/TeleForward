from pyrogram import Client

from config.config import api_id, api_hash, phone_number

Userbot = Client(
    "my_account",
    api_id,
    api_hash,
    phone_number=phone_number,
    device_model='PC')

