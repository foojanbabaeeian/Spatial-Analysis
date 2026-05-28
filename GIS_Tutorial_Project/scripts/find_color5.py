import sqlite3
import json

stylx_path = r"C:\Users\fooja\AppData\Roaming\ESRI\ArcGISPro\Favorites.stylx"

try:
    conn = sqlite3.connect(stylx_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables:", tables)

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} rows")

        # Sample some data
        cursor.execute(f"SELECT * FROM [{table}] LIMIT 2")
        cols = [d[0] for d in cursor.description]
        print(f"  Columns: {cols}")
        for row in cursor.fetchall():
            print(f"    {str(row)[:200]}")

    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
