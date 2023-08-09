#import os
#import re
#import mysql.connector

# 打开并解析 .text 文档
#def parse_text_file(file_path):
#    key_fields = []
#    with open(file_path, 'r') as file:
#        for line in file:
#             假设关键字段在每行以 'Key: Value' 的格式出现
#            match = re.search(r'Key:(.+)', line)
#            if match:
#                key_fields.append(match.group(1))
#    return key_fields

# 连接到 MySQL 数据库
#db = mysql.connector.connect(
#    host="192.168.6.5",
#    user="root",
#    password="123456",
#    database="mysql"
#)

# 解析文本文件并将关键字段插入到数据库
#def insert_key_fields_into_db(key_fields):
#    cursor = db.cursor()
#    for key_field in key_fields:
#        sql = "INSERT INTO test (name,value) VALUES (%s,%s)"
#        values = (key_field,"1",)
#        cursor.execute(sql, values)
#        db.commit()

#directory = "./"  # 替换为包含 .text 文件的文件夹路径
# 使用正则表达式匹配以一串数字开头的文件夹名字
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

# 解析单个 .text 文档，提取关键字段
def parse_text_file(file_path):
    key_fields = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r' +\d+.+', line)
            if match:
                key_fields.append(match.group())
    return key_fields

# 连接到 MySQL 数据库
db = mysql.connector.connect(
    host="192.168.6.5",
    user="root",
    password="123456",
    database="mysql"
)

# 创建数据库flow表
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
 # 创建数据库flow表
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

# 插入关键字段到数据库
def insert_flow_into_db(cursor, key_fields):
    sql = "INSERT INTO flow (STEP,A,B,C,D,E,F,J,K,L,M,N) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for key_field in key_fields:
        pattern = r'-?\d+\.\d+|\d+'  # 匹配整数和浮点数
        matches = re.findall(pattern, key_field)
        #matches.pop(0)
        #result_string = ','.join(matches)
        #result_string_with_parentheses = '(' + result_string +')'
        cursor.execute(sql,tuple(matches))
    db.commit()
def insert_measure_into_db(cursor, key_fields):
    sql = "INSERT INTO measure (STEP,A,B,C,D,E,F,J,K,L,M) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for key_field in key_fields:
        pattern = r'-?\d+\.\d+|\d+'  # 匹配整数和浮点数
        matches = re.findall(pattern, key_field)
        #matches.pop(0)
        #result_string = ','.join(matches)
        #result_string_with_parentheses = '(' + result_string +')'
        cursor.execute(sql,tuple(matches))
    db.commit()


# 关闭数据库连接
def close_connection():
    db.close()

if __name__ == "__main__":
    directory = "./"  # 替换为包含 .text 文件的文件夹路径
    
    flow_cursor = db.cursor()
    create_flow_table(flow_cursor)

    measure_cursor = db.cursor()
    create_measure_table(measure_cursor)

    # 使用正则表达式匹配以一串数字开头的文件夹名字
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
