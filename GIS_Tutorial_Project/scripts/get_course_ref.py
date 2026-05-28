import arcpy

# Course-provided completed Tutorial 1-4
course_path = r'C:\Users\fooja\Documents\GitHub\Spatial Analysis\H-SC-460B-Sec01-9223-Pub-Hlth-Maps-Spatial-Analysis-2026-May-16_07-08-10-802\viewer\files\Chapter1_Tutorials\Tutorial1-4.aprx'

try:
    aprx = arcpy.mp.ArcGISProject(course_path)
    print("Maps:", [m.name for m in aprx.listMaps()])

    for m in aprx.listMaps():
        for l in m.listLayers():
            if 'Poverty' in l.name:
                print(f"\n=== {l.name} in {m.name} ===")
                cim = l.getDefinition('V3')
                sym = cim.renderer.symbol.symbol
                for i, sl in enumerate(sym.symbolLayers):
                    print(f"  Layer {i}: {sl.__class__.__name__}")
                    if hasattr(sl, 'width'):
                        print(f"    width: {sl.width}")
                    if hasattr(sl, 'color') and sl.color:
                        print(f"    color: {sl.color.values}")

            if 'Municipalit' in l.name:
                print(f"\n=== {l.name} in {m.name} ===")
                cim = l.getDefinition('V3')
                print(f"  showLabels: {getattr(cim, 'showLabels', 'N/A')}")
                print(f"  visibility: {getattr(cim, 'visibility', 'N/A')}")
                if hasattr(cim, 'labelClasses') and cim.labelClasses:
                    for lc in cim.labelClasses:
                        ts = lc.textSymbol
                        if ts:
                            sym = ts.symbol if hasattr(ts, 'symbol') else ts
                            print(f"  TextSymbol height: {getattr(sym, 'height', 'N/A')}")
                            if hasattr(sym, 'symbolLayers'):
                                for j, sl in enumerate(sym.symbolLayers):
                                    print(f"    SymLayer {j}: {sl.__class__.__name__}")
                                    if hasattr(sl, 'color') and sl.color:
                                        print(f"      color: {sl.color.values}")
                                    if hasattr(sl, 'haloSize'):
                                        print(f"      haloSize: {sl.haloSize}")
                                    if hasattr(sl, 'haloSymbol') and sl.haloSymbol:
                                        hs = sl.haloSymbol
                                        print(f"      haloSymbol: {hs.__class__.__name__}")
                                        if hasattr(hs, 'symbolLayers'):
                                            for k, hsl in enumerate(hs.symbolLayers):
                                                print(f"        haloLayer {k}: {hsl.__class__.__name__}")
                                                if hasattr(hsl, 'color') and hsl.color:
                                                    print(f"          color: {hsl.color.values}")
                                                if hasattr(hsl, 'width'):
                                                    print(f"          width: {hsl.width}")
    del aprx
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
