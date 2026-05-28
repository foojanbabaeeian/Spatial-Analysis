"""
Comprehensive fix script for Chapter 2 ArcGIS Pro tutorials 2-2 through 2-8.
Modifies .aprx files (which are ZIP archives with JSON/XML layer files).
"""

import zipfile, json, os, shutil, copy, re

BASE = 'C:/Users/fooja/Desktop/Chapter2/Tutorials/'

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_zip(aprx):
    """Load all files from a .aprx zip into a dict."""
    files = {}
    with zipfile.ZipFile(aprx, 'r') as z:
        for name in z.namelist():
            files[name] = z.read(name)
    return files

def save_zip(aprx, files):
    """Save files dict back to .aprx zip."""
    tmp = aprx + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    if os.path.exists(aprx):
        os.remove(aprx)
    os.rename(tmp, aprx)

def parse_json(data):
    """Parse JSON from bytes (handles null-terminated strings)."""
    text = data.decode('utf-8') if isinstance(data, bytes) else data
    if text.endswith('\x00'):
        text = text[:-1]
    return json.loads(text)

def dump_json(obj):
    """Serialize JSON back to bytes with null terminator."""
    return (json.dumps(obj) + '\x00').encode('utf-8')

def rgb(r, g, b, a=100):
    return {'type': 'CIMRGBColor',
            'colorSpace': {'type': 'CIMICCColorSpace', 'url': 'Default RGB'},
            'values': [r, g, b, a]}

def solid_fill(color):
    return {'type': 'CIMSolidFill', 'enable': True, 'color': color}

def solid_stroke(color, width=0.7):
    return {
        'type': 'CIMSolidStroke', 'enable': True,
        'capStyle': 'Round', 'joinStyle': 'Round', 'lineStyle3D': 'Strip',
        'miterLimit': 10, 'width': width, 'height3D': 1, 'anchor3D': 'Center',
        'color': color
    }

def poly_symbol(fill_color, stroke_color=None, stroke_width=0.7):
    """Create a CIMPolygonSymbol."""
    stroke = stroke_color or rgb(110, 110, 110)
    return {
        'type': 'CIMPolygonSymbol',
        'symbolLayers': [
            solid_stroke(stroke, stroke_width),
            solid_fill(fill_color)
        ],
        'angleAlignment': 'Map'
    }

def make_class_break(upper_bound, label, fill_color, stroke_color=None, stroke_width=0.7):
    """Create a CIMClassBreak entry."""
    return {
        'type': 'CIMClassBreak',
        'label': label,
        'patch': 'Default',
        'symbol': {
            'type': 'CIMSymbolReference',
            'symbol': poly_symbol(fill_color, stroke_color, stroke_width)
        },
        'upperBound': upper_bound
    }

def gray_ramp_color(idx, total=5):
    """Generate grayscale colors from light to dark for class breaks."""
    # Light gray (230) to dark gray (30)
    gray_values = [230, 185, 140, 85, 30]
    v = gray_values[idx] if idx < len(gray_values) else 30
    return rgb(v, v, v)

def make_text_symbol(font_family='Tahoma', font_style='Regular', size=10,
                     color=None, halo=False, halo_color=None, halo_size=1.5):
    """Create a CIMTextSymbol."""
    text_color = color or rgb(0, 0, 0)
    sym = {
        'type': 'CIMTextSymbol',
        'blockProgression': 'TTB',
        'depth3D': 1,
        'extrapolateBaselines': True,
        'fontEffects': 'Normal',
        'fontEncoding': 'Unicode',
        'fontFamilyName': font_family,
        'fontStyleName': font_style,
        'fontType': 'Unspecified',
        'haloSize': 1,
        'height': size,
        'hinting': 'Default',
        'horizontalAlignment': 'Left',
        'kerning': True,
        'letterWidth': 100,
        'ligatures': True,
        'lineGapType': 'ExtraLeading',
        'symbol': {
            'type': 'CIMPolygonSymbol',
            'symbolLayers': [{'type': 'CIMSolidFill', 'enable': True, 'color': text_color}],
            'angleAlignment': 'Map'
        },
        'textCase': 'Normal',
        'textDirection': 'LTR',
        'verticalAlignment': 'Bottom',
        'verticalGlyphOrientation': 'Right',
        'wordSpacing': 100,
        'billboardMode3D': 'FaceNearPlane'
    }
    if halo:
        hc = halo_color or rgb(255, 255, 255)
        sym['haloSize'] = halo_size
        sym['haloSymbol'] = {
            'type': 'CIMSymbolReference',
            'symbol': {
                'type': 'CIMPolygonSymbol',
                'symbolLayers': [{'type': 'CIMSolidFill', 'enable': True, 'color': hc}],
                'angleAlignment': 'Map'
            }
        }
    return sym

