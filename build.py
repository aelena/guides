#!/usr/bin/env python3
"""Render a guide to PDF, EPUB and two cover images.

One pipeline for every guide, driven by each guide's guide.toml. The mechanisms
are the ones already proven in the two book pipelines in this account: WeasyPrint
for the PDF, pypdfium2 to rasterise page one into a cover, Pillow for the square
crop that storefronts want, and ebooklib for the EPUB.

WeasyPrint needs pango, cairo and harfbuzz, which are not available natively on
Windows. Use build.sh, which runs this inside a container that has them.

Usage
    python build.py                      every guide, every edition
    python build.py specs-driven-development
    python build.py specs-driven-development --lang en
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHARED_CSS = ROOT / "shared" / "style.css"
DIST = ROOT / "dist"


@dataclass
class Edition:
    slug: str
    lang: str
    source: Path
    title: str
    subtitle: str
    edition: str
    author: str
    extra_css: str

    @property
    def stem(self) -> str:
        return f"{self.slug}-{self.lang}"


def load_editions(guide_dir: Path) -> list[Edition]:
    config_path = guide_dir / "guide.toml"
    if not config_path.exists():
        return []

    with config_path.open("rb") as handle:
        config = tomllib.load(handle)

    author = config.get("author", "")
    slug = config.get("slug", guide_dir.name)

    # A guide's own style.css is appended after the shared one, so it wins.
    own_css = guide_dir / "style.css"
    extra_css = own_css.read_text(encoding="utf-8") if own_css.exists() else ""

    editions = []
    for entry in config.get("edition", []):
        source = guide_dir / entry["source"]
        if not source.exists():
            raise SystemExit(f"{config_path}: no such source {entry['source']}")
        editions.append(
            Edition(
                slug=slug,
                lang=entry["lang"],
                source=source,
                title=entry["title"],
                subtitle=entry.get("subtitle", ""),
                edition=entry.get("edition", ""),
                author=entry.get("author", author),
                extra_css=extra_css,
            )
        )
    return editions


# --- Markdown -------------------------------------------------------------

def to_html(markdown_text: str) -> str:
    import markdown

    return markdown.markdown(
        markdown_text,
        extensions=["tables", "fenced_code", "sane_lists", "footnotes", "attr_list"],
        output_format="html5",
    )


HEADING = re.compile(r"^## +(.+?)\s*$", re.MULTILINE)


def sections(markdown_text: str) -> list[tuple[str, str]]:
    """Split at level-two headings, which is where a guide's structure lives.

    Anything before the first heading is the front matter and comes back under
    an empty title, so the caller can decide what to do with it rather than
    having it silently dropped.
    """
    matches = list(HEADING.finditer(markdown_text))
    if not matches:
        return [("", markdown_text)]

    out = []
    preamble = markdown_text[: matches[0].start()].strip()
    if preamble:
        out.append(("", preamble))

    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown_text)
        out.append((match.group(1).strip(), markdown_text[match.start() : end].strip()))
    return out


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# --- PDF ------------------------------------------------------------------

def cover_html(ed: Edition) -> str:
    return f"""<section class="cover">
  <h1 class="cover-title">{escape(ed.title)}</h1>
  {f'<p class="cover-subtitle">{escape(ed.subtitle)}</p>' if ed.subtitle else ''}
  <hr class="cover-rule" />
  <p class="cover-author">{escape(ed.author)}</p>
  {f'<p class="cover-edition">{escape(ed.edition)}</p>' if ed.edition else ''}
