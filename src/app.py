import json
import os.path
import sys

from MainHandler import MainHandler
from WebApp import WebApp
from utils import reset_containers

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Insert shared folder path + containers list")
        sys.exit(1)

    args = sys.argv
    print(args)

    base_path = args[1]
    list_path = args[2]

    if os.path.isdir(base_path) and os.path.isfile(list_path):
        containers_list = json.loads(open(list_path).read())
    else:
        print("Shared Folder Path and Containers List INVALID")
        sys.exit(2)
    try:
        reset_containers()
        handler = MainHandler(base_path, containers_list)
        handler.start()

        webapp = WebApp()
        webapp.start()

    except Exception as e:
        print(e)
    finally:
        handler.stop()
        print(handler.thread.isAlive())
