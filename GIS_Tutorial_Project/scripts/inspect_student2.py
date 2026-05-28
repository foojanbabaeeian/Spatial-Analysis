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

            print(f"CIMTextSymbol attributes:")
            for attr in dir(ts):
                if not attr.startswith('_'):
                    try:
                        val = getattr(ts, attr)
                        if not callable(val):
                            print(f"  {attr}: {val}")
                    except:
                        pass

    del aprx
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
