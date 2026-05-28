# Video-Sourced GIS Tutorial Guide and Submission Audit

Student: Fozhan Babaeiyan  
Course: HSC 460B Pub Hlth Maps & Spatial Analysis, CSULB Spring 2026  
Instructor in videos: Monica Montano  
Textbook: GIS Tutorial 1 for ArcGIS Pro 3.1  
Prepared from local video transcripts generated on May 20, 2026.

## Sources Used

- Video transcripts: `C:\Users\fooja\Desktop\transcripts\`
- Submitted folders/zips: `C:\Users\fooja\Desktop\Chapter1_Tutorials`, `Chapter2`, `Chapter3`, `Chapter4`
- ArcPy project inspection: `C:\Users\fooja\Desktop\Submitted_Project_Inspection_FozhanBabaeiyan.json`
- Chapter 3 PDF text extracted from:
  - `C:\Users\fooja\Desktop\Chapter3\Tutorials\Resources\MapSharing.pdf`
  - `C:\Users\fooja\Desktop\Chapter3\Tutorials\Resources\StoryMapManuscript.pdf`

Important note: the videos say Chapter 4 is practice and not required for credit, but the assignment context says Chapter 4 was submitted as a chapter zip. This audit treats Chapter 4 as required because the user/course context says to upload it.

## High-Level Audit

All 21 named `.aprx` files exist and ArcPy found no broken layers. The four chapter zip files exist on the Desktop.

Major risk items found:

- Chapter 3 online work is the largest mismatch. The video expects Arts Employment and Cost of Living web maps plus an Arts Employment StoryMap. The current public StoryMap at `https://storymaps.arcgis.com/stories/c8e169c64b844fbc823199ceaf21bbf6` is a 311 Debris/Pittsburgh Neighborhoods StoryMap, not the Arts Employment StoryMap from the transcript.
- No ArcGIS Online items titled Arts Employment or Cost of Living were found under user `029701865_CSULB`; only 311 Debris/Pittsburgh items were found.
- Tutorial 3-1 should export a JPEG layout and a chart image named for the top 10 states. Current folder has `Tutorial3-1_ArtsEmploymentLayout.png`, not the narrated JPEG export, and no obvious `Top10States.jpg` export was found.
- Tutorial 2-3 appears mismatched: the video expects Food Facilities unique values by facility type, but the submitted project shows a class-break renderer on `CAPACITY` with a definition query.
- Tutorial 2-4 appears mismatched: the video expects `Over age 60 receiving food stamps` using `O60_FOOD` plus a 3D scene/extrusion. The submitted Tutorial 2-4 still shows `Neighborhoods` symbolized on `POV_FOOD`.
- Tutorial 2-5 appears mismatched: the video expects renamed layers and graduated/proportional symbols. The submitted Tutorial 2-5 still has two simple-renderer `Neighborhoods` layers.
- Tutorial 2-8 appears partially mismatched: video final state has Neighborhoods, Water, and World Light Gray Canvas off; submitted project has them on.
- Tutorial 1-2 is missing the video-created bookmark `McKees Rocks Poverty Area`; only `Allegheny County`, `Poverty Areas`, and `Pittsburgh East End` were found.
- Tutorial 1-3 should contain field-view/table edits and a `Population Density_Statistics` standalone table. The submitted project inspection found no standalone tables, and the final layer state resembles Tutorial 1-1.
- Tutorial 1-4 should contain FQHC symbol changes, Poverty Risk Area outline changes, Municipalities labels, and temporary Parks work. The submitted project final layer state resembles Tutorial 1-1, so these are not clearly saved.
- Tutorial 4-4 should contain a spatial-join output such as August 2015 Burglaries by Neighborhood, symbolized by `Join_Count`. Submitted Tutorial 4-4 shows only Crime Offenses with a burglary/date definition query, not the joined neighborhood layer.
- Tutorial 4-5 should create central/inside points and symbolize them by `Join_Count`. Submitted Tutorial 4-5 shows a polygon burglaries layer, not an obvious point output.
- Tutorial 4-6 should create `UCRHierarchyCode`, join it to Pittsburgh serious crimes, and symbolize by `Crime Type`. Submitted Tutorial 4-6 still has a simple renderer.

Persistent vs non-persistent warning: actions such as opening popups, clicking a clinic website, previewing a StoryMap, changing the camera angle, selecting rows, or using Swipe are not always saved in the `.aprx`. I only flagged them when the saved artifact should have retained evidence and did not.

---

# Complete Video-Sourced Tutorial Guide

## Tutorial 1-1 - ArcGIS Pro Overview

Goal: open the Chapter 1 health clinic project, learn layer visibility/drawing order, export a layout, and turn on clinic buffers.

1. Open `Tutorial1-1.aprx` from `Chapter1\Tutorials`.
2. If ArcGIS prompts for sign-in, use the organization URL option and type `CSULB`; do not update ArcGIS Pro when the update prompt appears.
3. Go to Project tab > Save Project As.
4. Save in the same Tutorials folder as `Tutorial1-1FozhanBabaeiyan.aprx`; file type must be `.aprx`.
5. In the Health Care Clinics map, use Map tab > Bookmarks > Allegheny County to recenter the map.
6. Add/remove basemaps:
   - Map tab > Layer group > Basemap > Streets.
   - In Contents, scroll to bottom, right-click World Street Map > Remove.
   - Map tab > Basemap > Light Gray Canvas; remove the bottom Light Gray Canvas Base and top Light Gray Canvas Reference if present.
   - Map tab > Basemap > National Geographic; remove all National Geographic/World Hillshade layers it adds.
7. Turn on layers in Contents:
   - Urgent Care Clinics
   - FQHC Clinics
   - Poverty Risk Area
   - Pittsburgh
   - Allegheny County
   - Rivers
   - Streets
8. Demonstrate drawing order:
   - Drag Population Density to the top; note that it covers point/polygon layers.
   - Drag Population Density back down just above Poverty Density.
9. View tab > Catalog Pane if Catalog is not visible.
10. In Catalog, expand Maps and Layouts.
11. Double-click layout `FQHC and Urgent Care Clinics`.
12. Optional pane behavior shown in video: click the pushpin on Catalog to auto-hide it.
13. With the layout active, Share tab > Export Layout.
14. Export settings:
   - File Type: PNG
   - Name: `FQHCAndUrgentCareClinics`
   - Location: Desktop or Chapter 1 Tutorials folder
   - Resolution: 150 dpi
15. Click Export and verify the image opens.
16. Return to the Health Care Clinics map.
17. Turn on:
   - FQHC Buffer
   - Urgent Care Clinics Buffer
18. Return to the layout and confirm the buffers appear in the map/legend.
19. Save with Ctrl+S.

Checklist:

- `Tutorial1-1FozhanBabaeiyan.aprx` exists.
- Health Care Clinics map has Urgent Care Clinics, FQHC Clinics, Poverty Risk Area, Pittsburgh, Allegheny County, Rivers, Streets, Population Density, FQHC Buffer, and Urgent Care Clinics Buffer on.
- Population Density is below the point/boundary layers and above Poverty Density.
- Layout `FQHC and Urgent Care Clinics` exists.
- Exported PNG `FQHCAndUrgentCareClinics.png` exists and shows title, legend, scale bar, and buffers.

Audit for submitted work:

- Mostly matches. The project has no broken layers and final visibility includes both buffers.

## Tutorial 1-2 - Navigate Maps

Goal: use popups, zoom tools, bookmarks, raster visibility, Select By Attributes, and feature searching.

