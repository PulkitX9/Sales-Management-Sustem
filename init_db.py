import sqlite3
conn = sqlite3.connect("instance/sales.db")

with open("sales.sql", "r") as f:
    sql_script = f.read()

conn.executescript(sql_script)
conn.commit()
conn.close()

print("Database created successfully!")
