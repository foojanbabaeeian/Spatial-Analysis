import arcpy
import shutil
import os

aprx_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan.aprx'
copy_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan_fixed.aprx'

# From reference Tutorial1-4.aprx: Quetzal Green = RGB(76, 230, 0)
QUETZAL_GREEN_FILL = [76, 230, 0, 100]
OUTLINE_COLOR = [0, 0, 0, 100]  # black outline (keep as is)
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

        changed = False
        for sl in sym.symbolLayers or []:
            # Set size on the vector marker
            if hasattr(sl, 'size'):
                print(f"  size: {sl.size} -> {TARGET_SIZE}")
                sl.size = TARGET_SIZE
                changed = True

            # Navigate into markerGraphics to change fill color
            if hasattr(sl, 'markerGraphics') and sl.markerGraphics:
                for mg in sl.markerGraphics:
                    inner_sym = mg.symbol
                    if hasattr(inner_sym, 'symbolLayers'):
                        for isl in inner_sym.symbolLayers:
                            if isl.__class__.__name__ == 'CIMSolidFill':
                                if isl.color is not None:
                                    print(f"  fill color: {isl.color.values} -> {QUETZAL_GREEN_FILL}")
                                    isl.color.values = QUETZAL_GREEN_FILL
                                    changed = True
                            # Keep stroke as black (already correct per reference)
                            elif isl.__class__.__name__ == 'CIMSolidStroke':
                                if isl.color is not None:
                                    print(f"  stroke color: {isl.color.values} (keeping)")

        if changed:
            lyr.setDefinition(cim)
            aprx.saveACopy(copy_path)
            print(f"\nSaved to: {copy_path}")
            print("SUCCESS")
        else:
            print("WARNING: No changes")

    del aprx

    # Replace original with fixed copy
    if os.path.exists(copy_path):
        shutil.copy2(copy_path, aprx_path)
        os.remove(copy_path)
        print(f"Original overwritten with fixed version.")
    else:
        print("ERROR: copy not created")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
