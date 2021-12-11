#! /Users/kakeru/opt/anaconda3/bin/python3
# NewNews.py - サーバからデータをダウンロードして表示する

# TODO: お気に入り機能とブックマーク機能
# BUG: お気に入り機能とブックマーク機能が一つのタブにしか対応していない(タブが変更された時にボタンを更新するようにすれば解決可能?)
# TODO: サーバーと最新の情報を入手する
# NOTE: 処理の状況を伝えるメッセージ
# TODO: configファイルから読み込むアプリを決定する
# TODO: リストの体裁を整える


import tkinter as tk
import tkinter.ttk as ttk
import json, datetime, os, threading, logging, traceback
from typing import Dict, List, Tuple

import dataLoad, eventFunc
from Qiita import get_new_items
from getDataFromServer import get_data_from_server

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s - %(message)s")

PGMFILE = os.path.dirname(__file__)



class WidgetsWindow():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        # 種々のリストのセッティング
        self.tab_dict: Dict[str, ttk.Frame] = {}                # タブをしまうようのリスト
        self.tree_dict: Dict[str, Tuple[ttk.Treeview, ttk.Scrollbar]] = {}      # ツリーをしまうようのリスト
        self.dat = {}       # データをしまうリスト
        self.pairs = {}     # リストの表示情報をしまうリスト
        self.favdat = []


        # ボタンのセッティング
        self.btnframe = tk.Frame(self.root)                     # ボタンの枠
        self.btnFav = ttk.Button(self.btnframe, text="Favorite", command=lambda: self.fav_button_cmd("Qiita"))
        self.btnbook = ttk.Button(self.btnframe, text="Bookmark" """, command=self.push_button_book""")
        # ボタンの描画
        self.btnframe.pack(side=tk.TOP, anchor=tk.W, padx=15, pady=7)
        self.btnFav.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=0)
        self.btnbook.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=0)

        # タブのセッティング
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=0)

        # Qiitaのツリーを作る
        self.make_list("Qiita")
        


    def make_list(self, appname: str) -> None:
        """タブとツリーを作る"""
        # タブを作る
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=appname)

        # ツリーを作る
        tree = ttk.Treeview(tab, columns=('Title', 'Tags', 'Date'))
        # 列の設定
        tree.column('#0',width=0, stretch='no')
        tree.column('Title', anchor='center', width=200, stretch=True)
        tree.column('Tags',anchor='w', width=200)
        tree.column('Date', anchor='center', width=5, minwidth=5)
        # 列の見出し設定
        tree.heading('#0',text='')
        tree.heading('Title', text='Title',anchor='center')
        tree.heading('Tags', text='Tags', anchor='w')
        tree.heading('Date',text='Date', anchor='center')

        # スクロールバーを作る
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        # 描画する
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=0, pady=0)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ローカルのデータを読み込む
        dat, pairs = dataLoad.load_local_data(tree, appname)
        
        # イベントを設定する
        tree.tag_bind("item", "<Double-ButtonPress>", lambda event:eventFunc.open_url(event, tree, pairs))
        tree.tag_bind("item", "<Return>", lambda event: eventFunc.open_url(event, tree, pairs))

        # 種々のデータを格納する
        # タブとツリーを格納する
        self.tab_dict[appname] = tab                    # タブをしまう
        self.tree_dict[appname] = (tree, scrollbar)     # ツリーをしまう
        self.dat[appname] = dat
        self.pairs[appname] = pairs

    

    def fav_button_cmd(self, appname: str) -> List[Dict]:
        """お気に入りボタン"""
        # BUG: 一つのタブにしか対応していない(タブが変更された時にボタンを更新するようにすれば解決可能?)
        select = self.tree_dict[appname][0].focus()
        if select == "":
            pass
        else:
            select_value = self.tree_dict[appname][0].item(select, "values")
            if select_value[0].startswith("⭐️ "):
                # すでにお気に入り登録されている時
                self.tree_dict[appname][0].set(select, "Title", select_value[0][3:])
                self.favdat.remove({"title": select_value[0][3:], "tags": select_value[1].split(sep=", "), "user": self.pairs[appname][select]["user"], "url": self.pairs[appname][select]["url"], "date": self.pairs[appname][select]["date"]})
            else:
                # お気に入り登録されていない時
                self.tree_dict[appname][0].set(select, "Title", "⭐️ " + select_value[0])
                self.favdat.append({"title": select_value[0], "tags": select_value[1].split(sep=", "), "user": self.pairs[appname][select]["user"], "url": self.pairs[appname][select]["url"], "date": self.pairs[appname][select]["date"]})
        json.dump(self.favdat, open(PGMFILE + "/lib/data/usrfavorite.json", "w"), indent=2, ensure_ascii=False)
        



    





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