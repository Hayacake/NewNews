#! /usr/bin/python3
# NewNews.py - サーバからデータをダウンロードして表示する

import tkinter as tk
import tkinter.ttk as ttk
import json, datetime, webbrowser, os, threading, logging
from typing import Dict, List

from Qiita import get_new_items
from getDataFromServer import get_data_from_server

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s - %(message)s")

PGMFILE = os.path.dirname(__file__)



# TODO: 処理の状況を伝えるメッセージ
# TODO: ブックマーク機能
# TODO: リストの体裁を整える




class WidgetsWindow:
    """widgetを並べたwindowクラス"""
    def __init__(self, root: tk.Tk) -> None:
        self.root = root


        # Pack形式で積んでいく(gridにしたい)

        # ===============================================================================================

        # お気に入りボタン
        self.btnFav = ttk.Button(self.root, text="Favorite", command=self.push_button_fav)

        # お気に入りデータの読み込み
        self.favData = self.load_fav()

        # ===============================================================================================

        # リスト
        self.column = ('Title', 'Tags', 'Date')
        self.tree = ttk.Treeview(self.root, columns=self.column)

        # 列の設定
        self.tree.column('#0',width=0, stretch='no')
        self.tree.column('Title', anchor='center', width=200, stretch=True)
        self.tree.column('Tags',anchor='w', width=200)
        self.tree.column('Date', anchor='center', width=5, minwidth=5)
        # 列の見出し設定
        self.tree.heading('#0',text='')
        self.tree.heading('Title', text='Title',anchor='center')
        self.tree.heading('Tags', text='Tags', anchor='w')
        self.tree.heading('Date',text='Date', anchor='center')


        # URLを開くために{id: URL, user: user情報}のペアを作る
        self.idUrlPair: Dict[str, str] = {}

        # ローカルからデータの追加
        self.load_local_data(self.favData)

        # サーバとローカルによるデータの更新+最新情報の取得(別スレッドで)
        self.is_server = threading.Event()
        thLoadingServer = threading.Thread(target=self.load_server_data, args=(self.favData, ), name="Server")
        thLoadingServer.start()

        thLoadingNewest = threading.Thread(target=self.load_newest_data, args=(self.favData, ), name="Newest")
        thLoadingNewest.start()

        # 未読と既読を色分けする
        self.tree.tag_configure("unread", background="#a0d8ef")

        # イベントの追加
        # URLオープンイベント
        self.tree.tag_bind("item", "<Double-ButtonPress>", self.event_open_url)
        self.tree.tag_bind("item", "<Return>", self.event_open_url)

        # ===============================================================================================

        # スクロールバー
        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        # ===============================================================================================

        # 描画する
        self.btnFav.pack(side=tk.TOP, anchor=tk.W, padx=15, pady=10)
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=15, pady=5)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # ===============================================================================================
        
    


    def load_local_data(self, favData: List[Dict]) -> None:
        """ローカルからファイルをロードする"""
        logging.info("start loading local file")

        # ファイルを読み込む
        datLocal = json.load(open(PGMFILE + "/lib/data/Qiita.json"))
        self.dat = datLocal
        print(datLocal)

        # お気に入りのタイトルリスト
        listFavTitle = [item["title"] for item in favData]
        self.listRead = [item["title"] for item in datLocal if item.get("read", 0) == 1]

        for item in datLocal:
            date = datetime.datetime.fromisoformat(item["date"])
            if item["title"] not in listFavTitle:
                id = self.tree.insert(parent="", index="end", values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old"])
            else:
                id = self.tree.insert(parent="", index="end", values=("⭐️ " + item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old"])
            # ペアを格納
            self.idUrlPair[id] = {"url": item["url"], "user": item.get("user", {}), "flagNew": 0}
        logging.info("success loading local data")



    def load_server_data(self, favData: List[Dict]) -> None:
        """サーバーからファイルをロードする"""
        logging.info("start loading server file")

        # ファイルを読み込む
        datServer = get_data_from_server()

        if datetime.datetime.fromisoformat(self.dat[0]["date"]) >= datetime.datetime.fromisoformat(datServer[0]["date"]):
            logging.info("local data is newest")
            self.is_server.set()
            pass
        else:
            logging.info("update to server data (local data is not newest)")
            self.dat = datServer

            self.is_server.set()                        # 最新情報を動かす

            # お気に入りのリスト
            listFavTitle = [item["title"] for item in favData]
            # リストに情報を入れていく
            for item in datServer[::-1]:
                item["read"] = 1
                date = datetime.datetime.fromisoformat(item["date"])
                if item["title"] not in listFavTitle:
                    # お気に入りではないとき
                    if item["title"] not in self.listRead:
                        # 新着記事の時
                        id = self.tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old", "unread"])
                    else:
                        id = self.tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old"])
                else:
                    # お気に入りの時
                    if item["title"] not in self.listRead:
                        # 新着記事の時
                        id = self.tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old", "unread"])
                    else:
                        id = self.tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old"])
                # ペアを格納
                self.idUrlPair[id] = {"url": item["url"], "user": item.get("user", {}), "flagNew": 0}
        logging.info("success loading server file")



    def load_newest_data(self, favData: List[Dict]) -> None:
        """最新の情報をAPIから取得する"""
        logging.info("start loading from web API")

        # 最新の情報を取得する
        datWeb = get_new_items()
        self.is_server.wait()
        logging.info("success getting newest")

        # delete multify 
        i = 0; deleteItems = []; listWebTitle = [article["title"] for article in datWeb]
        for item in self.dat:
            flag = 0
            if item["title"] in listWebTitle:
                deleteItems.append(item)
                flag = 1
            if flag == 0:
                i += 1
            if i > 5:
                break
        for i in deleteItems:
            self.dat.remove(i)
            assert not i in self.dat, i
        
        # データを作る
        self.dat = datWeb + self.dat
        listFavTitle = [item["title"] for item in favData]

        # リストに表示する
        for item in self.dat[::-1]:
            date = datetime.datetime.fromisoformat(item["date"])
            if item["title"] not in listFavTitle:
                # お気に入りではないとき
                if item["title"] not in self.listRead:
                    # 新着記事の時
                    id = self.tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old", "unread"])
                else:
                    id = self.tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old"])
            else:
                # お気に入りの時
                if item["title"] not in self.listRead:
                    # 新着記事の時
                    id = self.tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old", "unread"])
                else:
                    id = self.tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old"])
            # ペアを格納
            self.idUrlPair[id] = {"url": item["url"], "user": item.get("user", {}), "flagNew": 1}
        
        # ローカルに保存する
        json.dump(self.dat, open(PGMFILE + "/lib/data/Qiita.json", "w"), indent=2, ensure_ascii=False)

        # 古いデータを消す
        for i, v in self.idUrlPair.items():
            if v["flagNew"] == 0:
                self.tree.delete(i)



    
    
    def load_fav(self) -> List[Dict]:
        favData = json.load(open(PGMFILE + "/lib/data/usrfavorite.json"))
        return favData



    def event_open_url(self, event):
        if event.type == "4":
            select = self.tree.identify_row(event.y)
        elif event.type == "2":
            select = self.tree.focus()
        webbrowser.open(self.idUrlPair[select]["url"])

    

    def push_button_fav(self) -> None:
        select = self.tree.focus()
        if select == "":
            pass
        else:
            recordVal = self.tree.item(select, "values")
            # すでにお気に入り登録されているかのチェック
            if recordVal[0].startswith("⭐️ "):
                self.tree.set(select, "Title", recordVal[0].lstrip("⭐️ "))
                self.favData.remove({"title": recordVal[0].lstrip("⭐️ "), "tags": recordVal[1].split(sep=", "), "user": self.idUrlPair[select]["user"], "url": self.idUrlPair[select]["url"], "date": recordVal[2]})
            else:
                self.tree.set(select, "Title", "⭐️ " + recordVal[0])
                self.favData.append({"title": recordVal[0], "tags": recordVal[1].split(sep=", "), "user": self.idUrlPair[select]["user"], "url": self.idUrlPair[select]["url"], "date": recordVal[2]})
            json.dump(self.favData, open(PGMFILE + "/lib/data/usrfavorite.json", "w"), indent=2, ensure_ascii=False)

    




def main():
    root = tk.Tk()
    root.title("NewNews")
    root.geometry("1000x800")
    ww = WidgetsWindow(root)
    root.mainloop()



if __name__ == "__main__":
    logging.info("start App")
    main()
    logging.info("stop App")
    logging.info("===============================-")