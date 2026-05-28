import arcpy

student_path = r'C:\Users\fooja\Desktop\Chapter1_Tutorials\Tutorial1-4FozhanBabaeiyan.aprx'
PASS = "  ✓ PASS"
FAIL = "  ✗ FAIL"

try:
    aprx = arcpy.mp.ArcGISProject(student_path)
    m = aprx.listMaps('Health Care Clinics')[0]
    issues = []

    print("=" * 60)
    print("TUTORIAL 1-4 VERIFICATION")
    print("=" * 60)

    # ── FQHC Clinics ────────────────────────────────────────────
    print("\n[FQHC Clinics]")
    for l in m.listLayers():
        if l.name == 'FQHC Clinics':
            cim = l.getDefinition('V3')
            sym = cim.renderer.symbol.symbol
            for sl in sym.symbolLayers:
                if hasattr(sl, 'size'):
                    ok = abs(sl.size - 8) < 0.01
                    print(f"  Size = {sl.size}" + (PASS if ok else FAIL + " (expected 8)"))
                    if not ok: issues.append("FQHC size wrong")
                if hasattr(sl, 'markerGraphics') and sl.markerGraphics:
                    for mg in sl.markerGraphics:
                        for isl in mg.symbol.symbolLayers:
                            if isl.__class__.__name__ == 'CIMSolidFill':
                                c = isl.color.values
                                ok = (c[0] == 76 and c[1] == 230 and c[2] == 0)
                                print(f"  Fill color = {c}" + (PASS if ok else FAIL + " (expected [76,230,0,100])"))
                                if not ok: issues.append("FQHC fill color wrong")
                            if isl.__class__.__name__ == 'CIMSolidStroke':
                                c = isl.color.values
                                ok = (c[0] == 0 and c[1] == 0 and c[2] == 0)
                                print(f"  Stroke color = {c}" + (PASS if ok else FAIL))

    # ── Poverty Risk Area ────────────────────────────────────────
    print("\n[Poverty Risk Area]")
    for l in m.listLayers():
        if l.name == 'Poverty Risk Area':
            cim = l.getDefinition('V3')
            sym = cim.renderer.symbol.symbol
            for sl in sym.symbolLayers:
                if sl.__class__.__name__ == 'CIMSolidStroke':
                    ok_w = abs(sl.width - 2) < 0.01
                    print(f"  Stroke width = {sl.width}" + (PASS if ok_w else FAIL + " (expected 2)"))
                    if not ok_w: issues.append("Poverty width wrong")
                    c = sl.color.values
                    # Dark red family: R>0, G==0, B==0, R<=130
                    ok_c = (c[0] <= 130 and c[1] == 0 and c[2] == 0 and c[3] == 100)
                    print(f"  Stroke color = {c}" + (PASS if ok_c else FAIL + " (expected dark red)"))
                    if not ok_c: issues.append("Poverty color wrong")

    # ── Municipalities ──────────────────────────────────────────
    print("\n[Municipalities]")
    for l in m.listLayers():
        if l.name == 'Municipalities':
            cim = l.getDefinition('V3')

            # Layer visibility
            ok = (cim.visibility == False)
            print(f"  Layer visibility = {cim.visibility}" + (PASS if ok else FAIL + " (expected False)"))
            if not ok: issues.append("Municipalities visibility wrong")

            # Labels on
            ok = (cim.labelVisibility == True)
            print(f"  labelVisibility = {cim.labelVisibility}" + (PASS if ok else FAIL + " (expected True)"))
            if not ok: issues.append("Municipalities labelVisibility wrong")

            lc = cim.labelClasses[0]
            ts = lc.textSymbol.symbol

            # Font size
            ok = abs(ts.height - 7) < 0.01
            print(f"  Font size = {ts.height}" + (PASS if ok else FAIL + " (expected 7)"))
            if not ok: issues.append("Municipalities font size wrong")

            # Text color (dark gray 60%)
            for sl in ts.symbol.symbolLayers:
                if sl.__class__.__name__ == 'CIMSolidFill':
                    c = sl.color.values
                    # Allow range around gray 60% (RGB ~100-110)
                    ok = (90 <= c[0] <= 115 and 90 <= c[1] <= 115 and 90 <= c[2] <= 115)
                    print(f"  Text color = {c}" + (PASS if ok else FAIL + " (expected ~[102,102,102])"))
                    if not ok: issues.append("Municipalities text color wrong")

            # Halo size
            ok = abs(ts.haloSize - 0.75) < 0.01
            print(f"  Halo size = {ts.haloSize}" + (PASS if ok else FAIL + " (expected 0.75)"))
            if not ok: issues.append("Municipalities halo size wrong")

            # Halo symbol exists
            ok = ts.haloSymbol is not None
            print(f"  Halo symbol exists = {ok}" + (PASS if ok else FAIL))
            if not ok:
                issues.append("Municipalities halo symbol missing")
            else:
                for hsl in ts.haloSymbol.symbolLayers:
                    if hsl.__class__.__name__ == 'CIMSolidFill':
                        c = hsl.color.values
                        ok = (c[0] == 255 and c[1] == 255 and c[2] == 255)
                        print(f"  Halo fill color = {c}" + (PASS if ok else FAIL + " (expected white)"))
                        if not ok: issues.append("Halo not white")

    # ── Maps present ────────────────────────────────────────────
    print("\n[Maps]")
    map_names = [mm.name for mm in aprx.listMaps()]
    ok = 'Health Care Clinics' in map_names
    print(f"  Health Care Clinics map: {ok}" + (PASS if ok else FAIL))
    ok = 'Health Care Clinics_3D' in map_names
    print(f"  Health Care Clinics_3D scene: {ok}" + (PASS if ok else FAIL))

    del aprx

    print("\n" + "=" * 60)
    if issues:
        print(f"ISSUES FOUND ({len(issues)}):")
        for i in issues:
            print(f"  - {i}")
    else:
        print("ALL CHECKS PASSED ✓")
    print("=" * 60)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
