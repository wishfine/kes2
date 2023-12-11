
import tkinter as tk
import json
from tkinter import scrolledtext, END


class credit:
    def __init__(self):
        self.xls = None
        self.root1 = tk.Tk()
        self.root1.title("课程管理系统")
        
        self.x_int = 0
        l1 = tk.Label(self.root1, text="本学期需要修得的最大学分数(24~30)：")
        l1.pack()  
        self.xls_text = tk.StringVar()
        self.xls = tk.Entry(self.root1, textvariable=self.xls_text)
        self.xls.insert(10, "25")
        self.xls.pack()
        tk.Button(self.root1, text="确定", command=self.on_click).pack()
        print(self.x_int)
        # 居中显示
        width = 300
        height = 100
        screenwidth = self.root1.winfo_screenwidth()
        screenheight = self.root1.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root1.geometry(alignstr)
        self.root1.resizable(0, 0)
        self.root1.mainloop()

    def on_click(self):
        self.x = self.xls.get()
        print(type(self.x))
        self.x_int = int(self.x)
        try:
            if 24 <= (int)(self.x) <= 30:
                self.root1.withdraw()
                self.root1.quit()
            if (int)(self.x) < 20 or (int)(self.x) > 30:
                self.xls.delete(0, END)
        except ValueError:
            self.xls.delete(0, END)
