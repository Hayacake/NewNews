#! /usr/bin/python3
# NewNews.py - サーバからデータをダウンロードして表示する

import tkinter as tk
import tkinter.ttk as ttk
import json, datetime, webbrowser
from typing import Dict




# TODO: リストの体裁を整える
# TODO: 未読既読の表示を行う(データをクライアントにとっておいて、サーバーと照合?)
# TODO: 気になるチェックを作る



class WidgetsWindow:
    """widgetを並べたwindowクラス"""
    def __init__(self, root: tk.Tk) -> None:
        self.root = root


        # Pack形式で積んでいく(gridにしたい)
        # リスト
        self.column = ('Title', 'Tags', 'Date')
        self.tree = ttk.Treeview(self.root, columns=self.column)

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

        # レコードの追加
        self.load_file()

        # イベントの追加
        self.tree.tag_bind("item", "<Double-ButtonPress>", self.event_open_url)
        self.tree.tag_bind("item", "<Return>", self.event_open_url)


        # スクロールバー
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)


        # 描画する
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=15, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    


    def load_file(self) -> None:
        # ファイルを読み込む
        # NOTE: これはテスト用のデータ
        newsData = json.load(open("NewNews/lib/data/qiitaNewItems.json"))

        # URLを開くためにid: URLのペアを作る
        self.idUrlPair: Dict[str, str] = {}

        for item in newsData:
            date = datetime.datetime.fromisoformat(item["date"])
            id = self.tree.insert(parent="", index="end", values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")), tags="item")
            # ペアを格納
            self.idUrlPair[id] = item["url"]   
    


    def event_open_url(self, event):
        print(str(event.type))
        if event.type == "4":
            select = self.tree.identify_row(event.y)
            webbrowser.open(self.idUrlPair[select])
        elif event.type == "2":
            select = self.tree.focus()
            webbrowser.open(self.idUrlPair[select])
        
    
    




def main():
    root = tk.Tk()
    root.title("test for tkinter")
    root.geometry("1000x800")
    ww = WidgetsWindow(root)
    root.mainloop()



if __name__ == "__main__":
    main()