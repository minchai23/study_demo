import pymysql


# Cursor类型
# 1. Cursor 每行数据以元组形式返回
# 2. DictCursor 每行数据以dict形式返回，key式列名
# 3. SSCursor和SSDictCursor 服务端游标，处理大数据，减少内存使用；execute执行后，少量多次获取数据

# Cursor执行sql
# execute 第一个参数query是sql语句，%s占位符；第二个参数args是sql中变量值，用元组表示
# executemany 参数基本同execute，只是第二个参数是多个元组组成的Iterable对象，比如list中存放多个tuple

# Cursor获取数据
# fetchone 返回一行数据，返回类型Cursor -> tuple   DictCursor -> dict，没有查询到数据返回None
# fetchall 返回所有数据list(x)，没有查询到数据返回list()
# fetchmany 参数size指定一次返回几条数据，返回list(x)，没有查询到数据返回tuple()

connection = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="mysql.1024",
                             database="study",
                             charset="utf8mb4",
                             cursorclass=pymysql.cursors.SSDictCursor)
with connection:
    with connection.cursor() as cursor:
        sql = "select name, gender, birth_date from study.family_members where birth_date >= %s"
        cursor.execute(sql, ('1990-01-01',))
        
        while True:
            line = cursor.fetchmany(1)
            if line is None or len(line) == 0:
                break
            row = line[0]
            print(row['name'], row['gender'], row['birth_date'])
    connection.commit()
