# getDataFromServer.py - サーバからデータをダウンロードする

import pickle, socket
from typing import List, Dict



IP_ADDRESS = "133.242.175.169"
PORT = 56747
BUFFER_SIZE = 4096



def get_data_from_server() -> str:
    """サーバからデータを取得する"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # サーバーからのデータを受信
        s.sendto(b"connection", (IP_ADDRESS, PORT))

        # データを受信
        fullData = b""
        while True:
            data, addr = s.recvfrom(BUFFER_SIZE)
            if data == b"finish":
                break
            fullData += data
            s.sendto(b"received", (IP_ADDRESS, PORT))

        return pickle.loads(fullData)


if __name__ == "__main__":
    print(get_data_from_server())