import arcpy
import json

# Read the reference tutorial file to get the exact symbol
ref_path = r'C:\Users\fooja\Documents\GitHub\Spatial Analysis\GISTforPro\EsriPress\GISTforPro\Chapter1\Tutorials\Tutorial1-4.aprx'

try:
    aprx = arcpy.mp.ArcGISProject(ref_path)
    maps = aprx.listMaps()
    print("Maps:", [m.name for m in maps])

    for m in maps:
        layers = m.listLayers()
        for l in layers:
            if 'FQHC' in l.name or 'fqhc' in l.name.lower() or 'Clinic' in l.name:
                print(f"\nFound layer: {l.name} in map: {m.name}")
                try:
                    cim = l.getDefinition('V3')
                    sym = cim.renderer.symbol.symbol

                    print(f"Symbol class: {sym.__class__.__name__}")
                    if sym.symbolLayers:
                        for i, sl in enumerate(sym.symbolLayers):
                            print(f"  Layer {i}: {sl.__class__.__name__}")
                            if hasattr(sl, 'size'):
                                print(f"    size: {sl.size}")
                            if hasattr(sl, 'markerGraphics') and sl.markerGraphics:
                                for j, mg in enumerate(sl.markerGraphics):
                                    inner_sym = mg.symbol
                                    print(f"    markerGraphic {j}: {inner_sym.__class__.__name__}")
                                    if hasattr(inner_sym, 'symbolLayers'):
                                        for k, isl in enumerate(inner_sym.symbolLayers):
                                            print(f"      inner layer {k}: {isl.__class__.__name__}")
                                            if hasattr(isl, 'color') and isl.color:
                                                print(f"        color: {isl.color.__class__.__name__} = {isl.color.values}")
                except Exception as e:
                    print(f"  Error: {e}")

    del aprx

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
