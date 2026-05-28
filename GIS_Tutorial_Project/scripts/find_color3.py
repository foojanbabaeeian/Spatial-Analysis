import sqlite3

stylx_path = r"C:\Users\fooja\AppData\Local\Programs\ArcGIS\Pro\Resources\Styles\Styles.stylx"

try:
    conn = sqlite3.connect(stylx_path)
    cursor = conn.cursor()

    # List tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables:", tables)

    # Search for Quetzal in all tables
    for table in tables:
        try:
            cursor.execute(f"SELECT * FROM [{table}] LIMIT 1")
            cols = [d[0] for d in cursor.description]
            print(f"\nTable: {table}, Columns: {cols}")

            # Try searching for Quetzal
            for col in cols:
                try:
                    cursor.execute(f"SELECT * FROM [{table}] WHERE CAST([{col}] AS TEXT) LIKE '%Quetzal%' LIMIT 3")
                    rows = cursor.fetchall()
                    if rows:
                        print(f"  Found in column '{col}':")
                        for row in rows:
                            print(f"    {str(row)[:300]}")
                except:
                    pass
        except Exception as e:
            print(f"Error in table {table}: {e}")

    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
