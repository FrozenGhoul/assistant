from .module_loader import sort_text, learn_text, snake_case
from .audio_manager import get_text_from_speech
from .configurer import load_config
from speech_recognition import Recognizer
from .speaker import speak

CONFIG = load_config()

class AudioTextManager():
    def __init__(self, events, recognizer):
        self.events = events
        self.recog = recognizer

    def listen(self):
        with sr.Microphone() as source:
            return get_text_from_speech(self.recog, source)

    def say(self, speech):
        speak(speech)

    def understand(self, modules, raw_text, explicit=False):
        subwords, keywords = sort_text(raw_text, explicit)
        module_info = learn_text(keywords, modules)
        print(module_info)
        return snake_case(module_info[0].split("@")[1])
