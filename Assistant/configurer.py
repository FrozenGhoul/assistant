from types import MappingProxyType as dictproxy
from json import JSONDecodeError, load as load_json
from os.path import split

jsonerr = "Invalid JSON syntax on {} specification file."

def _load_json_file(file):
    with open(file) as source:
        try:
            return dictproxy(load_json(source))
        except JSONDecodeError as error:
            raise SyntaxError(jsonerr.format(split(file)[-1])) from error

def load_config(file="config.json"):
    return _load_json_file(file)

def load_modules(file="modules.json"):
    return _load_json_file(file)
