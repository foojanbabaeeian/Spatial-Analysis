import arcpy

aprx_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan.aprx'
copy_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan_sym.aprx'

# Quetzal Green from ArcGIS Colors palette: RGB(57, 168, 117)
QUETZAL_GREEN = [57, 168, 117, 100]
TARGET_SIZE = 8

try:
    aprx = arcpy.mp.ArcGISProject(aprx_path)
    m = aprx.listMaps('Health Care Clinics')[0]

    lyr = None
    for l in m.listLayers():
        if l.name == 'FQHC Clinics':
            lyr = l
            break

    if lyr is None:
        print("ERROR: FQHC Clinics not found")
    else:
        print(f"Found: {lyr.name}")
        cim = lyr.getDefinition('V3')
        sym = cim.renderer.symbol.symbol  # CIMPointSymbol

        print(f"Symbol class: {sym.__class__.__name__}")
        print(f"Number of symbol layers: {len(sym.symbolLayers) if sym.symbolLayers else 0}")

        changed = False
        for i, sl in enumerate(sym.symbolLayers or []):
            sl_class = sl.__class__.__name__
            print(f"  Layer {i}: {sl_class}")

            # Size - on marker layers
            if hasattr(sl, 'size'):
                print(f"    size: {sl.size}")
                sl.size = TARGET_SIZE
                print(f"    -> set to {TARGET_SIZE}")
                changed = True

            # Color - on marker fill layers (CIMCharacterMarker, CIMVectorMarker, CIMSolidStroke, etc.)
            if hasattr(sl, 'color') and sl.color is not None:
                c = sl.color
                print(f"    color type: {c.__class__.__name__}, values: {getattr(c, 'values', None)}")
                c.values = QUETZAL_GREEN
                print(f"    -> color set to {QUETZAL_GREEN}")
                changed = True

            # Some symbol layers have nested symbolLayers (e.g. CIMVectorMarker)
            if hasattr(sl, 'frame') and sl.frame is not None:
                f = sl.frame
                if hasattr(f, 'color') and f.color is not None:
                    print(f"    frame color type: {f.color.__class__.__name__}, values: {getattr(f.color, 'values', None)}")

        if changed:
            lyr.setDefinition(cim)
            aprx.saveACopy(copy_path)
            print(f"\nSaved copy to: {copy_path}")
            print("SUCCESS")
        else:
            print("WARNING: No changes applied")

    del aprx

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
