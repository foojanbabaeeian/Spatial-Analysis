import arcpy

# Search for Quetzal Green in the ArcGIS Colors style
try:
    # Try to get the color from the style manager
    style_items = arcpy.ListStyleItems("", "Color", "Quetzal Green")
    if style_items:
        for item in style_items:
            print(f"Name: {item.name}")
            print(f"Category: {item.category}")
            print(f"Style path: {item.stylePath}")
    else:
        print("Not found via ListStyleItems")
except Exception as e:
    print(f"ListStyleItems error: {e}")

# Also try arcpy.mp approach
try:
    # Get the color from a temporary symbol
    sym = arcpy.symbols.SimpleMarkerSymbol()
    print(f"Symbol type: {type(sym)}")
except Exception as e:
    print(f"Symbol error: {e}")

# Try fetching from a style file
import os
style_paths = [
    r"C:\Users\fooja\AppData\Local\Programs\ArcGIS\Pro\Resources\Styles",
]
for sp in style_paths:
    if os.path.exists(sp):
        print(f"Style path exists: {sp}")
        for f in os.listdir(sp):
            print(f"  {f}")
    else:
        print(f"Not found: {sp}")
