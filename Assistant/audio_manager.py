from speech_recognition import UnknownValueError, RequestError
from .speaker import speak_from_os, speak_from_pygame
from .configurer import load_config
from .speaker import play_sound

CONFIG = load_config()

errstr = ("Invalid value for '{}' configuration parameter")

ENGINES = {"ibm": "recognize_ibm",
           "houndify": "recognize_houndify",
           "bing": "recognize_bing",
           "wit": "recognize_wit",
           "google_cloud": "recognize_google_cloud",
           "google": "recognize_google",
           "sphinx": "recognize_sphinx"}

CREDENTIALS = {"sphinx": None,
               "google": {"key": CONFIG["google_speech_api"]},
               "google_cloud": {"google_cloud_speech_credentials": \
                                CONFIG['google_cloud_speech_api']},
               "wit": {"wit_ai_key": CONFIG['wit.ai_speech_api']},
               "bing": {"bing_key": CONFIG['bing_speech_api']},
               "houndify":{"houndify_client_key": CONFIG['houndify_client_key'],
                           "houndify_client_id": CONFIG['houndify_client_id']},
               "ibm": {"ibm_username": CONFIG['ibm_username'],
                       "ibm_password": CONFIG['ibm_password']}}

def get_text_from_speech(recognizer, source, signals=True, engine=CONFIG["stt_engine"]):
    print(CONFIG['command_prompt'])
    recognizer.adjust_for_ambient_noise(source, duration=1)
    if signals:
        play_sound(CONFIG['beep_start'])
    try:
        audio = recognizer.listen(source)
    except AssertionError as e:
        print(CONFIG['listened_error_text'])
        return False
    else:
        print(CONFIG['listened_success_text'])
    finally:
        if signals:
            play_sound(CONFIG['beep_end'])
    if engine not in ENGINES:
        raise Exception(errstr.format("stt_engine")) 
    login = CREDENTIALS[engine]
    try:
        text = getattr(recognizer, ENGINES[engine])(audio, **login)
        print("{} thinks you said: '{}'".format(engine.title(), text))
        return text
    except UnknownValueError:
        print("{} could not understand audio.".format(engine.title()))
    except RequestError as error:
        print(error)
    return False