1. Open `Tutorial1-2.aprx`.
2. Project tab > Save Project As > `Tutorial1-2FozhanBabaeiyan.aprx`.
3. Map tab > Navigate group > Full Extent globe to reset.
4. Map tab > Explore. Click the northernmost Urgent Care Clinics point.
5. In the popup, verify it is `Express Care at Wexford Health and Wellness Pavilion`; note name, address, and website.
6. Click the popup website if desired to verify the clinic page.
7. In the popup, click the magnifying glass at bottom right to zoom to the selected urgent care clinic.
8. Notice scale-dependent behavior:
   - Streets labels appear when zoomed in.
   - FQHC Buffer and Urgent Care Clinics Buffer disappear at very close scale.
9. Use mouse drag or arrow keys to pan.
10. Full Extent globe to return to county view.
11. Show raster layer behavior:
   - Leave Poverty Risk Area, Pittsburgh, Allegheny County, Rivers, Streets on.
   - Turn off FQHC Buffer and Urgent Care Clinics Buffer.
   - Turn off Population Density.
   - Turn on Poverty Density.
12. Zoom in to see raster pixels/cells in Poverty Density.
13. Full Extent.
14. Turn Poverty Density off.
15. Turn on all layers except Municipalities and Poverty Density.
16. Map tab > Bookmarks > Poverty Areas.
17. Zoom into the small poverty area near McKees Rocks until streets are visible.
18. Map tab > Bookmarks > New Bookmark.
19. Name it exactly `McKees Rocks Poverty Area`; click OK.
20. Return to Allegheny County bookmark or Full Extent.
21. Use Bookmarks and confirm the new bookmark returns to the same view.
22. Map tab > Bookmarks > Manage Bookmarks.
23. Alphabetize bookmarks:
   - Allegheny County
   - McKees Rocks Poverty Area
   - Pittsburgh East End
   - Poverty Areas
24. Full Extent.
25. In Contents, clear Population Density and turn on Municipalities.
26. Right-click Municipalities > Attribute Table.
27. Map tab > Select By Attributes.
28. Input Rows: Municipalities.
29. Selection Type: New selection.
30. Where clause:
   - Field: `Name`
   - Operator: is equal to
   - Value: `McKees Rocks`
31. Click Apply/OK.
32. In the Municipalities table, use Show Selected Records to view only McKees Rocks.
33. Right-click Municipalities layer > Selection > Zoom To Selection.
34. Clear Selection.
35. Close table.
36. Turn Municipalities off and Population Density on.
37. Right-click FQHC Clinics > Attribute Table.
38. Select By Attributes:
   - Input: FQHC Clinics
   - Field: `Name`
   - Operator: is equal to
   - Value: `Birmingham Free Clinic`
39. Zoom to selected from layer or table.
40. Show selected row only, then Clear Selection.
41. Save.

Checklist:

- `Tutorial1-2FozhanBabaeiyan.aprx` exists.
- Bookmark `McKees Rocks Poverty Area` exists on the Health Care Clinics map.
- No selections remain active.
- Final map is saved with the relevant clinic, boundary, streets, buffer, and Population Density layers available.

Audit for submitted work:

- The expected new bookmark was not found. This is a likely skipped step.

## Tutorial 1-3 - Attribute Data

Goal: manipulate attribute tables, field visibility/aliases, selections, and summary statistics.

1. Open `Tutorial1-3.aprx`.
2. Save As `Tutorial1-3FozhanBabaeiyan.aprx`.
3. Right-click FQHC Clinics > Attribute Table.
4. Drag the `Website` field before `Latitude`.
5. Sort `Name` ascending:
   - Either right-click Name > Sort Ascending, or double-click the field header.
6. Close the FQHC table and save.
7. Turn off all layers; turn on only Population Density.
8. Right-click Population Density > Attribute Table.
9. Sort `PopDensity` descending.
10. Select the row with maximum PopDensity: about `29,492.7`.
11. Try right-click Population Density > Selection > Zoom To Selection.
12. Full Extent, then Clear Selection.
13. Close table.
14. Turn off Population Density and turn on Municipalities.
15. Right-click Municipalities > Attribute Table.
16. Open Field View from the table menu (three horizontal lines) > Fields View.
17. Move `MTFCC` above `STATEFP`; save the Fields edit.
18. Delete `STATEFP`:
   - Select the field row.
   - Right-click the row box > Delete.
   - Save.
19. Hide all fields except `GEOID` and `Name`.
20. Change alias for `Name` to `Municipality`.
21. Save; verify the Municipalities table only shows GEOID and Municipality.
22. Close Fields view.
23. Sort Municipality ascending.
24. Close Municipalities table.
25. Right-click Streets > Attribute Table.
26. Open Fields View.
27. Change alias of `FULLNAME` to `Street Name`.
28. Turn visibility on only for:
   - `FULLNAME`
   - `L_F_ADD`
   - `L_T_ADD`
   - `R_F_ADD`
   - `R_T_ADD`
   - `ZIP_L`
   - `ZIP_R`
29. Save and verify the table now shows Street Name plus the left/right address and ZIP fields.
30. Keep Municipalities on and turn on FQHC Clinics.
31. Open FQHC Clinics table; sort Name ascending.
32. Select the first six rows, then clear selection.
33. Contents pane > List By Selection.
34. Make only Urgent Care Clinics and FQHC Clinics selectable.
35. Return to List By Drawing Order.
36. Map tab > Select.
37. Hold Shift and drag a selection rectangle around clinics; practice selecting different sizes of boxes.
38. Hold Shift and click any five FQHC clinics manually.
39. Use Switch Selection to invert selected/unselected FQHCs.
40. Clear Selection.
41. Turn off FQHC Clinics and turn on Population Density.
42. Analysis tab > Tools.
43. In Geoprocessing, go to Toolboxes > Analysis Tools > Statistics > Summary Statistics.
44. Input Table: Population Density.
45. Output table: default `PopulationDensity_Statistics` or equivalent.
46. Statistics Fields:
   - `PopDensity` Minimum
   - `PopDensity` Maximum
   - `PopDensity` Mean
   - `PopDensity` Standard Deviation
47. Run.
48. Right-click the new standalone table > Open.
49. Verify values:
   - Min: 0
   - Max: about 29,492.7
   - Mean: about 4,560.15
   - Standard deviation: about 4,100
50. Save.

Checklist:

- `Tutorial1-3FozhanBabaeiyan.aprx` exists.
- Municipalities field view keeps GEOID and Name/Municipality visible, with `STATEFP` deleted.
- Streets field aliases/visibility are simplified.
- Population Density summary statistics table exists in the project/geodatabase.
- No selections remain active.

Audit for submitted work:

- The ArcPy inspection found no standalone summary-statistics table. This likely means the summary-statistics step was not saved or not completed.
- Layer visibility resembles Tutorial 1-1, so the saved state does not strongly prove the Tutorial 1-3 attribute-table work.

## Tutorial 1-4 - Symbology, Labels, Parks, and 3D

Goal: change symbols, label municipalities, add/remove a Parks feature class, and open a 3D scene.

1. Open `Tutorial1-4.aprx`.
2. Save As `Tutorial1-4FozhanBabaeiyan.aprx`.
3. Right-click FQHC Clinics > Symbology.
4. Click the symbol preview; choose Gallery > `Circle 4`.
5. Go to Properties:
   - Color: green, the video uses `Quetzal Green`
   - Size: `8 pt`
6. Click Apply.
7. Right-click Poverty Risk Area > Symbology.
8. Set outline width to `2`.
9. Set outline color to the red specified by the book/video: `Poinsettia Red` (transcript captured it as "point set red").
10. Click Apply.
11. In Contents:
   - Turn off Population Density.
   - Turn off FQHC Buffer.
   - Turn off Urgent Care Clinics Buffer.
   - Turn on Municipalities.
