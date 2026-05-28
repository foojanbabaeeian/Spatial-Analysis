import arcpy
import json

ref_path = r'C:\Users\fooja\Documents\GitHub\Spatial Analysis\GISTforPro\EsriPress\GISTforPro\Chapter1\Tutorials\Tutorial1-4.aprx'

try:
    aprx = arcpy.mp.ArcGISProject(ref_path)
    for m in aprx.listMaps():
        for l in m.listLayers():
            if 'Municipalit' in l.name or 'municipalit' in l.name.lower():
                print(f"\nFound: {l.name} in map: {m.name}")
                cim = l.getDefinition('V3')
                # Check label classes
                if hasattr(cim, 'labelClasses') and cim.labelClasses:
                    for i, lc in enumerate(cim.labelClasses):
                        print(f"  LabelClass {i}: name={lc.name}")
                        ts = lc.textSymbol
                        if ts:
                            sym = ts.symbol if hasattr(ts, 'symbol') else ts
                            print(f"    TextSymbol type: {sym.__class__.__name__}")
                            if hasattr(sym, 'height'):
                                print(f"    height/size: {sym.height}")
                            if hasattr(sym, 'symbol'):
                                inner = sym.symbol
                                if hasattr(inner, 'height'):
                                    print(f"    inner height: {inner.height}")
                                if hasattr(inner, 'symbolLayers'):
                                    for j, sl in enumerate(inner.symbolLayers):
                                        print(f"    SymLayer {j}: {sl.__class__.__name__}")
                                        if hasattr(sl, 'color') and sl.color:
                                            print(f"      color: {sl.color.values}")
                                        if hasattr(sl, 'haloSymbol') and sl.haloSymbol:
                                            print(f"      haloSymbol: {sl.haloSymbol.__class__.__name__}")
                                            if hasattr(sl, 'haloSize'):
                                                print(f"      haloSize: {sl.haloSize}")
                            # Try direct access
                            if hasattr(sym, 'symbolLayers'):
                                for j, sl in enumerate(sym.symbolLayers):
                                    print(f"    SymLayer {j}: {sl.__class__.__name__}")
                                    if hasattr(sl, 'color') and sl.color:
                                        print(f"      color: {sl.color.values}")
                                    if hasattr(sl, 'haloSymbol') and sl.haloSymbol:
                                        print(f"      haloSymbol class: {sl.haloSymbol.__class__.__name__}")
                                        hs = sl.haloSymbol
                                        if hasattr(hs, 'symbolLayers'):
                                            for k, hsl in enumerate(hs.symbolLayers):
                                                print(f"        halo layer {k}: {hsl.__class__.__name__}")
                                                if hasattr(hsl, 'color') and hsl.color:
                                                    print(f"          color: {hsl.color.values}")
                                                if hasattr(hsl, 'width'):
                                                    print(f"          width: {hsl.width}")
                                    if hasattr(sl, 'haloSize'):
                                        print(f"      haloSize: {sl.haloSize}")
                # Check if labels are enabled
                if hasattr(cim, 'showLabels'):
                    print(f"  showLabels: {cim.showLabels}")
                if hasattr(cim, 'visibility'):
                    print(f"  visibility: {cim.visibility}")
    del aprx
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
