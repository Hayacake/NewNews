#! /usr/bin/python3
# sendCliant.py - send json data to cliant

import socket, os, pickle, json, logging, time

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")



IP_ADDRESS = "133.242.175.169"
PORT = 56747
BUFFER_SIZE =  4096
DIRNAME = os.path.dirname(__file__)


# Socketの作成
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # IP Adress とPort番号をソケット割り当てる
    s.bind((IP_ADDRESS, PORT))
    logging.info("start listening")
    # socketの待機状態
    s.listen(5)

    # while Trueでクライアントからの要求を待つ
    while True:
        # 要求があれば接続の確立とアドレス、アドレスを代入
        conn, addr = s.accept()
        logging.info("connect with {}; {}".format(conn, addr))

        data = json.load(open(DIRNAME + "/data/qiitaNewItems.json"))
        # data = {"food": "Apple", "count": 4}
        data = pickle.dumps(data)
        logging.info("data size is {}".format(len(data)))

        size = len(data)
        size = str(size)
        conn.sendall(bytes(size, "utf-8"), socket.MSG_WAITALL)

        # データを送信する
        startTime = time.time()
        conn.sendall(data)
        logging.info("finish sending; {} sec".format(time.time() - startTime))
        logging.info("=================================")


        """
        # 分割して送る
        n = 0
        print(len(data))
        logging.info("start sending data")
        while True:
            payload = data[n * 1000: (n + 1) * 1000]
            logging.info("{}; {}; {}".format(n, payload[:5], addr))
            # 送るデータがなくなったと伝える
            if payload == b"":
                s.sendto(b"", addr)
                logging.info("end sending data")
                logging.info("=====================")
                break
            s.sendto(payload, addr)
            n += 1
            # time.sleep(0.25)
            d, addr = s.recvfrom(BUFFER_SIZE)
            """
       