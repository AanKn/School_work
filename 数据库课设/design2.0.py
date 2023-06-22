import tkinter as tk
from tkinter import messagebox
import pymssql
import pyodbc
import datetime

def conn():
    serverName = '127.0.0.1'  # 目的主机ip地址
    dbName = 'library'  # 对应数据库名称
    # connection = pymssql.connect(server=serverName, database=dbName, charset='GBK')  # Window默认身份验证建立连接
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=library;UID=sa;PWD=123456')  # Window默认身份验证建立连接
    return connection


conn = conn()
cursor = conn.cursor()


def menu():
    menu = tk.Tk()
    menu.title('图书借阅管理系统')
    menu.geometry("{0}x{1}+0+0".format(menu.winfo_screenwidth(), menu.winfo_screenheight()))

    image = tk.PhotoImage(file='img.png')
    tk.Label(menu, image=image).place(x=0, y=-240, relwidth=1, relheight=1)

    function1 = tk.Button(menu, text='借书', font=('Arial', 12), width=15, height=1, command=borrow_book)
    function1.place(x=300, y=400)
    function2 = tk.Button(menu, text='增加书籍', font=('Arial', 12), width=15, height=1, command=add_book)
    function2.place(x=500, y=400)
    function3 = tk.Button(menu, text='归还书籍', font=('Arial', 12), width=15, height=1, command=return_book)
    function3.place(x=700, y=400)
    function4 = tk.Button(menu, text='超时罚款缴纳', font=('Arial', 12), width=15, height=1, command=pay_fine)
    function4.place(x=700, y=600)
    function5 = tk.Button(menu, text='查询所有图书信息', font=('Arial', 12), width=15, height=1, command=search_bookinfo)
    function5.place(x=1100, y=400)
    function5_1 = tk.Button(menu, text='按出版社查询图书', font=('Arial', 12), width=15, height=1, command=search_bookinfo1)
    function5_1.place(x=1100, y=500)
    function5_2 = tk.Button(menu, text='按作者查询图书', font=('Arial', 12), width=15, height=1, command=search_bookinfo2)
    function5_2.place(x=1100, y=600)
    function6 = tk.Button(menu, text='查询所有读者信息', font=('Arial', 12), width=15, height=1, command=search_reader_info)
    function6.place(x=900, y=400)
    function6_1 = tk.Button(menu, text='按名查询读者', font=('Arial', 12), width=15, height=1, command=search_readerinfo1)
    function6_1.place(x=900, y=500)
    function6_1 = tk.Button(menu, text='按班级查询读者', font=('Arial', 12), width=15, height=1, command=search_readerinfo2)
    function6_1.place(x=900, y=600)
    function7 = tk.Button(menu, text='查询管理员信息', font=('Arial', 12), width=15, height=1, command=search_managerinfo)
    function7.place(x=500, y=600)
    function8 = tk.Button(menu, text='查询借阅信息', font=('Arial', 12), width=15, height=1, command=search_borrowinfo)
    function8.place(x=500, y=500)
    menu.mainloop()

def search_borrowinfo():
    def show_borrow_records():
        # 查询所有借阅记录信息
        query = "SELECT RecordID, ReaderID, BookID, BorrowNum, BorrowDate,ReturnDate, BorrowNum FROM BorrowRecord"
        cursor.execute(query)
        results = cursor.fetchall()

        # 清空显示区域
        text.delete('1.0', tk.END)

        # 将查询结果显示在界面上
        if results:
            for row in results:
                text.insert(tk.END, f"{row[0]}  {row[1]}  {row[2]}  {row[3]}  {row[4]} {row[5]} {row[6]}\n")
        else:
            text.insert(tk.END, "没有找到借阅记录")

    # 创建主界面
    root = tk.Tk()
    root.title('借阅记录查询')
    root.geometry('800x600')

    # 添加按钮
    button = tk.Button(root, text='显示所有借阅记录', font=('Arial', 14), command=show_borrow_records)
    button.pack(pady=20)

    # 添加显示区域
    text = tk.Text(root, font=('Arial', 14))
    text.pack(fill=tk.BOTH, expand=True)

    # 进入主循环
    root.mainloop()


