# dataLoad.py - NewNews.pyのデータロードで使われる関数を格納する

import tkinter as tk
import tkinter.ttk as ttk
import json, logging, os, datetime, threading, time
from typing import Dict, List, Union

PGMFILE = os.path.dirname(__file__)



def load_local_data(tree: ttk.Treeview, appname: str, favdat: List[Dict] = [], bookdat: List[Dict] = []) -> Dict:
    """ローカルからデータをロードする"""
    logging.info(f"start loading local data: {appname}")

    # データを読み込む
    dat = json.load(open(PGMFILE + f"/lib/data/{appname}.json"))
    # データを表示する
    pairs = _insert_row(tree=tree, data=dat, favdat=favdat, bookdat=bookdat, appname=appname)

    logging.info(f"success load local data: {appname}")
    return dat, pairs


def load_server_data(tree: ttk.Treeview, appname: str, thevent: threading.Event, favdat: List[Dict] = [], bookdat: List[Dict] = []) -> Dict:
    """サーバからデータをダウンロードする"""
    logging.info(f"start loading server data: {appname}")

    
def load_server_data(tree: ttk.Treeview, appname: str, thevent: threading.Event, favdat: List[Dict] = [], bookdat: List[Dict] = []) -> Dict:
    """Webからデータをダウンロードする"""
    logging.info(f"start loading newest data: {appname}")





def _insert_row(tree: ttk.Treeview, data: List[Dict], favdat: List[Dict], bookdat: List[Dict], appname: str) -> Dict:
    # 表示しないさまざまな情報を格納しておく
    id_url_pairs = {}
    # お気に入りリスト中のタイトルをしまう
    list_fav = [item["title"] for item in favdat]
    # ブックマークリスト中のタイトルをしまう
    list_book = [item["title"] for item in bookdat]

    for item in data[::-1]:
        # 日付の読み込み
        date = datetime.datetime.fromisoformat(item["date"])
        # お気に入りリストの確認
        if item["title"] not in list_fav:
            # お気に入りでない時
            if item["title"] in list_book:
                id = tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", appname, "booked"])
            else:
                id = tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", appname])
        else:
            # お気に入りの時
            if item["title"] in list_book:
                id = tree.insert(parent="", index=-1, values=("⭐️ " + item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", appname, "booked"])
            else:
                id = tree.insert(parent="", index=-1, values=("⭐️ " + item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=["item", appname])
        # 情報の格納
        id_url_pairs[id] = {"title": item["title"],"url": item["url"], "user": item.get("user", {}), "date": item["date"]}
    tree.tag_configure(tagname="booked", background="#eebbcb")          # bookmarkの色を変える
    return id_url_pairs



def load_fav() -> List[Dict]:
        favdat = json.load(open(PGMFILE + "/lib/data/usrfavorite.json"))
        return favdat

def load_book() -> List[Dict]:
    bookdat = json.load(open(PGMFILE + "/lib/data/bookmark.json"))
    return bookdat