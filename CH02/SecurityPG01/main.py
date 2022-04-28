
from TCPClient import *
from UDPClient import *


# メイン処理
def main():

    # TCPクライアントテスト
    tcp_conn_test()

    # UPDクライアントテスト
    udp_conn_test()


# アプリケーションのエントリポイント関数
if __name__ == '__main__':
    main()

