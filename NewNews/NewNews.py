#! /Users/kakeru/opt/anaconda3/bin/python3
# NewNews.py - サーバからデータをダウンロードして表示する

# NOTE: 処理の状況を伝えるメッセージ
# TODO: リストの体裁を整える



import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Frame, messagebox
import json, datetime, webbrowser, os, threading, logging, traceback
from typing import Dict, List, Tuple

from Qiita import get_new_items
from getDataFromServer import get_data_from_server

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s - %(message)s")

PGMFILE = os.path.dirname(__file__)



class WidgetsWindow():
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        # ボタンのセッティング
        self.btnframe = tk.Frame(self.root)                     # ボタンの枠
        self.btnFav = ttk.Button(self.btnframe, text="Favorite" """, command=self.push_button_fav""")
        self.btnbook = ttk.Button(self.btnframe, text="Bookmark" """, command=self.push_button_book""")
        # ボタンの描画
        self.btnframe.pack(side=tk.TOP, anchor=tk.W, padx=15, pady=7)
        self.btnFav.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=0)
        self.btnbook.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=0)

        # タブのセッティング
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=0)
        # タブをしまうようのリスト
        self.tab_dict: Dict[str, ttk.Frame] = {}
        # ツリーをしまうようのリスト
        self.tree_dict: Dict[str, Tuple[ttk.Treeview, ttk.Scrollbar]] = {}

        # Qiitaのツリーを作る
        self.make_list("Qitta")



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

        # 種々のデータを格納する
        self.tab_dict[appname] = tab
        self.tree_dict[appname] = (tree, scrollbar)





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