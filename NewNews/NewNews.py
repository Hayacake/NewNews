#! /usr/bin/python3
# NewNews.py - サーバからデータをダウンロードして表示する

import tkinter as tk
import tkinter.ttk as ttk




# TODO: テストデータを引っ張ってきてそれをGUIにリスト形式で表示する

class WidgetsWindow:
    """widgetを並べたwindowクラス"""
    def __init__(self, root: tk.Tk) -> None:
        # メインフレームを作る
        self.tf = tk.Frame(root)
        self.tf.grid(row=0, column=0, padx=15, pady=15)

        # メインフレームに配置していく
        # ラベル
        self.label = tk.Label(self.tf, text="こんにちは")
        self.label.grid(row=0, column=0, sticky="w")

        # エントリー
        self.entry = tk.Entry(self.tf)
        self.entry.grid(row=0, column=1)

        # ボタン
        self.btn1 = tk.Button(self.tf, text="参照")
        self.btnExe = tk.Button(self.tf, text="実行")
        self.btn1.grid(row=0, column=2)
        self.btnExe.grid(row=1, column=1)



def main():
    root = tk.Tk()
    root.title("test for tkinter")
    root.geometry("500x100")
    ww = WidgetsWindow(root)
    root.mainloop()



if __name__ == "__main__":
    main()