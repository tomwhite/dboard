import os


def open_file(filename, mode="r"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return open(filename, mode)
