"""Verify that all tutorial fixes were applied correctly."""
import zipfile, json

BASE = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/'

def load(aprx, path):
    with zipfile.ZipFile(aprx, 'r') as z:
        data = z.read(path)
    text = data.decode('utf-8')
    if text.endswith('\x00'): text = text[:-1]
    return json.loads(text)

pass_count = 0
fail_count = 0

def check(desc, condition, details=''):
    global pass_count, fail_count
    if condition:
        print(f'  PASS: {desc}')
        pass_count += 1
    else:
        print(f'  FAIL: {desc}  {details}')
        fail_count += 1

# === TUTORIAL 2-2 ===
print('\n=== Tutorial 2-2 ===')
t22 = BASE + 'Tutorial2-2FozhanBabaeiyan.aprx'
zl = load(t22, 'new_york_city_zoning/zoninglanduse.xml')
lc = zl.get('labelClasses', [])
check('ZoningLandUse displayAnnotation=true', zl.get('displayAnnotation') == True)
check('ZoningLandUse showPopups=false', zl.get('showPopups') == False)
check('ZoningLandUse LC field=[ZONE]', lc and lc[0].get('expression') == '[ZONE]')
check('ZoningLandUse LC size=8', lc and lc[0]['textSymbol']['symbol']['height'] == 8)
ts_sym = lc[0]['textSymbol']['symbol']['symbol']['symbolLayers'][0] if lc else {}
check('ZoningLandUse LC color=gray50%', ts_sym.get('color', {}).get('values', [])[:3] == [128, 128, 128])

nei = load(t22, 'new_york_city_zoning/neighborhoods.xml')
nlc = nei.get('labelClasses', [])
check('Neighborhoods displayAnnotation=true', nei.get('displayAnnotation') == True)
check('Neighborhoods LC font=Arial', nlc and nlc[0]['textSymbol']['symbol']['fontFamilyName'] == 'Arial')
check('Neighborhoods LC style=Bold', nlc and nlc[0]['textSymbol']['symbol']['fontStyleName'] == 'Bold')
check('Neighborhoods LC size=11', nlc and nlc[0]['textSymbol']['symbol']['height'] == 11)
check('Neighborhoods LC has halo', nlc and 'haloSymbol' in nlc[0]['textSymbol']['symbol'])
check('Neighborhoods has popupInfo', nei.get('popupInfo') is not None)

water = load(t22, 'new_york_city_zoning/water.xml')
wlc = water.get('labelClasses', [])
check('Water displayAnnotation=true', water.get('displayAnnotation') == True)
check('Water showPopups=false', water.get('showPopups') == False)
check('Water LC font=Times New Roman', wlc and wlc[0]['textSymbol']['symbol']['fontFamilyName'] == 'Times New Roman')
check('Water LC size=12', wlc and wlc[0]['textSymbol']['symbol']['height'] == 12)
# Atlantic Blue: RGB(102, 153, 205)
wts_sym = wlc[0]['textSymbol']['symbol']['symbol']['symbolLayers'][0] if wlc else {}
check('Water LC color=Atlantic Blue', wts_sym.get('color', {}).get('values', [])[:3] == [102, 153, 205])

# === TUTORIAL 2-3 ===
print('\n=== Tutorial 2-3 ===')
t23 = BASE + 'Tutorial2-3FozhanBabaeiyan.aprx'
fac = load(t23, 'nyc_food_pantries_and_soup_kitchens/facilities.xml')
check('Facilities name=food facilities', fac.get('name') == 'food facilities')
defexp = fac.get('featureTable', {}).get('definitionExpression', '')
check('Facilities has definition query', '4901' in defexp and '4902' in defexp and '4903' in defexp)
check('Facilities renderer=UniqueValue', fac.get('renderer', {}).get('type') == 'CIMUniqueValueRenderer')
groups = fac.get('renderer', {}).get('groups', [])
classes = groups[0].get('classes', []) if groups else []
check('Facilities has 3 classes', len(classes) == 3)
labels = [c.get('label', '') for c in classes]
check('Facilities has Soup Kitchen class', 'Soup Kitchen' in labels)
check('Facilities has Food Pantry class', 'Food Pantry' in labels)
check('Facilities has Joint class', any('Joint' in l for l in labels))

