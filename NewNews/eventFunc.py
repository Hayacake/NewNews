# eventFunc.py - ボタンなどのクリックイベントを制御する

import tkinter as tk
import tkinter.ttk as ttk
import webbrowser, os

from typing import Dict, List

PGMFILE = os.path.dirname(__file__)




def open_url(event, tree: ttk.Treeview, pairs: Dict[str, Dict]) -> str:
        """ツリーイベント: rowの記事サイトを開く。URLを返す"""
        if event.type == "4":
            select = tree.identify_row(event.y)
        elif event.type == "2":
            select = tree.focus()
        url = pairs[select]["url"]
        webbrowser.open(url)
        return url