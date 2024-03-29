import re
import yaml
import sys
from plumbum import local
from plumbum.path.utils import copy

VAULT_DIR = r"s:\SharedAppData\Obsidian\My Vault" + "\\"
MDFILES_PATH = VAULT_DIR + r"Projects\PPP Modeling"
ATTACH_PATH = VAULT_DIR + r"attachments"
ABSTRACTS_PATH = MDFILES_PATH + "\\" + r"Chapter abstracts.md"
ZOTERO_BIB = r"s:\SharedAppData\Zotero\My Library.bib"
TPL_PATH = local.cwd / "book-src"
BOOK_OUTPATH = local.cwd / "book-prod"
FIGURES_OUTPATH = BOOK_OUTPATH / "Figures"
ALT_TEXT_PAGES = 4

pandoc = local["pandoc"]
inkscape = local["inkscape"]
latexmk = local["latexmk"]
pdftk = local["pdftk"]


def convert_image(filename):
    with open(f"{filename}.svg", encoding="utf-8") as f:
        data = f.read()

    data = data.replace("Virgil, Segoe UI Emoji", "Virgil 3 YOFF")

    fixed_svg = f"{filename}-f.svg"
    with open(fixed_svg, "w", encoding="utf-8") as ef:
        ef.write(data)

    inkscape(f"--export-filename={filename}.pdf", fixed_svg)
    local.path(f"{filename}.svg").delete()
    local.path(f"{filename}-f.svg").delete()


def copy_images(mdfile):
    with open(mdfile, encoding="utf-8") as f:
        data = f.read()
    # read all image names
    svg_matches = re.findall(r"!\[.*\]\((.+\.excalidraw)\)", data)
    png_matches = re.findall(r"!\[.*\]\((.+\.png)\)", data)

    print(svg_matches + png_matches)
    with local.cwd(ATTACH_PATH):
        for m in svg_matches:
            copy(f"{m}.svg", FIGURES_OUTPATH)
            with local.cwd(FIGURES_OUTPATH):
                convert_image(m)

        for m in png_matches:
            copy(m, FIGURES_OUTPATH)


def add_alt_text(title):
    with open(f"{title}.md", encoding="utf-8") as f:
        data = f.read()

    matches = re.findall(r"<!-- {ALT}{@(.+?)} (.+?) -->", data)

    with open(BOOK_OUTPATH / "alttext.tex", "a", encoding="utf-8") as ef:
        for m in matches:
            ef.write("\\textbf{\\ref{" + m[0] + "}} " + m[1] + "\r\n")


def make_xe_version(ch, title):
    with open(f"{title}.md", encoding="utf-8") as f:
        data = f.read()

    data = re.sub(r"<!--{xe:(.+?)}-->", r"\\index{\1}", data)
    with open(BOOK_OUTPATH / ch / f"{title}-xe.md", "w", encoding="utf-8") as ef:
        ef.write(data)


def convert_chapter(ch):
    print(f"Converting '{ch}'")
    local.path(BOOK_OUTPATH / ch).mkdir()

    # chapter titles in metadata have dashes instead of spaces
    title = ch.replace("-", " ")

    if "-skipfig" not in sys.argv:
        copy_images(f"{title}.md")

    make_xe_version(ch, title)
    add_alt_text(title)

    pandoc(
        BOOK_OUTPATH / ch / f"{title}-xe.md",
        "Metadata.md",
        "--wrap=preserve",
        "--shift-heading-level-by=-1",
        "-F",
        "pandoc-crossref",
        "-F",
        "pandoc-minted",
        "--natbib",
        "-r",
        "markdown-auto_identifiers",
        "-M",
        f"title:{title}",
        "-M",
        "codeBlockCaptions=true",
        "-M",
        "figPrefix=Figure",
        "-M",
        "lstPrefix=Listing",
        "-M",
        "tblPrefix=Table",
        "--template",
        TPL_PATH / "chapter-template.tex",
        "-o",
        BOOK_OUTPATH / ch / f"{ch}.tex",
    )


def read_metadata():
    with local.cwd(MDFILES_PATH):
        with open("Metadata.md", encoding="utf-8") as meta_file:
            meta = yaml.safe_load_all(meta_file)
            return next(meta)


### MAIN ###

local.path(FIGURES_OUTPATH).mkdir()
with open(BOOK_OUTPATH / "alttext.tex", "w", encoding="utf-8") as at:
    at.write("\\textbf{ALT TEXT}\r\n")
copy(TPL_PATH / "Nemilov.cls", BOOK_OUTPATH)
copy(ZOTERO_BIB, BOOK_OUTPATH / "biblio.bib")

metadata = read_metadata()

with local.cwd(MDFILES_PATH):
    for ch in metadata["frontmatters"] + metadata["mainchapters"]:
        convert_chapter(ch)

    pandoc(
        "Metadata.md",
        "--natbib",
        "--template",
        TPL_PATH / "main-template.tex",
        "-o",
        BOOK_OUTPATH / "main.tex",
    )

if "-makepdf" in sys.argv:
    print("building pdf")
    with local.cwd(BOOK_OUTPATH):
        latexmk("-c")
        latexmk(
            "-pdf",
            "-shell-escape",
            "-interaction=nonstopmode",
            "-file-line-error",
            "main.tex",
        )

        local.path("main.pdf").rename("main_f.pdf")
        pdftk("A=main_f.pdf", "cat", f"r{ALT_TEXT_PAGES}-r1", "output", "alttext.pdf")
        pdftk("A=main_f.pdf", "cat", f"1-r{ALT_TEXT_PAGES+1}", "output", "main.pdf")
        pandoc(ABSTRACTS_PATH, "-o", "abstracts.pdf")
        local.path("main_f.pdf").delete()
