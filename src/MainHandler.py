import os

import Pyro4

from utils import read_json


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
        self.daemon.requestLoop()

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
        if len(self.containers_list) == 0:
            if 'input_json' in kwargs:
                info = read_json(kwargs['input_json'])
                obj = Pyro4.Proxy(self.containers['Training'])
                for container in self.containers.items():
                    if container[0] in ['G2P', 'SRILM', 'SPHINXBASE']:
                        obj.slave_register(container[0], container[1])
                print("Main Container: Run")
                return True
            else:
                raise TypeError('input_json is required')
        else:
            raise ValueError("There are no configured containers : {}".format(' '.join(self.containers_list)))
