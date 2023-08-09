#import os
#import re
#import mysql.connector

# �򿪲����� .text �ĵ�
#def parse_text_file(file_path):
#    key_fields = []
#    with open(file_path, 'r') as file:
#        for line in file:
#             ����ؼ��ֶ���ÿ���� 'Key: Value' �ĸ�ʽ����
#            match = re.search(r'Key:(.+)', line)
#            if match:
#                key_fields.append(match.group(1))
#    return key_fields

# ���ӵ� MySQL ���ݿ�
#db = mysql.connector.connect(
#    host="192.168.6.5",
#    user="root",
#    password="123456",
#    database="mysql"
#)

# �����ı��ļ������ؼ��ֶβ��뵽���ݿ�
#def insert_key_fields_into_db(key_fields):
#    cursor = db.cursor()
#    for key_field in key_fields:
#        sql = "INSERT INTO test (name,value) VALUES (%s,%s)"
#        values = (key_field,"1",)
#        cursor.execute(sql, values)
#        db.commit()

#directory = "./"  # �滻Ϊ���� .text �ļ����ļ���·��
# ʹ��������ʽƥ����һ�����ֿ�ͷ���ļ�������
#folder_pattern = re.compile(r'^\d+')

#for filename in os.listdir(directory):
#        if filename.endswith(".text"):
#            file_path = os.path.join(directory, filename)
#            parsed_fields = parse_text_file(file_path)
#            insert_key_fields_into_db(parsed_fields)
#db.close

import os
import re
import mysql.connector

# �������� .text �ĵ�����ȡ�ؼ��ֶ�
def parse_text_file(file_path):
    key_fields = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r' +\d+.+', line)
            if match:
                key_fields.append(match.group())
    return key_fields

# ���ӵ� MySQL ���ݿ�
db = mysql.connector.connect(
    host="192.168.6.5",
    user="root",
    password="123456",
    database="mysql"
)

# �������ݿ�flow��
def create_flow_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flow (
        id INT AUTO_INCREMENT PRIMARY KEY,
        STEP VARCHAR(255),
        A VARCHAR(255),
        B VARCHAR(255),
        C  VARCHAR(255),
        D VARCHAR(255),
        E VARCHAR(255),
        F VARCHAR(255),
        J VARCHAR(255),
        K VARCHAR(255),
        L VARCHAR(255),
        M VARCHAR(255),
        N VARCHAR(255)
    )
    """)
 # �������ݿ�flow��
def create_measure_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS measure (
        id INT AUTO_INCREMENT PRIMARY KEY,
        STEP VARCHAR(255),
        A VARCHAR(255),
        B VARCHAR(255),
        C VARCHAR(255),
        D VARCHAR(255),
        E VARCHAR(255),
        F VARCHAR(255),
        J VARCHAR(255),
        K VARCHAR(255),
        L VARCHAR(255),
        M VARCHAR(255)
    )
    """)

# ����ؼ��ֶε����ݿ�
def insert_flow_into_db(cursor, key_fields):
    sql = "INSERT INTO flow (STEP,A,B,C,D,E,F,J,K,L,M,N) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for key_field in key_fields:
        pattern = r'-?\d+\.\d+|\d+'  # ƥ�������͸�����
        matches = re.findall(pattern, key_field)
        #matches.pop(0)
        #result_string = ','.join(matches)
        #result_string_with_parentheses = '(' + result_string +')'
        cursor.execute(sql,tuple(matches))
    db.commit()
def insert_measure_into_db(cursor, key_fields):
    sql = "INSERT INTO measure (STEP,A,B,C,D,E,F,J,K,L,M) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for key_field in key_fields:
        pattern = r'-?\d+\.\d+|\d+'  # ƥ�������͸�����
        matches = re.findall(pattern, key_field)
        #matches.pop(0)
        #result_string = ','.join(matches)
        #result_string_with_parentheses = '(' + result_string +')'
        cursor.execute(sql,tuple(matches))
    db.commit()


# �ر����ݿ�����
def close_connection():
    db.close()

if __name__ == "__main__":
    directory = "./"  # �滻Ϊ���� .text �ļ����ļ���·��
    
    flow_cursor = db.cursor()
    create_flow_table(flow_cursor)

    measure_cursor = db.cursor()
    create_measure_table(measure_cursor)

    # ʹ��������ʽƥ����һ�����ֿ�ͷ���ļ�������
    folder_pattern = re.compile(r'^\d+')

    for filename in os.listdir(directory):
        folder_path = os.path.join(directory, filename)
        if os.path.isdir(folder_path) and folder_pattern.match(filename):
            for text_filename in os.listdir(folder_path):
                if text_filename.endswith("flow.text"):
                    text_file_path = os.path.join(folder_path, text_filename)
                    parsed_fields = parse_text_file(text_file_path)
                    insert_flow_into_db(flow_cursor, parsed_fields)
                if text_filename.endswith("measure.text"):
                    text_file_path = os.path.join(folder_path, text_filename)
                    parsed_fields = parse_text_file(text_file_path)
                    insert_measure_into_db(measure_cursor, parsed_fields)

    flow_cursor.close()
    measure_cursor.close()
    close_connection()
