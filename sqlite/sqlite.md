sqlite命令行工具
- 下载sqlite命令行工具，比如sqlite3.exe
- 连接数据库 sqlite3 sqlite.db
- 查询表信息 select * from sqlite_master;
- 退出 .exit

python sqlite3标准库
```python
import sqlite3

# 连接数据库
connect = sqlite3.connect("sqlite.db")

# 获取光标（用来执行sql）
cursor = connect.cursor()

# 隐式开启事务
# 执行sql: ?占位符，防止sql注入
cursor.execute("update tb_software set lang = ? where name = ?", ("java", "neo4j"))

# 回滚事务
# connect.rollback()

# 提交事务
connect.commit()

# 关闭光标
cursor.close()

# 断开连接
connect.close()
```