# TODO: for excalidraw conversion:
# - copy SVG versions of the pictures
# - replace everywhere in the svg "Virgil, Segoe UI Emoji" => "Virgil GS"
# convert with
# inkscape --export-filename=<outfile>.pdf <infile>.svg

import re
import yaml
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


def convert_image(filename):
    with open(f"{filename}.svg", encoding="utf-8") as f:
        data = f.read()

    data = data.replace("Virgil, Segoe UI Emoji", "Virgil GS")

    fixed_svg = f"{filename}-f.svg"
    with open(fixed_svg, "w", encoding="utf-8") as ef:
        ef.write(data)

    inkscape(f"--export-filename={filename}.pdf", fixed_svg)

    # to_write = False
    # with open(filename, "w") as ef:
    #     for line in lines:
    #         if line.startswith("```"):
    #             to_write = False
    #         if to_write:
    #             ef.write(line)
    #         if line.startswith("```json"):
    #             to_write = True
    # ee = local["excalidraw_export.cmd"]
    # ee("--pdf", filename)


def copy_images(mdfile):
    with open(mdfile, encoding="utf-8") as f:
        data = f.read()
    # read all image names
    matches = re.findall(r"!\[.+\]\((.+\.excalidraw)\)", data)

    print(matches)
    with local.cwd(ATTACH_PATH):
        for m in matches:
            copy(f"{m}.svg", FIGURES_OUTPATH)
            with local.cwd(FIGURES_OUTPATH):
                convert_image(m)


def convert_chapter(ch):
    print(f"Converting '{ch}'")
    local.path(BOOK_OUTPATH / ch).mkdir()

    # chapter titles in metadata have dashes instead of spaces
    title = ch.replace("-", " ")

    copy_images(f"{title}.md")

    pandoc(
        f"{title}.md",
        "Metadata.md",
        "--wrap=preserve",
        # "--listings",
        "--shift-heading-level-by=-1",
        "-F",
        "pandoc-minted",
        "-F",
        "pandoc-fignos",
        "--biblatex",
        "-r",
        "markdown-auto_identifiers",
        "-M",
        f"title:{title}",
        "-M",
        "fignos-plus-name:Figure",
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
copy(TPL_PATH / "Nemilov.cls", BOOK_OUTPATH)
copy(ZOTERO_BIB, BOOK_OUTPATH / "biblio.bib")

metadata = read_metadata()

with local.cwd(MDFILES_PATH):
    for ch in metadata["frontmatters"] + metadata["chapters"]:
        convert_chapter(ch)

    # main production
    pandoc(
        "Metadata.md",
        "--template",
        TPL_PATH / "main-template.tex",
        "-o",
        BOOK_OUTPATH / "main.tex",
    )
