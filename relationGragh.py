
import tkinter as tk
import json
from tkinter import scrolledtext, END


class relationGragh:

    def __init__(self, res):
        self.res = res
        self.falseOrTrue = 0
        self.root2 = tk.Toplevel()
        self.root2.title("课程管理系统")


        self.canvas = tk.Canvas(self.root2, width=1500, height=650, background="white")
        self.canvas.place(x=0, y=50)

        # 允许调整大小
        self.root2.resizable(True, True)

        self.canvas.create_line(180, 25, 180, 650, dash=(4, 4))
        self.canvas.create_line(360, 25, 360, 650, dash=(4, 4))
        self.canvas.create_line(540, 25, 540, 650, dash=(4, 4))
        self.canvas.create_line(720, 25, 720, 650, dash=(4, 4))
        self.canvas.create_line(900, 25, 900, 650, dash=(4, 4))
        self.canvas.create_line(1080, 25, 1080, 650, dash=(4, 4))
        self.canvas.create_line(1260, 25, 1260, 650, dash=(4, 4))
        for i in range(8):
            tk.Label(self.root2, bd=1, text='第' + str(i + 1) + '学期',width=8,height=1,
                     font=("Consolas", 10)).place(
                x=i * 180 + 55,
                y=27)

        self.normal_button = tk.Button(self.root2, command=self.display_relation,  text="显示课程先修关系",width=16,
                                        height=1,
                                       cursor="hand2", relief="ridge", bd=1,font=("Consolas", 10))
        self.normal_button2 = tk.Button(self.root2, command=self.goback, text="返回",width=4,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,font=("Consolas", 10))

        self.normal_button.place(x=25, y=0)
        self.normal_button2.place(x=155, y=0)


        for i in range(len(self.res)):
            for j in range(len(self.res[i])):
                self.canvas.create_rectangle(i * 180 + 25, j * 50 + 10, i * 180 + 150, j * 50 + 40)
                tk.Label(self.root2, text=self.res[i][j],bg= 'white').place(x=i * 180 + 35, y=j * 50 + 65)
        # 居中显示
        width = 1400
        height = 700
        screenwidth = self.root2.winfo_screenwidth()
        screenheight = self.root2.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root2.geometry(alignstr)
        # 大小不变
        self.root2.resizable(0, 0)

        self.root2.mainloop()

    def display_relation(self):
        self.falseOrTrue += 1
        startX = 0  # 划线的四个坐标
        startY = 0
        endX = 0
        endY = 0
        f = open(r"data\test.json", encoding='UTF-8')
        setting = json.load(f)
        for ii in range(len(setting)):
            for i in range(len(self.res)):
                for j in range(len(self.res[i])):
                    if self.res[i][j] == setting[ii]["CName"]:
                        startX = i * 180 + 150
                        startY = j * 50 + 25
                    if self.res[i][j] == setting[ii]["toName"]:
                        endX = i * 180 + 25
                        endY = j * 50 + 25
            if (self.falseOrTrue % 2) == 1:
                self.canvas.create_line(startX, startY, endX, endY, arrow=tk.LAST, fill='black')
            else:
                self.canvas.create_line(startX, startY, endX, endY, arrow=tk.LAST, fill="white")

        pass

    def goback(self):
        self.root2.withdraw()
