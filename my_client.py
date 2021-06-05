import socket
import time
import re


class ClientError(Exception):
    pass


class Client():

    def __init__(self, host, port, timeout=None):

        self.sock = socket.create_connection((host, port), timeout)
        self.request = ""
        self.response = ""
        self.response_status = True

    def get(self, metric):
        self.request = "get " + str(metric) + "\n"
        self.sock.sendall(self.request.encode("utf8"))
        self.response = self.sock.recv(1024)
        my_dict = {}

        if self.response == b"error\nwrong command\n\n":
            self.response_status = False
            raise ClientError
        elif self.validate() or self.response == b"ok\n\n":
            all_metrics = self.response.decode("utf8").split('\n')
            for one_metric in all_metrics:
                data = one_metric.split(' ')
                if len(data) != 3:
                    continue
                if data[0] not in my_dict:
                    my_dict[data[0]] = []
                my_dict[data[0]].append((int(data[2]), float(data[1])))
        else:
            raise ClientError
        for key in my_dict:
            my_dict[key].sort(key=lambda x: x[0])
        return my_dict

    def put(self, metric, value, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())
        self.request = "put " + str(metric) + " " + \
            str(value) + " " + str(timestamp) + "\n"
        self.sock.sendall(self.request.encode("utf8"))
        # получим ответ
        self.response = self.sock.recv(1024)

        if self.response == b"ok\n\n":
            self.response_status = True
        elif self.response == b"error\nwrong command\n\n":
            self.response_status = False
            raise ClientError
        else:
            raise ClientError

    def validate(self):
        #regex = re.compile('^ok\n(.*\n)+\n\n$')
        data = self.response.decode("utf8")
        print(data)
        # '^ok\n(.*\n)+\n\n$'
        if re.search('^ok(\n.*)+\n\n$', data) is None:
            return False
        all_data = data.split('\n')
        for counter in range(1, len(all_data) - 2):
            one_data = all_data[counter].split(' ')
            if len(one_data) != 3:
                return False
            try:
                trash = float(one_data[1])
                trash = int(one_data[2])
            except ValueError:
                raise ClientError
        return True

    def __del__(self):
        self.sock.close()


# тестирование
'''
client = Client("127.0.0.1", 8888, timeout=15)

# client.put("palm.cpu", 0.5, timestamp=1150864247)

print(client.get("*"))
input()
'''
