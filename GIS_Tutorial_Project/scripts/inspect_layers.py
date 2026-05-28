import zipfile, json

def read_file(aprx, path):
    with zipfile.ZipFile(aprx, 'r') as z:
        data = z.read(path)
    text = data.decode('utf-8')
    if text.endswith('\x00'): text = text[:-1]
    return json.loads(text)

base = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/'

# T2-2 files
t22 = base + 'Tutorial2-2FozhanBabaeiyan.aprx'
for fname in ['new_york_city_zoning/zoninglanduse.xml', 'new_york_city_zoning/neighborhoods.xml', 'new_york_city_zoning/water.xml']:
    obj = read_file(t22, fname)
    print(f'\n=== T2-2 {fname} ===')
    r = obj.get('renderer', {})
    print(f'  renderer type: {r.get("type")}')
    print(f'  displayAnnotation: {obj.get("displayAnnotation")}')
    lc = obj.get('labelClasses', [])
    print(f'  label classes count: {len(lc)}')
    if lc:
        for i, l in enumerate(lc):
            ts = l.get('textSymbol', {}).get('symbol', {})
            print(f'    LC{i}: expr={l.get("expression","?")}, displayAnnotation={l.get("displayAnnotation","?")}')
            print(f'          font={ts.get("fontFamilyName","?")}, size={ts.get("height","?")}')
    popup = obj.get('popupInfo')
    print(f'  popupInfo present: {popup is not None}')
    print(f'  popupEnabled: {obj.get("popupEnabled", "not set")}')

# T2-3
print('\n\n=== T2-3 FACILITIES ===')
t23 = base + 'Tutorial2-3FozhanBabaeiyan.aprx'
obj = read_file(t23, 'nyc_food_pantries_and_soup_kitchens/facilities.xml')
print(f'  name: {obj.get("name")}')
r = obj.get('renderer', {})
print(f'  renderer type: {r.get("type")}')
print(f'  displayAnnotation: {obj.get("displayAnnotation")}')
dq = obj.get('definitionQuery')
print(f'  definitionQuery: {dq}')

print('\n=== T2-3 MANHATTANSTREETS ===')
obj2 = read_file(t23, 'nyc_food_pantries_and_soup_kitchens/manhattanstreets.xml')
print(f'  renderer type: {obj2.get("renderer",{}).get("type")}')
sym = obj2.get('renderer', {}).get('symbol', {}).get('symbol', {})
print(f'  symbol layers: {len(sym.get("symbolLayers",[]))}')

# T2-4 GISProject.json
print('\n\n=== T2-4 GISProject.json (first 3000 chars) ===')
t24 = base + 'Tutorial2-4FozhanBabaeiyan.aprx'
with zipfile.ZipFile(t24, 'r') as z:
    data = z.read('GISProject.json')
text = data.decode('utf-8')
if text.endswith('\x00'): text = text[:-1]
obj = json.loads(text)
# Find maps
maps = obj.get('maps', [])
print(f'  maps count: {len(maps)}')
for m in maps:
    print(f'  map: {m.get("mapType")} layers={len(m.get("layers",[]))}')

# T2-4 neighborhoods in map
t24obj = read_file(t24, 'map1/map1.xml')
print(f'\n=== T2-4 map1.xml renderer ===')
r = t24obj.get('renderer', {})
print(f'  renderer type: {r.get("type")}')
print(f'  name: {t24obj.get("name")}')
