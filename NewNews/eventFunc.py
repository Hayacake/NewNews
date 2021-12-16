# eventFunc.py - ボタンなどのクリックイベントを制御する

import tkinter as tk
import tkinter.ttk as ttk
import webbrowser, os, json, datetime

from typing import Dict, List

PGMFILE = os.path.dirname(__file__)




def open_url(event, tree: ttk.Treeview, pairs: Dict[str, Dict]) -> str:
        """ツリーイベント: rowの記事サイトを開く。URLを返す"""
        if event.type == "4":
            select = tree.identify_row(event.y)
        elif event.type == "2":
            select = tree.focus()
        # 既読への切り替え
        tgs = tree.item(select, "tags"); tgs = list(tgs)
        if "unread" in tgs:
            tgs.remove("unread"); tree.item(select, tags=tgs)
        url = pairs[select]["url"]
        webbrowser.open(url)



def load_fav() -> List[Dict]:
        favdat = json.load(open(PGMFILE + "/lib/data/usrfavorite.json"))
        return favdat

def load_book() -> List[Dict]:
    bookdat = json.load(open(PGMFILE + "/lib/data/bookmark.json"))
    return bookdat



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