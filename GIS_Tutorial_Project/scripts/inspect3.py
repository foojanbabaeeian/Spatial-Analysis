import zipfile, json

def load_zip_file(aprx, path):
    with zipfile.ZipFile(aprx, 'r') as z:
        data = z.read(path)
    text = data.decode('utf-8')
    if text.endswith('\x00'): text = text[:-1]
    return json.loads(text)

base = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/'

# T2-4: Look at how layers are referenced in map1.xml
t24 = base + 'Tutorial2-4FozhanBabaeiyan.aprx'
obj = load_zip_file(t24, 'map1/map1.xml')
# layers are URIs to other files
print('=== T2-4 map1 layers ===')
for l in obj.get('layers', []):
    print(' ', l)  # probably URI strings

print('\n=== T2-4 Neighborhoods_3D renderer ===')
obj3d = load_zip_file(t24, 'NYC_Food_Stamps_SNAP_Households_by_Neighbor/Neighborhoods_3D.json')
print('type:', obj3d.get('type'))
print('renderer:', obj3d.get('renderer', {}).get('type'))