</section>"""


CONTENTS_LABEL = {"en": "Contents", "es": "Índice"}


def contents_html(ed: Edition, titles: list[str]) -> str:
    """A contents page built from the numbered sections.

    Only the numbered ones: a guide's front matter and its sources are not
    places anybody navigates to by number, and listing them makes the page
    harder to scan for the thing that is.
    """
    rows = []
    for title in titles:
        match = re.match(r"^(\d+)\.\s*(.+)$", title)
        if not match:
            continue
        rows.append(
            f'<li><span class="num">{match.group(1)}</span>{escape(match.group(2))}</li>'
        )
    if not rows:
        return ""

    label = CONTENTS_LABEL.get(ed.lang, "Contents")
    return (
        f'<section class="contents"><h2>{label}</h2><ol>' + "".join(rows) + "</ol></section>"
    )


def build_pdf(ed: Edition, parts: list[tuple[str, str]]) -> Path:
    try:
        from weasyprint import CSS, HTML
    except ImportError as err:
        raise SystemExit(
            "WeasyPrint is missing, or its system libraries are. "
            "On Windows use build.sh, which runs this in a container that has "
            f"pango and cairo. Original error: {err}"
        ) from err

    body = [cover_html(ed), contents_html(ed, [t for t, _ in parts if t])]
    body += [to_html(text) for _, text in parts]

    html = (
        f'<!doctype html><html lang="{ed.lang}"><head><meta charset="utf-8">'
        f"<title>{escape(ed.title)}</title></head><body>"
        + "".join(body)
        + "</body></html>"
    )

    css = SHARED_CSS.read_text(encoding="utf-8") + "\n" + ed.extra_css
    out = DIST / f"{ed.stem}.pdf"
    HTML(string=html).write_pdf(out, stylesheets=[CSS(string=css)])
    return out


# --- Covers ---------------------------------------------------------------

COVER_DPI = 200
INK_THRESHOLD = 250


def render_covers(ed: Edition, pdf_path: Path) -> list[Path]:
    """Rasterise page one, then crop a square from it.

    Storefronts show a square thumbnail in their listings and a tall one on the
    product page, so both get built. The square is cropped from the same render
    rather than laid out separately, which is what keeps the two identical.
    """
    import pypdfium2
    from PIL import Image

    document = pypdfium2.PdfDocument(str(pdf_path))
    page = document[0]
    image = page.render(scale=COVER_DPI / 72).to_pil().convert("RGB")

    tall = DIST / f"{ed.stem}-cover.png"
    image.save(tall)

    width, height = image.size
    grey = image.convert("L")
    ink = grey.point(lambda value: 255 if value < INK_THRESHOLD else 0).getbbox()

    side = min(width, height)

    if ink is None:
        # A blank first page. Centre the crop rather than failing: an ugly cover
        # is recoverable and a failed storefront upload at the wrong moment is not.
        box_top = (height - side) // 2
    else:
        ink_area = (ink[2] - ink[0]) * (ink[3] - ink[1])
        full_bleed = ink_area > 0.9 * width * height
        if full_bleed:
            box_top = (height - side) // 2
        else:
            # Centre the ink, nudged up an eighth. A typographic cover is mostly
            # white, so cropping from the top of the text leaves the whole square
            # bottom-heavy with nothing, and dead-centring reads slightly low:
            # optical centre sits above geometric centre.
            middle = (ink[1] + ink[3]) // 2
            box_top = middle - side // 2 - side // 8
            box_top = max(0, min(box_top, height - side))

    left = (width - side) // 2
    square = image.crop((left, box_top, left + side, box_top + side))
    square_path = DIST / f"{ed.stem}-cover-square.png"
    square.save(square_path)

    return [tall, square_path]


# --- EPUB -----------------------------------------------------------------

EPUB_CSS = """
body { font-family: serif; line-height: 1.5; }
h1, h2, h3 { font-weight: normal; line-height: 1.2; }
h2 { margin-top: 0; }
/* No background is set anywhere on purpose. A reader in night mode supplies
   its own, and a page that paints one while inheriting the reader's text colour
   is how an EPUB ends up black on black. */
code, pre { font-family: monospace; font-size: 0.9em; }
pre { padding: 0.6em; border: 1px solid rgba(128,128,128,0.35); white-space: pre-wrap; }
code { background: rgba(128,128,128,0.12); padding: 0 0.2em; }
blockquote { margin: 1em 0 1em 1em; padding-left: 0.8em;
             border-left: 3px solid rgba(128,128,128,0.4); }
table { border-collapse: collapse; width: 100%; font-size: 0.9em; }
th, td { text-align: left; padding: 0.35em 0.5em;
         border-bottom: 1px solid rgba(128,128,128,0.3); }
hr { display: none; }
"""


def build_epub(ed: Edition, parts: list[tuple[str, str]], cover: Path | None) -> Path:
    from ebooklib import epub

    book = epub.EpubBook()
    book.set_identifier(ed.stem)
    book.set_title(ed.title)
    book.set_language(ed.lang)
    book.add_author(ed.author)

    style = epub.EpubItem(
        uid="style", file_name="style/main.css",
        media_type="text/css", content=EPUB_CSS,
    )
    book.add_item(style)

    if cover and cover.exists():
        book.set_cover("cover.png", cover.read_bytes())

    chapters = []
    for index, (title, text) in enumerate(parts):
        name = title or ed.title
        chapter = epub.EpubHtml(
            title=name, file_name=f"chap_{index:02d}.xhtml", lang=ed.lang,
        )
        chapter.content = f"<h2>{escape(name)}</h2>{to_html(text)}" if not title else to_html(text)
        chapter.add_item(style)
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", *chapters]

    out = DIST / f"{ed.stem}.epub"
    epub.write_epub(str(out), book)
    return out


# --- Driver ---------------------------------------------------------------

def build(ed: Edition) -> None:
    print(f"  {ed.stem}")
    text = ed.source.read_text(encoding="utf-8")
    parts = sections(text)
    words = len(text.split())

    pdf = build_pdf(ed, parts)
    covers = render_covers(ed, pdf)
    epub_path = build_epub(ed, parts, covers[0])

    print(f"    {words} words, {len(parts)} sections")
    for path in [pdf, *covers, epub_path]:
        print(f"    {path.relative_to(ROOT)}  {path.stat().st_size // 1024} KB")


def guide_dirs(only: str | None) -> list[Path]:
    if only:
        path = ROOT / only
        if not (path / "guide.toml").exists():
            raise SystemExit(f"{only}: no guide.toml there")
        return [path]
    # Underscore-prefixed directories are working material, not guides.
    return sorted(
        d for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith((".", "_")) and (d / "guide.toml").exists()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("guide", nargs="?", help="directory name; default is all")
    parser.add_argument("--lang", help="build only this language")
    args = parser.parse_args()

    DIST.mkdir(exist_ok=True)
    built = 0

    for directory in guide_dirs(args.guide):
        editions = [
            ed for ed in load_editions(directory)
            if args.lang is None or ed.lang == args.lang
        ]
        if not editions:
            continue
        print(directory.name)
        for ed in editions:
            build(ed)
            built += 1

    if built == 0:
        print("Nothing to build. Check the guide name and --lang.")
        return 1
    print(f"\n{built} edition(s) built into {DIST.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
