#! /Users/kakeru/opt/anaconda3/bin/python3
# NewNews.py - サーバからデータをダウンロードして表示する

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import json, datetime, webbrowser, os, threading, logging, traceback
from typing import Dict, List

from Qiita import get_new_items
from getDataFromServer import get_data_from_server

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s - %(message)s")

PGMFILE = os.path.dirname(__file__)



# TODO: コードのクリーンアップ
# NOTE: 処理の状況を伝えるメッセージ
# TODO: リストの体裁を整える




class WidgetsWindow:
    """widgetを並べたwindowクラス"""
    def __init__(self, root: tk.Tk) -> None:
        self.root = root


        # Pack形式で積んでいく(gridにしたい)

        # ===============================================================================================

        # ボタン用のフレーム
        self.btnframe = tk.Frame(self.root)

        # お気に入りボタン
        self.btnFav = ttk.Button(self.btnframe, text="Favorite", command=self.push_button_fav)
        self.btnbook = ttk.Button(self.btnframe, text="Bookmark", command=self.push_button_book)

        # お気に入りデータの読み込み
        self.favData = self.load_fav()

        # ===============================================================================================
        # タブ
        self.notebook = ttk.Notebook(root)
        
        self.tabAll = tk.Frame(self.notebook)
        self.tabBooked = tk.Frame(self.notebook)

        self.notebook.add(self.tabAll, text="All")
        self.notebook.add(self.tabBooked, text="bookmark")

        # リストの準備
        self.column = ('Title', 'Tags', 'Date')
        # リストをしまう辞書
        self.dictTree: Dict[str, ttk.Treeview] = {}


        # リスト(all)
        self.dictTree["Qiita"] = ttk.Treeview(self.tabAll, columns=self.column)

        # 列の設定
        self.dictTree["Qiita"].column('#0',width=0, stretch='no')
        self.dictTree["Qiita"].column('Title', anchor='center', width=200, stretch=True)
        self.dictTree["Qiita"].column('Tags',anchor='w', width=200)
        self.dictTree["Qiita"].column('Date', anchor='center', width=5, minwidth=5)
        # 列の見出し設定
        self.dictTree["Qiita"].heading('#0',text='')
        self.dictTree["Qiita"].heading('Title', text='Title',anchor='center')
        self.dictTree["Qiita"].heading('Tags', text='Tags', anchor='w')
        self.dictTree["Qiita"].heading('Date',text='Date', anchor='center')


        # 各種データ保存用
        self.dat = {}
        # データ保存用のIDペア
        self.idUrlPair = {}
        # 既読リスト
        self.dictRead = {}

        # ローカルからデータの追加
        self.load_local_data(favData=self.favData, appName="Qiita")

        # サーバとローカルによるデータの更新+最新情報の取得(別スレッドで)
        self.is_server = threading.Event()
        thLoadingServer = threading.Thread(target=self.load_server_data, args=(self.favData, "Qiita", ), name="Server")
        thLoadingServer.start()

        thLoadingNewest = threading.Thread(target=self.load_newest_data, args=(self.favData, "Qiita", ), name="Newest")
        thLoadingNewest.start()

        # 未読と既読を色分けする
        self.dictTree["Qiita"].tag_configure("unread", background="#a0d8ef")

        # イベントの追加
        # URLオープンイベント
        self.dictTree["Qiita"].tag_bind("item", "<Double-ButtonPress>", lambda event: self.event_open_url(event, "Qiita"))
        self.dictTree["Qiita"].tag_bind("item", "<Return>", lambda event: self.event_open_url(event, "Qiita"))

        # ===============================================================================================

        # スクロールバー
        self.scrollbar = ttk.Scrollbar(self.tabAll, orient=tk.VERTICAL, command=self.dictTree["Qiita"].yview)
        self.dictTree["Qiita"].configure(yscroll=self.scrollbar.set)

        # ===============================================================================================

        # リスト(Booked)
        self.bookDat = self.load_book()
        self.dictTree["bookmark"] = ttk.Treeview(self.tabBooked, columns=self.column)

        # 列の設定
        self.dictTree["bookmark"].column('#0',width=0, stretch='no')
        self.dictTree["bookmark"].column('Title', anchor='center', width=200, stretch=True)
        self.dictTree["bookmark"].column('Tags',anchor='w', width=200)
        self.dictTree["bookmark"].column('Date', anchor='center', width=5, minwidth=5)
        # 列の見出し設定
        self.dictTree["bookmark"].heading('#0',text='')
        self.dictTree["bookmark"].heading('Title', text='Title',anchor='center')
        self.dictTree["bookmark"].heading('Tags', text='Tags', anchor='w')
        self.dictTree["bookmark"].heading('Date',text='Date', anchor='center')

        # データの挿入
        self.load_local_data(appName="bookmark")

        # イベントの追加
        # URLオープンイベント
        self.dictTree["bookmark"].tag_bind("item", "<Double-ButtonPress>", lambda event: self.event_open_url(event, "bookmark"))
        self.dictTree["bookmark"].tag_bind("item", "<Return>", lambda event: self.event_open_url(event, "bookmark"))

        # スクロールバー
        self.scrollbarBook = ttk.Scrollbar(self.tabBooked, orient=tk.VERTICAL, command=self.dictTree["bookmark"].yview)
        self.dictTree["bookmark"].configure(yscroll=self.scrollbarBook.set)

        # ===============================================================================================

        # 描画する
        self.btnframe.pack(side=tk.TOP, anchor=tk.W, padx=15, pady=7)
        self.btnFav.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=0)
        self.btnbook.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=0)

        self.notebook.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=0)
        self.dictTree["Qiita"].pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=0, pady=0)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.dictTree["bookmark"].pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=0, pady=0)
        self.scrollbarBook.pack(side=tk.RIGHT, fill=tk.Y)

        # ===============================================================================================
        
    


    def load_local_data(self, appName: str, favData: List[Dict] = []) -> None:
        """ローカルからファイルをロードする"""
        logging.info("start loading local file")
        app = appName

        # ファイルを読み込む
        datLocal = json.load(open(PGMFILE + f"/lib/data/{appName}.json"))
        self.dat[appName] = datLocal

        # 既読のタイトルリスト
        self.dictRead[appName] = [item["title"] for item in datLocal if item.get("read", 0) == 1]

        # データを挿入する
        self._insert_tree(datLocal, favData, appName=app)

        logging.info("success loading local data")



    def load_server_data(self, favData: List[Dict], appName: str) -> None:
        """サーバーからファイルをロードする"""
        logging.info("start loading server file")
        app = appName

        # ファイルを読み込む
        while True:
            try:
                datServer = get_data_from_server()
                if datetime.datetime.fromisoformat(self.dat[appName][0]["date"]) >= datetime.datetime.fromisoformat(datServer[0]["date"]):
                    logging.info("local data is newest")
                    self.is_server.set()               # 最新情報を動かす
                    break
                else:
                    logging.info("update to server data (local data is not newest)")
                    self.dat[appName] = datServer

                    self.is_server.set()               # 最新情報を動かす

                    # データを挿入する
                    self._insert_tree(datServer, favData==favData, appName=app, isServer=True)

                    logging.info("success loading server file")
                    break
            except Exception as err:
                retry = messagebox.askretrycancel(title="ERROR!", message=traceback.format_exc())
                if not retry:
                    self.is_server.set()
                    break

        



    def load_newest_data(self, favData: List[Dict], appName: str) -> None:
        """最新の情報をAPIから取得する"""
        logging.info("start loading from web API")
        app = appName

        # 最新の情報を取得する
        datWeb = get_new_items()
        self.is_server.wait()
        logging.info("success getting newest")

        # delete multify 
        i = 0; deleteItems = []; listWebTitle = [article["title"] for article in datWeb]
        for item in self.dat[appName]:
            flag = 0
            if item["title"] in listWebTitle:
                deleteItems.append(item)
                flag = 1
            if flag == 0:
                i += 1
            if i > 5:
                break
        for i in deleteItems:
            self.dat[appName].remove(i)
            assert not i in self.dat[appName], i
        
        # データを作る
        self.dat[appName] = datWeb + self.dat[appName]
        
        # データを挿入する
        self._insert_tree(self.dat[appName], favData, appName=app, new=True)
        
        # ローカルに保存する
        json.dump(self.dat[appName], open(PGMFILE + f"/lib/data/{appName}.json", "w"), indent=2, ensure_ascii=False)

        # 古いデータを消す
        for i, v in self.idUrlPair.items():
            if v["flagNew"] == 0:
                self.dictTree[appName].delete(i)



    def load_fav(self) -> List[Dict]:
        favData = json.load(open(PGMFILE + "/lib/data/usrfavorite.json"))
        return favData


    def load_book(self) -> List[Dict]:
        bookdat = json.load(open(PGMFILE + "/lib/data/bookmark.json"))
        return bookdat



