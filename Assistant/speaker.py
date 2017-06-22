from .configurer import load_config
from eyed3 import load as load_meta
from platform import system
from pygame import mixer
from time import sleep
from gtts import gTTS
import os

CONFIG = load_config()

errstr = ("Invalid value for '{}' configuration parameter")

AUDIO_OUT = {"os": "speak_from_os", "mixer": "speak_from_pygame"}

def speak_from_os(path):
    plat = system()
    try:
        if plat == "Linux":
            os.system("xdg-open " + path)
        elif plat == "Darwin":
            os.system("afplay " + path)
        elif plat == "Windows":
            os.startfile(path)
        else:
            raise RuntimeError("Unsupported OS: " + plat)
    except OSError as error:
        raise RuntimeError("Couldn't find default mp3 player.") from error
    sleep(load_meta(path).info.time_secs + 2)

def speak_from_pygame(path):
    duration = load_meta(path).info.time_secs + 2
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()
    sleep(duration)
    mixer.quit()

def speak(text, lang="en"):
    if CONFIG['tts_engine'] != "google":
        raise ValueError(errstr.format("tts_engine"))
    gTTS(text, lang=lang).save(CONFIG['speech_filename'])
    play_sound(CONFIG['speech_filename'])

def play_sound(filepath):
    if CONFIG['tts_player'] not in AUDIO_OUT:
        raise ValueError(errstr.format("tts_player"))
    globals()[AUDIO_OUT[CONFIG["tts_player"]]](filepath)
