# dataLoad.py - NewNews.pyのデータロードで使われる関数を格納する

import tkinter as tk
import tkinter.ttk as ttk
import json, logging, os, datetime
from typing import Dict

PGMFILE = os.path.dirname(__file__)



def load_local_data(tree: ttk.Treeview, appname: str) -> Dict:
    """ローカルからデータをロードする"""
    logging.info("start loading local data")

    # データを読み込む
    dat = json.load(open(PGMFILE + f"/lib/data/{appname}.json"))
    # データを表示する
    pairs = _insert_row(tree=tree, data=dat)

    logging.info("success load local data")
    return dat, pairs




def _insert_row(tree: ttk.Treeview, data: Dict) -> Dict:
    # 表示しないさまざまな情報を格納しておく
    id_url_pairs = {}
    for item in data[::-1]:
        # 日付の読み込み
        date = datetime.datetime.fromisoformat(item["date"])
        # ツリーに表示する
        id = tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item"])
        # 情報の格納
        id_url_pairs[id] = {"url": item["url"], "user": item.get("user", {}), "date": item["date"]}
    return id_url_pairs

