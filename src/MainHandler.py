import os
from threading import Thread

import Pyro4

from utils import read_json, check_file


@Pyro4.expose
class MainHandler:
    def __init__(self, base_path, containers_list):
        """
        TODO DOCUMENTATION
        :param base_path:
        :param containers_list:
        """
        self.containers = {}
        self.containers_list = containers_list
        self.daemon = Pyro4.Daemon(port=4040)
        self.uri = str(self.daemon.register(self, objectId="MainController"))
        self.thread = Thread(target=self.daemon.requestLoop)
        self.base_path = base_path
        self.config_path = os.path.join(base_path, 'server.info')
        print("Main Container: Created - {}".format(self.uri))

    def start(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        with open(self.config_path, 'w') as f:
            f.write(str(self.uri))
        print("Main Container: Started")
        self.thread.start()

    def register(self, container, uri):
        """
        TODO DOCUMENTATION
        :param container:
        :param uri:
        :return:
        """
        if container in self.containers_list:
            print("Main Container: <{}> registered from <{}>".format(container, uri))
            self.containers[container] = uri
            self.containers_list.remove(container)
            return container, uri
        else:
            print("Main Container: <{}> not registered".format(container))
            raise ModuleNotFoundError('Container not expected')

    def unregister(self, container):
        if container in self.containers:
            print("Main Container: <{}> unregistered".format(container))
            del self.containers[container]
            self.containers_list.append(container)
            if container in ['G2P', 'SRILM', 'SPHINXBASE'] and 'Training' in self.containers:
                obj = Pyro4.Proxy(self.containers['Training'])
                obj.slave_unregister(container)

        else:
            print("Main Container: <{}> not registered".format(container))
            raise ModuleNotFoundError('Container not expected')

    def stop(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        os.remove(self.config_path)
        for container, uri in list(self.containers.items()):
            try:
                obj = Pyro4.Proxy(uri)
                obj.stop()
                print("Main Container: {} Stopped".format(container))
            except:
                print("Main Container: Container {} failed at the stop".format(container))
        self.daemon.shutdown()
        print("Main Container: Stopped")

    def run(self, **kwargs):
        """
        TODO DOCUMENTATION
        :return:
        """
        if not ('input_json' in kwargs and 'action' in kwargs):
            raise TypeError('input_json and action are required')
        action = kwargs['action']
        check_file(kwargs['input_json'])
        if action == 1:
            necessary_containers = ['GetAudioTrans']
            if all(i in self.containers for i in necessary_containers):
                print("OK - GetAudioTrans")
                obj = Pyro4.Proxy(self.containers['GetAudioTrans'])
                obj.run(input_json=kwargs['input_json'], output_folder=self.base_path)
            else:
                raise ValueError("There are no configured containers : {}".format(
                    ' '.join(filter(lambda x: x not in self.containers, necessary_containers))))
        elif action == 2:
            necessary_containers = ["AudioProcessing", "Training", "G2P", "SRILM", "SPHINXBASE"]
            if all(i in self.containers for i in necessary_containers):
                obj = Pyro4.Proxy(self.containers['Training'])
                for container in self.containers.items():
                    if container[0] in ['G2P', 'SRILM', 'SPHINXBASE']:
                        obj.slave_register(container[0], container[1])
                print("OK - Training")
            else:
                raise ValueError("There are no configured containers : {}".format(
                    ' '.join(filter(lambda x: x not in self.containers, necessary_containers))))
        elif action == 3 and 'Speech2Text' in self.containers:
            necessary_containers = ["AudioProcessing", "Training", "G2P", "SRILM", "SPHINXBASE"]
            if all(i in self.containers for i in necessary_containers):
                print("OK - Speech2Text")
            else:
                raise ValueError("There are no configured containers : {}".format(
                    ' '.join(filter(lambda x: x not in self.containers, necessary_containers))))
        else:
            raise ValueError("Incorrect Option")
