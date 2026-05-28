import arcpy

student_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan.aprx'

# Dark Red = ArcGIS "Dark Red" = RGB(115, 0, 0) -- 2nd col, 4th row in standard ArcGIS color picker
DARK_RED = [115, 0, 0, 100]
POVERTY_STROKE_WIDTH = 2

# Dark Gray 60% = RGB(102, 102, 102) = #666666
DARK_GRAY_60 = [102, 102, 102, 100]
LABEL_FONT_SIZE = 7
HALO_SIZE = 0.75
HALO_WHITE = [255, 255, 255, 100]

try:
    aprx = arcpy.mp.ArcGISProject(student_path)
    m = aprx.listMaps('Health Care Clinics')[0]

    # ─── 1. Poverty Risk Area ──────────────────────────────────────────────────
    for l in m.listLayers():
        if l.name == 'Poverty Risk Area':
            print(f"Found: {l.name}")
            cim = l.getDefinition('V3')
            sym = cim.renderer.symbol.symbol  # CIMPolygonSymbol
            changed = False
            for sl in sym.symbolLayers:
                if sl.__class__.__name__ == 'CIMSolidStroke':
                    print(f"  Stroke width: {sl.width} -> {POVERTY_STROKE_WIDTH}")
                    sl.width = POVERTY_STROKE_WIDTH
                    print(f"  Stroke color: {sl.color.values} -> {DARK_RED}")
                    sl.color.values = DARK_RED
                    changed = True
            if changed:
                l.setDefinition(cim)
                print("  Poverty Risk Area updated.")
            else:
                print("  WARNING: No stroke found.")

    # ─── 2. Municipalities labels ──────────────────────────────────────────────
    for l in m.listLayers():
        if l.name == 'Municipalities':
            print(f"\nFound: {l.name}")
            cim = l.getDefinition('V3')

            lc = cim.labelClasses[0]
            ts = lc.textSymbol.symbol  # CIMTextSymbol

            # Font size
            print(f"  height: {ts.height} -> {LABEL_FONT_SIZE}")
            ts.height = LABEL_FONT_SIZE

            # Text color (dark gray 60%)
            poly_sym = ts.symbol  # CIMPolygonSymbol
            for sl in poly_sym.symbolLayers:
                if sl.__class__.__name__ == 'CIMSolidFill':
                    print(f"  text color: {sl.color.values} -> {DARK_GRAY_60}")
                    sl.color.values = DARK_GRAY_60

            # Halo: white fill, no stroke, size 0.75
            print(f"  haloSize: {ts.haloSize} -> {HALO_SIZE}")
            ts.haloSize = HALO_SIZE

            # Build halo CIMPolygonSymbol
            halo_sym = arcpy.cim.CreateCIMObjectFromClassName('CIMPolygonSymbol', 'V3')

            halo_stroke = arcpy.cim.CreateCIMObjectFromClassName('CIMSolidStroke', 'V3')
            halo_stroke.enable = False
            halo_stroke.width = 0
            halo_stroke_color = arcpy.cim.CreateCIMObjectFromClassName('CIMRGBColor', 'V3')
            halo_stroke_color.values = [0, 0, 0, 100]
            halo_stroke.color = halo_stroke_color

            halo_fill = arcpy.cim.CreateCIMObjectFromClassName('CIMSolidFill', 'V3')
            halo_fill.enable = True
            halo_fill_color = arcpy.cim.CreateCIMObjectFromClassName('CIMRGBColor', 'V3')
            halo_fill_color.values = HALO_WHITE
            halo_fill.color = halo_fill_color

            halo_sym.symbolLayers = [halo_stroke, halo_fill]
            ts.haloSymbol = halo_sym
            print(f"  haloSymbol: created white fill, no stroke")

            # Turn labels ON (labelVisibility)
            print(f"  labelVisibility: {cim.labelVisibility} -> True")
            cim.labelVisibility = True

            # Layer visibility stays OFF (already False)
            print(f"  visibility stays: {cim.visibility}")

            l.setDefinition(cim)
            print("  Municipalities updated.")

    # ─── 3. Save ────────────────────────────────────────────────────────────────
    aprx.save()
    print("\nProject saved.")
    del aprx

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
