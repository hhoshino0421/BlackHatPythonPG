
import socket


def tcp_conn_test():

    target_host = "www.google.com"
    target_port = 80
    send_data = b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"

    tcp_conn(target_host, target_port, send_data)


def tcp_conn(target_host, target_port, send_data):

    client_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_obj.connect((target_host, target_port))
    client_obj.send(send_data)
    response_obj = client_obj.recv(4096)

    print(response_obj.decode())

    client_obj.close()