streets = load(t23, 'nyc_food_pantries_and_soup_kitchens/manhattanstreets.xml')
check('ManhattanStreets displayAnnotation=true', streets.get('displayAnnotation') == True)
r = streets.get('renderer', {})
sym = r.get('symbol', {}).get('symbol', {})
for sl in sym.get('symbolLayers', []):
    if sl.get('type') == 'CIMSolidStroke':
        check('ManhattanStreets color=gray20%', sl.get('color', {}).get('values', [])[:3] == [204, 204, 204])
        check('ManhattanStreets width=0.5', sl.get('width') == 0.5)
slc = streets.get('labelClasses', [])
check('ManhattanStreets labels on STREET', slc and slc[0].get('expression') == '[STREET]')

# World light gray
uuid_fac = '658d486924364d5a93465ec49d8844e7.xml'
uuid_obj = load(t23, uuid_fac)
check('World Light Gray Canvas visibility=False', uuid_obj.get('visibility') == False)

# === TUTORIAL 2-4 ===
print('\n=== Tutorial 2-4 ===')
t24 = BASE + 'Tutorial2-4FozhanBabaeiyan.aprx'
n3d = load(t24, 'NYC_Food_Stamps_SNAP_Households_by_Neighborhood/Neighborhoods_3D.json')
r4 = n3d.get('renderer', {})
check('Neighborhoods_3D field=O60_FOOD', r4.get('field') == 'O60_FOOD')
check('Neighborhoods_3D method=Quantile', r4.get('classificationMethod') == 'Quantile')
check('Neighborhoods_3D has 5 breaks', len(r4.get('breaks', [])) == 5)
# Check grayscale colors
brk_colors = []
for b in r4.get('breaks', []):
    for sl in b.get('symbol', {}).get('symbol', {}).get('symbolLayers', []):
        if sl.get('type') == 'CIMSolidFill':
            c = sl.get('color', {}).get('values', [])[:3]
            brk_colors.append(c)
check('Neighborhoods_3D uses grayscale', all(c[0] == c[1] == c[2] for c in brk_colors))
check('Neighborhoods_3D colors go dark', brk_colors and brk_colors[-1][0] < brk_colors[0][0])

# === TUTORIAL 2-5 ===
print('\n=== Tutorial 2-5 ===')
t25 = BASE + 'Tutorial2-5FozhanBabaeiyan.aprx'
nfb = load(t25, 'nyc_food_facilities_and_food_stamps_snap_neighbood_study/neighborhoods.xml')
check('FoodBank layer name correct', nfb.get('name') == 'number of food banks / soup kitchens')
check('FoodBank renderer=GraduatedSymbol', nfb.get('renderer', {}).get('type') == 'CIMClassBreaksRenderer')
check('FoodBank field=food_FASIL', nfb.get('renderer', {}).get('field') == 'food_FASIL')
check('FoodBank classBreakType=GraduatedSymbol', nfb.get('renderer', {}).get('classBreakType') == 'GraduatedSymbol')

nu18 = load(t25, 'nyc_food_stamps_snap_households_by_neighborhood/neighborhoods.xml')
check('Under18 layer name correct', nu18.get('name') == 'under 18 receiving food stamps')
check('Under18 renderer=Proportional', nu18.get('renderer', {}).get('type') == 'CIMProportionalRenderer')
check('Under18 field=U18_FOOD', nu18.get('renderer', {}).get('field') == 'U18_FOOD')

