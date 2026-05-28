# Read ArcGIS FGDB (File Geodatabase) tables using raw binary parsing
# The .gdbtable file has a simple structure we can parse for field names

import os, struct

gdb_path = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/Chapter2.gdb'

# First, find which table number corresponds to "Neighborhoods"
# Table a00000001 is the GDB_SystemCatalog which maps table names to numbers
def read_catalog(gdb_path):
    catalog_path = os.path.join(gdb_path, 'a00000001.gdbtable')
    with open(catalog_path, 'rb') as f:
        data = f.read()

    # Look for table names in the binary data
    text = data.decode('latin-1')
    names = []
    i = 0
    while i < len(text):
        if text[i:i+4] == '\x00\x00\x00\x00':
            # Try to find readable strings
            pass
        i += 1

    # Just search for strings that look like table names
    import re
    # Find ASCII strings of length > 4
    pattern = re.compile(r'[A-Za-z][A-Za-z0-9_]{3,}')
    matches = list(set(pattern.findall(text)))
    matches.sort()
    print("String matches in catalog:", [m for m in matches if len(m) > 4][:50])

read_catalog(gdb_path)

# Try a simpler approach: search all .gdbtable files for field definitions
# The .gdbtable file format starts with a header that includes field definitions
def find_fields_in_table(table_file):
    with open(table_file, 'rb') as f:
        data = f.read()

    import re
    # Look for field names - they appear as length-prefixed UTF-16 strings
    # or as simple ASCII strings in the header
    text = data.decode('latin-1')
    # Find plausible field name patterns
    pattern = re.compile(r'[A-Z][A-Z0-9_]{2,20}')
    fields = list(set(pattern.findall(text)))
    return [f for f in fields if len(f) >= 3]

# Try to find the Neighborhoods table
all_tables = [f for f in os.listdir(gdb_path) if f.endswith('.gdbtable')]
print(f"\nTotal tables: {len(all_tables)}")

for tbl in sorted(all_tables):
    tbl_path = os.path.join(gdb_path, tbl)
    size = os.path.getsize(tbl_path)
    if size > 1000:  # Skip tiny tables
        fields = find_fields_in_table(tbl_path)
        # Filter for plausible field names
        plausible = [f for f in fields if any(kw in f.upper() for kw in ['POP', 'FOOD', 'BNAME', 'NAME', 'BORO', 'HH', 'U18', 'O60'])]
        if plausible:
            print(f"{tbl} (size={size}): {plausible[:15]}")
