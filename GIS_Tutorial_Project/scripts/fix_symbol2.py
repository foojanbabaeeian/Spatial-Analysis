import arcpy

aprx_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan.aprx'
copy_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan_sym.aprx'

# Quetzal Green from ArcGIS Colors palette: RGB(57, 168, 117)
QUETZAL_GREEN = [57, 168, 117, 100]
TARGET_SIZE = 8

def print_obj(obj, prefix=""):
    """Recursively print CIM object attributes"""
    if obj is None:
        return
    cls = obj.__class__.__name__
    if cls in ('str', 'int', 'float', 'bool', 'NoneType'):
        return
    print(f"{prefix}[{cls}]")
    for attr in dir(obj):
        if attr.startswith('_'):
            continue
        try:
            val = getattr(obj, attr)
            if callable(val):
                continue
            val_cls = val.__class__.__name__
            if val_cls in ('str', 'int', 'float', 'bool'):
                print(f"{prefix}  {attr}: {val}")
            elif val_cls == 'list':
                print(f"{prefix}  {attr}: list[{len(val)}]")
                for i, item in enumerate(val[:3]):
                    print_obj(item, prefix + f"    [{i}] ")
            elif val is not None:
                print(f"{prefix}  {attr}: ({val_cls})")
                if val_cls not in ('method', 'builtin_function_or_method'):
                    print_obj(val, prefix + "    ")
        except Exception:
            pass

try:
    aprx = arcpy.mp.ArcGISProject(aprx_path)
    m = aprx.listMaps('Health Care Clinics')[0]

    lyr = None
    for l in m.listLayers():
        if l.name == 'FQHC Clinics':
            lyr = l
            break

    if lyr:
        cim = lyr.getDefinition('V3')
        sym = cim.renderer.symbol.symbol  # CIMPointSymbol

        print("=== FULL SYMBOL STRUCTURE ===")
        for i, sl in enumerate(sym.symbolLayers or []):
            print(f"\n--- Symbol Layer {i}: {sl.__class__.__name__} ---")
            print_obj(sl, "  ")

    del aprx

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
