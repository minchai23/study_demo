import sqlite3

def main():
    # 连接数据库并获取游标
    connect = sqlite3.connect("sqlite.db")
    cursor = connect.cursor()

    # 创建表
    cursor.execute("""
        create table if not exists tb_software (
            id integer primary key autoincrement,
            name text,
            repo text,
            home text,
            lang text,
            unique (name, repo)
        )
    """)

    # 插入数据，?占位
    software_data = [
        ("zlib", "https://github.com/madler/zlib", "https://zlib.net", "C"),
        ("sqlite", "https://github.com/sqlite/sqlite", "https://sqlite.org", "C"),
        ("neo4j", "https://github.com/neo4j/neo4j", "https://neo4j.com", "Java")
    ]
    for name, repo, home, lang in software_data:
        cursor.execute("""
            insert into tb_software 
            (name, repo, home, lang)
            values (?, ?, ?, ?)
        """, (name, repo, home, lang))
    
    connect.commit()

    # 更新数据
    cursor.execute("""
        update tb_software
        set lang = ?
        where name = ?
    """, ("java", "neo4j"))
    connect.commit()

    # 删除数据
    cursor.execute("""
        delete from tb_software
        where name = ?
    """, ("neo4j",))
    connect.commit()

    # 关闭游标和连接
    cursor.close()
    connect.close()

if __name__ == "__main__":
    main()

