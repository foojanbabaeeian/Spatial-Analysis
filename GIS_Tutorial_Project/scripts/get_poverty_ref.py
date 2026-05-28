import arcpy
import json

ref_path = r'C:\Users\fooja\Documents\GitHub\Spatial Analysis\GISTforPro\EsriPress\GISTforPro\Chapter1\Tutorials\Tutorial1-4.aprx'

try:
    aprx = arcpy.mp.ArcGISProject(ref_path)
    for m in aprx.listMaps():
        for l in m.listLayers():
            if 'Poverty' in l.name or 'poverty' in l.name.lower():
                print(f"\nFound: {l.name} in map: {m.name}")
                try:
                    cim = l.getDefinition('V3')
                    sym = cim.renderer.symbol.symbol  # CIMPolygonSymbol
                    print(f"Symbol class: {sym.__class__.__name__}")
                    if sym.symbolLayers:
                        for i, sl in enumerate(sym.symbolLayers):
                            print(f"  Layer {i}: {sl.__class__.__name__}")
                            if hasattr(sl, 'width'):
                                print(f"    width: {sl.width}")
                            if hasattr(sl, 'color') and sl.color:
                                print(f"    color: {sl.color.__class__.__name__} = {sl.color.values}")
                            if hasattr(sl, 'enable'):
                                print(f"    enable: {sl.enable}")
                except Exception as e:
                    print(f"  Error: {e}")
    del aprx
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
