import socket
import json
from unicodedata import name

# data为一个表示车道流量数据的列表
# [东左转，东直行，西直行，西左转，北直行，北左转，南直行，南左转]
# 调用函数后服务端会返回" I have received data: ” + data
def send_data(data):
    content = json.dumps(data)
    content = content.encode('utf-8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8000))
    sock.send(content)
    receive = sock.recv(4096)
    sock.close()
    return receive.decode('utf-8')

if __name__ == '__main__':
    print(send_data([1, 2, 3]))