12. Click Municipalities once.
13. Labeling tab:
   - Field: Name
   - Font size: `7`
   - Color: `Gray 60%` or dark gray
14. Open the full Text Symbol settings.
15. Halo:
   - Halo symbol/fill: white
   - Outline color: No color
   - Width/size: `0.75`
16. Click Apply.
17. Labeling tab > Label button to turn labels on.
18. Zoom in to inspect municipality labels.
19. Turn Municipalities off.
20. Map tab > Full Extent.
21. Catalog pane > Databases > Chapter1.gdb.
22. Drag `Parks` onto the map.
23. Ensure Parks is above Population Density in drawing order.
24. Click the Parks symbol square.
25. In Symbology Gallery, choose the green `Park` symbol.
26. Map tab > Bookmarks > Pittsburgh East End.
27. Zoom in until street names and parks are readable.
28. Full Extent.
29. Right-click Parks > Remove.
30. Save.
31. Catalog pane > Maps > double-click `Health Care Clinics_3D`.
32. In 3D, zoom and tilt by holding `V` while dragging; inspect Population Density as 3D columns.
33. Save.

Checklist:

- FQHC Clinics are green Circle 4, size 8.
- Poverty Risk Area has red outline width 2.
- Municipalities labels exist using Name, size 7, dark gray, white halo/no outline.
- Parks is not left in the final 2D map, but Parks exists in Chapter1.gdb.
- `Health Care Clinics_3D` opens and contains the 3D Population Density/Census Tracts scene.

Audit for submitted work:

- Submitted Tutorial 1-4 still looks like Tutorial 1-1 in final visibility and does not clearly prove the narrated symbology/label work. This should be reviewed in ArcGIS Pro if time permits.

---

## Tutorial 2-1 - Unique Values Land Use Map

Goal: symbolize NYC zoning/land use with transparent neighborhoods and category colors.

1. Open `Tutorial2-1.aprx`.
2. Save As `Tutorial2-1FozhanBabaeiyan.aprx`.
3. Map tab > Bookmarks > Lower Manhattan.
4. Change Neighborhoods symbol:
   - Click the Neighborhoods symbol square.
   - Properties.
   - Fill Color: No Color.
   - Outline Color: `Gray 60%`.
   - Apply.
5. Turn on Water.
6. Click Water symbol and choose Gallery > Water Area.
7. Turn on Zoning Land Use.
8. Right-click Zoning Land Use > Symbology.
9. Primary Symbology: Unique Values.
10. Field: `LANDUSE2`.
11. More > Format All Symbols.
12. Properties > Outline Color: `Gray 20%`; Apply.
13. Set category fills:
   - Commercial: `Rose Quartz` (first row, second column).
   - Manufacturing: `Lilac` (first row, 11th column).
   - Park: `Apple Dust` (seventh row, sixth column).
   - Residential: `Yucca Yellow` (first row, fifth column).
   - Residential LT-MFG: `Soapstone Dust` (seventh row, third column).
   - Waterfront: `Atlantic Blue` (ninth row, ninth column).
14. Save.

Checklist:

- Neighborhoods outline only, no fill.
- Water blue.
- Zoning Land Use unique values by `LANDUSE2`, six categories, gray 20% outlines, pastel category colors.

Audit for submitted work:

- Renderer uses unique values on `LANDUSE2`; likely mostly complete.

## Tutorial 2-2 - Labels and Popups

Goal: label zoning, neighborhoods, water, and configure popups.

1. Open `Tutorial2-2.aprx`.
2. Save As `Tutorial2-2FozhanBabaeiyan.aprx`.
3. Map tab > Bookmarks > West Village.
4. Click Zoning Land Use once.
5. Labeling tab:
   - Field: `Zone`
   - Click Label button.
   - Text size: `8`
   - Text color: `Gray 50%`.
6. Map tab > Bookmarks > Lower Manhattan.
7. Click Neighborhoods.
8. Labeling tab:
   - Field: `Name`
   - Click Label.
   - Open expanded Text Symbol.
   - Font: `Arial`
   - Style: Bold
   - Size: `11`
   - Halo: white
   - Apply.
9. Label Placement Style: `Land Parcel`.
10. Click Water.
11. Labeling tab:
   - Field: `Landname`
   - Click Label.
   - Font: `Times New Roman`
   - Size: `12`
   - Color: `Atlantic Blue`.
12. Right-click Water > Labeling Properties.
13. Position > Conflict Resolution.
14. Remove duplicate labels: `Remove all`.
15. Right-click Zoning Land Use > Disable Pop-ups.
16. Right-click Water > Disable Pop-ups.
17. Right-click Neighborhoods > Configure Pop-ups.
18. In the Fields item, click the pencil.
19. Uncheck "Only use visible fields."
20. Turn off display for all fields.
21. Turn display on for:
   - `BoroName`
   - population field (`Pop`)
   - population impoverished field
   - population 18 and under field
   - population 18 and under impoverished field
22. Click a neighborhood to verify the popup only shows those fields.
23. Save.

Checklist:

- Zoning labels on by Zone, gray 50%, size 8.
- Neighborhood labels on by Name, Arial Bold 11 with white halo, Land Parcel placement.
- Water labels on by Landname, Times New Roman 12, Atlantic Blue, duplicate labels removed.
- Zoning Land Use and Water popups disabled.
- Neighborhood popup reduced to five fields.

Audit for submitted work:

- Labels/popups require visual inspection in ArcGIS Pro. Renderer and layer set look plausible, but field-level popup configuration was not fully verified by ArcPy.

## Tutorial 2-3 - Definition Queries and Food Facilities

Goal: filter facilities to food pantry/soup kitchen types and symbolize them.

1. Open `Tutorial2-3.aprx`.
2. Save As `Tutorial2-3FozhanBabaeiyan.aprx`.
3. Right-click Facilities > Properties.
4. Definition Query > New Definition Query.
5. Build query:
   - `FACILITY_T` is equal to `4901`
   - OR `FACILITY_T` is equal to `4902`
   - OR `FACILITY_T` is equal to `4903`
6. Apply and OK.
7. Open Facilities attribute table and verify about `631` records remain and `FACILITY_T` only contains 4901, 4902, 4903.
8. Map tab > Bookmarks > Manhattan.
9. Rename Facilities to `Food Facilities`.
10. Right-click Food Facilities > Symbology.
11. Primary Symbology: Unique Values.
12. Field: `FAC_TYPE` / facility type field.
13. Reorder classes:
   - Soup Kitchen first.
   - Food Pantry second.
   - Joint Soup Kitchen and Food Pantry third.
14. Soup Kitchen symbol:
   - Gallery: `Square 3`
   - Color: red
   - Size: `8`
15. Food Pantry symbol:
   - Gallery: `Circle 3`
   - Color: blue
   - Size: `8`
16. Joint Soup Kitchen/Food Pantry symbol:
   - Gallery: `Cross 3`
   - Color: yellow, e.g. Solar Yellow
   - Size: `10`
17. More > uncheck Show all other values.
18. Turn off World Light Gray Canvas/Base layer.
19. Turn on Manhattan Streets.
20. Set Manhattan Streets symbol:
   - Color: `Gray 20%`
   - Width: `0.5`
21. Label Manhattan Streets:
   - Click Manhattan Streets.
   - Labeling tab.
   - Field: `Street`
   - Click Label.
22. Zoom in until street names are readable.
23. Save.

Checklist:

