from lib.utils.load_json import JsonLoader
from lib.utils.temp_clean import TempCleaner
from lib.utils.graphic_interface import GUI

from lib.helpers.bot import Bot

import ctypes
import os


TempCleaner.clear()
Bot.init()

config = JsonLoader.load('config.json')

talkingImage = 'static\\images\\bottalk.jpg'
notTalkingImage = 'static\\images\\botnottalk.jpg'

talkingImageDir = GUI.draw_image_on_primary_monitor(talkingImage)
notTalkingImageDir = GUI.draw_image_on_primary_monitor(notTalkingImage)

bot = Bot(config, talkingImageDir)

GUI.draw_image_on_primary_monitor(notTalkingImage)

while True:

    try:
        bot.update()
    except Exception as err:
        print(err)

    if bot.stoped_talking_timer():
        GUI.change_wallpaper(notTalkingImageDir)
    
    
