

import socket


def udp_conn_test():

    target_host = "127.0.0.1"
    target_port = 9997
    send_data = b"AAABBBCCC"

    upd_conn(target_host, target_port, send_data)


def upd_conn(target_host, target_port, send_data):

    client_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_obj.sendto(send_data,(target_host, target_port))
    data, address = client_obj.recvfrom(4096)
    print(data.decode('utf-8'))
    print(address)

    client_obj.close()