def make_label_class(expression, font_family='Tahoma', font_style='Regular',
                     size=10, color=None, halo=False, halo_color=None,
                     placement_method='HorizontalInPolygon',
                     min_scale=None, max_scale=None,
                     remove_duplicates=False):
    """Create a CIMLabelClass for a polygon feature layer."""
    text_sym = make_text_symbol(font_family, font_style, size, color,
                                halo, halo_color)
    lc = {
        'type': 'CIMLabelClass',
        'expression': expression,
        'expressionEngine': 'VBScript',
        'featuresToLabel': 'AllVisibleFeatures',
        'maplexLabelPlacementProperties': {
            'type': 'CIMMaplexLabelPlacementProperties',
            'featureType': 'Polygon',
            'avoidPolygonHoles': True,
            'canOverrunFeature': True,
            'canPlaceLabelOutsidePolygon': True,
            'canRemoveOverlappingLabel': True,
            'canStackLabel': True,
            'centerLabelAnchorType': 'Symbol',
            'connectionType': 'Unambiguous',
            'constrainOffset': 'NoConstraint',
            'contourAlignmentType': 'Page',
            'contourLadderType': 'Straight',
            'contourMaximumAngle': 90,
            'enableConnection': True,
            'featureWeight': 0,
            'fontHeightReductionLimit': 4,
            'fontHeightReductionStep': 0.5,
            'fontWidthReductionLimit': 90,
            'fontWidthReductionStep': 5,
            'graticuleAlignmentType': 'Straight',
            'keyNumberGroupName': 'Default',
            'labelBuffer': 15,
            'labelLargestPolygon': False,
            'labelPriority': -1,
            'labelStackingProperties': {
                'type': 'CIMMaplexLabelStackingProperties',
                'stackAlignment': 'ChooseBest',
                'maximumNumberOfLines': 3,
                'minimumNumberOfCharsPerLine': 3,
                'maximumNumberOfCharsPerLine': 24,
                'separators': [
                    {'type': 'CIMMaplexStackingSeparator', 'separator': ' ', 'splitAfter': True},
                    {'type': 'CIMMaplexStackingSeparator', 'separator': ',', 'visible': True, 'splitAfter': True}
                ],
                'trimStackingSeparators': True,
                'preferToStackLongLabels': True
            },
            'lineFeatureType': 'General',
            'linePlacementMethod': 'OffsetCurvedFromLine',
            'maximumLabelOverrun': 80,
            'maximumLabelOverrunUnit': 'Point',
            'minimumFeatureSizeUnit': 'Map',
            'multiPartOption': 'OneLabelPerPart',
            'offsetAlongLineProperties': {
                'type': 'CIMMaplexOffsetAlongLineProperties',
                'placementMethod': 'BestPositionAlongLine',
                'labelAnchorPoint': 'CenterOfLabel',
                'distanceUnit': 'Percentage',
                'useLineDirection': True
            },
            'pointExternalZonePriorities': {
                'type': 'CIMMaplexExternalZonePriorities',
                'aboveLeft': 4, 'aboveCenter': 2, 'aboveRight': 1,
                'centerRight': 3, 'belowRight': 5, 'belowCenter': 7,
                'belowLeft': 8, 'centerLeft': 6
            },
            'pointPlacementMethod': 'AroundPoint',
            'polygonAnchorPointType': 'GeometricCenter',
            'polygonBoundaryWeight': 0,
            'polygonExternalZones': {
                'type': 'CIMMaplexExternalZonePriorities',
                'aboveLeft': 4, 'aboveCenter': 2, 'aboveRight': 1,
                'centerRight': 3, 'belowRight': 5, 'belowCenter': 7,
                'belowLeft': 8, 'centerLeft': 6
            },
            'polygonFeatureType': 'General',
            'polygonInternalZones': {'type': 'CIMMaplexInternalZonePriorities', 'center': 1},
            'polygonPlacementMethod': placement_method,
            'primaryOffset': 1,
            'primaryOffsetUnit': 'Point',
            'removeAmbiguousLabels': 'All',
            'removeExtraWhiteSpace': True,
            'repetitionIntervalUnit': 'Map',
            'rotationProperties': {
                'type': 'CIMMaplexRotationProperties',
                'rotationType': 'Arithmetic',
                'alignmentType': 'Straight'
            },
            'secondaryOffset': 100,
            'secondaryOffsetUnit': 'Percentage',
            'strategyPriorities': {
                'type': 'CIMMaplexStrategyPriorities',
                'stacking': 1, 'overrun': 2, 'fontCompression': 3,
                'fontReduction': 4, 'abbreviation': 5
            },
            'thinningDistanceUnit': 'Point',
            'truncationMarkerCharacter': '.',
            'truncationMinimumLength': 1,
            'truncationPreferredCharacters': 'aeiou',
            'polygonAnchorPointPerimeterInsetUnit': 'Point'
        },
        'name': 'Class 1',
        'priority': -1,
        'standardLabelPlacementProperties': {
            'type': 'CIMStandardLabelPlacementProperties',
            'featureType': 'Line',
            'featureWeight': 'Low',
            'labelWeight': 'High',
            'numLabelsOption': 'OneLabelPerName',
            'lineLabelPosition': {'type': 'CIMStandardLineLabelPosition', 'above': True, 'inLine': True, 'parallel': True},
            'lineLabelPriorities': {
                'type': 'CIMStandardLineLabelPriorities',
                'aboveStart': 3, 'aboveAlong': 3, 'aboveEnd': 3,
                'centerStart': 3, 'centerAlong': 3, 'centerEnd': 3,
                'belowStart': 3, 'belowAlong': 3, 'belowEnd': 3
            },
            'pointPlacementMethod': 'AroundPoint',
            'pointPlacementPriorities': {
                'type': 'CIMStandardPointPlacementPriorities',
                'aboveLeft': 2, 'aboveCenter': 2, 'aboveRight': 1,
                'centerLeft': 3, 'centerRight': 2, 'belowLeft': 3,
                'belowCenter': 3, 'belowRight': 2
            },
            'rotationType': 'Arithmetic',
            'polygonPlacementMethod': 'AlwaysHorizontal'
        },
        'textSymbol': {'type': 'CIMSymbolReference', 'symbol': text_sym},
        'useCodedValue': False,
        'visibility': True,
        'iD': -1
    }
    if min_scale is not None:
        lc['minimumScale'] = min_scale
    if max_scale is not None:
        lc['maximumScale'] = max_scale
    if remove_duplicates:
        lc['maplexLabelPlacementProperties']['removeDuplicates'] = 'All'
        lc['maplexLabelPlacementProperties']['removeDuplicatesUnit'] = 'Map'
    return lc

