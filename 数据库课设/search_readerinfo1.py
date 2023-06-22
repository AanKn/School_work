import tkinter as tk
from tkinter import messagebox
import pymssql
import pyodbc
import datetime

def connect():
    serverName = '127.0.0.1'  # 目的主机ip地址
    dbName = 'library'  # 对应数据库名称
    # connection = pymssql.connect(server=serverName, database=dbName, charset='GBK')  # Window默认身份验证建立连接
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=library;UID=sa;PWD=123456')  # Window默认身份验证建立连接
    return connection

conn = connect()
cursor = conn.cursor()

def search_readerinfo1():
    def search_book_():
        # 获取用户输入的出版社名称
        name = entry.get().strip()
        # 查询符合条件的书籍信息
        query = ("SELECT ReaderID,Name,Gender,Age,Class,BorrowLimit FROM Book WHERE Name = '%s'" % ( name))

        cursor.execute(query)
        results = cursor.fetchall()
        print(results)

        # 清空显示区域
        text.delete('1.0', tk.END)

        # 将查询结果显示在界面上
        if results:
            for row in results:
                text.insert(tk.END, f"{row[0]}  {row[1]}  {row[2]}  {row[3]}  {row[4]}  {row[5]}  {row[6]}  {row[7]}\n")
        else:
            text.insert(tk.END, "没有找到符合条件的读者")


    # 创建主界面
    root = tk.Tk()
    root.title('读者查询')
    root.geometry('800x600')

    # 添加输入框和按钮
    label = tk.Label(root, text='请输入读者名称', font=('Arial', 14))
    label.pack(pady=20)
    entry = tk.Entry(root, font=('Arial', 14))
    entry.pack(pady=20)
    button = tk.Button(root, text='查询', font=('Arial', 14), command=search_book_)
    button.pack(pady=20)

    # 添加显示区域
    text = tk.Text(root, font=('Arial', 14))
    text.pack(fill=tk.BOTH, expand=True)

    # 进入主循环
    root.mainloop()