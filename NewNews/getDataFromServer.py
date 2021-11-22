# getDataFromServer.py - サーバからデータをダウンロードする

import pickle, socket
from typing import List, Dict



IP_ADDRESS = "133.242.175.169"
PORT = 56747
BUFFER_SIZE = 4096



def get_data_from_server() -> str:
    """サーバからデータを取得する"""
    fullData = b""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # サーバーに接続を要求する
        s.connect((IP_ADDRESS, PORT))
        s.settimeout(180)
        # サーバーからのデータを受信
        while True:
            data = s.recv(BUFFER_SIZE)
            if len(data) <= 0:
                break
            fullData += data

        return fullData


if __name__ == "__main__":
    print(pickle.loads(get_data_from_server()))