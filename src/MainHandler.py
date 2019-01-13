import os

import Pyro4


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
        else:
            print("Main Container: <{}> not registered".format(container))
            raise ModuleNotFoundError('Container not expected')

    def stop(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        os.remove(self.config_path)
        # TODO STOP ALL REGISTERED CONTAINERS
        print("Main Container: Stopped")

    def run(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        if len(self.containers_list) == 0:
            obj = Pyro4.Proxy(self.containers['Training'])
            obj.register([i for i in self.containers.items() if i[0] in ['G2P', 'SRILM', 'SPHINXBASE']])
            print("Main Container: Run")
            return True
        else:
            print("There are no configured containers : {}".format(' '.join(self.containers_list)))
            return False
