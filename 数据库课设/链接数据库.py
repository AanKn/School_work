# -*- coding: GBK -*-

import pymssql

serverName = '127.0.0.1'  # Ŀ������ip��ַ
dbName = 'library'  # ��Ӧ���ݿ�����
connect = pymssql.connect(server=serverName, database=dbName, charset='GBK')  # WindowĬ�������֤��������


def increment_string(string):
    # �ָ��ַ���
    prefix = string[:-3]  # ��ȡǰ׺����
    number = int(string[-3:])  # ��ȡ���ֲ��ֲ�ת��Ϊ����

    # ���ּ�1
    number += 1

    # ��ʽ��Ϊ��λ���ֵ��ַ���
    new_number = str(number).zfill(3)

    # �ϲ�Ϊ���ַ���
    new_string = prefix + new_number

    return new_string
print(increment_string('F010'))
if connect:
    print("���ݿ������ӳɹ�")
cursor = connect.cursor()  # ����һ���α����python���sql��䶼Ҫͨ��cursor��ִ��
book_id = 'B007'
reader_id = 'R005'
new_FineID, readerid, bookid, fine='F011','R003','B003',5
# query = "INSERT INTO FineRecord (FineID, ReaderID, BookID, FineAmount, FineStatus) VALUES (?, ?, ?, ?, ?)"
# values = (new_FineID, readerid, bookid, fine, 'δ����')
# cursor.execute(
#     "INSERT INTO FineRecord (FineID,ReaderID, BookID,FineAmount,FineStatus) VALUES ('%s', '%s', '%s', '%s','%s')" % (new_FineID, readerid, bookid, fine, 'δ����'))

# cursor.execute(query, values)
print('ok')
connect.commit()  # �ύcursor.close()#�ر��α�
connect.close()  # �ر����ӣ�������رգ�python��һֱռ�ã�
