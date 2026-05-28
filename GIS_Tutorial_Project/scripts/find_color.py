import sqlite3, os

stylx_paths = [
    r'C:\Users\fooja\AppData\Roaming\ESRI\ArcGISPro\Favorites.stylx',
]

# Also look for ArcGIS Colors style in the installation
import glob
patterns = [
    r'C:\Users\fooja\AppData\Local\Programs\ArcGIS\Pro\Resources\**\*.stylx',
    r'C:\Users\fooja\AppData\Roaming\ESRI\**\*.stylx',
]
for pat in patterns:
    for f in glob.glob(pat, recursive=True):
        if 'ArcGIS_Colors' in f or 'Colors' in f:
            stylx_paths.append(f)
            print(f'Found: {f}')

for path in stylx_paths:
    if os.path.exists(path):
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            for t in tables:
                try:
                    cursor.execute(f'SELECT * FROM {t[0]} WHERE CAST(Content AS TEXT) LIKE ? LIMIT 1', ('%Quetzal%',))
                    rows = cursor.fetchall()
                    if rows:
                        print(f'Found Quetzal Green in {path}, table {t[0]}')
                        print(str(rows[0])[:300])
                except: pass
            conn.close()
        except Exception as e:
            print(f'Error with {path}: {e}')
