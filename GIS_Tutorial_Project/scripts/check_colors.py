import sqlite3
conn = sqlite3.connect(r'C:\Users\fooja\AppData\Local\Programs\ArcGIS\Pro\Resources\ColorBooks\colorbooks.sqlite')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('Tables:', cursor.fetchall())
cursor.execute("SELECT * FROM sqlite_master WHERE type='table' LIMIT 5")
for row in cursor.fetchall():
    print(row)
conn.close()
