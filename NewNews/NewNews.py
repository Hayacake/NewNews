#! /Users/kakeru/opt/anaconda3/bin/python3
# NewNews.py - サーバからデータをダウンロードして表示する

# NOTE: 処理の状況を伝えるメッセージ
# TODO: リストの体裁を整える



import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import json, datetime, webbrowser, os, threading, logging, traceback
from typing import Dict, List

from Qiita import get_new_items
from getDataFromServer import get_data_from_server

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s - %(message)s")

PGMFILE = os.path.dirname(__file__)



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