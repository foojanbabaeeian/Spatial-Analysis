import arcpy

student_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan.aprx'

try:
    aprx = arcpy.mp.ArcGISProject(student_path)
    m = aprx.listMaps('Health Care Clinics')[0]

    for l in m.listLayers():
        if 'Municipalit' in l.name:
            cim = l.getDefinition('V3')
            lc = cim.labelClasses[0]
            ts = lc.textSymbol.symbol  # CIMTextSymbol

            # Inspect ts.symbol (the CIMPolygonSymbol for text color)
            poly_sym = ts.symbol
            print(f"ts.symbol type: {poly_sym.__class__.__name__}")
            if hasattr(poly_sym, 'symbolLayers'):
                for i, sl in enumerate(poly_sym.symbolLayers):
                    print(f"  Layer {i}: {sl.__class__.__name__}")
                    if hasattr(sl, 'color') and sl.color:
                        print(f"    color: {sl.color.__class__.__name__} = {sl.color.values}")
                    if hasattr(sl, 'enable'):
                        print(f"    enable: {sl.enable}")

            # Check label class visibility
            print(f"\nlabelClass visibility: {getattr(lc, 'visibility', 'N/A')}")

            # Check the layer's label visibility property
            print(f"\nLayer CIM attrs related to labels:")
            for attr in dir(cim):
                if 'label' in attr.lower() and not attr.startswith('_'):
                    try:
                        val = getattr(cim, attr)
                        if not callable(val):
                            print(f"  {attr}: {val}")
                    except:
                        pass

    del aprx
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
