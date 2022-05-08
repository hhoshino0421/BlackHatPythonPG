
import sys
from TCPClient import *
from UDPClient import *
from TCPServer import *


# メイン処理
def main():

    args = sys.argv

    if len(args) < 1:
        # コマンドライン引数不足
        print("引数不足")
        return

    if not args[1].isdigit():
        # 第一引数が数値以外
        print("第一引数は数値が必要")
        return

    # 第一引数を数値化
    first_flg = int(args[1])

    if first_flg == 1:

        # TCPクライアントテスト
        tcp_conn_test()

    elif first_flg == 2:

        # UPDクライアントテスト
        udp_conn_test()

    elif first_flg == 3:

        # TCPサーバのテスト
        server_ip = '0.0.0.0'
        server_port = 9998
        max_clients = 5
        server_main(server_ip, server_port, max_clients)

    else:
        # 第一引数エラー
        print("第一引数の指定に誤り")
        return


# アプリケーションのエントリポイント関数
if __name__ == '__main__':
    main()

