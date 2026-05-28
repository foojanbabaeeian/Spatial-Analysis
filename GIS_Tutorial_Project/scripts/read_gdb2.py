# Read FGDB GDB_Items to find schema for Neighborhoods table
import os, re, struct

gdb_path = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/Chapter2.gdb'

# Read a00000004 to look for ALL field names (not just filtered ones)
table_path = os.path.join(gdb_path, 'a00000004.gdbtable')
with open(table_path, 'rb') as f:
    data = f.read()

# Try to decode as utf-16-le to find field names
try:
    text_utf16 = data.decode('utf-16-le', errors='ignore')
    # Look for plausible field name patterns in utf-16
    pattern16 = re.compile(r'[A-Za-z][A-Za-z0-9_]{2,30}')
    matches16 = list(set(pattern16.findall(text_utf16)))
    print("UTF-16 matches:", sorted([m for m in matches16 if len(m) >= 3])[:80])
except:
    pass

# Also try the GDB_Items table to find XML schema
gdb_items_path = os.path.join(gdb_path, 'a00000004.gdbtable')
# GDB_Items is usually around a00000001
for f in os.listdir(gdb_path):
    if f.endswith('.gdbtable'):
        fpath = os.path.join(gdb_path, f)
        with open(fpath, 'rb') as fp:
            d = fp.read(10000)  # Read first 10KB
        # Look for XML-like content with field definitions
        text = d.decode('latin-1')
        if '<Name>' in text and ('POP' in text.upper() or 'BNAME' in text.upper() or 'BRONAME' in text.upper()):
            print(f'\nFound XML schema in {f}:')
            # Extract Name tags
            names = re.findall(r'<Name>([^<]+)</Name>', text)
            print('  Field Names:', names[:30])

# Look for the Neighborhoods table schema in GDB_Items (usually a00000004)
# The GDB stores schemas as XML blobs
print('\n\n=== Searching all tables for Neighborhoods schema ===')
for f in sorted(os.listdir(gdb_path)):
    if f.endswith('.gdbtable'):
        fpath = os.path.join(gdb_path, f)
        size = os.path.getsize(fpath)
        if size < 500000:  # Only look at smaller tables
            with open(fpath, 'rb') as fp:
                d = fp.read()
            text = d.decode('latin-1', errors='ignore')
            if 'Neighborhoods' in text and 'Field' in text:
                print(f'\nTable {f} has Neighborhoods + Field references')
                # Look for field names
                fn = re.findall(r'(?:Name|field_name).*?([A-Z][A-Z0-9_]+)', text)
                print('  Possible fields:', fn[:20])
