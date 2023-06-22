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

def borrow_book():

    def borrow_book1():
        book_id, reader_id, num = entry_1.get().strip(), entry_2.get().strip(), int(entry_3.get())
        print(book_id, reader_id, num )
        # 查询 Book 表中指定 BookID 的书籍库存数量
        query = ("SELECT StockNum FROM Book WHERE BookID ='%s'"%(book_id))
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)
        if result:
            stock_num = result[0]
        else:
            stock_num = 0

        # 查询借了多少本书
        query1 = ("SELECT SUM(BorrowNum) FROM BorrowRecord WHERE ReaderID ='%s' AND ReturnDate IS NULL"%(reader_id))
        cursor.execute(query1)
        result1 = cursor.fetchone()
        print('res1:',result1)
        if result1:
            borrowed_num = result1[0]
        else:
            borrowed_num = 0

        # 查询能借多少书
        query2 = ("SELECT BorrowLimit FROM Reader WHERE ReaderID = '%s'"%(reader_id))
        cursor.execute(query2)
        result2 = cursor.fetchone()
        print(result2)
        BorrowLimit = result2[0]

        num = int(num)
        if borrowed_num + num > BorrowLimit:
            tk.messagebox.showinfo(title="提示", message='借阅数量超出借阅限制数，无法借阅')
            return
        if stock_num < num:
            tk.messagebox.showinfo(title="提示", message="库存数量不足")
            return

        # 更新 Book 表中指定 BookID 的书籍库存数量
        update_book_query = ("UPDATE Book SET StockNum = '%s' WHERE BookID = '%s'"%(stock_num - num, book_id))
        cursor.execute(update_book_query)
        conn.commit()
        time = datetime.datetime.now().date().strftime("%Y-%m-%d")
        # 插入 BorrowRecord 表中的借阅记录
        insert_record_query = (
            "INSERT INTO BorrowRecord (ReaderID, BookID, BorrowNum, BorrowDate) VALUES ('%s', '%s', '%s', '%s')"%(reader_id, book_id, num, time))
        cursor.execute(insert_record_query, ())
        conn.commit()

        message = f'借阅成功，借阅了 {num} 本书'
        tk.messagebox.showinfo(title="提示", message=message)
        root1.destroy()

    root1 = tk.Tk()
    root1.title('图书信息删除')
    root1.geometry('700x400')

    tk.Label(root1, text='请输入书籍编号', ).place(x=220, y=50)
    entry_1 = tk.Entry(root1, )
    entry_1.place(x=350, y=50)
    tk.Label(root1, text='请输入借阅者编号', ).place(x=220, y=80)
    entry_2 = tk.Entry(root1, )
    entry_2.place(x=350, y=80)
    tk.Label(root1, text='请输入所借本书', ).place(x=220, y=110)
    entry_3 = tk.Entry(root1, )
    entry_3.place(x=350, y=110)
    print(entry_1.get(), entry_3.get(), entry_2.get())


    tk.Button(root1, text='确定', command=borrow_book1).place(x=220, y=230)
    tk.Button(root1, text='返回', command=root1.destroy).place(x=350, y=230)
    root1.mainloop()

borrow_book()