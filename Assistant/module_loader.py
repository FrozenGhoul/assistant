from .configurer import load_config, load_modules
from .sounder import search, RESERVED_WORDS
from metaphone import doublemetaphone as dm
from difflib import SequenceMatcher as sm

import importlib.util as iu
import pip
import re
import os

CONFIG = load_config()
MODULES = load_modules()

loaderrstr = ("Couldn't load module: {}. Please check if its specifications on "
              "the modules configuration file obey the module guidelines.")
execerrstr = ("Couldn't run loaded module: {}. Please check if its "
              "implementation is obeys the module guidelines.")

def snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def run_module(ATManager, raw_text):
    subwords, keywords = sort_text(raw_text)
    class_at_method, module_keywords = learn_text(keywords)
    className, methodName = class_at_method.split("@")
    function_name = snake_case(methodName)
    module_name = snake_case(className)
    module_path = os.path.join(CONFIG["modules_folder"], module_name + ".py")
    spec = iu.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise Exception(loaderrstr.format(module_name))
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)
    args = (module_keywords, raw_text, subwords, keywords, ATManager, CONFIG)
    try:
        return getattr(getattr(module, className)(*args), function_name)()
    except AttributeError as error:
        raise RuntimeError(execerrstr.format(module_name)) from error
    except ImportError as error:
        print(f"Couldn't find dependency module: {error.name}. Perhaps it's "
               "not installed... would you like me to try to install it now?")
        if input("y/n").startswith("y"):
            if not pip.main(["install", error.name]):
                return f"Successfully installed module: {error.name}."
            raise RuntimeError("Couldn't install dependency.")
        raise

def sort_text(raw_text):
    raw_text_array = raw_text.lower().split()
    assistant_name = CONFIG['assistant_name']
    meta_name = dm(assistant_name)[0]
    for index, raw_text in enumerate(raw_text_array):
        meta_text = dm(raw_text)[0]
        chances = sm(None, meta_name, meta_text).ratio()
        if chances > 0.7:
            raw_text_array = raw_text_array[index+1:]
            break
    key_words = raw_text_array.copy()
    sub_words = []
    for index, raw_text in enumerate(raw_text_array):
        if raw_text in RESERVED_WORDS:
            sub_words.append(raw_text)
            key_words.remove(raw_text)
    return sub_words, key_words

def learn_text(keywords, modules=MODULES):
    print(keywords)
    index = search(keywords, modules.values())
    name = tuple(modules)[index]
    print(f"Loading {name} module")
    return name, modules[name]
