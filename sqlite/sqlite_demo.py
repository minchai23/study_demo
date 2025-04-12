import sqlite3

def main():
    connect = sqlite3.connect("sqlite.db")
    cursor = connect.cursor()

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

    cursor.execute("""
        update tb_software
        set lang = ?
        where name = ?
    """, ("java", "neo4j"))
    connect.commit()

    cursor.execute("""
        delete from tb_software
        where name = ?
    """, ("neo4j",))
    connect.commit()

    cursor.close()
    connect.close()

if __name__ == "__main__":
    main()