- Food Facilities layer has definition query with 4901/4902/4903.
- Food Facilities uses unique values by facility type, not graduated/class breaks.
- Soup Kitchen = red Square 3 size 8.
- Food Pantry = blue Circle 3 size 8.
- Joint = yellow Cross 3 size 10.
- Manhattan Streets on, gray 20%, width 0.5, labeled by Street.
- World Light Gray Canvas off.

Audit for submitted work:

- Submitted renderer appears to be class breaks on `CAPACITY`, not unique values by facility type. This is a likely incorrect/skipped symbology step.

## Tutorial 2-4 - Choropleth and 3D Extrusion

Goal: map over-60 food stamp/SNAP recipients by neighborhood and convert to a 3D local scene.

1. Open `Tutorial2-4.aprx`.
2. Save As `Tutorial2-4FozhanBabaeiyan.aprx`.
3. If Neighborhoods has a red X:
   - Right-click Neighborhoods > Properties > Source.
   - Set Data Source.
   - Databases > `Chapter2.gdb` > `Neighborhoods`.
   - OK.
4. Rename Neighborhoods to `Over age 60 receiving food stamps`.
5. Right-click the renamed layer > Symbology.
6. Primary Symbology: Graduated Colors.
7. Field: `O60_FOOD`.
8. Method: `Quantile`.
9. Classes: `5`.
10. Color Scheme: `Blue Green (5 classes)`; use Show Names to find it.
11. Open Histogram tab to inspect distribution.
12. Change Method to `Geometric Interval`; inspect changed breaks.
13. Change Color Scheme to `Gray (5 classes)`.
14. Change Method to `Defined Interval`.
15. Interval Size: `2500`.
16. Change Method back to `Quantile`.
17. View tab > Convert > To Local Scene.
18. In the new 3D map, drag `Over age 60 receiving food stamps` below the `3D Layers` heading.
19. Select the layer.
20. Feature Layer tab > Extrusion.
21. Extrusion Type: `Base Height`.
22. Field: `O60_FOOD`.
23. Hold `V` and drag to tilt/rotate the 3D scene.
24. Click features if desired to inspect popups.
25. Save.

Checklist:

- Layer is renamed `Over age 60 receiving food stamps`.
- Field is `O60_FOOD`.
- Final 2D method returned to Quantile.
- 3D local scene exists, with the over-60 layer under 3D Layers and extruded by `O60_FOOD`.

Audit for submitted work:

- Submitted Tutorial 2-4 is still `Neighborhoods` and appears symbolized on `POV_FOOD`, not `O60_FOOD`. The 3D scene appears in another submitted project, so Tutorial 2-4 is likely incorrect.

## Tutorial 2-5 - Graduated and Proportional Point Symbols

Goal: compare food facilities, over-60 food stamps, and under-18 food stamps.

1. Open `Tutorial2-5.aprx`.
2. Save As `Tutorial2-5FozhanBabaeiyan.aprx`.
3. Rename the first Neighborhoods layer to `Number of Food Banks/Soup Kitchens`.
4. Select that layer.
5. Feature Layer tab > Symbology > Graduated Symbols.
6. Field: `FOOD_FACIL`.
7. Method: `Quantile`.
8. Template Symbol: `Circle 3`.
9. Color: `Solar Yellow`.
10. Rename the second Neighborhoods layer to `Under 18 receiving food stamps`.
11. Select it.
12. Feature Layer tab > Symbology > Proportional Symbols.
13. Field: `U18_FOOD`.
14. Minimum size: `2`.
15. Check/set Maximum size: `20`.
16. Template/symbol color: purple.
17. Map tab > Bookmarks > Bronx; inspect relationship between:
   - yellow circles: food facilities
   - purple circles: under-18 receiving food stamps
   - blue polygon fill: over-60 receiving food stamps
18. Map tab > Bookmarks > Brooklyn; inspect same relationship.
19. Full Extent globe; zoom in a little if desired so circles are visible.
20. Save.

Checklist:

- First layer renamed Number of Food Banks/Soup Kitchens and uses Graduated Symbols on `FOOD_FACIL`.
- Second layer renamed Under 18 receiving food stamps and uses Proportional Symbols on `U18_FOOD`, min 2, max 20, purple.
- Over age 60 receiving food stamps remains as background choropleth.

Audit for submitted work:

- Submitted Tutorial 2-5 still has two simple-renderer Neighborhoods layers, so the key symbology and renaming appear missing.

## Tutorial 2-6 - Normalized Population Maps and Swipe

Goal: normalize female/male headed household food stamp counts by total households and apply custom class breaks.

1. Open `Tutorial2-6.aprx`.
2. Save As `Tutorial2-6FozhanBabaeiyan.aprx`.
3. Select `Female headed households receiving food stamps`.
4. Symbology: Graduated Colors.
5. Field: `U18FHHFOOD` / `U18_FHH_FOOD` as displayed.
6. Normalization: `TOT_HH`.
7. Method: `Quantile`.
8. Classes: `5`.
9. Color Scheme: `Gray 5 classes`.
10. Advanced tab > Format Labels.
11. Category: Percentage.
12. Number represents: Fraction.
13. Decimal places: `0`.
14. Return to Primary Symbology.
15. Change Method to `Manual Interval`.
16. Set upper values:
   - `0.02`
   - `0.04`
   - `0.08`
   - `0.16`
   - `0.26`
17. Check Histogram tab.
18. Select `Male headed households receiving food stamps`.
19. Feature Layer tab > Drawing group > Import.
20. Import symbology:
   - Input Layer: Male headed households receiving food stamps.
   - Symbology Layer: Female headed households receiving food stamps.
   - Type: Value field.
   - Source Field: `U18FHHFOOD`.
   - Target Field: `U18MHHFOOD`.
   - Normalization source/target: `TOT_HH`.
21. Click OK/Apply.
22. Select Female layer.
23. Feature Layer tab > Compare group > Swipe.
24. Drag swipe down/up to compare female vs male maps.
25. Map tab > Explore to deactivate Swipe.
26. Save.

Checklist:

- Female layer uses class breaks on normalized `U18FHHFOOD / TOT_HH`, manual intervals 2%, 4%, 8%, 16%, 26%.
- Male layer imports same breaks/colors using `U18MHHFOOD / TOT_HH`.

Audit for submitted work:

- Submitted renderers show class breaks on female/male fields, likely mostly complete. Manual break values should still be visually checked.

## Tutorial 2-7 - Dot Density

Goal: symbolize persons receiving food stamps with dot density.

1. Open `Tutorial2-7.aprx`.
2. Save As `Tutorial2-7FozhanBabaeiyan.aprx`.
3. Right-click `Persons receiving food stamps` > Symbology.
4. Primary Symbology: Dot Density.
5. Add fields:
   - `U18_FOOD`
   - `O60_FOOD`
6. Change labels:
   - `U18_FOOD` -> `Population under 18`
   - `O60_FOOD` -> `Population over 60`
7. Dot size: keep `2`.
8. Dot value: set to `50`, observe many dots.
9. Change Dot value to `100` as final value.
10. Save.

Checklist:

- Dot Density renderer on Persons receiving food stamps.
- Fields `U18_FOOD` and `O60_FOOD`.
- Labels Population under 18 and Population over 60.
- Dot size 2, dot value 100.

Audit for submitted work:

- Submitted project has a dot density renderer; likely complete.

## Tutorial 2-8 - Visibility Ranges

Goal: use scale ranges for labels and feature visibility.