def make_line_label_class(expression, font_family='Tahoma', font_style='Regular',
                          size=10, color=None, min_scale=None, max_scale=None):
    """Create a CIMLabelClass for a line feature layer."""
    text_sym = make_text_symbol(font_family, font_style, size, color)
    lc = {
        'type': 'CIMLabelClass',
        'expression': expression,
        'expressionEngine': 'VBScript',
        'featuresToLabel': 'AllVisibleFeatures',
        'maplexLabelPlacementProperties': {
            'type': 'CIMMaplexLabelPlacementProperties',
            'featureType': 'Line',
            'avoidPolygonHoles': True,
            'canOverrunFeature': True,
            'canPlaceLabelOutsidePolygon': True,
            'canRemoveOverlappingLabel': True,
            'canStackLabel': False,
            'centerLabelAnchorType': 'Symbol',
            'connectionType': 'Unambiguous',
            'constrainOffset': 'AboveLine',
            'contourAlignmentType': 'Page',
            'contourLadderType': 'Straight',
            'contourMaximumAngle': 90,
            'enableConnection': True,
            'featureWeight': 0,
            'fontHeightReductionLimit': 4,
            'fontHeightReductionStep': 0.5,
            'fontWidthReductionLimit': 90,
            'fontWidthReductionStep': 5,
            'graticuleAlignmentType': 'Straight',
            'keyNumberGroupName': 'Default',
            'labelBuffer': 15,
            'labelLargestPolygon': False,
            'labelPriority': -1,
            'labelStackingProperties': {
                'type': 'CIMMaplexLabelStackingProperties',
                'stackAlignment': 'ChooseBest',
                'maximumNumberOfLines': 3,
                'minimumNumberOfCharsPerLine': 3,
                'maximumNumberOfCharsPerLine': 24,
                'separators': [
                    {'type': 'CIMMaplexStackingSeparator', 'separator': ' ', 'splitAfter': True}
                ],
                'trimStackingSeparators': True,
                'preferToStackLongLabels': False
            },
            'lineFeatureType': 'General',
            'linePlacementMethod': 'CenteredHorizontalOnLine',
            'maximumLabelOverrun': 80,
            'maximumLabelOverrunUnit': 'Point',
            'minimumFeatureSizeUnit': 'Map',
            'multiPartOption': 'OneLabelPerPart',
            'offsetAlongLineProperties': {
                'type': 'CIMMaplexOffsetAlongLineProperties',
                'placementMethod': 'BestPositionAlongLine',
                'labelAnchorPoint': 'CenterOfLabel',
                'distanceUnit': 'Percentage',
                'useLineDirection': True
            },
            'pointExternalZonePriorities': {
                'type': 'CIMMaplexExternalZonePriorities',
                'aboveLeft': 4, 'aboveCenter': 2, 'aboveRight': 1,
                'centerRight': 3, 'belowRight': 5, 'belowCenter': 7,
                'belowLeft': 8, 'centerLeft': 6
            },
            'pointPlacementMethod': 'AroundPoint',
            'polygonAnchorPointType': 'GeometricCenter',
            'polygonBoundaryWeight': 0,
            'polygonExternalZones': {
                'type': 'CIMMaplexExternalZonePriorities',
                'aboveLeft': 4, 'aboveCenter': 2, 'aboveRight': 1,
                'centerRight': 3, 'belowRight': 5, 'belowCenter': 7,
                'belowLeft': 8, 'centerLeft': 6
            },
            'polygonFeatureType': 'General',
            'polygonInternalZones': {'type': 'CIMMaplexInternalZonePriorities', 'center': 1},
            'polygonPlacementMethod': 'HorizontalInPolygon',
            'primaryOffset': 1,
            'primaryOffsetUnit': 'Point',
            'removeAmbiguousLabels': 'All',
            'removeExtraWhiteSpace': True,
            'repetitionIntervalUnit': 'Map',
            'rotationProperties': {
                'type': 'CIMMaplexRotationProperties',
                'rotationType': 'Arithmetic',
                'alignmentType': 'Straight'
            },
            'secondaryOffset': 100,
            'secondaryOffsetUnit': 'Percentage',
            'strategyPriorities': {
                'type': 'CIMMaplexStrategyPriorities',
                'stacking': 1, 'overrun': 2, 'fontCompression': 3,
                'fontReduction': 4, 'abbreviation': 5
            },
            'thinningDistanceUnit': 'Point',
            'truncationMarkerCharacter': '.',
            'truncationMinimumLength': 1,
            'truncationPreferredCharacters': 'aeiou',
            'polygonAnchorPointPerimeterInsetUnit': 'Point'
        },
        'name': 'Class 1',
        'priority': -1,
        'standardLabelPlacementProperties': {
            'type': 'CIMStandardLabelPlacementProperties',
            'featureType': 'Line',
            'featureWeight': 'Low',
            'labelWeight': 'High',
            'numLabelsOption': 'OneLabelPerName',
            'lineLabelPosition': {'type': 'CIMStandardLineLabelPosition', 'above': True, 'inLine': True, 'parallel': True},
            'lineLabelPriorities': {
                'type': 'CIMStandardLineLabelPriorities',
                'aboveStart': 3, 'aboveAlong': 3, 'aboveEnd': 3,
                'centerStart': 3, 'centerAlong': 3, 'centerEnd': 3,
                'belowStart': 3, 'belowAlong': 3, 'belowEnd': 3
            },
            'pointPlacementMethod': 'AroundPoint',
            'pointPlacementPriorities': {
                'type': 'CIMStandardPointPlacementPriorities',
                'aboveLeft': 2, 'aboveCenter': 2, 'aboveRight': 1,
                'centerLeft': 3, 'centerRight': 2, 'belowLeft': 3,
                'belowCenter': 3, 'belowRight': 2
            },
            'rotationType': 'Arithmetic',
            'polygonPlacementMethod': 'AlwaysHorizontal'
        },
        'textSymbol': {'type': 'CIMSymbolReference', 'symbol': text_sym},
        'useCodedValue': False,
        'visibility': True,
        'iD': -1
    }
    if min_scale is not None:
        lc['minimumScale'] = min_scale
    if max_scale is not None:
        lc['maximumScale'] = max_scale
    return lc


# ============================================================
# TUTORIAL 2-2: LABELS AND POP-UPS
# ============================================================

