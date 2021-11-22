#! /usr/bin/python3
# NewNews.py - サーバからデータをダウンロードして表示する

import tkinter as tk
import tkinter.ttk as ttk
import json, datetime, webbrowser, os
from typing import Dict, List

from getDataFromServer import get_data_from_server

PGMFILE = os.path.dirname(__file__)

# TODO: リストの体裁を整える
# TODO: 未読既読の表示を行う(データをクライアントにとっておいて、サーバーと照合?)
# TODO: ブックマーク機能


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

        # レコードの追加
        self.load_file(self.favData)


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
        
    


    def load_file(self, favData: List[Dict]) -> None:
        # ファイルを読み込む
        # TODO: 非同期処理で最新の情報を手に入れる
        newsData = get_data_from_server()

        # お気に入りのタイトルリスト
        listFavTitle = [item["title"] for item in favData]

        # URLを開くために{id: URL, user: user情報}のペアを作る
        self.idUrlPair: Dict[str, str] = {}

        for item in newsData:
            date = datetime.datetime.fromisoformat(item["date"])
            if item["title"] not in listFavTitle:
                id = self.tree.insert(parent="", index="end", values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags="item")
            else:
                id = self.tree.insert(parent="", index="end", values=("⭐️ " + item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags="item")
            # ペアを格納
            self.idUrlPair[id] = {"url": item["url"], "user": item.get("user", {})}

    
    
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
    root.title("test for tkinter")
    root.geometry("1000x800")
    ww = WidgetsWindow(root)
    root.mainloop()



if __name__ == "__main__":
    main()