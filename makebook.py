import yaml
from plumbum import local

FILES_PATH = r"s:\SharedAppData\Obsidian\My Vault\Projects\Amusing Programming\Modeling & Animation (vol 1)"
BOOK_PATH = local.cwd / "book"
pandoc = local["pandoc"]


def convert_chapter(ch):
    print(f"Converting '{ch}'")
    local.path(BOOK_PATH / ch).mkdir()

    pandoc(
        f"{ch}.md",
        "Metadata.md",
        "-M",
        f"title:{ch}",
        "--template",
        BOOK_PATH / "chapter-template.tex",
        "-o",
        BOOK_PATH / ch / f"{ch}.tex",
    )


with local.cwd(FILES_PATH):
    with open("Metadata.md", "r") as meta_file:
        meta = yaml.safe_load_all(meta_file)
        meta = next(meta)
        chapters = meta["chapters"]

    for ch in chapters:
        convert_chapter(ch)

    pandoc(
        "Metadata.md",
        "--template",
        BOOK_PATH / "main-template.tex",
        "-o",
        BOOK_PATH / "main.tex",
    )