def fix_t22():
    aprx = BASE + 'Tutorial2-2FozhanBabaeiyan.aprx'
    files = load_zip(aprx)
    print("Fixing Tutorial 2-2...")

    # -- ZoningLandUse: labels on ZONE, size 8, Gray 50% --
    key = 'new_york_city_zoning/zoninglanduse.xml'
    obj = parse_json(files[key])
    obj['displayAnnotation'] = True
    obj['showPopups'] = False
    obj['labelClasses'] = [
        make_label_class('[ZONE]', size=8, color=rgb(128, 128, 128),
                         placement_method='HorizontalInPolygon')
    ]
    files[key] = dump_json(obj)

    # -- Neighborhoods: labels on Name, Arial Bold 11, white halo, Land Parcel --
    key = 'new_york_city_zoning/neighborhoods.xml'
    obj = parse_json(files[key])
    obj['displayAnnotation'] = True
    # Configure popup with 5 fields
    obj['popupInfo'] = {
        'type': 'CIMPopupInfo',
        'title': '{Name}',
        'mediaInfos': [],
        'fieldDescriptions': [
            {'type': 'CIMFieldDescription', 'alias': 'Borough Name', 'fieldName': 'BORONAME', 'numberFormat': None, 'visible': True, 'searchMode': 'Exact'},
            {'type': 'CIMFieldDescription', 'alias': 'Population', 'fieldName': 'POP2010', 'numberFormat': None, 'visible': True, 'searchMode': 'Exact'},
            {'type': 'CIMFieldDescription', 'alias': 'Population (Impoverished)', 'fieldName': 'POPIMPOV', 'numberFormat': None, 'visible': True, 'searchMode': 'Exact'},
            {'type': 'CIMFieldDescription', 'alias': 'Population Under 18', 'fieldName': 'POP18UNDER', 'numberFormat': None, 'visible': True, 'searchMode': 'Exact'},
            {'type': 'CIMFieldDescription', 'alias': 'Population Under 18 (Impoverished)', 'fieldName': 'POP18UNIMPOV', 'numberFormat': None, 'visible': True, 'searchMode': 'Exact'},
        ]
    }
    obj['labelClasses'] = [
        make_label_class('[Name]', font_family='Arial', font_style='Bold',
                         size=11, color=rgb(0, 0, 0), halo=True,
                         halo_color=rgb(255, 255, 255),
                         placement_method='HorizontalInPolygon')
    ]
    files[key] = dump_json(obj)

    # -- Water: labels on LANDNAME, Times New Roman 12, Atlantic Blue, no duplicates --
    key = 'new_york_city_zoning/water.xml'
    obj = parse_json(files[key])
    obj['displayAnnotation'] = True
    obj['showPopups'] = False
    obj['labelClasses'] = [
        make_label_class('[LANDNAME]', font_family='Times New Roman',
                         font_style='Regular', size=12,
                         color=rgb(102, 153, 205),  # Atlantic Blue
                         remove_duplicates=True)
    ]
    files[key] = dump_json(obj)

    save_zip(aprx, files)
    print("  Done: Tutorial 2-2")


# ============================================================
# TUTORIAL 2-3: DEFINITION QUERIES AND SYMBOLOGY
# ============================================================

def make_point_symbol(shape_type, fill_color, outline_color=None, size=8):
    """Make a CIMPointSymbol with marker (circle, square, cross).
    shape_type: 'circle', 'square', 'cross'
    """
    outline = outline_color or rgb(0, 0, 0)

    if shape_type == 'circle':
        # Circle using curveRings
        geometry = {
            'curveRings': [
                [
                    [1.2246467991473532e-16, 2],
                    {'a': [[1.2246467991473532e-16, 2], [0, 0], 0, 1]}
                ]
            ]
        }
    elif shape_type == 'square':
        geometry = {
            'rings': [
                [[-2, -2], [2, -2], [2, 2], [-2, 2], [-2, -2]]
            ]
        }
    elif shape_type == 'cross':
        # Cross shape
        geometry = {
            'rings': [
                [
                    [-0.5, -2], [0.5, -2], [0.5, -0.5], [2, -0.5],
                    [2, 0.5], [0.5, 0.5], [0.5, 2], [-0.5, 2],
                    [-0.5, 0.5], [-2, 0.5], [-2, -0.5], [-0.5, -0.5],
                    [-0.5, -2]
                ]
            ]
        }
    else:
        geometry = {
            'curveRings': [
                [[1.2246467991473532e-16, 2], {'a': [[1.2246467991473532e-16, 2], [0, 0], 0, 1]}]
            ]
        }

    marker_graphic = {
        'type': 'CIMMarkerGraphic',
        'geometry': geometry,
        'symbol': {
            'type': 'CIMPolygonSymbol',
            'symbolLayers': [
                solid_stroke(outline, 0.7),
                solid_fill(fill_color)
            ],
            'angleAlignment': 'Map'
        }
    }

    vector_marker = {
        'type': 'CIMVectorMarker',
        'enable': True,
        'anchorPointUnits': 'Relative',
        'dominantSizeAxis3D': 'Z',
        'size': size,
        'billboardMode3D': 'FaceNearPlane',
        'frame': {'xmin': -2, 'ymin': -2, 'xmax': 2, 'ymax': 2},
        'markerGraphics': [marker_graphic],
        'respectFrame': True
    }

    return {
        'type': 'CIMPointSymbol',
        'symbolLayers': [vector_marker],
        'haloSize': 1,
        'scaleX': 1,
        'angleAlignment': 'Display'
    }

def make_unique_value_class(values, label, fill_color, shape='circle', size=8, outline=None):
    """Make a CIMUniqueValueClass for a unique value renderer."""
    sym = make_point_symbol(shape, fill_color, outline, size)
    return {
        'type': 'CIMUniqueValueClass',
        'label': label,
        'patch': 'Default',
        'symbol': {'type': 'CIMSymbolReference', 'symbol': sym},
        'values': [{'type': 'CIMUniqueValue', 'fieldValues': [v]} for v in values],
        'visible': True,
        'editable': True
    }

