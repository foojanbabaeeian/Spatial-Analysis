import zipfile, json

def load_zip_file(aprx, path):
    with zipfile.ZipFile(aprx, 'r') as z:
        data = z.read(path)
    text = data.decode('utf-8')
    if text.endswith('\x00'): text = text[:-1]
    return json.loads(text)

base = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/'

# T2-4 Neighborhoods_3D full renderer to understand template structure
t24 = base + 'Tutorial2-4FozhanBabaeiyan.aprx'
obj4 = load_zip_file(t24, 'NYC_Food_Stamps_SNAP_Households_by_Neighborhood/Neighborhoods_3D.json')
r4 = obj4.get('renderer', {})
print("T2-4 Neighborhoods_3D renderer full:")
print(json.dumps(r4, indent=2))
print("\n\nT2-4 layer visibility:", obj4.get('visibility'))
print("T2-4 minScale:", obj4.get('minScale'))

# T2-5 - look at T2-1 graduated symbol renderer to understand the structure
# Actually T2-1 doesn't have it; let me look at T2-5's Over age 60 layer
t25 = base + 'Tutorial2-5FozhanBabaeiyan.aprx'
obj5_oa = load_zip_file(t25, 'food_stamp_recipients_and_resources/neighborhoods2.xml')
print("\n\n=== T2-5 Over age 60 renderer (CIMClassBreaksRenderer) ===")
r5 = obj5_oa.get('renderer', {})
print("type:", r5.get('type'))
print("field:", r5.get('field'))
print("classBreakType:", r5.get('classBreakType'))
print("breaks:", json.dumps(r5.get('breaks', [])[:2], indent=2))

# T2-5 nyc_food_stamps_snap neighborhoods
n5_s = load_zip_file(t25, 'nyc_food_stamps_snap_households_by_neighborhood/neighborhoods.xml')
print("\n=== T2-5 nyc_food_stamps neighborhoods (under-18 candidate) ===")
r = n5_s.get('renderer', {})
print("type:", r.get('type'))
sym = r.get('symbol', {}).get('symbol', {})
print("symbol layers:")
for sl in sym.get('symbolLayers', []):
    print("  SL:", sl.get('type'), "color:", sl.get('color', {}).get('values'))

# T2-5 nyc_food_facilities neighborhoods
n5_f = load_zip_file(t25, 'nyc_food_facilities_and_food_stamps_snap_neighbood_study/neighborhoods.xml')
print("\n=== T2-5 nyc_food_facilities neighborhoods (food bank candidate) ===")
r = n5_f.get('renderer', {})
print("type:", r.get('type'))
sym = r.get('symbol', {}).get('symbol', {})
for sl in sym.get('symbolLayers', []):
    print("  SL:", sl.get('type'), "color:", sl.get('color', {}).get('values'))

# T2-3 - see what fact_type looks like in the attribute fields
# Check if there is field metadata in the featureTable
obj3 = load_zip_file(t23 := base + 'Tutorial2-3FozhanBabaeiyan.aprx',
                     'nyc_food_pantries_and_soup_kitchens/facilities.xml')
ft = obj3.get('featureTable', {})
print("\n\nT2-3 facilities featureTable keys:", list(ft.keys())[:10])
fields = ft.get('fieldDescriptions', ft.get('fields', []))
print("fields:", [f.get('name') or f.get('alias') for f in fields[:15]])

# Check T2-8 zoninglanduse for label class structure
t28 = base + 'Tutorial2-8FozhanBabaeiyan.aprx'
obj8 = load_zip_file(t28, 'new_york_city_zoning/zoninglanduse.xml')
print("\n\nT2-8 zoninglanduse keys:", list(obj8.keys()))
print("visibility:", obj8.get('visibility'))
print("isVisible:", obj8.get('isVisible'))
lc = obj8.get('labelClasses', [])
if lc:
    print("LC keys:", list(lc[0].keys()))
