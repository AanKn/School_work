import tkinter as tk
from tkinter import messagebox
import pymssql
import datetime

def conn():
    serverName = '127.0.0.1'  # 目的主机ip地址
    dbName = 'library'  # 对应数据库名称
    connect = pymssql.connect(server=serverName, database=dbName, charset='GBK')  # Window默认身份验证建立连接
    return connect


conn = conn()
cursor = conn.cursor()
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
            sql1 = "INSERT INTO Admin (AdminID, Name, Gender, Contact, Password) VALUES ('%s','%s','%s','%s','%s')"%(admin_id, name, gender, contact, password)
            cursor.execute(sql1)
            conn.commit()
            conn.close()
            tk.messagebox.showinfo("成功", "管理员信息已添加")
            root.destroy()

    root = tk.Tk()
    app = LoginWindow(master=root)
    app.mainloop()
register()