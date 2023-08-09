# text_parse_tool
一种解析.text的python小工具
# 出发点
在项目中，往往存在一些文件需要解析出关键数据，再将解析出来的数据放入数据库，而使用C++、C、Java等语言，比较麻烦，基于此，我们设计了一个可以解析.text文件的python工具
# 库
os：一个可以访问系统文件的库

re：正则表达式库

mysql.connector： 连接和操作 MySQL 数据库
                   安装这个库 执行cmd命令  pip install mysql-connector-python
# 原理
第一步：判断文件夹、文件名字是否为目标文件；

第二部：
  parse_text_file函数内容如下：  
    key_fields = []
    with open(file_path, 'r') as file: #open函数 param1 路径 param2 打开方式  
        for line in file:  #for line in file  遍历文件每一行
            match = re.search(r' +\d+.+', line) #re.search() param1 正则表达式 param2 line
            if match:
                key_fields.append(match.group()) #match不为空 数组使用append函数 利用match的捕获组group函数 返回捕获内容
    return key_fields
    
第三步：
insert_flow_into_db函数 param1 cursor游标在创建时，需要指定表名，以及表中字段
                        param2 key_fields 数组
                        
函数内容：
        遍历数组key_fields
        使用re.findall函数  param1 正则表达式，param2 key_feild 函数返回值值为 匹配的元素列表
        cursor.execute(sql,tuple(matches))  使用游标的execute函数，param1  sql语句 param2 利用tuple将列表转换为元组
        db.commit 提交数据

第四步：
       关闭游标 cursor.close()
       关闭连接  db.close()


# 使用注意
所传文件中，压缩文件为待解析数据，需解压，另外，需要docker部署mysql镜像 然后开启docker
参考命令：docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=your_password -d mysql   your_password为密码

        