def fix_t23():
    aprx = BASE + 'Tutorial2-3FozhanBabaeiyan.aprx'
    files = load_zip(aprx)
    print("Fixing Tutorial 2-3...")

    # -- Facilities: definition query, rename, unique value renderer --
    key = 'nyc_food_pantries_and_soup_kitchens/facilities.xml'
    obj = parse_json(files[key])
    obj['name'] = 'food facilities'

    # Definition expression (OR-based query)
    obj['featureTable']['definitionExpression'] = (
        "facility_T = '4901' OR facility_T = '4902' OR facility_T = '4903'"
    )

    # Unique value renderer on fact_type
    obj['renderer'] = {
        'type': 'CIMUniqueValueRenderer',
        'defaultLabel': '<all other values>',
        'defaultSymbolPatch': 'Default',
        'defaultSymbol': {
            'type': 'CIMSymbolReference',
            'symbol': make_point_symbol('circle', rgb(130, 130, 130), size=8)
        },
        'fields': ['fact_type'],
        'groups': [
            {
                'type': 'CIMUniqueValueGroup',
                'classes': [
                    make_unique_value_class(
                        ['Soup Kitchen'], 'Soup Kitchen',
                        rgb(255, 0, 0),  # Red
                        shape='square', size=8
                    ),
                    make_unique_value_class(
                        ['Food Pantry'], 'Food Pantry',
                        rgb(0, 0, 255),  # Blue
                        shape='circle', size=8
                    ),
                    make_unique_value_class(
                        ['Joint Soup Kitchen Food Pantry'], 'Joint Soup Kitchen Food Pantry',
                        rgb(255, 255, 190),  # Solar Yellow
                        shape='cross', size=10
                    ),
                ],
                'heading': 'fact_type'
            }
        ],
        'useDefaultSymbol': False,
        'polygonSymbolColorTarget': 'Fill',
        'barrierWeight': 'High'
    }
    files[key] = dump_json(obj)

    # -- ManhattanStreets: gray 20%, width 0.5, labels on STREET --
    key = 'nyc_food_pantries_and_soup_kitchens/manhattanstreets.xml'
    obj = parse_json(files[key])
    obj['displayAnnotation'] = True

    # Update renderer stroke color and width
    renderer = obj.get('renderer', {})
    sym = renderer.get('symbol', {}).get('symbol', {})
    for sl in sym.get('symbolLayers', []):
        if sl.get('type') == 'CIMSolidStroke':
            sl['color'] = rgb(204, 204, 204)  # Gray 20%
            sl['width'] = 0.5

    obj['labelClasses'] = [
        make_line_label_class('[STREET]', font_family='Tahoma', size=8,
                              color=rgb(0, 0, 0))
    ]
    files[key] = dump_json(obj)

    # -- World Light Gray Canvas Base: turn off visibility --
    uuid_file = '658d486924364d5a93465ec49d8844e7.xml'
    if uuid_file in files:
        obj = parse_json(files[uuid_file])
        obj['visibility'] = False
        files[uuid_file] = dump_json(obj)

    save_zip(aprx, files)
    print("  Done: Tutorial 2-3")


# ============================================================
# TUTORIAL 2-4: CHOROPLETH MAPS (GRADUATED COLORS)
# ============================================================

def fix_t24():
    aprx = BASE + 'Tutorial2-4FozhanBabaeiyan.aprx'
    files = load_zip(aprx)
    print("Fixing Tutorial 2-4...")

    # -- Neighborhoods_3D.json: Quantile, O60_FOOD, Grayscale --
    key = 'NYC_Food_Stamps_SNAP_Households_by_Neighborhood/Neighborhoods_3D.json'
    obj = parse_json(files[key])
    r = obj.get('renderer', {})

    # Change field and method
    r['field'] = 'O60_FOOD'
    r['heading'] = 'O60_FOOD'
    r['classificationMethod'] = 'Quantile'

    # Update colorRamp to grayscale
    r['colorRamp'] = {
        'type': 'CIMLinearContinuousColorRamp',
        'colorSpace': {'type': 'CIMICCColorSpace', 'url': 'Default RGB'},
        'fromColor': rgb(240, 240, 240),
        'toColor': rgb(15, 15, 15)
    }

    # Update the 5 breaks with grayscale colors
    # Keep existing upperBound values (the breaks from NaturalBreaks on the original data)
    # but change colors to grayscale
    gray_fills = [
        rgb(230, 230, 230),  # lightest
        rgb(178, 178, 178),
        rgb(120, 120, 120),
        rgb(70, 70, 70),
        rgb(20, 20, 20),     # darkest
    ]
    breaks = r.get('breaks', [])
    for i, brk in enumerate(breaks):
        sym = brk.get('symbol', {}).get('symbol', {})
        for sl in sym.get('symbolLayers', []):
            if sl.get('type') == 'CIMSolidFill':
                sl['color'] = gray_fills[min(i, 4)]
                # Remove HSV colorSpace if present
                if 'colorSpace' in sl['color']:
                    sl['color']['colorSpace'] = {'type': 'CIMICCColorSpace', 'url': 'Default RGB'}
                sl['color']['type'] = 'CIMRGBColor'
    r['breaks'] = breaks

    # Also update numberFormat to show whole numbers
    r['normalizationType'] = 'Nothing'
    obj['renderer'] = r

    # Also set the extrusion on the 3D layer (using O60_FOOD for height)
    if 'layerEffectsMode' in obj:
        obj['layerEffectsMode'] = 'UseLayerEffects'

    files[key] = dump_json(obj)

    save_zip(aprx, files)
    print("  Done: Tutorial 2-4")


# ============================================================
# TUTORIAL 2-5: GRADUATED AND PROPORTIONAL POINT SYMBOLS
# ============================================================