1. Open `Tutorial2-8.aprx`.
2. Save As `Tutorial2-8FozhanBabaeiyan.aprx`.
3. Map tab > Bookmarks > West Village.
4. Click Zoning Land Use.
5. Labeling tab > Label.
6. Visibility Range > Minimum Scale > Current.
7. Zoom out to confirm labels disappear; zoom in to confirm they return.
8. Map tab > Bookmarks > Lower Manhattan.
9. Click Schools.
10. Feature Layer tab > Visibility Range > Minimum Scale > Current.
11. Zoom out to confirm school points disappear.
12. Click Boroughs.
13. Labeling tab > Label.
14. Visibility Range > Maximum Scale > Current.
15. Zoom in to confirm borough labels disappear; zoom out to confirm they return.
16. Map tab > Bookmarks > Lower Manhattan.
17. Click Neighborhoods.
18. Labeling tab > Label.
19. Visibility Range > Maximum Scale > Current.
20. Click Water.
21. Labeling tab > Label.
22. First set Maximum Scale > Current.
23. Then final adjustment for Water:
   - Maximum Scale: None
   - Minimum Scale: Current
24. Turn off Neighborhoods.
25. Turn off Water.
26. Turn off World Light Gray Canvas/Base.
27. Final checked layers should be Boroughs and Zoning Land Use; Schools may be checked or unchecked because visibility range controls display.
28. Save.

Checklist:

- Zoning labels visible only when zoomed to West Village scale or closer.
- Schools visible only at Lower Manhattan scale or closer.
- Borough labels visible when zoomed out, hidden when zoomed in.
- Water labels visible when zoomed in at the final configured scale.
- Neighborhoods, Water, and World Light Gray Canvas off at final save.

Audit for submitted work:

- Submitted project has visibility ranges, but Neighborhoods, Water, and World Light Gray Canvas are still on. Final state does not match the video.

---

## Tutorial 3-1 - Layouts and Charts

Goal: create a two-map layout, export it, make a bar chart and scatter plot.

1. Open `Tutorial3-1.aprx`.
2. Save As `Tutorial3-1FozhanBabaeiyan.aprx`.
3. Use the `Arts Employment per 1,000 Population` map tab.
4. Insert tab > New Layout > Letter 8.5 x 11.
5. In Catalog pane > Layouts, rename new layout to `Arts Employment Layout`.
6. Insert tab > Map Frame.
7. Choose `Arts Employment per 1,000 Population` > Default Extent.
8. Draw the frame on the top half of the page.
9. Insert tab > Map Frame.
10. Choose `Arts Employment` > Default Extent.
11. Draw the frame under the first one.
12. Set both map frames:
   - Width: `5.5`
   - Height: `3.5`
13. Click each map frame and Layout tab > Full Extent globe.
14. Turn on rulers/guides if needed by right-clicking layout white space and enabling Rulers and Guides.
15. Add guides:
   - Vertical: `5`
   - Vertical: `9`
   - Horizontal: `6.25`
   - Horizontal: `6.5`
   - Horizontal: `8`
16. Place top map with its upper-right corner at guide intersection `9` and `6.25`.
17. Place bottom map with its upper-right corner at guide intersection `5` and `6.25`.
18. Select bottom map frame.
19. Insert tab > Map Surrounds > Legend > Legend 1; draw legend in the prepared rectangle.
20. Select top map frame and add its legend the same way.
21. For each legend:
   - Right-click legend > Properties.
   - Options > Legend Items > Show Properties.
   - Uncheck Layer Name.
22. Insert tab > Graphics and Text > Rectangle Text.
23. Above top map, add:
   - `Arts Employment per 1,000 Population`
   - line break
   - `Annual Average Wages`
24. Text size: `12`.
25. Text box height: `0.45`.
26. Above/beside bottom map, add:
   - `Arts Employment`
   - line break
   - `Annual Average Wages`
27. Text size: `12`; height `0.45`.
28. Catalog pane > Layouts > right-click `Arts Employment Layout` > Export File.
29. Export:
   - File type: JPEG.
   - Color Depth: `24-bit True Color`.
   - Default folder is acceptable unless instructed otherwise.
30. Go to the `Arts Employment` map tab.
31. Click Employment layer.
32. Data tab > Visualize group > Create Chart > Bar Chart.
33. Chart Properties:
   - Category/Date: `Name`.
   - Aggregation: None.
   - Numeric field: `Employment Arts`.
   - Sort: Y-axis descending.
34. General:
   - Chart title: `Arts Employment for Top 10 States`
   - X-axis title: `State`
   - Y-axis title: `Employment`
35. Series:
   - Bar color: red.
36. Select the first 10 bars (California through Massachusetts in the video).
37. Click Filter By Selection.
38. Export chart:
   - Export > Export to File > Export as Graphic.
   - Save in `Resources`.
   - Name without spaces, e.g. `Top10States.jpg`.
39. Create another chart:
   - Data tab > Visualize > Create Chart > Scatter Plot.
   - X-axis: `Population`.
   - Y-axis: `Employment Arts`.
40. Save.

Checklist:

- Layout `Arts Employment Layout` exists with two map frames stacked vertically.
- Two legends exist with layer names removed.
- Two text titles exist with the exact map titles/wage subtitles.
- JPEG layout export exists.
- Bar chart exists, filtered to top 10 states, red bars, exported to Resources.
- Scatter plot exists with Population vs Employment Arts.

Audit for submitted work:

- Layout exists, but text/structure appears different from transcript.
- Export found was PNG, not the narrated JPEG.
- Expected top-10 chart export was not found.

## Tutorial 3-2 - Share Web Maps Online

Goal: publish Arts Employment and Cost of Living web maps, then edit styles and popups in ArcGIS Online Map Viewer.

1. Open `Tutorial3-2.aprx`.
2. Save As `Tutorial3-2FozhanBabaeiyan.aprx`.
3. On `Arts Employment`, zoom in enough to see Metropolitan Employment, then return to Full Extent.
4. Right-click `Arts Employment` map > Properties.
5. Verify `Allow assignment of unique numeric IDs for sharing web layers` is checked.
6. Repeat for `Cost of Living Index`.
7. Activate Arts Employment map.
8. Share tab > Share As > Web Map.
9. Name: `Arts Employment Fozhan Babaeiyan`.
10. Summary from `MapSharing.pdf`:
    - `Arts employment by state and metropolitan area for the U.S using Bureau of Labor Statistics 2014 data for the standard occupational major group, Arts, Design, Entertainment, Sports, and Media occupations.`
11. Tags:
    - `Arts, Employment, Wages`
12. Share with: Everyone.
13. Analyze.
14. Ignore the specific warning about feature layer display if it appears.
15. Share.
16. Activate Cost of Living Index map.
17. Share tab > Web Map.
18. Name: `Cost of Living Index Fozhan Babaeiyan`.
19. Summary from `MapSharing.pdf`:
    - `Cost of living Index by state and metropolitan area for the U.S using Council for Community and Economic Research's Cost of Living Index data (with permission) and Bureau of Labor Statistics data for the standard occupational major group, Arts, Design, Entertainment, Sports, and Media occupations.`
20. Tags:
    - `Arts, Cost of Living, Wages`
21. Share with Everyone, Analyze, ignore the same warning if present, Share.
22. Save and close ArcGIS Pro.
23. Open ArcGIS Online in browser; sign in with CSULB organization.
24. Content tab > My Content.
25. Open `Arts Employment Fozhan Babaeiyan` in Map Viewer.
26. In Layers, click `State Wages`.
27. Styles > Counts and Amounts (Size).
28. Click symbol rectangle and change it to an orange color; Done.
29. Zoom/pan to Southern California/Los Angeles so Metropolitan Employment points appear.
30. Click `Metropolitan Employment`.
31. Pop-ups panel (conversation bubble icon):
   - Enable popups.
   - Field list > Select fields.
   - Select all, then deselect all.
   - Select only `Employment Arts` and `Wages Arts`.
   - Done.
