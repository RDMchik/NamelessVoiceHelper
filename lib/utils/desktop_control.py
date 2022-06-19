from plyer import notification


class DesktopController(object):

    BOT_PROFILE_PICTURE_DIRECTORY = 'static\\images\\botpfp.ico'

    def notify(title: str, message: str) -> None:
        """send a desktop notification"""

        notification.notify(
            title=title,
            message=message,
            app_icon=DesktopController.BOT_PROFILE_PICTURE_DIRECTORY,
            timeout=10,
        )