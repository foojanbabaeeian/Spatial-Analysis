import zipfile, json

def load_zip_file(aprx, path):
    with zipfile.ZipFile(aprx, 'r') as z:
        data = z.read(path)
    text = data.decode('utf-8')
    if text.endswith('\x00'): text = text[:-1]
    return json.loads(text)

base = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/'

# T2-6 female renderer - look at breaks structure
t26 = base + 'Tutorial2-6FozhanBabaeiyan.aprx'
obj6 = load_zip_file(t26, 'food_stamp_recipients_and_resources/neighborhoods.xml')
r6 = obj6.get('renderer', {})
print("T2-6 female breaks structure:")
print(json.dumps(r6.get('breaks', []), indent=2)[:3000])
print("\nT2-6 female renderer numberFormat:")
print(json.dumps(r6.get('numberFormat', {}), indent=2))
print("\nT2-6 female colorRamp:")
print(json.dumps(r6.get('colorRamp', {}), indent=2)[:500])

# T2-3 facilities - look at attribute fields to find fact_type
# Actually, I need to look at the breaks/fields to understand the current structure
t23 = base + 'Tutorial2-3FozhanBabaeiyan.aprx'
obj3 = load_zip_file(t23, 'nyc_food_pantries_and_soup_kitchens/facilities.xml')
print("\n\nT2-3 facilities full renderer:")
r3 = obj3.get('renderer', {})
print("  field:", r3.get('field'))
print("  barrierWeight:", r3.get('barrierWeight'))
print("  breaks:", json.dumps(r3.get('breaks', []), indent=2)[:1000])
# Look at definitionExpression
print("  definitionExpression:", obj3.get('definitionExpression'))
print("  definitionQuery:", obj3.get('definitionQuery'))
# fields info
print("  All layer keys:", [k for k in obj3.keys()])

# T2-8 - look at boroughs.json structure for scale
t28 = base + 'Tutorial2-8FozhanBabaeiyan.aprx'
obj8_bor = load_zip_file(t28, 'new_york_city_land_use_school_study/boroughs.json')
print("\n\nT2-8 boroughs.json:")
print("  type:", obj8_bor.get('type'))
print("  name:", obj8_bor.get('name'))
print("  isVisible:", obj8_bor.get('isVisible'))
print("  minScale:", obj8_bor.get('minScale'))
print("  maxScale:", obj8_bor.get('maxScale'))
print("  displayAnnotation:", obj8_bor.get('displayAnnotation'))
lc = obj8_bor.get('labelClasses', [])
print("  label classes:", len(lc))
if lc:
    print("  LC expr:", lc[0].get('expression'))
    print("  LC minScale:", lc[0].get('minimumScale'))
    print("  LC maxScale:", lc[0].get('maximumScale'))

# T2-8 - check facilities layer
obj8_fac = load_zip_file(t28, 'new_york_city_zoning_and_land_use/facilities.json')
print("\nT2-8 facilities.json:")
print("  type:", obj8_fac.get('type'))
print("  name:", obj8_fac.get('name'))
print("  isVisible:", obj8_fac.get('isVisible'))
print("  minScale:", obj8_fac.get('minScale'))
print("  maxScale:", obj8_fac.get('maxScale'))

# T2-8 neighborhoods
obj8_nei = load_zip_file(t28, 'new_york_city_zoning/neighborhoods.xml')
print("\nT2-8 neighborhoods.xml:")
print("  isVisible:", obj8_nei.get('isVisible'))
print("  minScale:", obj8_nei.get('minScale'))
print("  maxScale:", obj8_nei.get('maxScale'))
lc = obj8_nei.get('labelClasses', [])
if lc:
    print("  LC minScale:", lc[0].get('minimumScale'))
    print("  LC maxScale:", lc[0].get('maximumScale'))

# T2-8 map.xml to find bookmarks and default extent
obj8_map = load_zip_file(t28, 'map/map.xml')
print("\nT2-8 map default extent/scale:")
ext = obj8_map.get('defaultExtent', {})
print("  defaultExtent:", ext)
print("  mapViewExtent keys:", list(obj8_map.get('defaultExtent', {}).keys()))
# Check for bookmarks in map
print("  mapType:", obj8_map.get('mapType'))