# === TUTORIAL 2-6 ===
print('\n=== Tutorial 2-6 ===')
t26 = BASE + 'Tutorial2-6FozhanBabaeiyan.aprx'
fem = load(t26, 'food_stamp_recipients_and_resources/neighborhoods.xml')
r6f = fem.get('renderer', {})
check('Female field=U18FHHFOOD', r6f.get('field') == 'U18FHHFOOD')
check('Female normField=TOT_HH', r6f.get('normalizationField') == 'TOT_HH')
check('Female method=ManualInterval', r6f.get('classificationMethod') == 'ManualInterval')
check('Female has 5 breaks', len(r6f.get('breaks', [])) == 5)
ub = [b.get('upperBound') for b in r6f.get('breaks', [])]
check('Female break at 0.02', 0.02 in ub)
check('Female break at 0.04', 0.04 in ub)
check('Female break at 0.08', 0.08 in ub)
check('Female break at 0.16', 0.16 in ub)
nf6 = r6f.get('numberFormat', {})
check('Female numberFormat=percentage', 'Percent' in nf6.get('type', ''))

male = load(t26, 'food_stamp_recipients_and_resources/neighborhoods2.xml')
r6m = male.get('renderer', {})
check('Male field=U18MHHFOOD', r6m.get('field') == 'U18MHHFOOD')
check('Male method=ManualInterval', r6m.get('classificationMethod') == 'ManualInterval')
check('Male same breaks', [b.get('upperBound') for b in r6m.get('breaks', [])] == ub)

# === TUTORIAL 2-7 ===
print('\n=== Tutorial 2-7 ===')
t27 = BASE + 'Tutorial2-7FozhanBabaeiyan.aprx'
dens = load(t27, 'density_maps/neighborhoods2.xml')
r7 = dens.get('renderer', {})
check('DotDensity type correct', r7.get('type') == 'CIMDotDensityRenderer')
check('DotDensity fields include U18_FOOD', 'U18_FOOD' in (r7.get('fieldNames') or []))
check('DotDensity fields include O60_FOOD', 'O60_FOOD' in (r7.get('fieldNames') or []))
check('DotDensity dotValue=100', r7.get('dotValue') == 100)
check('DotDensity dotSize=2', r7.get('dotSize') == 2)

# === TUTORIAL 2-8 ===
print('\n=== Tutorial 2-8 ===')
t28 = BASE + 'Tutorial2-8FozhanBabaeiyan.aprx'
zl8 = load(t28, 'new_york_city_zoning/zoninglanduse.xml')
check('T28 ZoningLandUse displayAnnotation=true', zl8.get('displayAnnotation') == True)
lc8 = zl8.get('labelClasses', [])
check('T28 ZoningLandUse LC has minimumScale', lc8 and lc8[0].get('minimumScale') is not None)

nei8 = load(t28, 'new_york_city_zoning/neighborhoods.xml')
check('T28 Neighborhoods visibility=False', nei8.get('visibility') == False)
check('T28 Neighborhoods displayAnnotation=true', nei8.get('displayAnnotation') == True)
nlc8 = nei8.get('labelClasses', [])
check('T28 Neighborhoods LC has maximumScale', nlc8 and nlc8[0].get('maximumScale') is not None)

water8 = load(t28, 'new_york_city_zoning/water.xml')
check('T28 Water visibility=False', water8.get('visibility') == False)
wlc8 = water8.get('labelClasses', [])
check('T28 Water LC has minimumScale', wlc8 and wlc8[0].get('minimumScale') is not None)

bor8 = load(t28, 'new_york_city_land_use_school_study/boroughs.json')
check('T28 Boroughs displayAnnotation=true', bor8.get('displayAnnotation') == True)
blc8 = bor8.get('labelClasses', [])
check('T28 Boroughs LC has maximumScale', blc8 and blc8[0].get('maximumScale') is not None)

uuid8 = '0539b3ec33df49d18d3b6a9cc12eb70f.xml'
uuid8_obj = load(t28, uuid8)
check('T28 World Light Gray visibility=False', uuid8_obj.get('visibility') == False)

# === SUMMARY ===
print(f'\n=== SUMMARY: {pass_count} passed, {fail_count} failed ===')
