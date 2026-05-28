import zipfile, json

def load_zip_file(aprx, path):
    with zipfile.ZipFile(aprx, 'r') as z:
        data = z.read(path)
    text = data.decode('utf-8')
    if text.endswith('\x00'): text = text[:-1]
    return json.loads(text)

base = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/'

# T2-4: The neighborhood layer is actually in the map1 folder but map1.xml is the map container
# Let me look at what's actually in the map1 folder
t24 = base + 'Tutorial2-4FozhanBabaeiyan.aprx'
print('=== T2-4 map1.xml keys ===')
obj = load_zip_file(t24, 'map1/map1.xml')
print(list(obj.keys()))
print('  type:', obj.get('type'))
print('  layers:', [l.get('type','?') + ':' + l.get('name','?') for l in obj.get('layers',[])])

# Check the 3D scene
print('\n=== T2-4 Neighborhoods_3D.json keys ===')
obj3d = load_zip_file(t24, 'NYC_Food_Stamps_SNAP_Households_by_Neighborhood/Neighborhoods_3D.json')
print(list(obj3d.keys()))
print('  type:', obj3d.get('type'))
print('  renderer type:', obj3d.get('renderer', {}).get('type'))
r3d = obj3d.get('renderer', {})
if 'field' in r3d:
    print('  field:', r3d.get('field'))

# T2-5: Look at map1 and the neighborhoods layers
print('\n\n=== T2-5 map1.xml ===')
t25 = base + 'Tutorial2-5FozhanBabaeiyan.aprx'
m1 = load_zip_file(t25, 'map1/map1.xml')
print('  type:', m1.get('type'))
print('  layers:', [l.get('type','?') + ':' + l.get('name','?') for l in m1.get('layers',[])])

print('\n=== T2-5 food_stamp_recipients/neighborhoods2.xml ===')
n2 = load_zip_file(t25, 'food_stamp_recipients_and_resources/neighborhoods2.xml')
print('  name:', n2.get('name'))
print('  renderer type:', n2.get('renderer', {}).get('type'))
r = n2.get('renderer', {})
print('  field:', r.get('field'))

print('\n=== T2-5 nyc_food_facilities/neighborhoods.xml ===')
nf = load_zip_file(t25, 'nyc_food_facilities_and_food_stamps_snap_neighbood_study/neighborhoods.xml')
print('  name:', nf.get('name'))
print('  renderer type:', nf.get('renderer', {}).get('type'))
rf = nf.get('renderer', {})
print('  field:', rf.get('field'))

print('\n=== T2-5 nyc_food_stamps/neighborhoods.xml ===')
ns = load_zip_file(t25, 'nyc_food_stamps_snap_households_by_neighborhood/neighborhoods.xml')
print('  name:', ns.get('name'))
print('  renderer type:', ns.get('renderer', {}).get('type'))

print('\n=== T2-5 3D: over_age_60.xml ===')
oa = load_zip_file(t25, 'nyc_food_stamps_snap_households_by_neighborhood1/over_age_60_receiving_food_stamps.xml')
print('  name:', oa.get('name'))
print('  renderer type:', oa.get('renderer', {}).get('type'))

# T2-6 neighborhoods
print('\n\n=== T2-6 neighborhoods.xml (female) ===')
t26 = base + 'Tutorial2-6FozhanBabaeiyan.aprx'
fn = load_zip_file(t26, 'food_stamp_recipients_and_resources/neighborhoods.xml')
print('  name:', fn.get('name'))
print('  renderer type:', fn.get('renderer', {}).get('type'))
r = fn.get('renderer', {})
print('  field:', r.get('field'))
print('  normField:', r.get('normalizationField'))
if 'classBreakInfos' in r:
    for cb in r['classBreakInfos']:
        print('    break:', cb.get('classMaximumValue'))

# T2-7 neighborhoods2
print('\n\n=== T2-7 neighborhoods2.xml ===')
t27 = base + 'Tutorial2-7FozhanBabaeiyan.aprx'
n7 = load_zip_file(t27, 'density_maps/neighborhoods2.xml')
print('  name:', n7.get('name'))
print('  renderer type:', n7.get('renderer', {}).get('type'))
r7 = n7.get('renderer', {})
print('  fields:', r7.get('fields'))

# T2-8 visibility
print('\n\n=== T2-8 zoninglanduse.xml displayAnnotation ===')
t28 = base + 'Tutorial2-8FozhanBabaeiyan.aprx'
zl = load_zip_file(t28, 'new_york_city_zoning/zoninglanduse.xml')
print('  displayAnnotation:', zl.get('displayAnnotation'))
lc = zl.get('labelClasses', [])
print('  labelClass minScale:', lc[0].get('minimumScale') if lc else 'none')
print('  labelClass maxScale:', lc[0].get('maximumScale') if lc else 'none')
print('  layer minScale:', zl.get('minScale'))
print('  layer maxScale:', zl.get('maxScale'))
