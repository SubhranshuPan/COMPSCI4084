"""
Cut the NEW pages out of the PDFs in PDF_Print/ into three small print bundles
(Print_New_Pages/).  Every page gets a small stamp (top right) naming its
source document and page number so loose sheets slot into your old printouts.

Setup (once):  pip install pypdf
Run:           python make_print_extracts.py
"""
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (DecodedStreamObject, DictionaryObject, NameObject)

PACK = Path(__file__).resolve().parent.parent
SRC = PACK / "PDF_Print"
OUT = PACK / "Print_New_Pages"

# (source pdf, label, pages to take [1-based])
BUNDLES = {
    "Print_1_SQLite_T4_new_pages.pdf": [
        ("T4_SQLite", "T4 SQLite", [1] + list(range(10, 19))),
    ],
    "Print_2_Pandas_and_Matplotlib_T5_T6_new_pages.pdf": [
        ("T5_Pandas_NumPy", "T5 Pandas", [1] + list(range(5, 9)) + list(range(11, 16))),
        ("T6_Matplotlib", "T6 Matplotlib", [1] + list(range(6, 9)) + list(range(11, 15))),
    ],
    "Print_3_CheatSheet_v2_and_PyTorch_T7_new_pages.pdf": [
        ("Exam_Day_Cheat_Sheet", "CHEAT SHEET v2 (replaces v1)", [1, 2, 3, 4]),
        ("T7_PyTorch_Basics", "T7 PyTorch", [1] + list(range(6, 12)) + list(range(15, 18))),
    ],
}


def stamp(page, text):
    """Add a small Helvetica stamp in the top-right margin of a page."""
    w, h = float(page.mediabox.width), float(page.mediabox.height)
    text = text.replace("\\", "").replace("(", "[").replace(")", "]")
    stream = DecodedStreamObject()
    x = max(10, w - 16 - 3.7 * len(text))          # ~3.7 pt per character at 7 pt
    stream.set_data(f"BT /FStamp 7 Tf {x:.0f} {h - 16:.0f} Td ({text}) Tj ET".encode("latin-1", "replace"))
    font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                             NameObject("/Subtype"): NameObject("/Type1"),
                             NameObject("/BaseFont"): NameObject("/Helvetica")})
    res = page.get("/Resources")
    res = res.get_object() if res is not None else DictionaryObject()
    fonts = res.get("/Font")
    fonts = fonts.get_object() if fonts is not None else DictionaryObject()
    fonts[NameObject("/FStamp")] = font
    res[NameObject("/Font")] = fonts
    page[NameObject("/Resources")] = res
    old = page["/Contents"].get_object()
    old_data = old.get_data() if hasattr(old, "get_data") else b"".join(c.get_object().get_data() for c in old)
    merged = DecodedStreamObject()
    merged.set_data(b"q\n" + old_data + b"\nQ\n" + stream.get_data())
    page[NameObject("/Contents")] = merged


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for out_name, parts in BUNDLES.items():
        writer = PdfWriter()
        total = 0
        for stem, label, pages in parts:
            reader = PdfReader(SRC / f"{stem}.pdf")
            first = None
            for n in pages:
                page = reader.pages[n - 1]
                note = ("replaces old page 1" if n == 1 else "file BEHIND your old copy, in order")
                if stem == "Exam_Day_Cheat_Sheet":
                    note = "NEW VERSION: throw away the old cheat sheet"
                stamp(page, f"{label} - page {n} of {len(reader.pages)} - NEW: {note}")
                writer.add_page(page)
                if first is None:
                    first = len(writer.pages) - 1
            writer.add_outline_item(f"{label}  (pages {', '.join(map(str, pages))})", first)
            total += len(pages)
        writer.add_metadata({"/Title": out_name[:-4].replace("_", " ")})
        with open(OUT / out_name, "wb") as fh:
            writer.write(fh)
        print(f"{out_name}: {total} pages")
