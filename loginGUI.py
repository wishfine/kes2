

import tkinter as tk
import json
from tkinter import scrolledtext, END, ttk

import main
from tkinter.scrolledtext import ScrolledText
import json
import random

from Concrete_schedule import schedule
from Credit import credit
from gragh import Gragh
from relationGragh import relationGragh


class loginGUI:
    def __init__(self, account):
        self.account = account
        self.temp_res = []
        self.end_res = []
        self.window = tk.Toplevel()
        self.window.title('课程管理系统')


        self.canvas = tk.Canvas(self.window, height=370, width=600)  # 创建画布
        self.canvas.pack(side='top')  # 放置画布（为上端）
        #学期按钮
        self.course_button1 = tk.Button(self.window, command=lambda: self.course_interface(1), text="大一上", width=16,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1, compound="center",
                                        font=("Consolas", 10))
        self.course_button2 = tk.Button(self.window, command=lambda: self.course_interface(2), text="大一下", width=16,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,  compound="center",
                                        font=("Consolas", 10))
        self.course_button3 = tk.Button(self.window, command=lambda: self.course_interface(3), text="大二上", width=16,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,  compound="center",
                                        font=("Consolas", 10))
        self.course_button4 = tk.Button(self.window, command=lambda: self.course_interface(4), text="大二下", width=16,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,  compound="center",
                                        font=("Consolas", 10))
        self.course_button5 = tk.Button(self.window, command=lambda: self.course_interface(5), text="大三上", width=16,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,  compound="center",
                                        font=("Consolas", 10))
        self.course_button6 = tk.Button(self.window, command=lambda: self.course_interface(6), text="大三下", width=16,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,  compound="center",
                                        font=("Consolas", 10))
        self.course_button7 = tk.Button(self.window, command=lambda: self.course_interface(7), text="大四上", width=16,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,  compound="center",
                                        font=("Consolas", 10))
        self.course_button8 = tk.Button(self.window, command=lambda: self.course_interface(8), text="大四下", width=16,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,  compound="center",
                                        font=("Consolas", 10))
        #功能按钮
        self.normal_button1 = tk.Button(self.window, command=self.go_back, text="返回",width=4,
                                        height=1, cursor="hand2", relief="ridge", bd=1,font=("Consolas", 10))
        self.normal_button2 = tk.Button(self.window, command=self.make_course, text="生成课表", width=8,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1, compound="center",
                                        font=("Consolas", 10))
        self.normal_button3 = tk.Button(self.window, command=lambda: self.adjust_course(-1), text="上移",width=8,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,font=("Consolas", 10))
        self.normal_button4 = tk.Button(self.window, command=lambda: self.adjust_course(1), text="下移",width=8,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,font=("Consolas", 10))
        self.normal_button5 = tk.Button(self.window, command=self.laststep, text="撤销",width=4,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1, font=("Consolas", 10))
        self.normal_button6 = tk.Button(self.window, command=self.save, text="保存",width=4,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,font=("Consolas", 10))
        self.normal_button7 = tk.Button(self.window, command=self.relation, text="生成有向图",width=10,
                                        height=1,
                                        cursor="hand2", relief="ridge", bd=1,font=("Consolas", 10))
        
        self.scr1 = scrolledtext.ScrolledText(self.window, width=16, height=5, font=("宋体", 10))
        self.scr2 = scrolledtext.ScrolledText(self.window, width=16, height=5, font=("宋体", 10))
        self.scr3 = scrolledtext.ScrolledText(self.window, width=16, height=5, font=("宋体", 10))
        self.scr4 = scrolledtext.ScrolledText(self.window, width=16, height=5, font=("宋体", 10))
        self.scr5 = scrolledtext.ScrolledText(self.window, width=16, height=5, font=("宋体", 10))
        self.scr6 = scrolledtext.ScrolledText(self.window, width=16, height=5, font=("宋体", 10))
        self.scr7 = scrolledtext.ScrolledText(self.window, width=16, height=5, font=("宋体", 10))
        self.scr8 = scrolledtext.ScrolledText(self.window, width=16, height=5, font=("宋体", 10))

        self.L1 = tk.Label(self.window, text="输入需要调整的课程名：",font=("Consolas", 10))

        self.xls_text = tk.StringVar()
        self.xls = tk.Entry(self.window, textvariable=self.xls_text, width=15)
        self.xls.insert(15, "集合与图论")

        self.xls_text2 = tk.StringVar()
        self.courseChosen = ttk.Combobox(self.window, width=14, textvariable=self.xls_text2,font=("Consolas", 10))
        self.courseChosen['values'] = ("近代史", "思修", "毛概", "马原", "大学英语", "高级英语",
                                       "高级英语阅读", "体育1", "体育2", "体育3", "体育4", "高数1", "大物1", "大物2", "大物实验1",
                                       "大物实验2", "电路与电子技术", "电子与电子技术实验", "高数2", "集合与图论", "代数与逻辑", "数据结构与算法",
                                       "线性代数", "概率论与数理方程", "物联网工程导论", "算法设计与分析", "数字逻辑", "数字逻辑实验", "计算机组成原理",
                                       "计算机组成原理课设", "计算机系统结构", "计算机网络", "操作系统", "高级语言程序设计", "高级语言程序设计课设", "面向对象程序设计",
                                       "汇编语言程序设计", "单片机原理与技术", "嵌入式系统", "无线传感器网络", "无线传感器网络课设", "嵌入式技术课设", "编译原理",
                                       "微型计算机接口", "RFID技术", "数据库原理", "数据结构与算法课设", "软件工程引论", "软件类综合课设", "计算机网络课设",
                                       "物联网感知课设", "物联网工程实践课设"
                                       )  # 设置下拉列表的值

        self.courseChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        self.course_button1.place(x=10, y=65)
        self.course_button2.place(x=150, y=65)
        self.course_button3.place(x=290, y=65)
        self.course_button4.place(x=430, y=65)
        self.course_button5.place(x=10, y=205)
        self.course_button6.place(x=150, y=205)
        self.course_button7.place(x=290, y=205)
        self.course_button8.place(x=430, y=205)
        self.normal_button1.place(x=550, y=10)
        self.normal_button2.place(x=483, y=10)
        self.normal_button3.place(x=335, y=333)
        self.normal_button4.place(x=405, y=333)
        self.normal_button5.place(x=24, y=333)
        self.normal_button6.place(x=22, y=10)
        self.normal_button7.place(x=64, y=10)
        self.scr1.place(x=10, y=110)  # 滚动文本框在页面的位置
        self.scr2.place(x=150, y=110)
        self.scr3.place(x=290, y=110)
        self.scr4.place(x=430, y=110)
        self.scr5.place(x=10, y=250)
        self.scr6.place(x=150, y=250)
        self.scr7.place(x=300, y=250)
        self.scr8.place(x=430, y=250)
        # self.xls.place(x=200, y=333)
        self.L1.place(x=64, y=333)
        self.courseChosen.place(x=206, y=333)
        # 主窗口循环显示

        # 居中显示
        width = 600
        height = 370
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.window.geometry(alignstr)
        # 大小不变
        self.window.resizable(0, 0)

        ff = open(r".\data\data.json", encoding='UTF-8')
        settingg = json.load(ff)

        for i in range(len(settingg)):
            if settingg[i]["account"] == self.account:
                self.restoChart(settingg[i]["course"])
                self.end_res = settingg[i]["course"]
                f = open(r"data\test.json", encoding='UTF-8')
                setting = json.load(f)

                self.g = Gragh(setting, settingg[i]["g"], settingg[i]["course"])

        self.window.mainloop()

    def course_interface(self, courseNumber):
        print(courseNumber)
        if len(self.scr1.get(1.0, 'end')) != 1:
            every_Schedule = schedule(courseNumber, self.g.res)
            if courseNumber == 1:
                tk.messagebox.showinfo(title='课程管理系统', message='进入第一学期课表')
            if courseNumber == 2:
                tk.messagebox.showinfo(title='课程管理系统', message='进入第二学期课表')
            if courseNumber == 3:
                tk.messagebox.showinfo(title='课程管理系统', message='进入第三学期课表')
            if courseNumber == 4:
                tk.messagebox.showinfo(title='课程管理系统', message='进入第四学期课表')
            if courseNumber == 5:
                tk.messagebox.showinfo(title='课程管理系统', message='进入第五学期课表')
            if courseNumber == 6:
                tk.messagebox.showinfo(title='课程管理系统', message='进入第六学期课表')
            if courseNumber == 7:
                tk.messagebox.showinfo(title='课程管理系统', message='进入第七学期课表')
            if courseNumber == 8:
                tk.messagebox.showinfo(title='课程管理系统', message='进入第八学期课表')
        else:
            tk.messagebox.showinfo(title='课程管理系统', message='错误！请先生成课表！')

    def make_course(self):
        f = open(r"data\test.json", encoding='UTF-8')
        setting = json.load(f)
        getCreditSum = credit()
        print("continue")
        maxCreditSum = getCreditSum.x_int
        self.g = Gragh(setting, maxCreditSum, [])
        res = self.g.topoSort()
        self.end_res = res
        ff = open(r".\data\data.json", encoding='UTF-8')
        settingg = json.load(ff)
        for i in range(len(settingg)):
            if settingg[i]["account"] == self.account:
                settingg[i]["course"] = res
                settingg[i]["g"] = maxCreditSum
        with open(r".\data\data.json", 'w') as fw:
            json.dump(settingg, fw)

        self.restoChart(res)

    def restoChart(self, res):
        if self.scr2.get(1.0, 'end') != "":
            self.scr1.delete(1.0, 'end')  # 删除所有元素
            self.scr2.delete(1.0, 'end')
            self.scr3.delete(1.0, 'end')
            self.scr4.delete(1.0, 'end')
            self.scr5.delete(1.0, 'end')
            self.scr6.delete(1.0, 'end')
            self.scr7.delete(1.0, 'end')
            self.scr8.delete(1.0, 'end')
        for i in range(len(res)):
            if i == 0:
                scr = self.scr1
            elif i == 1:
                scr = self.scr2
            elif i == 2:
                scr = self.scr3
            elif i == 3:
                scr = self.scr4
            elif i == 4:
                scr = self.scr5
            elif i == 5:
                scr = self.scr6
            elif i == 6:
                scr = self.scr7
            elif i == 7:
                scr = self.scr8
            for j in range(len(res[i])):
                if j == 0:
                    scr.insert(END, res[i][j])
                else:
                    scr.insert(END, "\n" + res[i][j])

    def adjust_course(self, location):

        coursename = self.courseChosen.get()

        if len(self.scr1.get(1.0, 'end')) != 1:
            res_adjust = self.g.adjustcourse(coursename, location)
            if not res_adjust:
                pass
            else:
                self.temp_res.append(self.g.resBackUp)
                self.end_res = res_adjust
                self.restoChart(res_adjust)
        else:
            pass

    def laststep(self):
        print("退一步")
        if not self.temp_res:
            pass
        else:
            resNow = self.temp_res[len(self.temp_res) - 1]
            self.end_res = resNow
            self.temp_res.pop()
            self.restoChart(resNow)

    def save(self):
        ff = open(r".\data\data.json", encoding='UTF-8')
        settingg = json.load(ff)
        for i in range(len(settingg)):
            if settingg[i]["account"] == self.account:
                settingg[i]["course"] = self.end_res
        with open(r".\data\data.json", 'w') as fw:
            json.dump(settingg, fw)

        tk.messagebox.showinfo(title='课程管理系统', message='保存成功！')

    def relation(self):
        self.relation1 = relationGragh(self.end_res)

    def go_back(self):
        self.window.withdraw()
        main.main()