def make_graduated_symbol_renderer(field, min_size, max_size, fill_color, num_breaks=5):
    """Create a CIMClassBreaksRenderer for graduated symbols."""
    # Create 5 breaks with increasing size
    sizes = [min_size + (max_size - min_size) * i / (num_breaks - 1) for i in range(num_breaks)]

    # Use placeholder upper bounds (will be recalculated by ArcGIS)
    upper_bounds = [100, 500, 1000, 2000, 5000]
    labels = ['0 - 100', '101 - 500', '501 - 1000', '1001 - 2000', '2001 - 5000']

    breaks = []
    for i in range(num_breaks):
        sz = sizes[i]
        brk = {
            'type': 'CIMClassBreak',
            'label': labels[i],
            'patch': 'Default',
            'symbol': {
                'type': 'CIMSymbolReference',
                'symbol': {
                    'type': 'CIMPointSymbol',
                    'symbolLayers': [
                        {
                            'type': 'CIMVectorMarker',
                            'enable': True,
                            'anchorPointUnits': 'Relative',
                            'dominantSizeAxis3D': 'Z',
                            'size': sz,
                            'billboardMode3D': 'FaceNearPlane',
                            'frame': {'xmin': -2, 'ymin': -2, 'xmax': 2, 'ymax': 2},
                            'markerGraphics': [
                                {
                                    'type': 'CIMMarkerGraphic',
                                    'geometry': {
                                        'curveRings': [
                                            [[1.2246467991473532e-16, 2], {'a': [[1.2246467991473532e-16, 2], [0, 0], 0, 1]}]
                                        ]
                                    },
                                    'symbol': {
                                        'type': 'CIMPolygonSymbol',
                                        'symbolLayers': [
                                            solid_stroke(rgb(0, 0, 0), 0.7),
                                            solid_fill(fill_color)
                                        ],
                                        'angleAlignment': 'Map'
                                    }
                                }
                            ],
                            'respectFrame': True
                        }
                    ],
                    'haloSize': 1,
                    'scaleX': 1,
                    'angleAlignment': 'Display'
                }
            },
            'upperBound': upper_bounds[i]
        }
        breaks.append(brk)

    return {
        'type': 'CIMClassBreaksRenderer',
        'barrierWeight': 'High',
        'classBreakType': 'GraduatedSymbol',
        'colorRamp': {
            'type': 'CIMLinearContinuousColorRamp',
            'colorSpace': {'type': 'CIMICCColorSpace', 'url': 'Default RGB'},
            'fromColor': fill_color,
            'toColor': fill_color
        },
        'field': field,
        'heading': field,
        'polygonSymbolColorTarget': 'Fill',
        'drawGraduatedSymbolsAboveAllLayers': True,
        'classificationMethod': 'Quantile',
        'breaks': breaks,
        'showInAscendingOrder': True,
        'defaultSymbolPatch': 'Default',
        'defaultSymbol': {
            'type': 'CIMSymbolReference',
            'symbol': {
                'type': 'CIMPointSymbol',
                'symbolLayers': [
                    {
                        'type': 'CIMVectorMarker',
                        'enable': True,
                        'anchorPointUnits': 'Relative',
                        'dominantSizeAxis3D': 'Z',
                        'size': min_size,
                        'billboardMode3D': 'FaceNearPlane',
                        'frame': {'xmin': -2, 'ymin': -2, 'xmax': 2, 'ymax': 2},
                        'markerGraphics': [
                            {
                                'type': 'CIMMarkerGraphic',
                                'geometry': {'curveRings': [[[1.2246467991473532e-16, 2], {'a': [[1.2246467991473532e-16, 2], [0, 0], 0, 1]}]]},
                                'symbol': {
                                    'type': 'CIMPolygonSymbol',
                                    'symbolLayers': [solid_stroke(rgb(0,0,0)), solid_fill(fill_color)],
                                    'angleAlignment': 'Map'
                                }
                            }
                        ],
                        'respectFrame': True
                    }
                ],
                'haloSize': 1, 'scaleX': 1, 'angleAlignment': 'Display'
            }
        },
        'numberFormat': {
            'type': 'CIMNumericFormat', 'alignmentOption': 'esriAlignLeft',
            'alignmentWidth': 0, 'roundingOption': 'esriRoundNumberOfDecimals',
            'roundingValue': 0, 'zeroPad': True
        },
        'alwaysUpdateClassLabels': True,
        'sampleSize': 10000,
        'normalizationType': 'Nothing',
        'minimumSymbolSize': min_size,
        'maximumSymbolSize': max_size,
        'exclusionSymbol': {'type': 'CIMSymbolReference'},
        'useExclusionSymbol': False,
        'exclusionSymbolPatch': 'Default'
    }

def make_proportional_renderer(field, min_size=2, max_size=20, fill_color=None):
    """Create a CIMProportionalRenderer for proportional symbols."""
    fc = fill_color or rgb(128, 0, 128)
    return {
        'type': 'CIMProportionalRenderer',
        'barrierWeight': 'High',
        'valueExpressionInfo': None,
        'field': field,
        'flanneryCompensation': False,
        'legendType': 'LegendFromTemplate',
        'minimumSymbolSize': min_size,
        'maximumSymbolSize': max_size,
        'symbolTemplate': {
            'type': 'CIMSymbolReference',
            'symbol': {
                'type': 'CIMPointSymbol',
                'symbolLayers': [
                    {
                        'type': 'CIMVectorMarker',
                        'enable': True,
                        'anchorPointUnits': 'Relative',
                        'dominantSizeAxis3D': 'Z',
                        'size': min_size,
                        'billboardMode3D': 'FaceNearPlane',
                        'frame': {'xmin': -2, 'ymin': -2, 'xmax': 2, 'ymax': 2},
                        'markerGraphics': [
                            {
                                'type': 'CIMMarkerGraphic',
                                'geometry': {'curveRings': [[[1.2246467991473532e-16, 2], {'a': [[1.2246467991473532e-16, 2], [0, 0], 0, 1]}]]},
                                'symbol': {
                                    'type': 'CIMPolygonSymbol',
                                    'symbolLayers': [solid_stroke(rgb(0,0,0)), solid_fill(fc)],
                                    'angleAlignment': 'Map'
                                }
                            }
                        ],
                        'respectFrame': True
                    }
                ],
                'haloSize': 1, 'scaleX': 1, 'angleAlignment': 'Display'
            }
        },
        'maxDataValue': 5000,
        'showInAscendingOrder': True,
        'defaultSymbol': {'type': 'CIMSymbolReference'},
        'defaultSymbolPatch': 'Default'
    }

def fix_t25():
    aprx = BASE + 'Tutorial2-5FozhanBabaeiyan.aprx'
    files = load_zip(aprx)
    print("Fixing Tutorial 2-5...")

    # -- nyc_food_facilities neighborhoods: rename + Graduated Symbols on food_FASIL --
    key = 'nyc_food_facilities_and_food_stamps_snap_neighbood_study/neighborhoods.xml'
    obj = parse_json(files[key])
    obj['name'] = 'number of food banks / soup kitchens'
    # Solar Yellow: RGB(255, 255, 190) - Yucca Yellow
    obj['renderer'] = make_graduated_symbol_renderer(
        field='food_FASIL',
        min_size=2,
        max_size=18,
        fill_color=rgb(255, 255, 190)  # Solar/Yucca Yellow
    )
    files[key] = dump_json(obj)

    # -- nyc_food_stamps neighborhoods: rename + Proportional Symbols on U18_FOOD --
    key = 'nyc_food_stamps_snap_households_by_neighborhood/neighborhoods.xml'
    obj = parse_json(files[key])
    obj['name'] = 'under 18 receiving food stamps'
    obj['renderer'] = make_proportional_renderer(
        field='U18_FOOD',
        min_size=2,
        max_size=20,
        fill_color=rgb(102, 0, 128)  # Purple
    )
    files[key] = dump_json(obj)

    save_zip(aprx, files)
    print("  Done: Tutorial 2-5")


