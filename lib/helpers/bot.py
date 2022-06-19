from lib.utils.sound_control import SoundController as sc
from lib.utils.desktop_control import DesktopController as dc

from lib.utils.graphic_interface import GUI
from lib.utils.load_json import JsonLoader
from lib.utils.internet_utils import InternetUtils

from lib.helpers.timer import Timer

import speech_recognition as sr

import webbrowser
import randfacts
import time
import os


# speech recognizer 
r = sr.Recognizer()


class Bot(object):
    """project's main class"""

    SETTINGS_DIRECTORY = 'data\\settings.json'
    TO_REMOVE_FOR_VOICE_MESSAGE_FINISH = [
        'to ', 'your ', 'by ', 'can ', 'you ', 'my ', 'youre ',
        'please ', 'could ', 'maybe ', 'would ', 'for ', 'hey ',
        'this ', 'that ', 'those ', 'these ', 'in ', 'though ',
        'innit ', '"', "(", ")", "-", "_", "=", 
    ]

    def init():
        """bot settings initialization"""

        connected_to_internet = InternetUtils.check_internet_connection()
 
        JsonLoader.add_change_key(Bot.SETTINGS_DIRECTORY, 'connected_to_internet', connected_to_internet)
        JsonLoader.add_change_key(Bot.SETTINGS_DIRECTORY, 'username', os.getlogin())

    def finish_voice_input(text: str) -> str:

        for word in Bot.TO_REMOVE_FOR_VOICE_MESSAGE_FINISH:
            text = text.replace(word, '')

        return text

    def __init__(self, config: any, talking_image_dir: str) -> None:
        
        self.config = config
        self.talking_image_dir = talking_image_dir

        self.next_fact_timer = Timer(config['facts_delay'])
        self.stoped_talking_timer = Timer(0)

        self.__setup()

    def __get_settings(self) -> dict:
        return JsonLoader.load(Bot.SETTINGS_DIRECTORY)

    def __talk(self, text: str) -> None:
        """play something (audio) and send desktop notification"""

        self.stoped_talking_timer = Timer(int(len(text)/46) + 1)
        GUI.change_wallpaper(self.talking_image_dir)

        if self.config['enable_notifications']:
            bot_name = self.__get_settings()['bot_nickname']
            dc.notify(str('%s is saying' % (bot_name if bot_name else 'Nameless')).capitalize(), text)
        
        if not self.config['enable_talking']:
            return

        if not self.__get_settings()['connected_to_internet']:
            dc.notify(str('%s is saying' % (bot_name if bot_name else 'Nameless')).capitalize(), "check internet connection")
            return

        try:
            sc.play_filemp3(sc.create_filemp3_from_text(text))
        except Exception:
            dc.notify(str('%s is saying' % (bot_name if bot_name else 'Nameless')).capitalize(), "an error occurred while talking, check internet connection")

    def __setup(self) -> None:
        """setup at the end of object initialization"""

        bot_name = self.__get_settings()['bot_nickname']
        print("Running bot as %s" % (bot_name if bot_name else 'Nameless'))

        self.__talk("Welcome back %s" % self.__get_settings()['username'])

        if not self.__get_settings()['bot_nickname']:
            self.__talk("I am your nameless voice helper, but if you want to you could give me a name!")

        if not self.__get_settings()['connected_to_internet']:
            self.__talk("You are not connected to internet!")

    def __get_speech_to_text(self) -> str:
        """returns what the user is saying"""

        global r

        try:
            with sr.Microphone() as source:
                
                audio_data = r.record(source, duration=5)
                text = r.recognize_google(audio_data)

                print("%s: %s" % (self.__get_settings()['username'], text))

                return text
        except Exception:

            r = sr.Recognizer()

    def update(self) -> None:
        """check user input and work with it"""

        connected_to_internet = InternetUtils.check_internet_connection()
        JsonLoader.add_change_key(Bot.SETTINGS_DIRECTORY, 'connected_to_internet', connected_to_internet)

        if self.next_fact_timer:
            if self.next_fact_timer():

                self.next_fact_timer = Timer(self.config['facts_delay'])

                if not self.__get_settings()['connected_to_internet']:
                    self.__talk("You are not connected to internet!")

                if self.__get_settings()['facts']:
                    fact = randfacts.get_fact()
                    self.__talk("A random fact! %s" % fact)

        try:
            speech_text = self.__get_speech_to_text()
        except sr.UnknownValueError:
            return
        else:
            if not speech_text:
                return
            speech_text = speech_text.lower()

        if speech_text == '' or speech_text == ' ' or not speech_text:
            return

        if Bot.finish_voice_input(speech_text).startswith('change'):

            if 'name' in speech_text:
                
                try:
                    new_nick = Bot.finish_voice_input(speech_text).split()[2]
                except IndexError:
                    return

                JsonLoader.add_change_key(Bot.SETTINGS_DIRECTORY, 'bot_nickname', new_nick) 

                self.__talk("Successfully changed my nickname to %s" % new_nick)

        if Bot.finish_voice_input(speech_text).startswith('open'):

            to_open = Bot.finish_voice_input(speech_text).split()[1]

            self.__talk("Opening %s in browser" % to_open)

            to_open = 'http://%s.com' % to_open

            print(to_open)
            webbrowser.open(to_open)

        if Bot.finish_voice_input(speech_text).startswith('search'):

            to_open = Bot.finish_voice_input(speech_text).split()
            to_open.pop(0)

            web_link = 'http://google.com/search?q='
            for word in to_open:
                web_link += '%s+' % word

            self.__talk("Searching %s in browser" % Bot.finish_voice_input(speech_text)[6:])

            print(web_link)
            webbrowser.open(web_link)

        if 'shut' in speech_text and 'down' in speech_text:

            self.__talk("Shutting myself down, see you next time!")

            time.sleep(4)

            quit()

        if 'fact' in speech_text:

            if 'enable' in speech_text:

                JsonLoader.add_change_key(Bot.SETTINGS_DIRECTORY, 'facts', True)
                self.__talk('Enabling random facts!')
            
            elif 'disable' in speech_text:

                JsonLoader.add_change_key(Bot.SETTINGS_DIRECTORY, 'facts', False)
                self.__talk('Disabling random facts!')

            elif 'say' in speech_text or 'tell' in speech_text:

                self.next_fact_timer = Timer(self.config['facts_delay'])

                if not self.__get_settings()['connected_to_internet']:
                    self.__talk("You are not connected to internet!")

                if self.__get_settings()['facts']:
                    fact = randfacts.get_fact()
                    self.__talk("A random fact! %s" % fact)

        if 'remind' in speech_text:

            if 'name' in speech_text:

                bot_name = self.__get_settings()['bot_nickname']

                self.__talk("My current nickname is %s" % bot_name)

