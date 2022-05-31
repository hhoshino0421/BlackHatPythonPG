
from TCPProxy import *


# 使い方表示
def usage():
    print("Usage: ./main.py [local_host] [local_port]", end="")
    print(" [remote_host] [remote_port] [receive_first]")
    print("Example ./main.py 127.0.0.1 9000 10.12.132.1 9999 True")
    return


# メイン関数
def main():

    if len(sys.argv[1:]) != 5:
        # コマンドライン引数エラー
        # 使い方を表示して終了
        usage()

        return

    # コマンドライン引数を変数化
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first_in = sys.argv[5]

    if "True" in receive_first_in:
        receive_first = True
    else:
        receive_first = False

    # TCPプロキシ処理を起動
    tcp_proxy_main(local_host, local_port, remote_host, remote_port, receive_first)


# アプリケーションのエントリポイント関数
if __name__ == '__main__':
    main()

