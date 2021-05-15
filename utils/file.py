from os import remove, path, makedirs
from pickle import load, dump
from utils.common import log


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.readlines()


def write_to_file(filepath, data):
    with open(filepath, "w") as file:
        for line in data:
            file.write(line)


def delete_file(file_path):
    try:
        remove(file_path)
    except FileNotFoundError:
        log(f"File with the filepath = {file_path} cannot be found!", "error")


def filepath_exists(filepath):
    return path.exists(filepath)


def file_exists(filepath):
    return path.isfile(filepath)


def create_dir_if_not_exists(dir_path):
    if not filepath_exists(dir_path):
        makedirs(dir_path)


def get_pickle_file(pickle_filepath):
    return open(pickle_filepath, 'rb')


def load_pickle(pickle_file):
    return load(pickle_file)


def dump_pickle(pickle_filepath, value, protocol=0):
    with open(pickle_filepath, 'wb') as pickle_file:
        dump(value, pickle_file, protocol=protocol)
