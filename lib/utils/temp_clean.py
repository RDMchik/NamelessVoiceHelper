import os


class TempCleaner(object):
    """cleans temp sub directories"""

    TEMP_AUDIO_DIRECTORY = 'temp\\audio'
    TEMP_IMAGES_DIRECTORY = 'temp\\images'

    def clear() -> None:

        for file in os.listdir(TempCleaner.TEMP_AUDIO_DIRECTORY):
            os.remove(os.path.join(TempCleaner.TEMP_AUDIO_DIRECTORY, file))

        for file in os.listdir(TempCleaner.TEMP_IMAGES_DIRECTORY):
            os.remove(os.path.join(TempCleaner.TEMP_IMAGES_DIRECTORY, file))