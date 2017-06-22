from .speaker import speak
from requests.exceptions import RequestException
import requests

UPDATE_URL = None
UPDATE_FAIL = "Couldn't access stephanie's version update information."
UPDATE_FOUND = "A new version of this software is available. Check the link out for more information."
    
def check_for_updates(version):
    try:
        data = requests.get(UPDATE_URL).json()
    except RequestException as error:
        raise RuntimeError(UPDATE_FAIL) from error
    if str(version) != str(data['version']):
        speak(UPDATE_FOUND)
        print(UPDATE_URL)