32. Click `State Employment`.
33. Enable popups and select only:
   - `Population`
   - `Employment Arts`
   - `Wages Arts`
34. Home/default view.
35. Click a state such as Texas to verify popup fields.
36. Save the web map.
37. Save/Open > Open Map > open `Cost of Living Index Fozhan Babaeiyan`.
38. Click `State Cost of Living Index`.
39. Pop-ups:
   - Enable popups.
   - Field list > Select fields.
   - Select all, deselect all.
   - Select only `Index`.
40. Click states such as Idaho and California to compare index values.
41. Save the web map.

Checklist:

- Two public web maps exist:
  - Arts Employment Fozhan Babaeiyan
  - Cost of Living Index Fozhan Babaeiyan
- Arts web map has orange State Wages size symbols.
- Metropolitan Employment popup shows only Employment Arts and Wages Arts.
- State Employment popup shows only Population, Employment Arts, Wages Arts.
- Cost of Living Index popup shows only Index.

Audit for submitted work:

- No Arts Employment or Cost of Living web map items were found online. Current online items are 311 Debris/Pittsburgh Neighborhoods, which do not match the video.

## Tutorial 3-3 - ArcGIS StoryMap

Goal: create and publish a public Arts Employment StoryMap using the web map from Tutorial 3-2.

1. In browser, sign in to ArcGIS Online.
2. Content tab.
3. Create App > ArcGIS StoryMaps.
4. Open `Resources\StoryMapManuscript.pdf`.
5. Cover title:
   - `Arts employment by state and metropolitan area Fozhan Babaeiyan`
6. Subtitle:
   - `Employment levels, average wages, and cost of living index`
7. Add Cover Image/Video:
   - Upload `Resources\pexels-engin-akyurt-6137963.jpg`.
8. Design > Cover > Full.
9. Image settings > Display > Attribution:
   - `www.pexels.com/photo/light-down-red-art-blue-6137963`
10. Image settings > Accessibility > Alternative Text:
   - `Background image with abstract art on cover page of story.`
11. Add text block:
   - Text: `Arts Employment`
   - Format: Heading 1.
12. Add text block:
   - `Where are the jobs in the arts field? What are average wages versus cost of living?`
   - Format: Heading 2.
13. Add paragraph block with Paragraphs 2-3 from manuscript; manually insert the paragraph breaks.
14. Italicize the final sentence beginning `You might be better off with a good, but not top-paying job...`
15. Add text block:
   - `Disclaimer`
   - Format: Heading 2.
16. Add paragraph:
   - `The information in this story map is generally helpful, but there are sampling errors and approximations involved in making estimates or otherwise using the data presented. There are no guarantees of accuracy.`
17. Add block > Immersive > Sidecar.
18. Choose Docked sidecar.
19. In the Sidecar media area, Add > Map.
20. Select `Arts Employment Fozhan Babaeiyan`.
21. Save the map placement.
22. Map settings > Alternative Text:
   - `Interactive map of the lower 48 states and metropolitan areas with employment levels and annual wages for the arts field`
23. Continue story after sidecar.
24. Add text:
   - `Arts Employment map`
   - Format: Heading 1.
25. Add text:
   - `Map use and navigation`
   - Format: Heading 2.
26. Add bulleted list using manuscript Bulleted list 3-3; split into separate bullets:
   - Click the legend button (top right, second button down) to see the map legend.
   - Click the magnifying glass to search for a location.
   - Click the layers button at the bottom on the right to turn layers on and off.
   - Click the + to zoom in, - to zoom out, and house icon to zoom to the default map view.
   - You can also drag the map to pan and use your mouse wheel to zoom in and out.
   - Click the magnifying glass icon (upper left of map) to search for an address or place.
   - Zoom in far enough and metropolitan areas appear as points.
   - Hover over a metropolitan point to get a pop-up with data on the area.
   - Lastly click the fourth button down on the left to take a screen shot of the map.
27. Add Image:
   - `Resources\Table1.png`
   - Caption: `The top 10 states in terms of annual average wages in the arts`
28. Add text:
   - `Patterns on the map`
   - Format: Heading 2.
29. Add Image:
   - `Resources\Table2.png`
   - Caption: `The top 10 metropolitan areas in terms of wages in the arts (while only the major city is listed, data is for the city and surrounding metropolitan area)`
30. Design > turn on Navigation and Credits.
31. Add Credits section. Include:
   - Employment and average annual wages data: U.S. Bureau of Labor Statistics and its occupational classification; Arts, Design, Entertainment, Sports, and Media Occupations `http://www.bls.gov/soc/major_groups.htm`
   - Population data: American Community Survey of the U.S. Census Bureau `https://www.census.gov/programs-surveys/acs`
   - Cost of living index data: Council for Community and Economic Research `https://www.c2er.org/`
   - State and metropolitan area boundary maps: U.S. Census Bureau `https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html`
32. Preview on desktop/tablet/phone.
33. Publish.
34. Share setting: Everyone/Public.
35. View published story and copy the URL.
36. Submit a Word document or Canvas comment containing only the published StoryMap link.

Your Turn / optional extra from the video:

- Add the Cost of Living Index section from manuscript section 4.
- Include:
  - Heading: Cost of living index map.
  - Subheading: The data.
  - Paragraph 4-3, hyperlink Council for Community and Economic Research to `https://www.c2er.org/`.
  - Bulleted list 4-4.
  - Subheading: Patterns on the map.
  - Paragraphs 4-6.
  - Images Table3, Table4, and CostOfLivingWeights with captions from manuscript.

Checklist:

- StoryMap is public.
- Title includes Fozhan Babaeiyan.
- Uses Arts Employment web map, not an unrelated map.
- Includes cover image, attribution, alt text, intro text, sidecar map, Table1/Table2 images, navigation, credits.
- URL is saved for Canvas.

Audit for submitted work:

- Current public StoryMap exists and loads, but content is 311 Debris/Pittsburgh Neighborhoods, not the required Arts Employment StoryMap. This is a critical mismatch.

## Tutorial 3-4 - No Video Transcript Found

No `Tutorial_3_4` video exists in the provided 21 MP4 files. The course folder contains `Tutorial3-4.aprx`, but the narrated sequence labels the StoryMap work as Tutorial 3-3 and says there is no ArcGIS Pro folder submission for that tutorial, only a StoryMap URL.

Checklist:

- If Canvas requires the entire Chapter 3 folder, keep `Tutorial3-4FozhanBabaeiyan.aprx` in the folder.
- Do not treat the 311 Debris project as a substitute for the Arts Employment StoryMap unless the instructor explicitly assigned it outside these videos.

---

## Tutorial 4-1 - Import Data into a New Project

Goal: create a new Youth Population project, connect Maricopa County data, convert shapefiles and CSVs, and practice geodatabase management.

1. Open ArcGIS Pro directly.
2. New Project > Map.
3. Name: `Youth Population`.
4. Location: Chapter 4 folder.
5. Click OK.
6. Project tab > Options to view the home folder, default geodatabase, and toolbox.
7. Project tab > Save Project As.
8. Save as `Tutorial4-1FozhanBabaeiyan.aprx`.
9. Open Catalog pane if needed.
10. Expand Folders.
11. Right-click Folders > Add Folder Connection.
12. Browse to `Chapter4\Data\MaricopaCounty`; select the folder itself; OK.
13. Expand MaricopaCounty.
14. Analysis tab > Tools > search `Export Features`.
15. Input Features: `Municipalities.shp`.
16. Output Feature Class: `Cities`.
17. Run.
18. Run Export Features again:
   - Input Features: `Tracts.shp`.
   - Output Feature Class: `Tracts`.
