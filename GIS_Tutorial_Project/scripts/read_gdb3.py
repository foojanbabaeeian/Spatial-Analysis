# Read the GDB_Items XML blobs to find Neighborhoods schema
import os, re

gdb_path = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/Chapter2.gdb'

# The GDB metadata table contains XML schema definitions
# Try to find schema info in each table
all_tables = sorted(os.listdir(gdb_path))
gdbtables = [f for f in all_tables if f.endswith('.gdbtable')]

for f in gdbtables:
    fpath = os.path.join(gdb_path, f)
    with open(fpath, 'rb') as fp:
        data = fp.read()

    # Search for field definition XML patterns
    # In FGDB format, field definitions appear as binary structures
    # but the field names are stored as length-prefixed UTF-16-LE strings

    # Try to find field name patterns by looking at utf-16 encoded strings
    found_fields = []

    # Scan for 2-byte aligned UTF-16 strings
    i = 0
    while i < len(data) - 2:
        # Try to read a potential length-prefixed string
        if i + 2 <= len(data):
            length = struct.unpack_from('<H', data, i)[0] if i + 2 <= len(data) else 0
            if 4 <= length <= 60:  # Reasonable field name length
                # Try to decode as UTF-16-LE
                start = i + 2
                end = start + length * 2
                if end <= len(data):
                    try:
                        s = data[start:end].decode('utf-16-le')
                        if s.isidentifier() and s.isupper() and len(s) >= 3:
                            found_fields.append(s)
                    except:
                        pass
        i += 1

    if found_fields:
        # Check if it looks like a feature class (has OBJECTID or Shape)
        has_oid = 'OBJECTID' in found_fields or 'OID' in found_fields
        has_shape = 'SHAPE' in found_fields or 'Shape' in found_fields
        pop_fields = [f for f in found_fields if 'POP' in f or 'BNAME' in f or 'FOOD' in f or 'HH' in f]
        if pop_fields:
            print(f'\n{f}:')
            print('  All uppercase fields:', sorted(set(found_fields))[:30])

import struct

# Also scan all gdbtable files for readable field name strings near headers
print('\n\n=== Scanning for Neighborhoods layer field names ===')
for f in gdbtables:
    fpath = os.path.join(gdb_path, f)
    with open(fpath, 'rb') as fp:
        header = fp.read(50000)  # Read first 50KB

    # Look for field names as length-prefixed UTF-16-LE in header region
    fields_found = []
    for i in range(0, min(len(header)-4, 50000)):
        try:
            length = struct.unpack_from('<H', header, i)[0]
            if 3 <= length <= 40:
                end = i + 2 + length * 2
                if end <= len(header):
                    s = header[i+2:end].decode('utf-16-le', errors='strict')
                    if all(c.isalnum() or c == '_' for c in s) and s[0].isalpha():
                        fields_found.append(s)
        except:
            pass

    pop_fields = [fld for fld in fields_found if any(kw in fld.upper() for kw in ['POP', 'BNAME', 'BORO', 'FOOD', 'NAME', 'HH', 'IMPOV', 'U18'])]
    if pop_fields:
        unique_pop = list(dict.fromkeys(pop_fields))  # Remove dupes while preserving order
        print(f'\n{f}: {unique_pop[:25]}')
