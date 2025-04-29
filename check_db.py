import sqlite3

conn = sqlite3.connect("instance/sales.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("📋 Tables found:", tables)

for (table,) in tables:
    print(f"\n--- {table} ---")
    cursor.execute(f"SELECT * FROM {table} ")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

conn.close()
