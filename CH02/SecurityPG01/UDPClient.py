
import socket


# UDPコネクションテスト
def udp_conn_test():

    # 接続先ホスト定義
    target_host = "127.0.0.1"
    # 接続先ポート番号定義
    target_port = 9997
    # 送信データ定義
    send_data = b"AAABBBCCC"

    # UDP通信実行
    upd_conn(target_host, target_port, send_data)


#  UDP通信
def upd_conn(target_host, target_port, send_data):

    # ソケットオブジェクト生成(UDP指定)
    client_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # データ送信
    client_obj.sendto(send_data,(target_host, target_port))
    # データ受信
    data, address = client_obj.recvfrom(4096)
    # 受信データ出力
    print(data.decode('utf-8'))
    # 受信アドレス情報出力
    print(address)

    # ソケットオブジェクトクローズ
    client_obj.close()
