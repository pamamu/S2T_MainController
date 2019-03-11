import json
import os.path
import sys

from MainHandler import MainHandler

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Insert shared folder path + containers list")
        sys.exit(1)
    base_path = sys.argv[1]
    list_path = sys.argv[2]
    if os.path.isdir(base_path) and os.path.isfile(list_path):
        containers_list = json.loads(open(list_path).read())
    else:
        print("Shared Folder Path and Containers List INVALID")
        sys.exit(2)
    try:
        handler = MainHandler(base_path, containers_list)
        handler.start()
        input("-- ENTER for menu --\n")

        input_value = "1"
        while int(input_value) != 0:
            print("\n--------- MENU OPTIONS ----------\n"
                  "|  0: Exit\t\t\t|\n"
                  "|  1: Download audios + trans\t|\n"
                  "|  2: Train Models\t\t|\n"
                  "|  3: Speech2Text\t\t|\n"
                  "---------------------------------\n")
            input_value = input("Input number: ")
            integer_value = int(input_value)
            info_path = input("Json Info Path: ")
            handler.run(action=integer_value, input_json=info_path)

    except Exception as e:
        print(e)
    finally:
        handler.stop()
        print(handler.thread.isAlive())
