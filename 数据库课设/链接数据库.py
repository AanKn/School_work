# -*- coding: GBK -*-

import pymssql

serverName = '127.0.0.1'  # 目的主机ip地址
dbName = 'library'  # 对应数据库名称
connect = pymssql.connect(server=serverName, database=dbName, charset='GBK')  # Window默认身份验证建立连接


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
print(increment_string('F010'))
if connect:
    print("数据库已连接成功")
cursor = connect.cursor()  # 创建一个游标对象，python里的sql语句都要通过cursor来执行
book_id = 'B007'
reader_id = 'R005'
new_FineID, readerid, bookid, fine='F011','R003','B003',5
# query = "INSERT INTO FineRecord (FineID, ReaderID, BookID, FineAmount, FineStatus) VALUES (?, ?, ?, ?, ?)"
# values = (new_FineID, readerid, bookid, fine, '未缴纳')
# cursor.execute(
#     "INSERT INTO FineRecord (FineID,ReaderID, BookID,FineAmount,FineStatus) VALUES ('%s', '%s', '%s', '%s','%s')" % (new_FineID, readerid, bookid, fine, '未缴纳'))

# cursor.execute(query, values)
print('ok')
connect.commit()  # 提交cursor.close()#关闭游标
connect.close()  # 关闭连接（如果不关闭，python会一直占用）
