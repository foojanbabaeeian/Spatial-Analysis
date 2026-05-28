import arcpy
import shutil
import os

aprx_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-3FozhanBabaeiyan.aprx'
tbl_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Chapter1.gdb\SummaryStatistics'
copy_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-3FozhanBabaeiyan_new.aprx'

try:
    aprx = arcpy.mp.ArcGISProject(aprx_path)
    maps = aprx.listMaps()
    print('Maps:', [m.name for m in maps])

    # Add to the 2D map "Health Care Clinics"
    m = aprx.listMaps('Health Care Clinics')[0]
    print('Using map:', m.name)

    # Check if table already exists
    existing = [t.name for t in m.listTables()]
    print('Existing tables:', existing)

    if 'SummaryStatistics' not in existing:
        m.addDataFromPath(tbl_path)
        print('Table added.')
    else:
        print('Table already exists in map.')

    # Save a copy
    aprx.saveACopy(copy_path)
    print('SaveACopy done:', copy_path)

    # Overwrite original with copy
    del aprx  # Release the object

    if os.path.exists(copy_path):
        shutil.copy2(copy_path, aprx_path)
        os.remove(copy_path)
        print('Original overwritten with new copy.')
    else:
        print('ERROR: copy file not found!')

except Exception as e:
    print('ERROR:', str(e))
    import traceback
    traceback.print_exc()
