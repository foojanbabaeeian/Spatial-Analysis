import arcpy

ref_path = r'C:\Users\fooja\Documents\GitHub\Spatial Analysis\GISTforPro\EsriPress\GISTforPro\Chapter3\Tutorials\Tutorial3-2.aprx'
stu_path = r'C:\Users\fooja\Desktop\Chapter3\Tutorials\Tutorial3-2FozhanBabaeiyan.aprx'

# Layers to copy renderer from reference -> student
# Format: (map_name, layer_name)
LAYERS_TO_FIX = [
    ('Cost of Living Index', 'Metropolitan Cost of Living Index'),
    ('Cost of Living Index', 'State Cost of Living Index'),
    ('Arts Employment', 'Metropolitan Employment'),
]

try:
    ref_aprx = arcpy.mp.ArcGISProject(ref_path)
    stu_aprx = arcpy.mp.ArcGISProject(stu_path)

    for map_name, layer_name in LAYERS_TO_FIX:
        print(f'\n[{map_name}] -> [{layer_name}]')

        # Get reference renderer CIM
        ref_m = ref_aprx.listMaps(map_name)[0]
        ref_cim = None
        for l in ref_m.listLayers():
            if l.name == layer_name:
                ref_cim = l.getDefinition('V3')
                print(f'  REF renderer: {ref_cim.renderer.__class__.__name__}')
                print(f'  REF method: {ref_cim.renderer.classificationMethod}')
                print(f'  REF breaks: {len(ref_cim.renderer.breaks)}')
                break

        if ref_cim is None:
            print(f'  ERROR: layer not found in reference!')
            continue

        # Apply to student layer
        stu_m = stu_aprx.listMaps(map_name)[0]
        applied = False
        for l in stu_m.listLayers():
            if l.name == layer_name:
                stu_cim = l.getDefinition('V3')
                print(f'  STU renderer before: {stu_cim.renderer.classificationMethod}, {len(stu_cim.renderer.breaks)} breaks')
                # Replace renderer with reference renderer
                stu_cim.renderer = ref_cim.renderer
                l.setDefinition(stu_cim)
                print(f'  Applied reference renderer.')
                applied = True
                break

        if not applied:
            print(f'  ERROR: layer not found in student!')

    stu_aprx.save()
    print('\nProject saved.')
    del ref_aprx
    del stu_aprx
    print('DONE.')

except Exception as e:
    print(f'ERROR: {e}')
    import traceback
    traceback.print_exc()
