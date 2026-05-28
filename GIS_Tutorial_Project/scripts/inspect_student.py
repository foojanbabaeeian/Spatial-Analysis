import arcpy

student_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan.aprx'

try:
    aprx = arcpy.mp.ArcGISProject(student_path)
    m = aprx.listMaps('Health Care Clinics')[0]

    for l in m.listLayers():
        if 'Municipalit' in l.name:
            print(f"=== {l.name} ===")
            cim = l.getDefinition('V3')
            print(f"  showLabels: {getattr(cim, 'showLabels', 'NOT FOUND')}")
            print(f"  visibility: {getattr(cim, 'visibility', 'NOT FOUND')}")
            if hasattr(cim, 'labelClasses') and cim.labelClasses:
                for i, lc in enumerate(cim.labelClasses):
                    print(f"  LabelClass {i}:")
                    print(f"    name: {lc.name}")
                    print(f"    expressionEngine: {getattr(lc, 'expressionEngine', 'N/A')}")
                    ts = lc.textSymbol
                    print(f"    textSymbol type: {ts.__class__.__name__}")
                    # CIMSymbolReference has a .symbol attribute
                    if hasattr(ts, 'symbol'):
                        sym = ts.symbol
                        print(f"    ts.symbol type: {sym.__class__.__name__}")
                        print(f"    height: {getattr(sym, 'height', 'N/A')}")
                        if hasattr(sym, 'symbolLayers'):
                            for j, sl in enumerate(sym.symbolLayers):
                                print(f"    SymLayer {j}: {sl.__class__.__name__}")
                                if hasattr(sl, 'color') and sl.color:
                                    print(f"      color: {sl.color.__class__.__name__} = {sl.color.values}")
                                if hasattr(sl, 'haloSize'):
                                    print(f"      haloSize: {sl.haloSize}")
                                if hasattr(sl, 'haloSymbol'):
                                    hs = sl.haloSymbol
                                    print(f"      haloSymbol: {hs}")
                                    if hs and hasattr(hs, 'symbolLayers'):
                                        for k, hsl in enumerate(hs.symbolLayers):
                                            print(f"        haloLayer {k}: {hsl.__class__.__name__}")
                                            if hasattr(hsl, 'color') and hsl.color:
                                                print(f"          color: {hsl.color.values}")
                                            if hasattr(hsl, 'width'):
                                                print(f"          width: {hsl.width}")
            else:
                print("  No labelClasses!")

    del aprx
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
