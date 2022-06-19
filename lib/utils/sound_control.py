from playsound import playsound
from gtts import gTTS

import random


class SoundController(object):
    """class to control sounds"""

    def create_filemp3_from_text(text: str) -> str:
        """creates a new mp3 file in temp/audio
        using gTTS from string (removed on restart)"""

        audio_id = str(random.randint(1000000, 9999999))
 
        tts = gTTS(text)
        tts.save('temp\\audio\\%s.mp3' % audio_id)

        return audio_id

    def play_filemp3(audio_id: str) -> None:

        filename = 'temp\\audio\\%s.mp3' % audio_id

        playsound(filename)
