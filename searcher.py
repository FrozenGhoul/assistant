from mimetypes import guess_type
from tempfile import TemporaryFile
from fire import Fire
from sys import argv
from os import scandir

def find_str(pattern, path=".", recursive=True, showline=False):
    for entry in scandir(path):
        if entry.is_file():
            file_type, encoding = guess_type(entry.path)
            if file_type is not None and file_type.startswith("text"):
                with open(entry.path) as file:
                    for i, line in enumerate(file):
                        if pattern in line:
                            yield f"Found match on line {i+1:0=3d} of {entry.name}"
                            if showline: yield line + "\n"
        elif entry.is_dir() and recursive:
            for match in find_str(pattern, entry.path, recursive):
                yield match

def edit_line(pattern, new, path=".", recursive=False):
    for entry in scandir(path):
        if entry.is_file() and not __file__.endswith(entry.path):
            file_type, encoding = guess_type(entry.path)
            if file_type is not None and file_type.startswith("text"):
                with TemporaryFile(mode="w+") as tmp:
                    with open(entry.path) as src:
                        for i, line in enumerate(src):
                            if pattern in line:
                                tmp.write(line.replace(pattern, new))
                                yield f"Edited line {i+1:0=3d} of {entry.name}"
                            else:
                                tmp.write(line)
                    tmp.seek(0)
                    with open(entry.path, "w") as dst:
                        for line in tmp:
                            dst.write(line)
        elif entry.is_dir() and recursive:
            for match in find_str(pattern, entry.path, recursive):
                yield match

class DemoWrapper():
    @staticmethod
    def find_str(pattern, path=".", recursive=True, showline=False):
        for match in find_str(pattern, path, recursive, showline):
            print(match)
    @staticmethod
    def edit_line(pattern, new="", path=".", recursive=False):
        for match in edit_line(pattern, new=new, path=path, recursive=recursive):
            print(match)
            
if __name__ == "__main__":
    Fire(DemoWrapper)