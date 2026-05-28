import sqlite3
import json

stylx_path = r"C:\Users\fooja\AppData\Local\Programs\ArcGIS\Pro\Resources\Styles\Styles.stylx"

try:
    conn = sqlite3.connect(stylx_path)
    cursor = conn.cursor()

    # Search DATA table KEY column for Quetzal
    cursor.execute("SELECT ID, KEY, CONTENT FROM DATA WHERE KEY LIKE '%Quetzal%' LIMIT 10")
    rows = cursor.fetchall()
    print(f"KEY search results: {len(rows)} rows")
    for row in rows:
        print(f"  ID={row[0]}, KEY={row[1]}")
        content = row[2]
        if content:
            try:
                # Try to parse as JSON
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='replace')
                j = json.loads(content)
                print(f"  Content (JSON): {json.dumps(j, indent=2)[:500]}")
            except:
                print(f"  Content (raw): {str(content)[:200]}")

    # Also search CONTENT column
    print("\n--- Searching CONTENT column ---")
    cursor.execute("SELECT ID, KEY FROM DATA WHERE CAST(CONTENT AS TEXT) LIKE '%Quetzal%' LIMIT 10")
    rows = cursor.fetchall()
    print(f"CONTENT search results: {len(rows)} rows")
    for row in rows:
        print(f"  ID={row[0]}, KEY={row[1]}")
        cursor.execute("SELECT CONTENT FROM DATA WHERE ID=?", (row[0],))
        content = cursor.fetchone()[0]
        if content:
            try:
                if isinstance(content, bytes):
                    content = content.decode('utf-8', errors='replace')
                j = json.loads(content)
                print(f"  Content: {json.dumps(j, indent=2)[:600]}")
            except:
                print(f"  Content (raw): {str(content)[:300]}")

    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
