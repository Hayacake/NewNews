#! /usr/bin/python3
# sendCliant.py - send json data to cliant

import socket, os, pickle, json, time



IP_ADDRESS = "133.242.175.169"
PORT = 56747
BUFFER_SIZE =  4096
DIRNAME = os.path.dirname(__file__)


# Socketの作成
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # IP Adress とPort番号をソケット割り当てる
    s.bind((IP_ADDRESS, PORT))

    # while Trueでクライアントからの要求を待つ
    while True:
        # 要求があれば接続の確立とアドレス、アドレスを代入
        msg, addr = s.recvfrom(BUFFER_SIZE)

        data = json.load(open(DIRNAME + "/data/qiitaNewItems.json"))
        data = pickle.dumps(data)

        # 分割して送る
        n = 0
        print(len(data))
        while True:
            payload = data[n * 4000: (n + 1) * 4000]
            # 送るデータがなくなったと伝える
            if payload == b"":
                s.sendto(b"finish", addr)
                break
            s.sendto(payload, addr)
            n += 1
            # time.sleep(0.25)
            d, a = s.recvfrom(BUFFER_SIZE)
       