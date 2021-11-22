# getDataFromServer.py - サーバからデータをダウンロードする

import socket



IP_ADDRESS = "133.242.175.169"
PORT = 56747



def get_data_from_server():
    """サーバからデータを取得する"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_ADDRESS, PORT))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    msg = s.recv(1024)
    print(msg.decode("utf-8"))


if __name__ == "__main__":
    get_data_from_server()