19. Analysis tab > Tools > search `Export Table`.
20. Input Table: `PopYouth.csv`.
21. Output Table: `PopYouth`.
22. Run.
23. In Catalog > Databases, verify the Youth Population geodatabase contains `Cities`, `Tracts`, and `PopYouth`.
24. Right-click Databases > New File Geodatabase.
25. Name: `MaricopaTracks.gdb`.
26. Expand Youth Population geodatabase.
27. Right-click Cities > Copy.
28. Right-click MaricopaTracks.gdb > Paste.
29. Right-click PopYouth > Copy.
30. Right-click MaricopaTracks.gdb > Paste.
31. If needed, right-click MaricopaTracks.gdb > Refresh.
32. In MaricopaTracks.gdb, right-click PopYouth > Rename.
33. Rename to `TractsPopYouth`.
34. Delete `Tracts` from MaricopaTracks.gdb only.
35. Delete the entire MaricopaTracks.gdb as practice.
36. Save but do not close if continuing to 4-2.

Checklist:

- `Tutorial4-1FozhanBabaeiyan.aprx` exists.
- Maricopa County folder connection exists.
- Youth Population/default geodatabase contains Cities, Tracts, PopYouth.
- Temporary MaricopaTracks.gdb practice actions understood; it may be deleted at final.

Audit for submitted work:

- Submitted project has a Maricopa imports map and no broken layers, but naming/path differs from the video's Youth Population/default geodatabase workflow.

## Tutorial 4-2 - Modify Attribute Tables and Join Data

Goal: clean fields, calculate fields, join PopYouth to Tracts, create youth population measures, and build tract name strings.

1. Continue from Tutorial 4-1.
2. Save As `Tutorial4-2FozhanBabaeiyan.aprx`.
3. Right-click Tracts > Zoom To Layer.
4. Map tab > Bookmarks > New Bookmark.
5. Name: `Maricopa County`.
6. Turn off World Hillshade and World Topographic Map basemaps.
7. Right-click Tracts > Data Design > Fields.
8. Delete all non-required fields except:
   - ObjectID
   - Shape
   - GEOID
   - Shape_Length
   - Shape_Area
