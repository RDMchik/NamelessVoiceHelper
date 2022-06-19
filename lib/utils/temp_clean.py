import os


class TempCleaner(object):
    """cleans temp sub directories"""

    TEMP_AUDIO_DIRECTORY = 'temp\\audio'

    def clear() -> None:

        for file in os.listdir(TempCleaner.TEMP_AUDIO_DIRECTORY):
            os.remove(os.path.join(TempCleaner.TEMP_AUDIO_DIRECTORY, file))