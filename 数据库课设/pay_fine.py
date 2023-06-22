import tkinter as tk
from tkinter import messagebox
import pymssql
import datetime

def connect():
    serverName = '127.0.0.1'  # 目的主机ip地址
    dbName = 'library'  # 对应数据库名称
    connection = pymssql.connect(server=serverName, database=dbName, charset='GBK')  # Window默认身份验证建立连接
    return connection

conn = connect()
cursor = conn.cursor()
def pay_fine():
    def Search():
        # 从输入框中获取读者ID
        reader_id = reader_id_entry.get()

        # 查询FineRecord表中读者ID等于输入的读者ID的所有记录
        cursor.execute(f"SELECT * FROM FineRecord WHERE ReaderID = '{reader_id}'")
        records = cursor.fetchall()

        # 将查询结果显示在文本框中，并为每个记录创建一个按钮
        info_text.delete('1.0', 'end')
        for record in records:
            fine_id, reader_id, book_id, fine_amount, fine_status = record
            info_text.insert('end', f"罚款ID：{fine_id}，读者ID：{reader_id}，图书ID：{book_id}，罚款金额：{fine_amount}，罚款状态：{fine_status}\n")
            pay_button = tk.Button(info_text, text="缴纳", command=lambda fine_id=fine_id: pay_fine1(fine_id))
            info_text.window_create('end', window=pay_button)
            info_text.insert('end', '\n')

    def pay_fine1(fine_id):
        # 将FineRecord表中对应罚款ID的记录的罚款金额设置为0

        cursor.execute(f"UPDATE FineRecord SET FineStatus='已缴纳' WHERE FineID = '{fine_id}'")
        conn.commit()

        # 弹出一个消息框，提示罚款已缴纳
        tk.messagebox.showinfo("缴纳成功", "罚款已缴纳！")

    # 创建主窗口
    root = tk.Tk()
    root.title("缴纳罚款")

    # 创建读者ID输入框和登录按钮
    reader_id_label = tk.Label(root, text="读者ID：")
    reader_id_label.pack()
    reader_id_entry = tk.Entry(root)
    reader_id_entry.pack()
    login_button = tk.Button(root, text="查询", command=Search)
    login_button.pack()

    # 创建文本框用于显示FineRecord表中的记录
    info_text = tk.Text(root)
    info_text.pack()

    # 启动GUI主循环
    root.mainloop()