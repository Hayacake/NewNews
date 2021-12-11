# dataLoad.py - NewNews.pyのデータロードで使われる関数を格納する

import tkinter as tk
import tkinter.ttk as ttk
import json, logging, os, datetime
from typing import Dict, List

PGMFILE = os.path.dirname(__file__)



def load_local_data(tree: ttk.Treeview, appname: str, favdat: List[Dict] = []) -> Dict:
    """ローカルからデータをロードする"""
    logging.info("start loading local data")

    # データを読み込む
    dat = json.load(open(PGMFILE + f"/lib/data/{appname}.json"))
    # データを表示する
    pairs = _insert_row(tree=tree, data=dat, favdat=favdat)

    logging.info("success load local data")
    return dat, pairs




def _insert_row(tree: ttk.Treeview, data: Dict, favdat: List[Dict] = []) -> Dict:
    # 表示しないさまざまな情報を格納しておく
    id_url_pairs = {}
    # お気に入りリスト中のタイトルをしまう
    list_fav = [item["title"] for item in favdat]

    for item in data[::-1]:
        # 日付の読み込み
        date = datetime.datetime.fromisoformat(item["date"])
        if item["title"] not in list_fav:
            # お気に入りでない時
            id = tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item"])
        else:
            # お気に入りの時
            id = tree.insert(parent="", index=-1, values=("⭐️ " + item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item"])
        # 情報の格納
        id_url_pairs[id] = {"url": item["url"], "user": item.get("user", {}), "date": item["date"]}
    return id_url_pairs



def load_fav() -> List[Dict]:
        favdat = json.load(open(PGMFILE + "/lib/data/usrfavorite.json"))
        return favdat