
import argparse
import locale
import os
import shlex
import socket
import subprocess
import sys
import textwrap
import threading


# NETCATクラス
class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        # 実行メソッド
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        # 送信メソッド
        # 接続
        self.socket.connect((self.args.target, self.args.port))

        if self.buffer:
            # データ送信
            self.socket.send(self.buffer)

        try:

            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    # データ受信
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break

                if response:
                    # 受信データ出力
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())

        except KeyboardInterrupt:
            # キーボード押下
            # ターミナル終了
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):

        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)

        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket, )
            )
            client_thread.start()

    def handle(self, client_socket):

        if self.args.execute:

            output = netcat_execute(self.args.execute)
            client_socket.send(output.encode)

        elif self.args.upload:

            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)

            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:

            cmd_buffer = b''

            while True:

                try:
                    client_socket.send(b'<BHP:#> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(46)
                    response = netcat_execute(cmd_buffer.decode())

                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''

                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()


# netcat関数のメイン関数
# 関数のエントリポイント関数
def netcat_main():

    # 対話型コマンドラインインタフェースを開始
    parser_obj = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            '''
            実行例:
            # 対話型コマンドシェルの起動
            netcat.py -t 192.168.1.108 -p 5555 -l -c
            # ファイルのアップロード
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt
            # コマンドの実行
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\"
            # 通信先サーバの135番ポートに文字列を送信
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135
            # サーバに接続
            netcat.py -t 192.168.1.108 -p 5555
            '''
        )
    )

    parser_obj.add_argument('-c', '--command', action='store_true', help='対話型シェルの初期化')

    parser_obj.add_argument('-e', '--execute', help='指定のコマンドの実行')

    parser_obj.add_argument('-l', '--listen', action='store_true', help='通常待受モード')

    parser_obj.add_argument('-p', '--port', type=int, default=5555)

    parser_obj.add_argument('-t', '--target', default='192.168.1.108', help='IPアドレスの指定')

    parser_obj.add_argument('-u', '--upload', help='ファイルのアップロード')

    args = parser_obj.parse_args()

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())

    nc.run()


# netcat実行関数
def netcat_execute(cmd):

    cmd_edit = cmd.strip()

    if not cmd_edit:
        print("実行コマンドが未指定")
        return

    if os.name == 'nt':
        # WindowsNT上で実行されている
        shell_flg = True
    else:
        # その他の環境上で実行されている
        shell_flg = False

    # 子プロセスを生成してコマンドを実行
    output = subprocess.check_output(
        shlex.split(cmd_edit),
        stderr=subprocess.STDOUT,
        shell=shell_flg
    )

    if locale.getdefaultlocale() == ('ja_JP', 'cp932'):
        return output.decode('cp932')
    else:
        return output.decode()

