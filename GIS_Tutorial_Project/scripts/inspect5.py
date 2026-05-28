import zipfile, json

def load_zip_file(aprx, path):
    with zipfile.ZipFile(aprx, 'r') as z:
        data = z.read(path)
    text = data.decode('utf-8')
    if text.endswith('\x00'): text = text[:-1]
    return json.loads(text)

base = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/'

# Look at T2-1 to see a working UniqueValue renderer
t21 = base + 'Tutorial2-1FozhanBabaeiyan.aprx'
with zipfile.ZipFile(t21, 'r') as z:
    files = sorted(z.namelist())
    print("T2-1 files:", files)

# Load the zoning layer to see the UniqueValue renderer
for f in files:
    if 'zoning' in f.lower() or 'land' in f.lower():
        obj = load_zip_file(t21, f)
        print(f"\n{f}:")
        print("  name:", obj.get('name'))
        r = obj.get('renderer', {})
        print("  renderer type:", r.get('type'))
        if r.get('type') == 'CIMUniqueValueRenderer':
            print("  field:", r.get('fields'))
            groups = r.get('groups', [])
            print("  groups:", len(groups))
            for g in groups[:2]:
                classes = g.get('classes', [])
                for cls in classes[:2]:
                    sym = cls.get('symbol', {}).get('symbol', {})
                    sls = sym.get('symbolLayers', [])
                    print("    class:", cls.get('values'), [sl.get('color',{}).get('values') for sl in sls])

# T2-6 - look at how classBreaks are structured (has breaks already)
t26 = base + 'Tutorial2-6FozhanBabaeiyan.aprx'
obj6 = load_zip_file(t26, 'food_stamp_recipients_and_resources/neighborhoods.xml')
r6 = obj6.get('renderer', {})
print("\n\nT2-6 female renderer full structure:")
print("classBreakInfos:", len(r6.get('classBreakInfos', [])))
print("breaks:", len(r6.get('breaks', [])))
print("colorRamp:", r6.get('colorRamp', {}).get('type') if r6.get('colorRamp') else None)
# Print the authoringInfo to understand
ai = r6.get('authoringInfo', {})
print("authoringInfo:", json.dumps(ai, indent=2)[:500])

# T2-7 - look at how DotDensity is structured
t27 = base + 'Tutorial2-7FozhanBabaeiyan.aprx'
obj7 = load_zip_file(t27, 'density_maps/neighborhoods2.xml')
r7 = obj7.get('renderer', {})
print("\n\nT2-7 DotDensity renderer full:")
print(json.dumps(r7, indent=2)[:2000])

# T2-8 - check how scale visibility is stored
t28 = base + 'Tutorial2-8FozhanBabaeiyan.aprx'
zl = load_zip_file(t28, 'new_york_city_zoning/zoninglanduse.xml')
print("\n\nT2-8 zoninglanduse visibility fields:")
print("  minScale:", zl.get('minScale'))
print("  maxScale:", zl.get('maxScale'))
lc = zl.get('labelClasses', [])
if lc:
    print("  LC minimumScale:", lc[0].get('minimumScale'))
    print("  LC maximumScale:", lc[0].get('maximumScale'))

# Check boroughs for T2-8
t28_bor_files = []
with zipfile.ZipFile(t28, 'r') as z:
    t28_bor_files = [f for f in z.namelist() if 'borou' in f.lower()]
print("T2-8 borough files:", t28_bor_files)