def borrow_book():

    def borrow_book1():
        book_id, reader_id, num1 = entry_1.get().strip(), entry_2.get().strip(), int(entry_3.get())
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
        print('result1',result1)
        if result1[0]:
            borrowed_num = result1[0]
        else:
            borrowed_num = 0

        # 查询能借多少书
        query2 = ("SELECT BorrowLimit FROM Reader WHERE ReaderID = '%s'"%(reader_id))
        cursor.execute(query2)
        result2 = cursor.fetchone()
        print(result2)
        BorrowLimit = result2[0]

        num1 = int(num1)
        print('num',num1)
        if borrowed_num + num1 > BorrowLimit:
            tk.messagebox.showinfo(title="提示", message='借阅数量超出借阅限制数，无法借阅')
            return
        if stock_num < num1:
            tk.messagebox.showinfo(title="提示", message="库存数量不足")
            return

        # 更新 Book 表中指定 BookID 的书籍库存数量
        update_book_query = ("UPDATE Book SET StockNum = '%s' WHERE BookID = '%s'"%(stock_num - num1, book_id))
        cursor.execute(update_book_query)
        time = datetime.datetime.now().date().strftime("%Y-%m-%d")

        get_RecordID = ("SELECT TOP 1 RecordID FROM BorrowRecord ORDER BY RecordID DESC")
        cursor.execute(get_RecordID)
        Raw_recordid0 = cursor.fetchone()
        Raw_recordid1= Raw_recordid0[0]
        num = int(Raw_recordid1[2:]) + 1
        Record_ID = f"BR{num:03}"
        conn.commit()
        # 插入 BorrowRecord 表中的借阅记录
        insert_record_query = (
            "INSERT INTO BorrowRecord (RecordID,ReaderID, BookID, BorrowNum, BorrowDate) VALUES ('%s','%s', '%s', '%s', '%s')"%(Record_ID,reader_id, book_id, num1, time))
        cursor.execute(insert_record_query)
        conn.commit()

        message = f'借阅成功，借阅了 {num1} 本书'
        tk.messagebox.showinfo(title="提示", message=message)
        root1.destroy()

    root1 = tk.Tk()
    root1.title('借书管理')
    root1.geometry('700x400')

    tk.Label(root1, text='请输入书籍编号', ).place(x=220, y=50)
    entry_1 = tk.Entry(root1, )
    entry_1.place(x=350, y=50)
    tk.Label(root1, text='请输入借阅者编号', ).place(x=220, y=80)
    entry_2 = tk.Entry(root1, )
    entry_2.place(x=350, y=80)
    tk.Label(root1, text='请输入所借本数', ).place(x=220, y=110)
    entry_3 = tk.Entry(root1, )
    entry_3.place(x=350, y=110)


    tk.Button(root1, text='确定', command=borrow_book1).place(x=220, y=230)
    tk.Button(root1, text='返回', command=root1.destroy).place(x=350, y=230)
    root1.mainloop()


def search_bookinfo1():
    def search_book_():
        # 获取用户输入的出版社名称
        press = entry.get().strip()

        # 查询符合条件的书籍信息
        query = ( "SELECT BookID, Title, Author, Press, PublishDate, Category, TotalNum, StockNum FROM Book WHERE Press = '%s'" % ( press))

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
            text.insert(tk.END, "没有找到符合条件的书籍")


    # 创建主界面
    root = tk.Tk()
    root.title('图书查询')
    root.geometry('800x600')

    # 添加输入框和按钮
    label = tk.Label(root, text='请输入出版社名称', font=('Arial', 14))
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


def search_readerinfo1():
    def search_book_():
        # 获取用户输入的出版社名称
        name = entry.get().strip()
        # 查询符合条件的书籍信息
        query = ("SELECT ReaderID,Name,Gender,Age,Class,BorrowLimit FROM Reader WHERE Name = '%s'" % (name))

        cursor.execute(query)
        results = cursor.fetchall()
        print(results)

        # 清空显示区域
        text.delete('1.0', tk.END)

        # 将查询结果显示在界面上
        if results:
            for row in results:
                text.insert(tk.END, f"{row[0]}  {row[1]}  {row[2]}  {row[3]}  {row[4]}  {row[5]}  \n")
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


def search_readerinfo2():
    def search_book_():
        # 获取用户输入的出版社名称
        name = entry.get().strip()
        # 查询符合条件的书籍信息
        query = ("SELECT ReaderID,Name,Gender,Age,Class,BorrowLimit FROM Reader WHERE Class = '%s'" % (name))

        cursor.execute(query)
        results = cursor.fetchall()

        # 清空显示区域
        text.delete('1.0', tk.END)

        # 将查询结果显示在界面上
        if results:
            for row in results:
                text.insert(tk.END, f"{row[0]}  {row[1]}  {row[2]}  {row[3]}  {row[4]}  {row[5]}  \n")
        else:
            text.insert(tk.END, "没有找到符合条件的读者")


    # 创建主界面
    root = tk.Tk()
    root.title('读者查询')
    root.geometry('800x600')

    # 添加输入框和按钮
    label = tk.Label(root, text='请输入读者班级', font=('Arial', 14))
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


