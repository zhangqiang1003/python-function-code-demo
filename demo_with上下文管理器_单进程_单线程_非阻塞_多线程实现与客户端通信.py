import socket
import gevent
import re

from gevent import monkey

monkey.patch_all()
import time

# with 上下文管理器
class SocketManager(object):
    def __init__(self, local_addr):
        self.__local_addr = local_addr
        self.__tcp_server_socket = None
        self.__client_socket = None
        self.__client_addr = None
        self.__client_sockets = list()

    def __enter__(self):
        # 创建监听套接字
        self.__tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定服务器ip
        self.__tcp_server_socket.bind(self.__local_addr)
        # 监听
        self.__tcp_server_socket.listen(128)
        # 实现监听套接字的非阻塞
        self.__tcp_server_socket.setblocking(False)
        # 返回监听套接字
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 关闭监听套接字
        self.__tcp_server_socket.close()

    def connect_client(self):
        '''
        接入与客户端交流的套接字

        因为已将 self.__tcp_server_socket 设置为非阻塞的模式，
        因此这里可能会出现灭有客户端接入导致代码执行报错的情况，
        故需要进行 异常处理
        '''
        try:
            self.__client_socket, self.__client_addr = self.__tcp_server_socket.accept()
        except Exception as err:
            # 没有新用户接入
            # print(err, 47)
            pass
        else:
            self.__client_socket.setblocking(False) # 将与客户端通信的socket套接字设置为非阻塞模式
            self.__client_sockets.append(self.__client_socket)

    def recv_request(self):
        '''
        接收来自浏览器端的请求

        1. 需要使用for循环遍历self.__client_sockets存储的客户端套接字
        2. 非阻塞的方式 接收 每一个客户端套接字发来的内容

        因为recv()方法实现了非阻塞，而客户端可能没有发来信息，这会导致报错
        因此需要进行 异常处理
        :return:
        '''
        for client_socket in self.__client_sockets:
            try:
                client_data = client_socket.recv(1024)
            except Exception as err:
                # print(err, 68)
                pass
            else:
                # 如果 client_data 非空，说明 客户端已关闭通信
                if client_data:
                    # 获取到客户端的信息，准备回应请求
                    # 这个地方实现多协程
                    g = gevent.spawn(self.send_response, client_socket, client_data)
                    # self.send_response(client_socket, client_data)
                    g.join()
                else:
                    # 关闭与客户端的通信
                    client_socket.close()
                    # 从self.__client_sockets中关闭该与客户端交流的套接字
                    self.__client_sockets.remove(client_socket)

    def send_response(self, client_socket, client_data):
        # 获取文件名
        file_name_line = client_data.decode('utf-8').splitlines()[0]
        file_name = re.match(r"[^/]+(/[^ ]*)", file_name_line).group(1)

        # 这里可能会文件名找不到导致报错，因此需要异常处理
        try:
            f = open('./demo_html%s' % file_name, 'rb')
        except Exception as err:
            # print(err, 91)
            # 没有该文件
            response_header = 'HTTP/1.1 404 NOT FOUND\r\n'
            response_header += 'Content-Length:%d\r\n' % 0
            client_socket.send(response_header.encode('utf-8'))
        else:
            html_info = f.read()
            f.close()
            response_body = html_info
            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += 'Content-Length:%d\r\n' % len(response_body)
            response_header += '\r\n'

            response = (response_header.encode('utf-8') + response_body)
            client_socket.send(response)

if __name__ == '__main__':
    local_addr = ('127.0.0.1', 7891)
    with SocketManager(local_addr) as tcp_server_socket:
        while True:
            # time.sleep(2)

            # 接入与客户端交流的套接字
            tcp_server_socket.connect_client()
            '''
            与客户端进行信息交流
            这里主要实现浏览器端发来资源名称，服务端读取相应内容并返回
            涉及到http协议
            '''
            # 接收来自浏览器端的请求
            tcp_server_socket.recv_request()