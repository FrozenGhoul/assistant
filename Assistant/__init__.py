from .audio_text_manager import AudioTextManager
from .event_dispatcher import EventDispatcher
from .module_loader import run_module
from .audio_manager import get_text_from_speech
from .configurer import load_config
from .updater import check_for_updates
from .sounder import probability as prob
from .speaker import speak
from types import MappingProxyType as dictproxy
import speech_recognition as sr

__all__ = ["run"]

CONFIG = load_config()

def sleep(interface, text):
    interface.events.add("sleep")
    interface.events.trigger("sleep")
    return CONFIG["sleep_msg"]

def quit(interface, text):
    interface.events.add("quit")
    interface.events.trigger("quit")
    return CONFIG["quit_msg"]

PRIMITIVES = dictproxy({tuple(CONFIG["sleep_cmd"].split()): sleep,
                        tuple(CONFIG["quit_cmd" ].split()): quit})

def run(threshold=0.5):
    running = awake = True
    events = EventDispatcher()
    recog = sr.Recognizer()
    interf = AudioTextManager(events, recog)
    if CONFIG["check_for_updates"]:
        check_for_updates(CONFIG["version"])
    with sr.Microphone() as source:
        while running:
            if not awake:
                text = get_text_from_speech(recognizer, source, CONFIG["stt_engine"])
                if not text:
                    return False
                command_list = CONFIG["wake_up_cmd"].lower().split()
                user_list = text.split()
                chances = prob(command_list, user_list)["chances"][0]
                awake = chances > treshold
            while awake:
                text = get_text_from_speech(recog, source, CONFIG["stt_engine"])
                if not text:
                    speak(CONFIG["listened_error_text"])
                    continue
                utxt = text.split()
                pbs = {prob(cmd, utxt)["chances"][0]: cmd for cmd in PRIMITIVES}
                if max(pbs) > threshold:
                    result = PRIMITIVES[pbs[max(pbs)]](interf, text)
                else:
                    result = run_module(interf, text)
                if result is None:
                    speak(CONFIG["listened_error_text"])
                    continue
                speak(result)
                if events.should_quit:
                    running = awake = False
                if events.sleep_status:
                    awake = False

if __name__ == "__main__":
    run()
    #TODO: fix sounder._pick so that it supports dictionaries