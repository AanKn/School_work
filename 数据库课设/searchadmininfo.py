import tkinter as tk
from tkinter import messagebox
import pymssql
import datetime

def conn():
    serverName = '127.0.0.1'  # 目的主机ip地址
    dbName = 'library'  # 对应数据库名称
    connect = pymssql.connect(server=serverName, database=dbName, charset='gbk')  # Window默认身份验证建立连接
    return connect


conn = conn()
cursor = conn.cursor()
def search_managerinfo():
    class AdminTableGUI:
        def __init__(self, master):
            # 连接数据库
            self.c = cursor

            # 创建GUI窗口
            self.master = master
            self.master.title('管理员列表')
            self.master.geometry('800x400')

            # 创建表格
            self.table = tk.Frame(self.master)
            self.table.pack(side='top', fill=tk.BOTH, expand=1)

            # 创建表头
            columns = ('AdminID', 'Name', 'Gender', 'Contact')
            for i, col in enumerate(columns):
                tk.Label(self.table, text=col, relief=tk.RIDGE, width=15, font=('Arial', 12, 'bold')).grid(row=0, column=i)

            # 查询并显示数据
            self.current_row = 1
            self.data = self.get_data()
            self.show_data()

            # 创建下一页按钮
            self.next_button = tk.Button(self.master, text='下一页', command=self.show_next)
            self.next_button.pack(side='bottom')

        def get_data(self):
            # 查询Admin表中的所有记录
            self.c.execute('SELECT AdminID, Name, Gender, Contact FROM Admin')
            data = self.c.fetchall()
            return data

        def show_data(self):
            # 显示查询结果
            for row in self.data[0: self.current_row + 10]:
                for i, cell in enumerate(row):
                    tk.Label(self.table, text=cell, relief=tk.RIDGE, width=15, font=('Arial', 12)).grid(row=self.current_row, column=i)
                self.current_row += 1

        def show_next(self):
            # 显示下一页
            if self.current_row + 10 > len(self.data):
                tk.messagebox.showinfo('提示', '没有下一页')
            else:
                self.show_data()
        #
        # def __del__(self):
        #     # 关闭数据库连接
        #     self.conn.close()
    root = tk.Tk()
    app = AdminTableGUI(root)
    root.mainloop()
search_managerinfo()
