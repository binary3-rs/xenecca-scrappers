from os import remove

from utils.common import log


def delete_file(file_path):
    try:
        remove(file_path)
    except FileNotFoundError:
        log(f"File with the filepath = {file_path} cannot be found!", "error")