import json
import os


def check_file(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    if not os.path.isfile(path):
        raise FileNotFoundError("File not found")
    return open(path)


def read_json(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    check_file(path)
    with open(path) as f:
        data = json.load(f)
    return data