# ============================================================
# TUTORIAL 2-6: NORMALIZED CHOROPLETH WITH CUSTOM SCALE
# ============================================================

def make_manual_interval_renderer(field, norm_field, breaks_upper, gray_fills, field_heading=None):
    """
    Create a CIMClassBreaksRenderer with manual interval breaks, gray colors,
    and percentage number format.
    breaks_upper: list of upper bound values (5 values for 5 classes)
    gray_fills: list of 5 grayscale RGB colors
    """
    # Build labels as percentages
    labels = []
    prev = 0.0
    for ub in breaks_upper:
        labels.append(f'{prev*100:.0f}% - {ub*100:.0f}%')
        prev = ub

    brk_list = []
    for i, (ub, lbl, fc) in enumerate(zip(breaks_upper, labels, gray_fills)):
        brk_list.append({
            'type': 'CIMClassBreak',
            'label': lbl,
            'patch': 'Default',
            'symbol': {
                'type': 'CIMSymbolReference',
                'symbol': poly_symbol(fc, rgb(110, 110, 110), 0.7)
            },
            'upperBound': ub
        })

    return {
        'type': 'CIMClassBreaksRenderer',
        'barrierWeight': 'None',
        'classBreakType': 'GraduatedColor',
        'colorRamp': {
            'type': 'CIMLinearContinuousColorRamp',
            'colorSpace': {'type': 'CIMICCColorSpace', 'url': 'Default RGB'},
            'fromColor': gray_fills[0],
            'toColor': gray_fills[-1]
        },
        'field': field,
        'heading': field_heading or field,
        'polygonSymbolColorTarget': 'Fill',
        'drawGraduatedSymbolsAboveAllLayers': True,
        'classificationMethod': 'ManualInterval',
        'breaks': brk_list,
        'showInAscendingOrder': True,
        'defaultSymbolPatch': 'Default',
        'defaultSymbol': {
            'type': 'CIMSymbolReference',
            'symbol': poly_symbol(rgb(130, 130, 130), rgb(110, 110, 110))
        },
        'numberFormat': {
            'type': 'CIMPercentageFormat',
            'alignmentOption': 'esriAlignLeft',
            'alignmentWidth': 12,
            'roundingOption': 'esriRoundNumberOfDecimals',
            'roundingValue': 0,
            'zeroPad': True,
            'percentSymbolPosition': 'ESuffix',
            'factor': 100
        },
        'alwaysUpdateClassLabels': True,
        'sampleSize': 10000,
        'normalizationType': 'Field',
        'normalizationField': norm_field,
        'exclusionSymbol': {'type': 'CIMSymbolReference'},
        'useExclusionSymbol': False,
        'exclusionSymbolPatch': 'Default',
        'authoringInfo': {
            'type': 'CIMClassBreaksRendererAuthoringInfo',
            'numberOfHistogramBins': 10,
            'templateSymbol': {
                'type': 'CIMSymbolReference',
                'symbol': poly_symbol(rgb(204, 204, 204), rgb(110, 110, 110))
            }
        }
    }

def fix_t26():
    aprx = BASE + 'Tutorial2-6FozhanBabaeiyan.aprx'
    files = load_zip(aprx)
    print("Fixing Tutorial 2-6...")

    # Manual interval breaks from tutorial: 0.02, 0.04, 0.08, 0.16, max
    # The max value in the data is ~0.258, so use 0.26 for last class
    breaks_upper = [0.02, 0.04, 0.08, 0.16, 0.26]

    # Gray 5 classes: lightest to darkest
    gray_fills = [
        rgb(240, 240, 240),
        rgb(190, 190, 190),
        rgb(130, 130, 130),
        rgb(80, 80, 80),
        rgb(30, 30, 30),
    ]

    # -- Female headed households (neighborhoods.xml) --
    key = 'food_stamp_recipients_and_resources/neighborhoods.xml'
    obj = parse_json(files[key])
    obj['renderer'] = make_manual_interval_renderer(
        field='U18FHHFOOD',
        norm_field='TOT_HH',
        breaks_upper=breaks_upper,
        gray_fills=gray_fills,
        field_heading='U18FHHFOOD'
    )
    files[key] = dump_json(obj)

    # -- Male headed households (neighborhoods2.xml): same symbology but different field --
    key = 'food_stamp_recipients_and_resources/neighborhoods2.xml'
    obj = parse_json(files[key])
    obj['renderer'] = make_manual_interval_renderer(
        field='U18MHHFOOD',
        norm_field='TOT_HH',
        breaks_upper=breaks_upper,
        gray_fills=gray_fills,
        field_heading='U18MHHFOOD'
    )
    files[key] = dump_json(obj)

    save_zip(aprx, files)
    print("  Done: Tutorial 2-6")


# ============================================================
# TUTORIAL 2-7: DOT DENSITY MAPS
# ============================================================

def fix_t27():
    aprx = BASE + 'Tutorial2-7FozhanBabaeiyan.aprx'
    files = load_zip(aprx)
    print("Fixing Tutorial 2-7...")

    key = 'density_maps/neighborhoods2.xml'
    obj = parse_json(files[key])
    r = obj.get('renderer', {})

    # Update dot density settings
    r['fieldNames'] = ['U18_FOOD', 'O60_FOOD']
    r['fieldLabels'] = ['Population under 18 receiving food stamps',
                        'Population over 60 receiving food stamps']
    r['dotValue'] = 100
    r['dotSize'] = 2
    r['symbolLabel'] = '1 dot = 100 persons'
    r['unitLabel'] = 'persons'

    # Update dot density symbol to show two colors
    r['dotDensitySymbol'] = {
        'type': 'CIMSymbolReference',
        'symbol': {
            'type': 'CIMPointSymbol',
            'symbolLayers': [
                {
                    'type': 'CIMVectorMarker',
                    'enable': True,
                    'anchorPointUnits': 'Relative',
                    'dominantSizeAxis3D': 'Z',
                    'size': 2,
                    'billboardMode3D': 'FaceNearPlane',
                    'frame': {'xmin': -2, 'ymin': -2, 'xmax': 2, 'ymax': 2},
                    'markerGraphics': [
                        {
                            'type': 'CIMMarkerGraphic',
                            'geometry': {'curveRings': [[[1.2246467991473532e-16, 2], {'a': [[1.2246467991473532e-16, 2], [0, 0], 0, 1]}]]},
                            'symbol': {
                                'type': 'CIMPolygonSymbol',
                                'symbolLayers': [solid_fill(rgb(78, 78, 78))],
                                'angleAlignment': 'Map'
                            }
                        }
                    ],
                    'respectFrame': True
                }
            ],
            'haloSize': 1, 'scaleX': 1, 'angleAlignment': 'Display'
        }
    }

    obj['renderer'] = r
    files[key] = dump_json(obj)

    save_zip(aprx, files)
    print("  Done: Tutorial 2-7")