# ================ヘルパー関数================
    def _insert_tree(self, data: List[Dict], favData: List[Dict], appName: str, new = False, isServer: bool = False):
        """Treeviewに`data`を挿入する"""
        # お気に入りをリストにまとめる
        listFavTitle = [item["title"] for item in favData]

        # 挿入していく
        for i in data[::-1]:
            # serverからの情報の時はreadパラメータを変える必要がある
            if isServer:
                i["read"] = 1
            # 日付形式の変更
            date = datetime.datetime.fromisoformat(i["date"])
            

            listr = self.dictRead[appName]
            if i["title"] not in listFavTitle:
                # お気に入りではないとき
                if i["title"] not in listr:
                    # 新着記事の時
                    id = self.dictTree[appName].insert(parent="", index=-1, values=(i["title"], ", ".join(i["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old", "unread"])
                else:
                    id = self.dictTree[appName].insert(parent="", index=-1, values=(i["title"], ", ".join(i["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old"])
            else:
                # お気に入りの時
                if i["title"] not in listr:
                    # 新着記事の時
                    id = self.dictTree[appName].insert(parent="", index=-1, values=("⭐️ " + i["title"], ", ".join(i["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old", "unread"])
                else:
                    id = self.dictTree[appName].insert(parent="", index=-1, values=("⭐️ " + i["title"], ", ".join(i["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", "old"])
            # ペアを格納
            self.idUrlPair[id] = {"url": i["url"], "user": i.get("user", {}), "flagNew": 1 if new else 0, "date": i["date"]}



# ================ボタンコマンド================
    def event_open_url(self, event, appName):
        if event.type == "4":
            select = self.dictTree[appName].identify_row(event.y)
        elif event.type == "2":
            select = self.dictTree[appName].focus()
        webbrowser.open(self.idUrlPair[select]["url"])

    
    def push_button_fav(self) -> None:
        select = self.dictTree["Qiita"].focus()
        if select == "":
            pass
        else:
            recordVal = self.dictTree["Qiita"].item(select, "values")
            # すでにお気に入り登録されているかのチェック
            if recordVal[0].startswith("⭐️ "):
                self.dictTree["Qiita"].set(select, "Title", recordVal[0].lstrip("⭐️ "))
                self.favData.remove({"title": recordVal[0].lstrip("⭐️ "), "tags": recordVal[1].split(sep=", "), "user": self.idUrlPair[select]["user"], "url": self.idUrlPair[select]["url"], "date": self.idUrlPair[select]["date"]})
            else:
                self.dictTree["Qiita"].set(select, "Title", "⭐️ " + recordVal[0])
                self.favData.append({"title": recordVal[0], "tags": recordVal[1].split(sep=", "), "user": self.idUrlPair[select]["user"], "url": self.idUrlPair[select]["url"], "date": self.idUrlPair[select]["date"]})
            json.dump(self.favData, open(PGMFILE + "/lib/data/usrfavorite.json", "w"), indent=2, ensure_ascii=False)

    
    def push_button_book(self) -> None:
        select = self.dictTree["Qiita"].focus()
        booklist = [item["title"] for item in self.bookDat]
        if select == "":
            pass
        else:
            recordVal = self.dictTree["Qiita"].item(select, "values")
            # すでにお気に入り登録されているかのチェック
            if recordVal[0] in booklist:
                self.bookDat.remove({"title": recordVal[0].lstrip("⭐️ "), "tags": recordVal[1].split(sep=", "), "user": self.idUrlPair[select]["user"], "url": self.idUrlPair[select]["url"], "date": self.idUrlPair[select]["date"]})
            else:
                self.bookDat.append({"title": recordVal[0].lstrip("⭐️ "), "tags": recordVal[1].split(sep=", "), "user": self.idUrlPair[select]["user"], "url": self.idUrlPair[select]["url"], "date": self.idUrlPair[select]["date"]})
            json.dump(self.bookDat, open(PGMFILE + "/lib/data/bookmark.json", "w"), indent=2, ensure_ascii=False)

    




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