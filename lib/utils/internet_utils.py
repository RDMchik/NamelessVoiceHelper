import urllib.request


class InternetUtils(object):
    """some of internet utils used"""

    CHECK_HOST = 'http://google.com'

    def check_internet_connection() -> bool:

        try:
            urllib.request.urlopen(InternetUtils.CHECK_HOST) 
        except:
            return False

        return True