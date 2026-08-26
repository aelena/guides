# Guides

Short, opinionated technical guides, written once in Markdown and rendered to the
formats a reader or a storefront actually wants: a print-ready PDF, an EPUB, and
two cover images.

One pipeline serves every guide. A guide is a directory with a `guide.toml` and
one Markdown file per language.

## Guides in here

| Directory | Guide | Editions |
|---|---|---|
| `specs-driven-development/` | Spec-Driven Development | en, es |
| `prd-json/` | Writing a Solid prd.json | en, es |

## Building

WeasyPrint needs pango, cairo and harfbuzz. Those are not available natively on
Windows, so the build runs inside a container and `build.sh` is the entry point:

```bash
./build.sh                              # every guide, every edition
./build.sh specs-driven-development     # one guide
./build.sh prd-json --lang es           # one edition
```

Output lands in `dist/`, which is gitignored: it is generated, and a PDF in git
history is a PDF in git history forever.

On a machine that already has the system libraries, skip the container:

```bash
pip install -r requirements.txt
python build.py
```

Each edition produces four files:

```
dist/<slug>-<lang>.pdf
dist/<slug>-<lang>-cover.png          tall, for a product page
dist/<slug>-<lang>-cover-square.png   square, for a listing thumbnail
dist/<slug>-<lang>.epub
```

The square cover is cropped from the same render as the tall one rather than laid
out separately. That is what keeps the two from drifting apart.

## Adding a guide

1. Make a directory. Its name is only used to find it; the published name comes
   from `slug`.
2. Write the guide in Markdown. Level-two headings are the structure: each one
   starts a new page in the PDF and becomes a chapter in the EPUB. Number them
   (`## 3. Something`) and they appear in the contents page.
3. Add a `guide.toml`:

```toml
slug = "my-guide"
author = "Antonio Elena"

[[edition]]
lang = "en"
source = "my-guide.en.md"
title = "My Guide"
subtitle = "The line that goes under the title"
edition = "Draft, August 2026"
```

Add another `[[edition]]` block per language. `author` can be overridden per
edition; everything else in the block is required except `subtitle` and
`edition`.

## House style

`shared/style.css` is the one stylesheet, so a reader who buys two guides
recognises the second. A guide may put its own `style.css` beside its
`guide.toml`; it is appended after the shared one and therefore wins. That seam
exists from day one deliberately, because the alternative is that the first
guide with a typographic need of its own forks the whole pipeline.

Sizes are in millimetres and points. This is print.

## Conventions the sources follow

- No em dashes. They are the most reliable tell of generated prose, and these
  guides are sold on the assumption that a person wrote them. The SDD guide
  holds to this; `prd-json` was written before the rule and has seventy of
  them, so it is a convention going forward rather than a description of
  everything already here.
- `---` between sections is fine in the source; the stylesheet hides it, because
  a horizontal rule at the foot of a page looks like a mistake once every
  section already starts its own page.
- Two-column tables read better than definition lists and are styled for it.

## Not in version control

`_previous originals/` holds six corporate standards written at a former
employer. They are marked Confidential, carry that employer's name and name
colleagues, so they stay on disk as reference and out of git. `.gitignore`
enforces it.
