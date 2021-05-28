import socket
import time


class Client():
    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)
        # self.sock.sendall("ping".encode("utf8"))
        #data = self.sock.recv(1024)
        # print(data)

    def get(self, metric):
        #raise ClientError
        pass

    def put(self, metric, value, timestamp=int(time.time())):
        request = "put " + str(metric) + " " + \
            str(value) + " " + str(timestamp) + "\n"
        self.sock.sendall(request.encode("utf8"))
        print(request.encode("utf8"))
        print(request)

    def __del__(self):
        self.sock.close()


client = Client("127.0.0.1", 8888, timeout=15)

client.put("palm.cpu", 0.5, timestamp=1150864247)
input()
