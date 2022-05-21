
import socket


# TCPコネクションテスト
def tcp_conn_test():

    # 接続先ホスト定義
    # target_host = "www.google.com"
    target_host = "localhost"
    # 接続先ポート番号定義
    # target_port = 80
    target_port = 9998
    # 送信データ定義
    # send_data = b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
    send_data = b"Mewmew\r\n"

    # TCP通信実行
    tcp_conn(target_host, target_port, send_data)


# TCP通信
def tcp_conn(target_host, target_port, send_data):

    # ソケットオブジェクト生成(TCP指定)
    client_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 相手ホストとポート番号を指定して接続
    client_obj.connect((target_host, target_port))
    # データ送信
    client_obj.send(send_data)
    # データ受信
    response_obj = client_obj.recv(4096)

    # 受信データ出力
    print(response_obj.decode())

    # ソケットオブジェクトをクローズ
    client_obj.close()
