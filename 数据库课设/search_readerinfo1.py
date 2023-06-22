import tkinter as tk
from tkinter import messagebox
import pymssql
import pyodbc
import datetime

def connect():
    serverName = '127.0.0.1'  # Ŀ������ip��ַ
    dbName = 'library'  # ��Ӧ���ݿ�����
    # connection = pymssql.connect(server=serverName, database=dbName, charset='GBK')  # WindowĬ�������֤��������
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=library;UID=sa;PWD=123456')  # WindowĬ�������֤��������
    return connection

conn = connect()
cursor = conn.cursor()

def search_readerinfo1():
    def search_book_():
        # ��ȡ�û�����ĳ���������
        name = entry.get().strip()
        # ��ѯ�����������鼮��Ϣ
        query = ("SELECT ReaderID,Name,Gender,Age,Class,BorrowLimit FROM Book WHERE Name = '%s'" % ( name))

        cursor.execute(query)
        results = cursor.fetchall()
        print(results)

        # �����ʾ����
        text.delete('1.0', tk.END)

        # ����ѯ�����ʾ�ڽ�����
        if results:
            for row in results:
                text.insert(tk.END, f"{row[0]}  {row[1]}  {row[2]}  {row[3]}  {row[4]}  {row[5]}  {row[6]}  {row[7]}\n")
        else:
            text.insert(tk.END, "û���ҵ����������Ķ���")


    # ����������
    root = tk.Tk()
    root.title('���߲�ѯ')
    root.geometry('800x600')

    # ��������Ͱ�ť
    label = tk.Label(root, text='�������������', font=('Arial', 14))
    label.pack(pady=20)
    entry = tk.Entry(root, font=('Arial', 14))
    entry.pack(pady=20)
    button = tk.Button(root, text='��ѯ', font=('Arial', 14), command=search_book_)
    button.pack(pady=20)

    # �����ʾ����
    text = tk.Text(root, font=('Arial', 14))
    text.pack(fill=tk.BOTH, expand=True)

    # ������ѭ��
    root.mainloop()