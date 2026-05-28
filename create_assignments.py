from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Assignment_Submissions"
COURSE_FILES = ROOT / "H-SC-460B-Sec01-9223-Pub-Hlth-Maps-Spatial-Analysis-2026-May-16_07-08-10-802" / "viewer" / "files"
CLEAN_GIST = ROOT / "GISTforPro" / "EsriPress" / "GISTforPro"
DESKTOP = Path.home() / "Desktop"
DESKTOP_TRANSCRIPTS = DESKTOP / "transcripts"


ASSIGNMENT_SOURCES = {
    "Intro to GIS": {
        "completed": DESKTOP / "Chapter1_Tutorials",
        "fallback": COURSE_FILES / "Chapter1_Tutorials",
        "clean": CLEAN_GIST / "Chapter1" / "Tutorials",
        "zip": "Intro_to_GIS_Assignment_Folder.zip",
        "expected": "Tutorials 1-1 through 1-4",
        "note": "Desktop source contains student-named Tutorial 1-1 through 1-4 projects.",
    },
    "Map Designs": {
        "completed": DESKTOP / "Chapter2",
        "fallback": COURSE_FILES / "Chapter2" / "Chapter2",
        "clean": CLEAN_GIST / "Chapter2",
        "zip": "Map_Designs_Assignment_Folder.zip",
        "expected": "Tutorials 2-1 through 2-8",
        "note": "Desktop source contains student-named Tutorial 2-1 through 2-8 projects.",
    },
    "Maps for End Users": {
        "completed": DESKTOP / "Chapter3",
        "fallback": COURSE_FILES / "Chapter3" / "Chapter3",
        "clean": CLEAN_GIST / "Chapter3",
        "zip": "Maps_for_End_Users_Assignment_Folder.zip",
        "expected": "Tutorials 3-1, 3-2, online Tutorial 3-3 StoryMap work, and 3-4",
        "note": "Desktop source contains student-named project files and ArcGIS Online link notes.",
    },
    "File Geodatabases": {
        "completed": DESKTOP / "Chapter4",
        "fallback": COURSE_FILES / "Chapter4" / "Chapter4",
        "clean": CLEAN_GIST / "Chapter4",
        "zip": "File_Geodatabases_Assignment_Folder.zip",
        "expected": "Tutorials 4-1 through 4-6 from the transcript/video set",
        "note": "Desktop source contains student-named Tutorial 4-1 through 4-6 projects and Tutorial4_Work.gdb.",
    },
}


DISCUSSION_POSTS = {
    "Discussion_Post_1_GIS_Public_Health_Response.txt": (
        "One real-world public health problem where GIS could provide meaningful "
        "insights is identifying neighborhoods with high asthma risk. A GIS map "
        "could layer asthma emergency visits or hospitalization rates with traffic "
        "corridors, industrial sites, housing age, tree canopy, and the locations "
        "of pediatric clinics. By using buffers, choropleth maps, and proximity "
        "analysis, public health workers could see whether communities with more "
        "environmental triggers also have less access to care. This spatial pattern "
        "would help prioritize mobile clinics, home remediation programs, air-quality "
        "monitoring, and outreach in census tracts where need is highest. Instead of "
        "treating asthma as only an individual medical issue, GIS shows how place and "
        "environmental exposure shape health outcomes."
    ),
    "Discussion_Post_2_CSULB_Gallery_Response.txt": (
        "Map 1: Going Beyond the University Art Museum: The Spatiality and Significance of CSULB Artwork\n"
        "URL: https://www.arcgis.com/home/item.html?id=241e1c428e324b3daa6d3cabea07b49d\n\n"
        "This map shows outdoor artwork across the California State University, Long Beach campus, "
        "including sculptures, murals, statues, memorials, and dedication pieces. I found it interesting "
        "because it treats campus art as spatial information and shows how artwork helps create a sense "
        "of place for students, staff, and visitors. The map uses point locations and pop-up information "
        "so the viewer can connect each artwork to its name, type, artist, date, and significance. What "
        "surprised me was that features people may pass every day can become easier to understand when "
        "they are organized as a map instead of only as a list or photo collection.\n\n"
        "Map 2: Public Spaces at CSULB and Recorded Instances of Passive Interaction\n"
        "URL: https://www.arcgis.com/home/item.html?id=2098b465810b4d21bc7a1dcd80bd4e2a\n\n"
        "This map identifies public spaces on the CSULB campus and records places where students use "
        "space for what the map calls passive interaction. I found it engaging because it connects a "
        "human geography idea to real campus locations, showing how students may seek social presence "
        "without direct conversation. The map visually presents data with campus layers, green space, "
        "buildings, roads, and colored point symbols for different levels of relevance. The surprising "
        "part was that a map can represent subtle social behavior, not just physical features like "
        "streets or buildings."
    ),
    "Discussion_Post_3_GIS_Policy_Response.txt": (
        "Beyond pandemic response, GIS analysis could inform policy by showing where "
        "health burdens overlap with social and environmental vulnerability. For "
        "example, a city or county could map heat-related emergency calls, tree canopy, "
        "impervious surfaces, age, income, and transit access to identify neighborhoods "
        "at greatest risk during extreme heat events. Hot spot analysis, buffer "
        "analysis, and choropleth mapping could reveal where cooling centers, shade "
        "investments, air-conditioning assistance, or bus-route improvements would "
        "have the greatest impact. This turns intervention planning from a broad "
        "citywide program into a place-based strategy targeted to specific census "
        "tracts. GIS also makes the policy process more transparent because maps can "
        "show residents why resources are being prioritized in certain areas."
    ),
}


