#! /usr/bin/python3
# NewNews.py - サーバからデータをダウンロードして表示する

import tkinter as tk
import tkinter.ttk as ttk
import json, datetime




# TODO: テストデータを引っ張ってきてそれをGUIにリスト形式で表示する

class WidgetsWindow:
    """widgetを並べたwindowクラス"""
    def __init__(self, root: tk.Tk) -> None:
        # Pack形式で積んでいく(gridにしたい)
        # リスト
        self.column = ('Title', 'Tags', 'Date')
        self.tree = ttk.Treeview(root, columns=self.column)

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

        # 描画する
        self.tree.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)
    

    def load_file(self) -> None:
        # ファイルを読み込む
        # NOTE: これはテスト用のデータ
        newsData = json.load(open("NewNews/lib/data/qiitaNewItems.json"))
        for item in newsData:
            date = datetime.datetime.fromisoformat(item["date"])
            self.tree.insert(parent="", index="end", values=(item["title"], ", ".join(item["tags"]), date.strftime("%h %d - %H:%M")))




def main():
    root = tk.Tk()
    root.title("test for tkinter")
    root.geometry("1000x800")
    ww = WidgetsWindow(root)
    root.mainloop()



if __name__ == "__main__":
    main()