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

def return_book():
    def return_book1():
        bookid = entry_1.get().strip()
        readerid = entry_2.get().strip()
        ReturnDate = entry_3.get().strip()
        cursor.execute("SELECT * FROM BorrowRecord WHERE BookID='%s' AND ReaderID='%s' AND ReturnDate IS NULL"% (bookid, readerid))
        record = cursor.fetchone()
        print(record)

        if record is None:
            tk.messagebox.showinfo(title="提示", message='该书未被借出')
        else:
            # borrow_date = datetime.strptime(record[3], '%Y-%m-%d')
            return_date = datetime.datetime.strptime(ReturnDate, '%Y-%m-%d').date()

            # 计算借阅天数和罚款金额
            days = (return_date - record[3]).days
            fine = max(0, (days - 30) * 0.5*record[5])


            cursor.execute('SELECT FineID FROM FineRecord ORDER BY FineID')
            fine_id = cursor.fetchall()

            def increment_string(string):
                # 分割字符串
                prefix = string[:-3]  # 获取前缀部分
                number = int(string[-3:])  # 获取数字部分并转换为整数

                # 数字加1
                number += 1

                # 格式化为三位数字的字符串
                new_number = str(number).zfill(3)

                # 合并为新字符串
                new_string = prefix + new_number

                return new_string

            new_FineID = increment_string(fine_id[-1][0])

            # 更新借阅记录和罚款记录
            print(ReturnDate,record[0])
            cursor.execute("UPDATE BorrowRecord SET ReturnDate='%s' WHERE RecordID='%s'" %(ReturnDate, record[0]))
            tk.messagebox.showinfo(title="提示", message='还书成功')
            if fine > 0:
                cursor.execute("INSERT INTO FineRecord (FineID,ReaderID, BookID,FineAmount,FineStatus) VALUES ('%s', '%s', '%s', '%s','%s')"%(new_FineID,bookid, readerid, fine,'未缴纳'))

            root2.destroy()

        return
    root2 = tk.Tk()
    root2.title('还书')
    root2.geometry('700x400')

    tk.Label(root2, text='请输入书籍编号', ).place(x=220, y=50)
    entry_1 = tk.Entry(root2, )
    entry_1.place(x=350, y=50)
    tk.Label(root2, text='请输入借书者编号', ).place(x=220, y=80)
    entry_2 = tk.Entry(root2, )
    entry_2.place(x=350, y=80)
    tk.Label(root2, text='请输入还书时间', ).place(x=220, y=110)
    entry_3 = tk.Entry(root2, )
    entry_3.place(x=350, y=110)

    tk.Button(root2, text='确定', command=return_book1).place(x=220, y=270)
    tk.Button(root2, text='返回', command=root2.destroy).place(x=350, y=270)
    root2.mainloop()
return_book()