import socket
import json
import pysnooper

class Real(object):
    def __init__(self) -> None:
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.sock.bind(('0.0.0.0', 5000))
        self.sock.listen(5)

    def get_data(self):
        cli_sock,cli_addr=self.sock.accept()
        req=cli_sock.recv(4096)
        req_str = req.decode('utf-8')
        data = json.loads(req_str)
        back_str = "I have received data : " + req_str
        back_str = back_str.encode('utf-8')
        cli_sock.send(back_str)
        cli_sock.close()
        return data

if __name__== '__main__':
    real_cross = Real()
    while(1):
        receive_data = real_cross.get_data()
        print(receive_data)