def search_bookinfo2():
    def search_book_():
        # 获取用户输入的出版社名称
        Author = entry.get().strip()

        # 查询符合条件的书籍信息
        query = ( "SELECT BookID, Title, Author, Press, PublishDate, Category, TotalNum, StockNum FROM Book WHERE Author = '%s'" % ( Author))

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
            text.insert(tk.END, "没有找到符合条件的书籍")


    # 创建主界面
    root = tk.Tk()
    root.title('图书查询')
    root.geometry('800x600')

    # 添加输入框和按钮
    label = tk.Label(root, text='请输入作者名称', font=('Arial', 14))
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


def add_book():

    def add_book1():
        BookID = entry_1.get().strip()
        Title = entry_2.get().strip()
        Author = entry_3.get().strip()
        Press = entry_4.get().strip()
        PublishDate = entry_5.get().strip()
        Category = entry_6.get().strip()
        TotalNum = int(entry_7.get().strip())
        StockNum = TotalNum
        query = ("INSERT INTO Book (BookID, Title, Author, Press, PublishDate, Category, TotalNum, StockNum) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(BookID, Title,Author,Press,PublishDate,Category,TotalNum,StockNum))
        print(query)
        cursor.execute(query)
        tk.messagebox.showinfo(title="提示", message='添加书籍成功')
        root2.destroy()


    root2 = tk.Tk()
    root2.title('图书信息更新')
    root2.geometry('700x400')

    tk.Label(root2, text='请输入书籍编号', ).place(x=220, y=50)
    entry_1 = tk.Entry(root2, )
    entry_1.place(x=350, y=50)
    tk.Label(root2, text='请输入图书名', ).place(x=220, y=80)
    entry_2 = tk.Entry(root2, )
    entry_2.place(x=350, y=80)
    tk.Label(root2, text='请输入作者', ).place(x=220, y=110)
    entry_3 = tk.Entry(root2, )
    entry_3.place(x=350, y=110)
    tk.Label(root2, text='请输入出版社', ).place(x=220, y=140)
    entry_4 = tk.Entry(root2, )
    entry_4.place(x=350, y=140)
    tk.Label(root2, text='请输入出版日期', ).place(x=220, y=170)
    entry_5 = tk.Entry(root2, )
    entry_5.place(x=350, y=170)
    tk.Label(root2, text='请输入图书类别', ).place(x=220, y=200)
    entry_6 = tk.Entry(root2, )
    entry_6.place(x=350, y=200)
    tk.Label(root2, text='请输入总数', ).place(x=220, y=230)
    entry_7 = tk.Entry(root2, )
    entry_7.place(x=350, y=230)

    tk.Button(root2, text='确定', command=add_book1).place(x=220, y=270)
    tk.Button(root2, text='返回', command=root2.destroy).place(x=350, y=270)


def return_book():
    def return_book1():
        bookid = entry_1.get().strip()
        readerid = entry_2.get().strip()
        ReturnDate = entry_3.get().strip()
        cursor.execute("SELECT * FROM BorrowRecord WHERE BookID='%s' AND ReaderID='%s' AND ReturnDate IS NULL"% (bookid, readerid))
        record = cursor.fetchone()

        if record is None:
            tk.messagebox.showinfo(title="提示", message='该书未被借出')
        else:
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
                cursor.execute("INSERT INTO FineRecord (FineID,ReaderID, BookID,FineAmount,FineStatus) VALUES ('%s', '%s', '%s', '%s','%s')"%(new_FineID,readerid,bookid,  fine,'未缴纳'))
            print("success")
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
            info_text.insert('end',
                             f"罚款ID：{fine_id}，读者ID：{reader_id}，图书ID：{book_id}，罚款金额：{fine_amount}，罚款状态：{fine_status}\n")
            pay_button = tk.Button(info_text, text="缴纳", command=lambda fine_id=fine_id: pay_fine1(fine_id))
            info_text.window_create('end', window=pay_button)
            info_text.insert('end', '\n')

    def pay_fine1(fine_id):
        # 将FineRecord表中对应罚款ID的记录的罚款金额设置为0

        cursor.execute(f"UPDATE FineRecord SET FineStatus='%s' WHERE FineID = '%s'"%('已缴纳',fine_id))
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


def search_bookinfo():
    class BookTableGUI:
        def __init__(self, master):
            # 连接数据库
            self.c = cursor

            # 创建GUI窗口
            self.master = master
            self.master.title('图书列表')
            self.master.geometry('1250x400')

            # 创建表格
            self.table = tk.Frame(self.master)
            self.table.pack(side='top', fill=tk.BOTH, expand=1)

            # 创建表头
            columns = ('BookID', 'Title', 'Author', 'Press', 'PublishDate', 'Category', 'TotalNum', 'StockNum')
            for i, col in enumerate(columns):
                tk.Label(self.table, text=col, relief=tk.RIDGE, width=15, font=('Arial', 12, 'bold')).grid(row=0,
                                                                                                           column=i)

            # 查询并显示数据
            self.current_row = 2
            self.data = self.get_data()
            self.show_data()

            # 创建下一页按钮
            self.next_button = tk.Button(self.master, text='下一页', command=self.show_next)
            self.next_button.pack(side='bottom')

        def get_data(self):
            # 查询BOOK表中的所有记录
            self.c.execute('SELECT * FROM BOOK')
            data = self.c.fetchall()
            return data

        def show_data(self):
            # 显示查询结果
            for row in self.data[0: self.current_row + 10]:
                for i, cell in enumerate(row):
                    tk.Label(self.table, text=cell, relief=tk.RIDGE, width=15, font=('Arial', 12)).grid(
                        row=self.current_row, column=i)
                self.current_row += 1

        def show_next(self):
            # 显示下一页
            if self.current_row + 10 > len(self.data):
                tk.messagebox.showinfo('提示', '没有下一页')
            else:
                self.show_data()

    root = tk.Tk()
    app = BookTableGUI(root)
    root.mainloop()


def search_reader_info():
    class ReaderTableGUI:
        def __init__(self, master):
            # 连接数据库
            self.c = cursor

            # 创建GUI窗口
            self.master = master
            self.master.title('读者列表')
            self.master.geometry('1000x400')

            # 创建表格
            self.table = tk.Frame(self.master)
            self.table.pack(side='top', fill=tk.BOTH, expand=1)

            # 创建表头
            columns = ('ReaderID', 'Name', 'Gender', 'Age', 'Class', 'BorrowLimit')
            for i, col in enumerate(columns):
                tk.Label(self.table, text=col, relief=tk.RIDGE, width=15, font=('Arial', 12, 'bold')).grid(row=0,
                                                                                                           column=i)

            # 查询并显示数据
            self.current_row = 1
            self.data = self.get_data()
            self.show_data()

            # 创建下一页按钮
            self.next_button = tk.Button(self.master, text='下一页', command=self.show_next)
            self.next_button.pack(side='bottom')

        def get_data(self):
            # 查询Reader表中的所有记录
            self.c.execute('SELECT ReaderID, Name, Gender, Age, Class, BorrowLimit FROM Reader')
            data = self.c.fetchall()
            return data

        def show_data(self):
            # 显示查询结果
            for row in self.data[0: self.current_row + 10]:
                for i, cell in enumerate(row):
                    tk.Label(self.table, text=cell, relief=tk.RIDGE, width=15, font=('Arial', 12)).grid(
                        row=self.current_row, column=i)
                self.current_row += 1

        def show_next(self):
            # 显示下一页
            if self.current_row + 10 > len(self.data):
                tk.messagebox.showinfo('提示', '没有下一页')
            else:
                self.show_data()



    root = tk.Tk()
    app = ReaderTableGUI(root)
    root.mainloop()


def search_managerinfo():
    class AdminTableGUI:
        def __init__(self, master):
            # 连接数据库
            self.c = cursor

            # 创建GUI窗口
            self.master = master
            self.master.title('管理员列表')
            self.master.geometry('640x400')

            # 创建表格
            self.table = tk.Frame(self.master)
            self.table.pack(side='top', fill=tk.BOTH, expand=1)

            # 创建表头
            columns = ('AdminID', 'Name', 'Gender', 'Contact')
            for i, col in enumerate(columns):
                tk.Label(self.table, text=col, relief=tk.RIDGE, width=15, font=('Arial', 12, 'bold')).grid(row=0,
                                                                                                           column=i)

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
                    tk.Label(self.table, text=cell, relief=tk.RIDGE, width=15, font=('Arial', 12)).grid(
                        row=self.current_row, column=i)
                self.current_row += 1

        def show_next(self):
            # 显示下一页
            if self.current_row + 10 > len(self.data):
                tk.messagebox.showinfo('提示', '没有下一页')
            else:
                self.show_data()


    root = tk.Tk()
    app = AdminTableGUI(root)
    root.mainloop()


def login():
    # 从输入框中获取用户名和密码
    user = username_entry.get()
    password = password_entry.get()

    if not user.strip() or not password.strip():
        message_label.config(text='请输入用户名和密码')
        return

    # 查询数据库中是否存在指定的用户账户和密码
    query = ("SELECT * FROM Admin WHERE AdminID = '%s' AND Password = '%s'"%(user, password))
    cursor.execute(query )
    result = cursor.fetchone()



    # 判断查询结果是否为空
    if result:
        root.destroy()
        return menu()
    else:
        message_label.config(text='账号或密码错误，请再次尝试')


def register():
    class LoginWindow(tk.Frame):
        def __init__(self, master=None):
            super().__init__(master)
            self.master = master
            self.master.title("管理员登录")
            self.create_widgets()

        def create_widgets(self):
            tk.Label(self.master, text="管理员编号").grid(row=0, column=0)
            self.admin_id_entry = tk.Entry(self.master)
            self.admin_id_entry.grid(row=0, column=1)

            tk.Label(self.master, text="姓名").grid(row=1, column=0)
            self.name_entry = tk.Entry(self.master)
            self.name_entry.grid(row=1, column=1)

            tk.Label(self.master, text="性别").grid(row=2, column=0)
            self.gender_entry = tk.Entry(self.master)
            self.gender_entry.grid(row=2, column=1)

            tk.Label(self.master, text="联系方式").grid(row=3, column=0)
            self.contact_entry = tk.Entry(self.master)
            self.contact_entry.grid(row=3, column=1)

            tk.Label(self.master, text="密码").grid(row=4, column=0)
            self.password_entry = tk.Entry(self.master, show="*")
            self.password_entry.grid(row=4, column=1)

            tk.Label(self.master, text="确认密码").grid(row=5, column=0)
            self.password_conf_entry = tk.Entry(self.master, show="*")
            self.password_conf_entry.grid(row=5, column=1)

            self.submit_button = tk.Button(self.master, text="确认", command=self.submit)
            self.submit_button.grid(row=6, column=0)

            self.cancel_button = tk.Button(self.master, text="取消", command=self.master.quit)
            self.cancel_button.grid(row=6, column=1)

        def submit(self):
            admin_id = self.admin_id_entry.get()
            name = self.name_entry.get()
            gender = self.gender_entry.get()
            contact = self.contact_entry.get()
            password = self.password_entry.get()
            password_conf = self.password_conf_entry.get()

            if password != password_conf:
                tk.messagebox.showerror("错误", "密码不一致")
                return

            cursor.execute("INSERT INTO Admin (AdminID, Name, Gender, Contact, Password) VALUES ('%s','%s','%s','%s','%s')"%(admin_id, name, gender, contact, password))
            conn.commit()
            # conn.close()
            tk.messagebox.showinfo("成功", "管理员信息已添加")

    root = tk.Tk()
    app = LoginWindow(master=root)
    app.mainloop()


root = tk.Tk()
root.title('图书管理系统')
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# 设置背景图片
image = tk.PhotoImage(file='img.png')
label = tk.Label(root, image=image)
label.place(x=0, y=-240, relwidth=1, relheight=1)

tk.Label(root, text='用户名', font=('Arial', 16)).place(x=600, y=400)
username_entry = tk.Entry(root, font=('Arial', 16))
username_entry.place(x=680, y=400)

# 创建密码标签和输入框
tk.Label(root, text='密码', font=('Arial', 16)).place(x=600, y=450)
password_entry = tk.Entry(root, show='*', font=('Arial', 16))
password_entry.place(x=680, y=450)

# 创建登录按钮和注册按钮
tk.Button(root, text='登录', command=login, font=('Arial', 16)).place(x=600, y=500)
tk.Button(root, text='注册', command=register, font=('Arial', 16)).place(x=730, y=500)
tk.Button(root, text='退出', command=root.quit, font=('Arial', 16)).place(x=860, y=500)
# 创建消息标签
message_label = tk.Label(root, text='')
message_label.place(x=600, y=550)

root.mainloop()
