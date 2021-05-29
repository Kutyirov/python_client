import socket
import time


class ClientError(Exception):
    pass


class Client():

    def __init__(self, host, port, timeout=None):

        self.sock = socket.create_connection((host, port), timeout)
        self.request = ""
        self.response = ""
        self.response_status = True
        # self.sock.sendall("ping".encode("utf8"))
        #data = self.sock.recv(1024)
        # print(data)

    def get(self, metric):
        self.request = "get" + str(metric) + "\n"
        self.sock.sendall(self.request.encode("utf8"))
        self.response = self.sock.recv(1024)
        my_dict = {}

        if self.response == b"error\nwrong command\n\n":
            self.response_status = False
            raise ClientError
        elif self.validate():
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
        return True

    def __del__(self):
        self.sock.close()


client = Client("127.0.0.1", 8888, timeout=15)

# client.put("palm.cpu", 0.5, timestamp=1150864247)

print(client.get("*"))
input()
