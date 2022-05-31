

import socket
import sys
import threading

# データがASCIIならそのまま保持、それ以外は"."に置換するテーブル
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]
)

timeout_second = 10


# エントリポイント関数
def tcp_proxy_main(local_host, local_port
                   , remote_host, remote_port, receive_first):

    # サーバループ処理を実行
    server_loop(local_host, local_port
                , remote_host, remote_port, receive_first)


# ローカル端末とリモート端末間の通信をコンソールに出力
def hexdump(src, length=16, show=True):

    if isinstance(src, bytes):
        src = src.decode()

    results = list()

    for i in range(0, len(src), length):

        word = str(src[i:i + length])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join(f'{ord(c):02X}' for c in word)
        hexwidth = length * 3
        results.append(f'{i:04X} {hexa:<{hexwidth}} {printable}')

    if show:

        for line in results:

            print(line)

    else:
        return results


# プロキシがデータを受信するための関数
def receive_from(connection):

    buffer = b""

    connection.settimeout(timeout_second)

    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data

    except Exception as ee:
        print("recv error")
        print(ee)
        return

    return buffer


# リクエストハンドラ
def request_handler(buffer):
    # ここでパケットの改変を行うことが可能
    return buffer


# レスポンスハンドラ
def response_handler(buffer):
    # ここでパケットの改変を行うことが可能
    return buffer


# プロキシ処理ハンドラ
def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:

        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):

            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[==>] Sent to local.")

        while True:

            local_buffer = receive_from(client_socket)

            if len(local_buffer):

                print("[<==] Received %d bytes from local." % len(local_buffer))
                hexdump(local_buffer)

                local_buffer = request_handler(local_buffer)
                remote_socket.send(local_buffer)
                print("[==>] Sent to remote.")

            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):

                print("[<==] Received %d bytes from remote." % len(remote_buffer))
                hexdump(remote_buffer)

                remote_buffer = response_handler(remote_buffer)
                client_socket.send(remote_buffer)
                print("[==>] Sent to local.")

            if not len(local_buffer) or not len(remote_buffer):

                client_socket.close()
                remote_socket.close()

                print("[*] No more data. Closing connections.")
                break


# サーバループ処理
def server_loop(local_host, local_port,
                remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        server.bind((local_host, local_port))

    except Exception as ee:

        print('Problem on bind: %r' % ee)
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d", (local_host, local_port))

    server.listen(5)

    while True:

        client_socket, addr = server.accept()

        # 接続情報の表示
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)

        # リモートホストとの接続を行うスレッドの開始
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()