9. Save Fields edits.
10. Close Fields view.
11. Right-click Tracts > Attribute Table.
12. Table menu > Fields View.
13. Add field:
   - Name: `GEOIDNum`
   - Type: Big Integer (video corrects the book's Double because PopYouth ID is Big Integer).
14. Save.
15. Right-click `GEOIDNum` > Calculate Field.
16. Expression: `!GEOID!`
17. Run.
18. Right-click Tracts > Joins and Relates > Add Join.
19. Input Table: Tracts.
20. Input Field: `GEOIDNum`.
21. Join Table: `PopYouth`.
22. Join Field: `ID`.
23. Validate Join.
24. OK.
25. Open Tracts table and verify PopYouth fields joined.
26. Right-click Tracts > Data > Export Features.
27. Output Feature Class: `MaricopaTracts`.
28. Run.
29. Open MaricopaTracts table/Fields view and verify joined fields no longer have `PopYouth.` prefixes.
30. Remove old Tracts layer from map; keep MaricopaTracts.
31. Add field to MaricopaTracts:
   - Name: `PopYouthUnder20`
32. Save.
33. Calculate `PopYouthUnder20`:
   - `!PopUnder5! + !Pop5To9! + !Pop10To14! + !Pop15To19!`
   - Use the exact field names shown in the table.
34. Add field:
   - Name: `PctPopYouthUnder20`
35. Before calculating, sort `PopTotal` and note there are four zero-population tracts.
36. Map tab > Select By Attributes.
37. Query: `PopTotal` is greater than `0`.
38. With selected rows only, calculate `PctPopYouthUnder20`:
   - `100 * !PopYouthUnder20! / !PopTotal!`
39. Clear Selection.
40. Add three text fields:
   - `TractNumber`, length 4.
   - `TractSuffix`, length 2.
   - `TractName`, length 20.
41. Calculate `TractNumber`:
   - `!GEOID![5:9]`
42. Calculate `TractSuffix`:
   - `!GEOID![9:11]`
43. Calculate `TractName`:
   - `"Census tract " + !TractNumber! + "." + !TractSuffix!`
44. Sort TractName ascending.
45. Save.

Checklist:

- MaricopaTracts exists with joined PopYouth fields.
- Old Tracts removed from map, not deleted from geodatabase unless intended.
- Fields exist: GEOIDNum, PopYouthUnder20, PctPopYouthUnder20, TractNumber, TractSuffix, TractName.
- Pct field was calculated only for PopTotal > 0 tracts.

Audit for submitted work:

- Current Tutorial4_Work.gdb contains youth-population-style outputs, but field names differ from the video names. Verify instructor tolerance if this was submitted for credit.

## Tutorial 4-3 - Attribute Queries

Goal: query Pittsburgh crime data by date, crime type, weekend/weekday, and suspect attributes.

1. Open `Tutorial4-3.aprx`.
2. Save As `Tutorial4-3FozhanBabaeiyan.aprx`.
3. Right-click Crime Offenses > Symbology.
4. More > Show Count.
5. Note counts:
   - Burglary: `846`
   - Robbery: `412`
6. Map tab > Select By Attributes.
7. Date range query:
   - `DateOccur` is on or after `7/1/2015`
   - AND `DateOccur` is on or before `7/31/2015`
8. Verify expression.
9. Apply; July 2015 crimes are selected.
10. In Select By Attributes pane, Save expression as `qryDateRange.exp` in Chapter 4 Data.
11. Open Crime Offenses attribute table; verify `3,924` selected.
12. Close table and clear selection.
13. Right-click Crime Offenses > Properties > Definition Query.
14. Add Definition Queries From File; choose `qryDateRange.exp`.
15. Open table; click Load All; verify only 3,924 July records.
16. Edit Definition Query to add crime type:
   - AND (`Crime` = `Burglary` OR `Crime` = `Robbery`)
17. Use SQL toggle and parentheses so the OR is grouped correctly.
18. Apply.
19. Right-click Crime Offenses > Symbology.
20. Symbolize Robbery dark red.
21. Clear active query by clicking the green checkmark in Definition Query.
22. Build August burglary query:
   - `DateOccur` is on or after `8/1/2015`
   - AND `DateOccur` is on or before `8/31/2015`
   - AND `Crime` = `Burglary`
23. Apply; verify `273` burglaries.
24. Optional instructor method: right-click Crime Offenses > Selection > Make Layer From Selected Features to create Crime Offenses Selection with 273 rows.
25. Weekend query:
   - `DayOfWeek` = `Saturday`
   - OR `DayOfWeek` = `Sunday`
26. Verify `84` weekend burglaries.
27. Switch Selection; verify `189` weekday burglaries.
28. Calculate daily averages:
   - Weekend: `84 / 10 = 8.4`
   - Weekday: `189 / 21 = 9.0`
29. Suspect query for arrested burglaries:
   - `ArrestName` is not null.
   - `ArrestSex` = Male.
   - `ArrestAge` >= 30.
   - `ArrestAge` < 40.
   - `ArrestResidence` contains `WARRINGTON`.
30. Re-click/apply `ArrestName is not null` if ArcGIS shows a null result unexpectedly.
31. Final suspect found in video: `John Bond`.
32. Save.

Checklist:

- Date query file `qryDateRange.exp` exists.
- July definition query can be loaded from file.
- August burglary selection workflow produces 273, 84 weekend, 189 weekday.
- Suspect query returns John Bond.

Audit for submitted work:

- Submitted project has no active final selection; this is expected. Query actions are mostly non-persistent unless query file/layers were saved.

## Tutorial 4-4 - Spatial Join

Goal: count burglaries by neighborhood and symbolize counts.

1. Open `Tutorial4-4.aprx`.
2. Save As `Tutorial4-4FozhanBabaeiyan.aprx`.
3. Analysis tab > Tools.
4. Open Spatial Join.
5. Target Features: `Neighborhoods`.
6. Join Features: `Crime Offenses` (burglaries).
7. Output Feature Class: `August2015BurglariesByNeighborhood` or `August 2015 Burglaries by Neighborhood`.
8. Join Operation: One to One.
9. Run.
10. Open the new output layer attribute table.
11. Verify new field `Join_Count` gives burglary count by neighborhood.
12. Right-click the output layer > Symbology.
13. Primary Symbology: Graduated Colors.
14. Field: `Join_Count`.
15. Normalization: None.
16. Method: Quantile.
17. Classes: 5.
18. Color scheme: any clear scheme, purple used in video.
19. Turn off Crime Offenses.
20. Right-click output layer > Zoom To Layer.
21. Save.

Checklist:

- Spatial join output exists.
- Output layer is visible and symbolized by `Join_Count`, 5 quantiles.
- Crime Offenses layer is off.

Audit for submitted work:

- Submitted Tutorial 4-4 does not show the joined output layer in the map; it shows Crime Offenses with a burglary/date definition query. This is likely incomplete.

## Tutorial 4-5 - Central Point Features

Goal: calculate central point coordinates and create inside point features for neighborhoods.

1. Open `Tutorial4-5.aprx`.
2. Save As `Tutorial4-5FozhanBabaeiyan.aprx`.
3. Analysis tab > Tools > Calculate Geometry Attributes.
4. Input Features: `Burglaries by Neighborhood`.
5. Geometry attributes:
   - Field `X`, property `Central point x-coordinate`.
   - Field `Y`, property `Central point y-coordinate`.
6. Leave coordinate format and coordinate system unchanged.
7. Run.
8. Open Burglaries by Neighborhood table and verify X/Y coordinate fields exist.
9. Analysis tab > Tools > Feature To Point.
10. Input Features: `Burglaries by Neighborhood`.
11. Output Feature Class: `BurglariesByNeighborhoodPoints`.
12. Check `Inside`.
13. Run.
14. Right-click new point layer > Symbology.
15. Primary Symbology: Graduated Symbols.
16. Field: `Join_Count`.
17. Method: Quantile.
18. Classes: 5.
19. Color scheme: your choice.
20. Right-click new point layer > Zoom To Layer.
21. Save.

Checklist:

- Polygon layer has X/Y central point fields.
- New point layer exists and points are inside polygons.
- Point layer uses graduated symbols by `Join_Count`, 5 quantiles.

Audit for submitted work:

- Submitted Tutorial 4-5 shows a polygon `Burglaries By Neighborhood` class-break layer, not an obvious inside point layer. Likely incomplete.

## Tutorial 4-6 - One-to-Many Join Code Table

Goal: create a crime hierarchy code table, join it, and optionally symbolize by crime type.

1. Open `Tutorial4-6.aprx`.
2. Save As `Tutorial4-6FozhanBabaeiyan.aprx`.
3. Analysis tab > Tools > Create Table.
4. Table Name: `UCRHierarchyCode`.
5. Run.
6. Open the new table.
7. Fields View.
8. Add fields:
   - `Hierarchy`, Short Integer.
   - `CrimeType`, Text, Length `25`.
9. Save.
10. Open table and manually add rows:
   - Hierarchy `3`, CrimeType `Robbery`
   - Hierarchy `4`, CrimeType `Aggravated Assault`
   - Hierarchy `5`, CrimeType `Burglary`
   - Hierarchy `6`, CrimeType `Larceny Theft`
11. Edit tab > Save.
12. Right-click Pittsburgh Serious Crimes > Joins and Relates > Add Join.
13. Input Field: `Hierarchy`.
14. Join Table: `UCRHierarchyCode`.
15. Join Field: `Hierarchy`.
16. Validate Join.
17. OK.
18. Open Pittsburgh Serious Crimes table and verify `CrimeType` appears.
19. Optional but shown in video: right-click Pittsburgh Serious Crimes > Symbology.
20. Primary Symbology: Unique Values.
21. Field 1: `CrimeType`.
22. Uncheck Show all other values.
23. Optionally change each crime type symbol.
24. Save.

Checklist:

- Table `UCRHierarchyCode` exists.
- It has four rows and fields Hierarchy/CrimeType.
- Pittsburgh Serious Crimes is joined to the table by Hierarchy.
- Optional final symbology: unique values by CrimeType.

Audit for submitted work:

- Submitted Tutorial 4-6 shows a simple renderer, not unique values by CrimeType, and the join/table should be verified manually.

---

# Final Submission Checklist

## Chapter 1 Zip

Upload: `C:\Users\fooja\Desktop\Chapter1_FozhanBabaeiyan.zip`

Before upload, verify:

- Tutorial 1-1: buffers on, layout export exists.
- Tutorial 1-2: bookmark `McKees Rocks Poverty Area` exists.
- Tutorial 1-3: summary statistics table exists and field edits are saved.
- Tutorial 1-4: FQHC/Poverty/Municipality labels/symbology saved; 3D scene opens.

## Chapter 2 Zip

Upload: `C:\Users\fooja\Desktop\Chapter2_FozhanBabaeiyan.zip`

Before upload, verify:

- 2-1: land use unique values by `LANDUSE2` with pastel colors.
- 2-2: labels and popups configured.
- 2-3: Food Facilities unique values by facility type; 4901/4902/4903 query.
- 2-4: Over age 60 layer uses `O60_FOOD` and 3D extrusion.
- 2-5: Number of Food Banks/Soup Kitchens and Under 18 layers renamed/symbolized.
- 2-6: female/male normalized manual intervals.
- 2-7: dot density fields/labels/dot value 100.
- 2-8: final visibility ranges and final layer visibility match video.

## Chapter 3 Zip and Online Links

Upload: `C:\Users\fooja\Desktop\Chapter3_FozhanBabaeiyan.zip`

Also submit StoryMap URL if Canvas has a comment field.

Before upload, verify:

- 3-1: layout JPEG and top-10 chart export exist.
- 3-2: public web maps exist for Arts Employment and Cost of Living Index.
- 3-3: StoryMap is an Arts Employment StoryMap, not 311 Debris/Pittsburgh Neighborhoods.
- 3-4: no matching transcript was found; keep the `.aprx` if the chapter-folder submission requires it.

Current critical issue:

- Existing StoryMap URL is public but appears to be the wrong subject for the narrated tutorial.

## Chapter 4 Zip

Upload: `C:\Users\fooja\Desktop\Chapter4_FozhanBabaeiyan.zip`

Before upload, verify:

- 4-1: Maricopa data imported into the intended geodatabase.
- 4-2: joined youth-population tracts and calculated fields exist.
- 4-3: query workflow and suspect result understood; saved query file exists if required.
- 4-4: spatial join output by neighborhood exists and is symbolized by `Join_Count`.
- 4-5: inside point layer exists and is symbolized by `Join_Count`.
- 4-6: `UCRHierarchyCode` table exists, join works, and optional unique values by CrimeType are applied.