# ============================================================
# TUTORIAL 2-8: VISIBILITY RANGES
# ============================================================

def fix_t28():
    aprx = BASE + 'Tutorial2-8FozhanBabaeiyan.aprx'
    files = load_zip(aprx)
    print("Fixing Tutorial 2-8...")

    # Scale values (approximate based on typical zoom levels):
    # West Village zoom (street level): ~1:4,800
    # Lower Manhattan zoom: ~1:75,000
    # Zoomed out to see boroughs: ~1:150,000
    WEST_VILLAGE_SCALE = 4800
    LOWER_MANHATTAN_SCALE = 75000
    BOROUGH_SCALE = 200000

    # -- ZoningLandUse: enable labels, set minScale on label class --
    key = 'new_york_city_zoning/zoninglanduse.xml'
    obj = parse_json(files[key])
    obj['displayAnnotation'] = True
    lc = obj.get('labelClasses', [])
    if lc:
        lc[0]['minimumScale'] = WEST_VILLAGE_SCALE
        # Remove maxScale if present
        lc[0].pop('maximumScale', None)
    files[key] = dump_json(obj)

    # -- Neighborhoods: enable labels, set maxScale, then turn OFF --
    key = 'new_york_city_zoning/neighborhoods.xml'
    obj = parse_json(files[key])
    obj['displayAnnotation'] = True
    obj['visibility'] = False  # Turn layer off at the end
    lc = obj.get('labelClasses', [])
    if lc:
        lc[0]['maximumScale'] = LOWER_MANHATTAN_SCALE
        lc[0].pop('minimumScale', None)
    files[key] = dump_json(obj)

    # -- Water: enable labels, set minScale (only show when zoomed in), turn OFF --
    key = 'new_york_city_zoning/water.xml'
    obj = parse_json(files[key])
    obj['displayAnnotation'] = True
    obj['visibility'] = False  # Turn layer off at the end
    lc = obj.get('labelClasses', [])
    if lc:
        lc[0]['minimumScale'] = LOWER_MANHATTAN_SCALE
        lc[0].pop('maximumScale', None)
    files[key] = dump_json(obj)

    # -- Boroughs: enable labels, set maxScale --
    key = 'new_york_city_land_use_school_study/boroughs.json'
    obj = parse_json(files[key])
    obj['displayAnnotation'] = True
    lc = obj.get('labelClasses', [])
    if lc:
        lc[0]['maximumScale'] = BOROUGH_SCALE
        lc[0].pop('minimumScale', None)
    files[key] = dump_json(obj)

    # -- Schools (facilities.json): already has minScale=75000 from template, keep it --
    # The tutorial also sets minScale on schools; the file already has it at 75000
    # which is the Lower Manhattan zoom level - correct behavior

    # -- World Light Gray Canvas Base: turn off visibility --
    # Find the UUID file that is the world light gray
    uuid_file = '0539b3ec33df49d18d3b6a9cc12eb70f.xml'
    if uuid_file in files:
        obj = parse_json(files[uuid_file])
        obj['visibility'] = False
        files[uuid_file] = dump_json(obj)

    save_zip(aprx, files)
    print("  Done: Tutorial 2-8")


# ============================================================
# CREATE SUBMISSION ZIP FILES
# ============================================================

def create_submission_zips():
    """Create submission ZIP files for each tutorial."""
    print("\nCreating submission ZIP files...")
    tutorials_dir = BASE
    gdb_path = os.path.join(tutorials_dir, 'Chapter2.gdb')
    index_path = os.path.join(tutorials_dir, 'Index')

    for t_num in ['1', '2', '3', '4', '5', '6', '7', '8']:
        aprx_name = f'Tutorial2-{t_num}FozhanBabaeiyan.aprx'
        aprx_path = os.path.join(tutorials_dir, aprx_name)
        zip_name = f'Tutorial2-{t_num}FozhanBabaeiyan.zip'
        zip_path = os.path.join(tutorials_dir, zip_name)

        if not os.path.exists(aprx_path):
            print(f"  Skipping Tutorial 2-{t_num}: .aprx not found")
            continue

        print(f"  Creating {zip_name}...")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add Chapter2.gdb (recursively)
            for root, dirs, fnames in os.walk(gdb_path):
                for fname in fnames:
                    fpath = os.path.join(root, fname)
                    arcname = os.path.relpath(fpath, tutorials_dir)
                    zf.write(fpath, arcname)

            # Add Index folder (recursively)
            if os.path.exists(index_path):
                for root, dirs, fnames in os.walk(index_path):
                    for fname in fnames:
                        fpath = os.path.join(root, fname)
                        arcname = os.path.relpath(fpath, tutorials_dir)
                        zf.write(fpath, arcname)

            # Add the .aprx file
            zf.write(aprx_path, aprx_name)

        zip_size = os.path.getsize(zip_path) / 1024 / 1024
        print(f"    Created: {zip_name} ({zip_size:.1f} MB)")

    print("  Submission ZIPs created!")


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print("=== Chapter 2 Tutorial Fix Script ===\n")

    # Kill ArcGIS Pro if running
    import subprocess
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'ArcGISPro.exe'], capture_output=True)
        print("Killed ArcGIS Pro processes")
    except:
        pass

    import time
    time.sleep(1)

    fix_t22()
    fix_t23()
    fix_t24()
    fix_t25()
    fix_t26()
    fix_t27()
    fix_t28()

    create_submission_zips()

    print("\n=== All done! ===")
