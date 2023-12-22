# TODO: for excalidraw conversion:
# - copy SVG versions of the pictures
# - replace everywhere in the svg "Virgil, Segoe UI Emoji" => "Virgil GS"
# convert with
# inkscape --export-filename=<outfile>.pdf <infile>.svg

# for Pandoc 3, upgrade pandoc-fignos as explained:
# https://github.com/tomduck/pandoc-xnos/pull/29

import re
import yaml
import sys
from plumbum import local
from plumbum.path.utils import copy

VAULT_DIR = r"s:\SharedAppData\Obsidian\My Vault" + "\\"
MDFILES_PATH = VAULT_DIR + r"Projects\Amusing Programming\Modeling & Animation"
ATTACH_PATH = VAULT_DIR + r"attachments"
ZOTERO_BIB = r"s:\SharedAppData\Zotero\My Library.bib"
TPL_PATH = local.cwd / "book-src"
BOOK_OUTPATH = local.cwd / "book-prod"
FIGURES_OUTPATH = BOOK_OUTPATH / "Figures"

pandoc = local["pandoc"]
inkscape = local["inkscape"]
latexmk = local["latexmk"]


def convert_image(filename):
    with open(f"{filename}.svg", encoding="utf-8") as f:
        data = f.read()

    data = data.replace("Virgil, Segoe UI Emoji", "Virgil GS")

    fixed_svg = f"{filename}-f.svg"
    with open(fixed_svg, "w", encoding="utf-8") as ef:
        ef.write(data)

    inkscape(f"--export-filename={filename}.pdf", fixed_svg)


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

    matches = re.findall(r"<!-- {{ALT}}{(.+)} (.+) -->", data)
    with open(BOOK_OUTPATH / "alttext.md", "a", encoding="utf-8") as ef:
        for m in matches:
            ef.write(f"**{m[0]}** {m[1]}\r\n\r\n")


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
        "--biblatex",
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
local.path(BOOK_OUTPATH / "alttext.md").delete()
copy(TPL_PATH / "Nemilov.cls", BOOK_OUTPATH)
copy(ZOTERO_BIB, BOOK_OUTPATH / "biblio.bib")

metadata = read_metadata()

with local.cwd(MDFILES_PATH):
    for ch in metadata["frontmatters"] + metadata["mainchapters"]:
        convert_chapter(ch)

    pandoc(
        "Metadata.md",
        BOOK_OUTPATH / "alttext.md",
        "--template",
        TPL_PATH / "main-template.tex",
        "-o",
        BOOK_OUTPATH / "main.tex",
    )

if "-makepdf" in sys.argv:
    with local.cwd(BOOK_OUTPATH):
        latexmk("-pdf", "-shell-escape", "main.tex")
