#! /usr/bin/python3
# sendCliant.py - send json data to cliant

import socket, os, pickle, json



IP_ADDRESS = "133.242.175.169"
PORT = 56747
BUFFER_SIZE =  1048576
DIRNAME = os.path.dirname(__file__)



# Socketの作成
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # IP Adress とPort番号をソケット割り当てる
    s.bind((IP_ADDRESS, PORT))
    # Socketの待機状態
    s.listen(5)
    # while Trueでクライアントからの要求を待つ
    while True:
        # 要求があれば接続の確立とアドレス、アドレスを代入
        conn, addr = s.accept()
        conn.settimeout(60)
        
        # JSONデータを読み込む
        payload = json.load(open(DIRNAME + "/data/qiitaNewItems.json"))
        pay = pickle.dumps(payload)
        # データを送信する
        conn.sendall(pay)