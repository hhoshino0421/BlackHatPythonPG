
import socket
import threading


# TCPサーバ メイン関数
def server_main(server_ip, server_port, max_clients):

    server_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_obj.bind((server_ip, server_port))
    server_obj.listen(max_clients)
    print(f'[*] Listening on {server_ip}:{server_port}')

    while True:
        client_obj, address = server_obj.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client_obj,))
        client_handler.start()


# データ受信時の処理ハンドラ関数
def handle_client(client_socket):

    with client_socket as sock:
        request_obj = sock.recv(1024)
        print(f'Received: {request_obj.decode("utf-8")}')
        sock.send(b'ACK')
