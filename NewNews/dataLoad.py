# dataLoad.py - NewNews.pyのデータロードで使われる関数を格納する

import tkinter as tk
import tkinter.ttk as ttk
import json, logging, os, datetime, threading, time
from typing import Dict, List, Tuple, Union

from getDataFromServer import get_data_from_server
from Qiita import get_new_items

PGMFILE = os.path.dirname(__file__)



def load_local_data(tree: ttk.Treeview, appname: str, favdat: List[Dict] = [], bookdat: List[Dict] = []) -> Tuple[List[Dict], Dict, List[str]]:
    """ローカルからデータをロードする"""
    logging.info(f"start loading local data: {appname}")

    # データを読み込む
    dat = json.load(open(PGMFILE + f"/lib/data/{appname}.json"))
    # ローカルのデータは全て既読である
    read_list = [item["title"] for item in dat]
    # データを表示する
    pairs = _insert_row(tree=tree, data=dat, favdat=favdat, bookdat=bookdat, read=read_list, appname=appname, )

    logging.info(f"success load local data: {appname}")
    return dat, pairs, read_list


def load_server_data(tree: ttk.Treeview, appname: str, thevent: threading.Event, favdat: List[Dict] = [], bookdat: List[Dict] = [], read_list: List[str] = []) -> Dict:
    """サーバからデータをダウンロードする"""
    logging.info(f"start loading server data: {appname}")
    time.sleep(5)
    logging.debug("wait 5 sec!")
    thevent.set()

    
def load_newest_data(tree: ttk.Treeview, appname: str, thevent: threading.Event, favdat: List[Dict] = [], bookdat: List[Dict] = [], read_list: List[str] = []) -> Dict:
    """Webからデータをダウンロードする"""
    logging.info(f"start loading newest data: {appname}")
    logging.debug("wait another thread")
    thevent.wait()
    logging.debug("finish waiting")





def _insert_row(tree: ttk.Treeview, data: List[Dict], favdat: List[Dict], bookdat: List[Dict], read: List[str], appname: str) -> Dict:
    # 表示しないさまざまな情報を格納しておく
    id_url_pairs = {}
    # お気に入りリスト中のタイトルをしまう
    list_fav = [item["title"] for item in favdat]
    # ブックマークリスト中のタイトルをしまう
    list_book = [item["title"] for item in bookdat]

    for item in data[::-1]:
        # 日付の読み込み
        date = datetime.datetime.fromisoformat(item["date"])

        # ブックマークの確認
        tgs = ["item", appname, "booked"] if item["title"] in list_book else ["item", appname]
        if item["title"] not in read: tgs.append("unread")

        # お気に入りリストの確認
        if item["title"] not in list_fav:
            # お気に入りでない時
            id = tree.insert(parent="", index=-1, values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=tgs)
        else:
            # お気に入りの時
            id = tree.insert(parent="", index=-1, values=("⭐️ " + item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags=tgs)
        # 情報の格納
        id_url_pairs[id] = {"title": item["title"],"url": item["url"], "user": item.get("user", {}), "date": item["date"]}
    tree.tag_configure(tagname="unread", background="#a0d8ef")          # 未読の色を変える
    tree.tag_configure(tagname="booked", background="#eebbcb")          # bookmarkの色を変える
    return id_url_pairs



def load_fav() -> List[Dict]:
        favdat = json.load(open(PGMFILE + "/lib/data/usrfavorite.json"))
        return favdat

def load_book() -> List[Dict]:
    bookdat = json.load(open(PGMFILE + "/lib/data/bookmark.json"))
    return bookdat