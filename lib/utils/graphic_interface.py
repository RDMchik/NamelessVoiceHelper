from screeninfo import get_monitors
from PIL import Image

import ctypes, win32con

import os


class GUI(object):
    """project's visuals"""

    RESIZE_AMOUNT = 5

    primary_monitor = None

    for m in get_monitors():
        if m.is_primary:
            primary_monitor = m

    def get_wallpaper_directory() -> str:

        ubuf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0)

        return ubuf.value

    def change_wallpaper(path) -> None:

        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.dirname(os.path.abspath('main.py')) + "\\" + path, 0)

    def draw_image_on_primary_monitor(image_directory: str) -> None:
        
        if not GUI.primary_monitor:
            raise Exception("No primary monitor detected")

        wallpaper_image = Image.open(GUI.get_wallpaper_directory())
        wallpaper_width, wallpaper_height = wallpaper_image.size

        overlay_image = Image.open(image_directory)
        overlay_image = overlay_image.resize((int(wallpaper_width/GUI.RESIZE_AMOUNT), int(wallpaper_width/GUI.RESIZE_AMOUNT)))

        wallpaper_image.paste(overlay_image, (int(wallpaper_width - wallpaper_width/GUI.RESIZE_AMOUNT), int(wallpaper_height - wallpaper_width/GUI.RESIZE_AMOUNT)))

        new_dir = 'temp\\images\\%s' % str(image_directory).split('\\')[-1]

        wallpaper_image.save(new_dir)

        return new_dir



        


        
