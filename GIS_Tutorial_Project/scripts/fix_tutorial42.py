import arcpy

aprx_path = r'C:\Users\fooja\Desktop\Chapter4\Tutorials\Tutorial4-2FozhanBabaeiyan.aprx'
gdb = r'C:\Users\fooja\Desktop\Chapter4\Tutorials\Tutorial4_Work.gdb'
popYouth_table = gdb + r'\PopYouth'
tracts_fc = gdb + r'\Tracts_PopYouth'

# ── 1. Build PopYouth lookup dict {GEOID_txt(10-digit): (PopTotal,...)} ──────
print('[1] Building PopYouth lookup...')
lookup = {}
with arcpy.da.SearchCursor(
        popYouth_table,
        ['GEOID_txt', 'PopTotal', 'PopUnder5', 'Pop5To9', 'Pop10To14', 'Pop15To19']) as cur:
    for row in cur:
        lookup[row[0]] = (row[1], row[2], row[3], row[4], row[5])
print(f'    Lookup entries: {len(lookup)}')

# ── 2. Update Tracts_PopYouth rows ────────────────────────────────────────────
print('[2] Populating Tracts_PopYouth...')
update_fields = ['GEOID', 'PopTotal', 'PopUnder5', 'Pop5To9',
                 'Pop10To14', 'Pop15To19', 'PopUnder20', 'PctUnder20']
updated = 0
missing_ids = []
with arcpy.da.UpdateCursor(tracts_fc, update_fields) as cur:
    for row in cur:
        geoid11 = row[0]                        # e.g. "04013618300"
        geoid10 = geoid11.lstrip('0')           # e.g.  "4013618300"
        if geoid10 in lookup:
            pt, p5, p59, p1014, p1519 = lookup[geoid10]
            p_under20 = (p5 or 0) + (p59 or 0) + (p1014 or 0) + (p1519 or 0)
            pct = (p_under20 / pt * 100.0) if (pt and pt > 0) else 0.0
            row[1] = pt
            row[2] = p5
            row[3] = p59
            row[4] = p1014
            row[5] = p1519
            row[6] = p_under20
            row[7] = pct
            cur.updateRow(row)
            updated += 1
        else:
            missing_ids.append(geoid10)
print(f'    Updated: {updated}  Missing: {len(missing_ids)}')
if missing_ids[:3]:
    print(f'    Sample missing: {missing_ids[:3]}')

# ── 3. Read all PctUnder20 values ─────────────────────────────────────────────
print('[3] Reading PctUnder20 values...')
vals = []
with arcpy.da.SearchCursor(tracts_fc, ['PctUnder20']) as cur:
    for row in cur:
        if row[0] is not None and row[0] > 0:
            vals.append(row[0])
vals.sort()
print(f'    Count: {len(vals)}  Min: {min(vals):.2f}  Max: {max(vals):.2f}')

# ── 4. Compute 5-class Jenks Natural Breaks ───────────────────────────────────
def jenks_breaks(data, k):
    """Returns k upper-bound break values for k classes (Jenks Natural Breaks)."""
    data = sorted(data)
    n = len(data)

    # n×k matrices for lower class limits and variance sums
    lcl = [[0] * (k + 1) for _ in range(n + 1)]
    vcm = [[1e30] * (k + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        lcl[i][1] = 1
        vcm[i][1] = 0.0

    for l in range(2, n + 1):
        s = 0.0; s2 = 0.0; nv = 0
        for m in range(1, l + 1):
            lo = l - m + 1
            v = data[lo - 1]
            nv += 1; s += v; s2 += v * v
            var = s2 - s * s / nv
            i4 = lo - 1
            if i4 != 0:
                for j in range(2, k + 1):
                    cand = var + vcm[i4][j - 1]
                    if vcm[l][j] >= cand:
                        lcl[l][j] = lo
                        vcm[l][j] = cand
        lcl[l][1] = 1
        vcm[l][1] = s2 - s * s / nv

    # Back-trace to get break upper bounds
    breaks = [0.0] * k
    breaks[k - 1] = data[n - 1]
    idx = n
    for j in range(k, 1, -1):
        prev_idx = lcl[idx][j] - 2
        breaks[j - 2] = data[prev_idx]
        idx = lcl[idx][j] - 1
    return breaks   # k values = upper bound of each class

print('[4] Computing Jenks Natural Breaks (5 classes)...')
breaks = jenks_breaks(vals, 5)
print(f'    Breaks: {[round(b, 2) for b in breaks]}')

# ── 5. Define color ramp (YlOrRd 5-class, matching T4-5 palette) ──────────────
COLORS = [
    [254, 240, 217, 100],   # class 1 – light yellow
    [253, 204, 138, 100],   # class 2 – yellow-orange
    [252, 141,  89, 100],   # class 3 – orange
    [227,  74,  51, 100],   # class 4 – orange-red
    [179,   0,   0, 100],   # class 5 – dark red
]
STROKE_COLOR = [0, 0, 0, 100]
STROKE_WIDTH = 0.4

# ── 6. Build CIM renderer and apply ──────────────────────────────────────────
print('[5] Building CIM renderer...')
aprx = arcpy.mp.ArcGISProject(aprx_path)
m = aprx.listMaps('Tutorial4-2 Population Under 20')[0]
for lyr in m.listLayers():
    if lyr.name == 'Tracts_PopYouth':
        cim = lyr.getDefinition('V3')
        r = cim.renderer   # CIMClassBreaksRenderer already set up

        # Set method and field
        r.classificationMethod = 'NaturalBreaks'
        r.field = 'PctUnder20'

        # Build 5 new break objects from the existing first break as template
        template_break = r.breaks[0]
        new_breaks = []
        for i, upper in enumerate(breaks):
            # Clone the template break via CIM
            b = arcpy.cim.CreateCIMObjectFromClassName('CIMClassBreak', 'V3')
            b.upperBound = upper

            # Build polygon symbol
            poly_sym = arcpy.cim.CreateCIMObjectFromClassName('CIMPolygonSymbol', 'V3')

            stroke = arcpy.cim.CreateCIMObjectFromClassName('CIMSolidStroke', 'V3')
            stroke.enable = True
            stroke.width = STROKE_WIDTH
            stroke_color = arcpy.cim.CreateCIMObjectFromClassName('CIMRGBColor', 'V3')
            stroke_color.values = STROKE_COLOR
            stroke.color = stroke_color

            fill = arcpy.cim.CreateCIMObjectFromClassName('CIMSolidFill', 'V3')
            fill.enable = True
            fill_color = arcpy.cim.CreateCIMObjectFromClassName('CIMRGBColor', 'V3')
            fill_color.values = COLORS[i]
            fill.color = fill_color

            poly_sym.symbolLayers = [stroke, fill]

            sym_ref = arcpy.cim.CreateCIMObjectFromClassName('CIMSymbolReference', 'V3')
            sym_ref.symbol = poly_sym
            b.symbol = sym_ref

            new_breaks.append(b)

        r.breaks = new_breaks
        r.minimumBreak = min(vals)

        lyr.setDefinition(cim)
        print('    Renderer applied.')
        break

aprx.save()
print('    Project saved.')
del aprx
print('\nDONE.')
