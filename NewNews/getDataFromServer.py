# getDataFromServer.py - サーバからデータをダウンロードする

import pickle, socket, logging, time
from typing import List, Dict

# logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


IP_ADDRESS = "133.242.175.169"
PORT = 56747
BUFFER_SIZE = 4096



def get_data_from_server() -> List[Dict]:
    """サーバからデータを取得する"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(30)
        logging.info("start TCP")
        # サーバに接続を要求する
        s.connect((IP_ADDRESS, PORT))

        # サーバからデータを受信する
        fullData = b""
        logging.info("start receiving")

        size = s.recv(BUFFER_SIZE).decode("utf-8")
        logging.info(size)

        while True:
            data = s.recv(BUFFER_SIZE)
            logging.info("receive {} byte: {} ~ {}".format(len(data), data[:5], data[-5:]))
            fullData += data
            # 終了のチェック
            if len(fullData) == int(size):
                logging.info("end of receiving: {} byte".format(len(fullData)))
                break
            logging.info("have received {} byte".format(len(fullData)))
        


        """
        # サーバーからのデータを受信
        s.sendto(b"connect", (IP_ADDRESS, PORT))

        # データを受信
        fullData = b""
        while True:
            data, addr = s.recvfrom(BUFFER_SIZE)
            logging.info("get {} from {}".format(data[:5], addr))
            if data == b"":
                logging.info("end receiving")
                break
            fullData += data
            print(s.sendto(b"received", addr))
        """

        return pickle.loads(fullData)


if __name__ == "__main__":
    print(get_data_from_server()[1])
    print("finish")