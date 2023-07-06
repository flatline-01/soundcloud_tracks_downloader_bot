import os
import re
import asyncio
import requests
from telebot.async_telebot import AsyncTeleBot
from sclib.asyncio import SoundcloudAPI, Track
from telebot.types import InputFile

token = os.getenv('TOKEN')
bot = AsyncTeleBot(token=token)


@bot.message_handler(commands=['start'])
async def greet(message):
    await bot.send_message(message.chat.id, 'Hey there. To download some track just enter its url.')


@bot.message_handler(func=lambda m: True)
async def download(message):
    chat_id = message.chat.id
    track_url = message.text

    pattern_web = re.compile("https://soundcloud.com/[-a-zA-Z0-9@:%._+~#=]{1,256}/[-a-zA-Z0-9@:%._+~#=]{1,256}+$")
    pattern_app = re.compile("https://soundcloud.app.goo.gl/[-a-zA-Z0-9@:%._+~#=]{5}+$")

    if pattern_web.match(track_url) or pattern_app.match(track_url):
        if pattern_app.match(track_url):
            track_url = requests.get(track_url).url
        await bot.send_message(chat_id, 'Wait a minute please.')
        track_path = await download_track(track_url)
        await bot.send_audio(chat_id, InputFile(track_path))
        os.remove(track_path)
    else:
        await bot.send_message(chat_id, 'Sorry, but I can\'t understand you. Send me a track url.')


async def download_track(url):
    api = SoundcloudAPI()
    track = await api.resolve(url)
    assert type(track) is Track
    track_path = f'tracks/{track.title}.mp3'
    with open(track_path, 'wb+') as file:
        await track.write_mp3_to(file)
    return track_path


asyncio.run(bot.infinity_polling())
