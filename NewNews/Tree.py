# dataLoad.py - NewNews.pyのデータロードで使われる関数を格納する

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import json, logging, os, datetime, threading, time, traceback
from typing import Dict, List, Tuple, Union

import eventFunc
from getDataFromServer import get_data_from_server
from Qiita import get_new_items

PGMFILE = os.path.dirname(__file__)



class NewsTree():
    def __init__(self, tab: ttk.Frame, appname: str, favdat, bookdat) -> None:
        self.appname = appname

        # ツリーを作る
        self.tree = ttk.Treeview(tab, columns=('Title', 'Tags', 'Date'))
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

        # スクロールバーを作る
        scrollbar = ttk.Scrollbar(tab, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # 描画する
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=0, pady=0)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        print(type(favdat))
        # ローカルのデータを読み込む(メインの記事の時)
        self.dat, self.pairs, self.read_list = self.load_local_data(self.tree, appname, favdat=favdat, bookdat=bookdat)

        # イベントを設定する
        self.tree.tag_bind("item", "<Double-ButtonPress>", lambda event:eventFunc.open_url(event, self.tree, self.pairs))
        self.tree.tag_bind("item", "<Return>", lambda event: eventFunc.open_url(event, self.tree, self.pairs))



    def load_local_data(self, tree: ttk.Treeview, appname: str, favdat: List[Dict] = [], bookdat: List[Dict] = []) -> Tuple[List[Dict], Dict, List[str]]:
        """ローカルからデータをロードする"""
        logging.info(f"start loading local data: {appname}")

        #  データを読み込む
        dat = json.load(open(PGMFILE + f"/lib/data/{appname}.json"))
        # ローカルのデータは全て既読である
        read_list = [item["title"] for item in dat]
        # データを表示する
        pairs = eventFunc._insert_row(tree=tree, data=dat, favdat=favdat, bookdat=bookdat, read=read_list, appname=appname, )

        logging.info(f"success load local data: {appname}")
        return dat, pairs, read_list


    def load_server_data(self, tree: ttk.Treeview, appname: str, thevent: threading.Event, favdat: List[Dict] = [], bookdat: List[Dict] = [], read_list: List[str] = []) -> Tuple[List[Dict], Dict]:
        """サーバからデータをダウンロードする"""
        logging.info(f"start loading server data: {appname}")
        # ファイルを読み込む
        while True:
            try:
                dat = get_data_from_server()
                pairs = eventFunc._insert_row(tree, dat, favdat=favdat, bookdat=bookdat, read=read_list, appname=appname)
                return dat, pairs
            except Exception as err:
                retry = tkinter.messagebox.askretrycancel(title="ERROR", message=traceback.format_exc())
                if not retry:
                    break

    
    def load_newest_data(self, tree: ttk.Treeview, appname: str, thevent: threading.Event, favdat: List[Dict] = [], bookdat: List[Dict] = [], read_list: List[str] = []) -> Tuple[List[Dict], Dict]:
        """Webからデータをダウンロードする"""
        logging.info(f"start loading newest data: {appname}")
        return [{"test": 1}], {"Idkaj": "test"}