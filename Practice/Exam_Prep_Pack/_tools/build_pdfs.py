"""
Turn every Markdown file in Exam_Prep_Pack into a print-ready A4 PDF
(PDF_Print/ folder).  Uses Google Chrome in headless mode for the PDF step.

Setup (once):  pip install markdown pygments
Run:           python build_pdfs.py            (all files)
               python build_pdfs.py T4_SQLite  (only files whose name matches)
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

PACK = Path(__file__).resolve().parent.parent          # .../Exam_Prep_Pack
OUT = PACK / "PDF_Print"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: A4; margin: 14mm 13mm 16mm 13mm;
        @bottom-center { content: "Page " counter(page);
                         font: 8pt sans-serif; color: #555; } }
* { box-sizing: border-box; }
body { font: 10pt/1.38 -apple-system, "Helvetica Neue", Arial, sans-serif;
       color: #111; margin: 0; }
h1 { font-size: 20pt; margin: 0 0 4pt; border-bottom: 2.5pt solid #000;
     padding-bottom: 3pt; }
h2 { font-size: 13.5pt; margin: 14pt 0 5pt; background: #e8e8e8;
     padding: 3pt 6pt; border-left: 5pt solid #000; page-break-after: avoid; }
h3 { font-size: 11pt; margin: 10pt 0 3pt; border-bottom: 0.7pt solid #888;
     page-break-after: avoid; }
h4 { font-size: 10pt; margin: 8pt 0 2pt; page-break-after: avoid; }
p, li { orphans: 3; widows: 3; }
p { margin: 3pt 0 5pt; } ul, ol { margin: 2pt 0 5pt; padding-left: 17pt; }
li { margin: 1pt 0; }
code { font: 8.6pt "SF Mono", Menlo, Consolas, monospace;
       background: #efefef; padding: 0 2pt; border-radius: 2pt; }
pre { font: 7.9pt/1.32 "SF Mono", Menlo, Consolas, monospace;
      background: #f6f6f6; border: 0.8pt solid #999; border-left: 4pt solid #000;
      padding: 4pt 6pt; margin: 4pt 0 7pt; white-space: pre-wrap;
      word-break: break-word; }
pre code { background: none; padding: 0; font: inherit; }
table { border-collapse: collapse; margin: 4pt 0 8pt; width: 100%;
        font-size: 9pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th, td { border: 0.7pt solid #666; padding: 2pt 5pt; vertical-align: top; }
th { background: #dcdcdc; text-align: left; }
blockquote { margin: 5pt 0; padding: 3pt 8pt; border-left: 4pt solid #555;
             background: #f2f2f2; }
em { color: #222; } hr { border: 0; border-top: 0.8pt solid #777; margin: 8pt 0; }
.pb { page-break-after: always; height: 0; }
.highlight .k, .highlight .kn, .highlight .kd, .highlight .kr,
.highlight .kc, .highlight .nb, .highlight .ow { font-weight: bold; }
.highlight .c, .highlight .c1, .highlight .cm, .highlight .sd { color: #444;
                                                                 font-style: italic; }
.highlight .s, .highlight .s1, .highlight .s2, .highlight .sa { color: #000; }
.highlight pre { margin: 4pt 0 7pt; }
"""

EXTS = ["fenced_code", "tables", "sane_lists", "attr_list", "md_in_html",
        "codehilite"]
EXT_CFG = {"codehilite": {"guess_lang": False, "css_class": "highlight"}}


def md_to_html(text, title):
    body = markdown.markdown(text, extensions=EXTS, extension_configs=EXT_CFG)
    return (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>{title}</title><style>{CSS}</style></head>"
            f"<body>{body}</body></html>")


def build(md_path):
    OUT.mkdir(exist_ok=True)
    text = md_path.read_text(encoding="utf-8")
    html = md_to_html(text, md_path.stem.replace("_", " "))
    with tempfile.TemporaryDirectory() as tmp:
        html_file = Path(tmp) / "doc.html"
        html_file.write_text(html, encoding="utf-8")
        pdf = OUT / (md_path.stem + ".pdf")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                        "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", html_file.as_uri()],
                       check=True, capture_output=True, timeout=120)
    return pdf


if __name__ == "__main__":
    pattern = sys.argv[1] if len(sys.argv) > 1 else ""
    files = sorted(p for p in PACK.rglob("*.md")
                   if "_tools" not in p.parts and pattern in p.name)
    for f in files:
        print("building", f.relative_to(PACK), "->", build(f).name)