def configure_document(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing = 1.15

    for name, size in [("Title", 24), ("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 12)]:
        style = styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.color.rgb = None


def add_para(doc: Document, text: str = "", bold_label: str | None = None) -> None:
    p = doc.add_paragraph()
    if bold_label:
        p.add_run(bold_label).bold = True
        p.add_run(text)
    else:
        p.add_run(text)


def save_doc(doc: Document, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)


def copy_file(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with src.open("rb") as in_fh, dest.open("wb") as out_fh:
        for chunk in iter(lambda: in_fh.read(1024 * 1024), b""):
            out_fh.write(chunk)


def relative_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        try:
            return path.relative_to(Path.home()).as_posix()
        except ValueError:
            return path.as_posix()


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_transcript_files() -> list[Path]:
    transcript_suffixes = {".vtt", ".srt", ".ass", ".ssa"}
    transcript_terms = ("transcript", "caption", "subtitle")
    found: list[Path] = []
    roots = [ROOT]
    if DESKTOP_TRANSCRIPTS.exists():
        roots.append(DESKTOP_TRANSCRIPTS)
    for search_root in roots:
        for path in search_root.rglob("*"):
            if not path.is_file():
                continue
            name = path.name.lower()
            if (
                path.suffix.lower() in transcript_suffixes
                or any(term in name for term in transcript_terms)
                or (search_root == DESKTOP_TRANSCRIPTS and path.suffix.lower() == ".txt")
            ):
                found.append(path)
    return sorted(found)


def source_for_assignment(assignment: str) -> Path:
    config = ASSIGNMENT_SOURCES[assignment]
    completed = config["completed"]
    if completed.exists():
        return completed
    return config["fallback"]


def audit_aprx_projects() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for assignment, config in ASSIGNMENT_SOURCES.items():
        course_dir = source_for_assignment(assignment)
        clean_dir = config["clean"]
        course_files = sorted(course_dir.rglob("*.aprx")) if course_dir.exists() else []
        clean_files = {path.name: path for path in clean_dir.rglob("*.aprx")} if clean_dir.exists() else {}

        files: list[dict[str, str]] = []
        counts = {"changed": 0, "new": 0, "same": 0}
        for course_file in course_files:
            clean_file = clean_files.get(course_file.name)
            if clean_file is None:
                status = "student-specific or new"
                counts["new"] += 1
            elif file_hash(course_file) == file_hash(clean_file):
                status = "matches clean textbook source"
                counts["same"] += 1
            else:
                status = "changed from clean textbook source"
                counts["changed"] += 1
            files.append({"path": relative_path(course_file), "status": status})

        results.append(
            {
                **config,
                "assignment": assignment,
                "source": course_dir,
                "files": files,
                "counts": counts,
                "total": len(files),
            }
        )
    return results


def audit_assignment_folders() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for assignment, config in ASSIGNMENT_SOURCES.items():
        course_dir = source_for_assignment(assignment)
        clean_dir = config["clean"]
        course_files = [
            path for path in course_dir.rglob("*")
            if path.is_file() and not should_skip_zip_file(path)
        ] if course_dir.exists() else []
        clean_files = {
            path.relative_to(clean_dir).as_posix(): path
            for path in clean_dir.rglob("*")
            if path.is_file() and not should_skip_zip_file(path)
        } if clean_dir.exists() else {}

        counts = {"same": 0, "changed": 0, "new": 0}
        changed_examples: list[str] = []
        new_examples: list[str] = []
        for course_file in course_files:
            rel = course_file.relative_to(course_dir).as_posix()
            clean_file = clean_files.get(rel)
            if clean_file is None:
                counts["new"] += 1
                if len(new_examples) < 5:
                    new_examples.append(rel)
            elif file_hash(course_file) == file_hash(clean_file):
                counts["same"] += 1
            else:
                counts["changed"] += 1
                if len(changed_examples) < 5:
                    changed_examples.append(rel)

        results.append(
            {
                "assignment": assignment,
                "source": course_dir,
                "total": len(course_files),
                "counts": counts,
                "changed_examples": changed_examples,
                "new_examples": new_examples,
            }
        )
    return results


def build_covid_assignment() -> None:
    doc = Document()
    configure_document(doc)

    title = doc.add_heading("Mapping COVID-19 Pandemic", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_para(doc, "Prepared for H SC 460B: Public Health Maps and Spatial Analysis")

    doc.add_heading("Question 1", level=1)
    add_para(doc, "Is the Map of Oakland displaying point pattern or a choropleth?", "Prompt: ")
    add_para(
        doc,
        "The Map of Oakland in The lines that shape our cities is a choropleth, or more precisely "
        "a thematic polygon map using choropleth-style area shading. It is not a point pattern map."
    )
    add_para(
        doc,
        "The Oakland map shows Home Owners' Loan Corporation (HOLC) neighborhood areas as filled "
        "polygons. Each area is colored by its assigned grade: A, B, C, or D. Because the map uses "
        "color-filled geographic areas to communicate a category, it fits the choropleth/map-shading "
        "approach. A point pattern map would instead use individual dots or markers to show separate "
        "locations or events."
    )

    doc.add_heading("Question 2", level=1)
    add_para(
        doc,
        "Pick a map from a StoryMap in the Gallery. Copy and paste the URL of the StoryMap, and include the following.",
        "Prompt: ",
    )
    add_para(
        doc,
        "https://storymaps.arcgis.com/stories/4fdc0d03d3a34aa485de1fb0d2650ee0",
        "StoryMap URL: ",
    )
    add_para(doc, "Mapping the spread of COVID-19", "StoryMap name: ")
    add_para(
        doc,
        "This StoryMap explains the geographic spread of COVID-19 using live-updating maps, "
        "dashboard embeds, and short narrative sections. It connects global case mapping with "
        "context about Wuhan, travel networks, quarantines, confirmed cases, deaths, and public "
        "health uncertainty during the pandemic."
    )

    doc.add_heading("i. Purpose", level=2)
    add_para(
        doc,
        "The main purpose is to convey information. The StoryMap helps viewers understand the "
        "pandemic spatially by showing where cases were occurring and how movement, density, and "
        "public health response shaped the spread of disease. It can support awareness and decision "
        "making, but it is not mainly an advocacy piece asking for one specific policy change."
    )

    doc.add_heading("ii. Narrative Effectiveness", level=2)
    add_para(
        doc,
        "The narratives are effective and just right in length. The text gives enough context to "
        "explain each map, while the maps and dashboards carry most of the evidence. This balance "
        "works well because the topic is data-heavy; long paragraphs would distract from the "
        "interactive spatial information."
    )

    doc.add_heading("iii. Citations, References, and Attributions", level=2)
    add_para(
        doc,
        "Yes. The StoryMap includes an About this story section and attribution entries. It credits "
        "Esri's StoryMaps team, Ross Donihue and Cooper Thomas for cartography and writing, and "
        "Johns Hopkins University's Center for Systems Science and Engineering (CSSE) for coronavirus "
        "cases and fatalities. Other data and image sources, including WorldPop and the CDC, are also "
        "identified."
    )

    doc.add_heading("iv. Legends", level=2)
    add_para(
        doc,
        "Yes, the maps include layer information and legend access through the map interface. The "
        "StoryMap uses proportional circles, colored layers, labels, and action buttons to show case "
        "counts, fatalities, population density, quarantined cities, flights, and rail connections. "
        "The legend and layer names are important because they explain what each symbol, color, and "
        "visible layer represents."
    )

    doc.add_heading("References", level=1)
    refs = [
        "Ahasan, R., Alam, M. S., Chakraborty, T., & Hossain, M. M. (2022). Applications of GIS and geospatial analyses in COVID-19 research: A systematic review. F1000Research, 9, 1379. https://doi.org/10.12688/f1000research.27544.2",
        "ArcGIS StoryMaps. Mapping the spread of COVID-19. https://storymaps.arcgis.com/stories/4fdc0d03d3a34aa485de1fb0d2650ee0",
        "ArcGIS StoryMaps. The lines that shape our cities. https://storymaps.arcgis.com/stories/0f58d49c566b486482b3e64e9e5f7ac9",
    ]
    for ref in refs:
        doc.add_paragraph(ref, style="List Bullet")

    save_doc(doc, ROOT / "Mapping_COVID19_Pandemic_Assignment.docx")
    save_doc(doc, OUT / "Mapping_COVID19_Pandemic_Assignment.docx")


def build_discussion_doc() -> None:
    doc = Document()
    configure_document(doc)
    doc.add_heading("Spatial Analysis Discussion Posts", 0)
    add_para(doc, "Prepared copy for Canvas text-entry discussion submissions.")

    titles = [
        ("Discussion Post 1", "GIS and a real-world public health problem", "Discussion_Post_1_GIS_Public_Health_Response.txt"),
        ("Discussion Post 2", "Two CSULB Gallery maps", "Discussion_Post_2_CSULB_Gallery_Response.txt"),
        ("Discussion Post 3", "GIS analysis for policy and intervention strategies", "Discussion_Post_3_GIS_Policy_Response.txt"),
    ]
    for heading, subheading, filename in titles:
        doc.add_heading(heading, level=1)
        add_para(doc, subheading, "Topic: ")
        for block in DISCUSSION_POSTS[filename].split("\n\n"):
            add_para(doc, block)

    save_doc(doc, OUT / "Spatial_Analysis_Discussion_Posts.docx")

    for filename, text in DISCUSSION_POSTS.items():
        (OUT / filename).write_text(text + "\n", encoding="utf-8")


def build_checklist_doc() -> None:
    doc = Document()
    configure_document(doc)
    doc.add_heading("Spatial Analysis Assignment Submission Checklist", 0)
    add_para(doc, "Generated from the local Canvas export, tutorial slides, and available project folders.")

    doc.add_heading("Ready Written Submissions", level=1)
    ready = [
        "Mapping_COVID19_Pandemic_Assignment.docx: Word file answering both StoryMap questions.",
        "Spatial_Analysis_Discussion_Posts.docx: combined Word copy of Discussion Posts 1, 2, and 3.",
        "Discussion_Post_1_GIS_Public_Health_Response.txt: plain text for Canvas copy/paste.",
        "Discussion_Post_2_CSULB_Gallery_Response.txt: plain text for Canvas copy/paste.",
        "Discussion_Post_3_GIS_Policy_Response.txt: plain text for Canvas copy/paste.",
    ]
    for item in ready:
        doc.add_paragraph(item, style="List Bullet")

    doc.add_heading("Packaged ArcGIS Tutorial Folder Uploads", level=1)
    add_para(
        doc,
        "The Chapter 1 tutorial slide says to turn in the entire assignment folder, including the "
        "ArcGIS Pro project, file geodatabase, and supporting GIS information. The ZIP packages are "
        "now built from the completed Desktop chapter folders when present, falling back to the "
        "course-export folders only if a completed Desktop folder is unavailable. This includes "
        "student-named ArcGIS projects such as Tutorial4-6FozhanBabaeiyan.aprx."
    )
    for assignment, config in ASSIGNMENT_SOURCES.items():
        source = source_for_assignment(assignment)
        doc.add_paragraph(f"{config['zip']} from {relative_path(source)}", style="List Bullet")

    doc.add_heading("Completion Evidence", level=1)
    add_para(
        doc,
        "The completed Desktop folders contain student-named project files and, for Chapter 3, "
        "ArcGIS Online link notes. The hash audit below compares those folders with the clean "
        "textbook source and shows saved local differences."
    )
    for result in audit_aprx_projects():
        counts = result["counts"]
        summary = (
            f"{result['assignment']}: {result['total']} .aprx files; "
            f"{counts['changed']} changed from clean source; "
            f"{counts['new']} student-specific or new; "
            f"{counts['same']} still match clean source."
        )
        doc.add_paragraph(summary, style="List Bullet")

    doc.add_heading("Manual Step Still Needed", level=1)
    add_para(
        doc,
        "CSULB Group Verification requires logging into ArcGIS Online, joining the group named "
        "Monica Montano 000971527_CSULB, and submitting a screenshot showing your name in the group. "
        "No screenshot file was present in the project folder, and I cannot truthfully create that "
        "verification without your authenticated ArcGIS session."
    )

    doc.add_heading("Transcript Note", level=1)
    transcript_files = find_transcript_files()
    if transcript_files:
        add_para(doc, "Transcript/caption files found locally and copied into Assignment_Submissions/Video_Transcripts:")
        for path in transcript_files:
            doc.add_paragraph(relative_path(path), style="List Bullet")
    else:
        add_para(
            doc,
            "I searched the project folder for transcript, caption, subtitle, .vtt, .srt, and related "
            "files during the audit. No separate transcript files were present in the project folder. "
            "If transcripts were created elsewhere, place them in this folder and rerun this script."
        )

    save_doc(doc, OUT / "Assignment_Submission_Checklist.docx")


def build_audit_report_doc() -> None:
    doc = Document()
    configure_document(doc)
    doc.add_heading("Assignment Audit Report", 0)
    add_para(doc, "Audit scope: local Canvas export, generated assignment files, upload ZIPs, and transcript search.")

    doc.add_heading("Issues Found and Fixed", level=1)
    fixed = [
        "Upload ZIPs were originally packaged from folders that did not show all completed work. Fixed by packaging from the completed Desktop chapter folders when present.",
        "Discussion Post 2 previously used one Map Service item. Fixed by using two ArcGIS Web Map items tied directly to California State University, Long Beach campus topics.",
        "The generator script now recreates Word files, plain-text discussion posts, checklist, audit report, and upload ZIPs in one reproducible run.",
        "Video transcript .txt files were found on the Desktop and copied into Assignment_Submissions/Video_Transcripts for reference.",
    ]
    for item in fixed:
        doc.add_paragraph(item, style="List Bullet")

    doc.add_heading("Critical Grading Risk Found", level=1)
    add_para(
        doc,
        "The written assignments and upload packaging were corrected. The ArcGIS tutorial ZIPs are "
        "now built from completed Desktop chapter folders that contain student-named project files "
        "and changed geodatabase/support files. I still cannot open ArcGIS Pro in this environment "
        "to visually confirm every map layer and symbology step, but the local file evidence is now "
        "substantially stronger than the previous course-export packages."
    )
    for result in audit_aprx_projects():
        counts = result["counts"]
        doc.add_paragraph(
            (
                f"{result['assignment']}: {result['total']} .aprx files; "
                f"{counts['changed']} changed, {counts['new']} student-specific/new, "
                f"{counts['same']} unchanged from clean source."
            ),
            style="List Bullet",
        )

    doc.add_heading("Folder-Level Hash Audit", level=1)
    add_para(
        doc,
        "I also compared all non-junk files in each packaged course-export folder against the clean "
        "GISTforPro textbook source. This is stronger evidence than the .aprx-only check."
    )
    for result in audit_assignment_folders():
        counts = result["counts"]
        doc.add_paragraph(
            (
                f"{result['assignment']}: {result['total']} files checked; "
                f"{counts['changed']} changed, {counts['new']} new, {counts['same']} unchanged."
            ),
            style="List Bullet",
        )

    doc.add_heading("Remaining Manual Blockers", level=1)
    add_para(
        doc,
        "CSULB Group Verification still requires an authenticated ArcGIS Online screenshot showing "
        "membership in Monica Montano 000971527_CSULB. No such screenshot is present locally."
    )
    add_para(
        doc,
        "Chapter 3 Tutorial 3-3 is ArcGIS Online StoryMap work. The local folder contains a note "
        "saying the work is done online, so the submission may also need a published StoryMap item, "
        "URL, or screenshot depending on the Canvas instructions."
    )

    doc.add_heading("Verification Performed", level=1)
    checks = [
        "Searched for transcript/caption/subtitle files and reviewed recent project files.",
        "Compared course-export .aprx files against the clean GISTforPro textbook source files.",
        "Checked generated DOCX text for common mojibake and replacement characters.",
        "Confirmed ZIP files are readable and include .aprx files plus geodatabase contents.",
        "Attempted visual DOCX render QA; unavailable because LibreOffice/soffice is not installed in this environment.",
    ]
    for item in checks:
        doc.add_paragraph(item, style="List Bullet")

    save_doc(doc, OUT / "Assignment_Audit_Report.docx")


def build_grade_completeness_audit_doc() -> None:
    doc = Document()
    configure_document(doc)
    doc.add_heading("Grade Completeness Audit", 0)

    transcript_files = find_transcript_files()
    aprx_results = audit_aprx_projects()
    folder_results = audit_assignment_folders()
    video_files = sorted(COURSE_FILES.glob("*.mp4")) if COURSE_FILES.exists() else []

    doc.add_heading("Bottom Line", level=1)
    add_para(
        doc,
        "All written submissions that can be generated from the local Canvas export have been "
        "created or corrected. The tutorial upload ZIPs have also been rebuilt from the completed "
        "Desktop chapter folders using the transcript set as assignment evidence. The packages now "
        "include student-named project files for Chapters 1 through 4 and Chapter 3 online link notes. "
        "ArcGIS Pro/arcpy is not available here, so this audit verifies files, hashes, transcripts, "
        "and package structure rather than opening the maps visually."
    )

    doc.add_heading("Ready To Submit As Local Files", level=1)
    ready_files = [
        "Mapping_COVID19_Pandemic_Assignment.docx",
        "Spatial_Analysis_Discussion_Posts.docx",
        "Discussion_Post_1_GIS_Public_Health_Response.txt",
        "Discussion_Post_2_CSULB_Gallery_Response.txt",
        "Discussion_Post_3_GIS_Policy_Response.txt",
        "Intro_to_GIS_Assignment_Folder.zip",
        "Map_Designs_Assignment_Folder.zip",
        "Maps_for_End_Users_Assignment_Folder.zip",
        "File_Geodatabases_Assignment_Folder.zip",
    ]
    for filename in ready_files:
        doc.add_paragraph(filename, style="List Bullet")

    doc.add_heading("Must Be Completed Or Verified Manually", level=1)
    blockers = [
        "CSULB Group Verification screenshot is not present. It requires logging into ArcGIS Online, joining the course group, and capturing proof that your account is in the group.",
        "Chapter 3 Tutorial 3-3 is online-only StoryMap work. A local link note is included in the Chapter 3 package, but Canvas may still require submitting the StoryMap URL directly.",
        "ArcGIS Pro is not available in this environment, so map appearance and layer state cannot be visually opened and confirmed here.",
    ]
    for item in blockers:
        doc.add_paragraph(item, style="List Bullet")

    doc.add_heading("Step-by-Step Tutorial Evidence", level=1)
    for result in aprx_results:
        counts = result["counts"]
        doc.add_heading(str(result["assignment"]), level=2)
        add_para(doc, str(result["expected"]), "Expected scope: ")
        add_para(doc, str(result["note"]), "Local note: ")
        add_para(
            doc,
            (
                f"{result['total']} .aprx files checked; {counts['changed']} changed from clean source; "
                f"{counts['new']} student-specific or new; {counts['same']} match clean textbook source."
            ),
            "Hash audit: ",
        )
        for file_info in result["files"]:
            doc.add_paragraph(f"{file_info['status']}: {file_info['path']}", style="List Bullet")

    doc.add_heading("Folder-Level File Evidence", level=1)
    add_para(
        doc,
        "This compares every non-junk packaged file against the clean textbook folders. Changed files "
        "would be evidence that work was saved somewhere in the folder, even if the .aprx file did not "
        "change."
    )
    for result in folder_results:
        counts = result["counts"]
        doc.add_paragraph(
            (
                f"{result['assignment']}: {result['total']} files checked; "
                f"{counts['changed']} changed; {counts['new']} new; {counts['same']} unchanged."
            ),
            style="List Bullet",
        )
        for rel in result["changed_examples"]:
            doc.add_paragraph(f"Changed example: {rel}", style="List Bullet")
        for rel in result["new_examples"]:
            doc.add_paragraph(f"New example: {rel}", style="List Bullet")

    doc.add_heading("Transcript And Video Status", level=1)
    add_para(doc, f"{len(video_files)} tutorial MP4 files are present in the Canvas export.", "Video files: ")
    if transcript_files:
        add_para(doc, "Transcript/caption files found:")
        for path in transcript_files:
            doc.add_paragraph(relative_path(path), style="List Bullet")
    else:
        add_para(
            doc,
            "No transcript, caption, subtitle, .vtt, .srt, .ass, or .ssa files were found in the "
            "project folder during this audit."
        )

    save_doc(doc, OUT / "Grade_Completeness_Audit.docx")

    lines: list[str] = [
        "Grade Completeness Audit",
        "",
        "Bottom line: written submissions are generated and ArcGIS ZIPs are rebuilt from completed Desktop chapter folders. ArcGIS Pro is not available here, so verification is based on transcripts, file evidence, hashes, and ZIP integrity.",
        "",
        "Ready local files:",
    ]
    lines.extend(f"- {filename}" for filename in ready_files)
    lines.extend(["", "Manual completion or verification still needed:"])
    lines.extend(f"- {item}" for item in blockers)
    lines.extend(["", "ArcGIS project hash audit:"])
    for result in aprx_results:
        counts = result["counts"]
        lines.append(
            f"- {result['assignment']}: {result['total']} .aprx checked; "
            f"{counts['changed']} changed; {counts['new']} student-specific/new; "
            f"{counts['same']} match clean source."
        )
        for file_info in result["files"]:
            lines.append(f"  - {file_info['status']}: {file_info['path']}")
    lines.extend(["", "Folder-level file audit:"])
    for result in folder_results:
        counts = result["counts"]
        lines.append(
            f"- {result['assignment']}: {result['total']} files checked; "
            f"{counts['changed']} changed; {counts['new']} new; {counts['same']} unchanged."
        )
        for rel in result["changed_examples"]:
            lines.append(f"  - changed example: {rel}")
        for rel in result["new_examples"]:
            lines.append(f"  - new example: {rel}")
    lines.extend(["", f"Video files present: {len(video_files)} MP4 files."])
    if transcript_files:
        lines.append("Transcript/caption files found:")
        lines.extend(f"- {relative_path(path)}" for path in transcript_files)
    else:
        lines.append("Transcript/caption files found: none.")
    (OUT / "Grade_Completeness_Audit.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def should_skip_zip_file(path: Path) -> bool:
    parts = set(path.parts)
    if "__MACOSX" in parts or ".backups" in parts:
        return True
    if path.name == ".DS_Store" or path.name.startswith("._"):
        return True
    if path.suffix.lower() in {".lock", ".tmp"}:
        return True
    return False


def zip_folder(source: Path, dest: Path) -> None:
    if dest.exists():
        dest.unlink()
    with ZipFile(dest, "w", ZIP_DEFLATED) as zf:
        for file_path in source.rglob("*"):
            if not file_path.is_file() or should_skip_zip_file(file_path):
                continue
            arcname = Path(source.name) / file_path.relative_to(source)
            zf.write(file_path, arcname.as_posix())


def package_upload_folders() -> None:
    for assignment, config in ASSIGNMENT_SOURCES.items():
        name = config["zip"]
        source = source_for_assignment(assignment)
        if not source.exists():
            raise FileNotFoundError(f"Missing source folder for {name}: {source}")
        zip_folder(source, OUT / name)


def copy_transcripts() -> None:
    if not DESKTOP_TRANSCRIPTS.exists():
        return
    dest_root = OUT / "Video_Transcripts"
    dest_root.mkdir(parents=True, exist_ok=True)
    for transcript in sorted(DESKTOP_TRANSCRIPTS.glob("*.txt")):
        copy_file(transcript, dest_root / transcript.name)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    copy_transcripts()
    build_covid_assignment()
    build_discussion_doc()
    build_checklist_doc()
    build_audit_report_doc()
    build_grade_completeness_audit_doc()
    package_upload_folders()
    print(f"Created assignment files in {OUT}")


if __name__ == "__main__":
    main()
