import json
import os
import socket

info_file = "resources/info.json"


def turn_container(container, state, uri=""):
    """
    TODO DOCUMENTATION
    :param container:
    :param state:
    :param uri:
    :return:
    """
    info = get_info()['containers']
    info[container]['status'] = state
    info[container]['uri'] = uri
    save_containers(info, info_file)


def reset_containers():
    """
    TODO DOCUMENTATION
    :return:
    """
    info = get_info()['containers']
    for container in info:
        info[container]['status'] = False
    save_containers(info, info_file)


def get_info():
    """
    TODO DOCUMENTATION
    :return:
    """
    info = read_json(info_file)
    return info


def save_containers(info, info_file):
    """
    TODO DOCUMENTATION
    :param info:
    :param info_file:
    :return:
    """
    all_info = get_info()
    all_info['containers'] = info
    save_json(all_info, info_file)


def set_shared_folder(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    info = get_info()
    info['shared_folder'] = path
    save_json(info, info_file)


def get_shared_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    return get_info()['shared_folder']


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


def save_json(data, path):
    """
    TODO DOCUMENTATION
    :param data:
    :param path:
    :return:
    """
    with open(path, 'w') as out:
        json.dump(data, out, indent=4, ensure_ascii=False)
    return path


def get_ip():
    """
    TODO DOCUMENTATION
    :return:
    """
    return socket.gethostbyname(socket.gethostname())
