import zipfile, json

def load_zip_file(aprx, path):
    with zipfile.ZipFile(aprx, 'r') as z:
        data = z.read(path)
    text = data.decode('utf-8')
    if text.endswith('\x00'): text = text[:-1]
    return json.loads(text)

base = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/'

# === T2-2 neighborhoods.xml - see full label class structure ===
t22 = base + 'Tutorial2-2FozhanBabaeiyan.aprx'
obj = load_zip_file(t22, 'new_york_city_zoning/neighborhoods.xml')
print("=== T2-2 neighborhoods labelClass ===")
lc = obj.get('labelClasses', [])
print(json.dumps(lc[0], indent=2))

# === T2-2 zoninglanduse.xml - see full label class structure ===
print("\n=== T2-2 zoninglanduse labelClass ===")
obj2 = load_zip_file(t22, 'new_york_city_zoning/zoninglanduse.xml')
lc2 = obj2.get('labelClasses', [])
print(json.dumps(lc2[0], indent=2))

# === T2-3 facilities.xml - see renderer and key fields ===
t23 = base + 'Tutorial2-3FozhanBabaeiyan.aprx'
obj3 = load_zip_file(t23, 'nyc_food_pantries_and_soup_kitchens/facilities.xml')
print("\n=== T2-3 facilities renderer (top keys) ===")
r = obj3.get('renderer', {})
print("renderer keys:", list(r.keys()))
print("renderer type:", r.get('type'))
print("field:", r.get('field'))

# See the UUID file for T2-3 to find World Light Gray
t23_uuid = '658d486924364d5a93465ec49d8844e7.xml'
objuuid = load_zip_file(t23, t23_uuid)
print("\n=== T2-3 UUID file ===")
print("type:", objuuid.get('type'))
print("name:", objuuid.get('name'))
print("visible:", objuuid.get('isVisible'))

# === T2-3 manhattanstreets - current renderer ===
ms = load_zip_file(t23, 'nyc_food_pantries_and_soup_kitchens/manhattanstreets.xml')
print("\n=== T2-3 manhattanstreets renderer ===")
r = ms.get('renderer', {})
sym = r.get('symbol', {}).get('symbol', {})
sls = sym.get('symbolLayers', [])
for sl in sls:
    print("  SL type:", sl.get('type'))
    print("  SL color:", sl.get('color', {}).get('values'))
    print("  SL width:", sl.get('width'))
    print("  SL capStyle:", sl.get('capStyle'))

# === T2-4 Neighborhoods_3D.json - full renderer ===
t24 = base + 'Tutorial2-4FozhanBabaeiyan.aprx'
obj4 = load_zip_file(t24, 'NYC_Food_Stamps_SNAP_Households_by_Neighborhood/Neighborhoods_3D.json')
print("\n=== T2-4 Neighborhoods_3D renderer ===")
r4 = obj4.get('renderer', {})
print("type:", r4.get('type'))
print("field:", r4.get('field'))
print("normalization:", r4.get('normalizationField'))
print("method:", r4.get('classificationMethod'))
print("keys:", list(r4.keys()))
breaks = r4.get('classBreakInfos', [])
print(f"breaks ({len(breaks)}):", [b.get('classMaximumValue') for b in breaks])
if breaks:
    print("First break symbol keys:", list(breaks[0].get('symbol', {}).keys()))
