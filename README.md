# Claude Code Developer Enablement — Reveal.js Decks

This folder holds the slide decks for the training program. Each `labN-deck/`
is a self-contained [Reveal.js](https://revealjs.com/) 6.0.1 presentation, and
`index.html` at the root is a menu linking to all of them.

- **`index.html`** — top-level deck menu (start here).
- **`lab1-deck/` … `lab8-deck/`** — one presentation per deck.
- **`shared/`** — CSS imported by every deck (`base.css`, `dark-theme.css`).
- **`vendor/reveal.js-6.0.1/`** — the Reveal.js library the decks load.
- **`scripts/build_deck.py`** — regenerates each deck's `index.html` from its slide sources.

---

## Quick start (launch locally)

The decks load Reveal.js, its plugins, and shared CSS through **relative paths**,
so they must be served over HTTP — opening a deck as a `file://` URL will break
the highlight/notes plugins and cross-deck navigation. Serve the whole `staging/`
folder with any static file server:

```bash
cd staging
python3 -m http.server 8000
```

Then open <http://localhost:8000/> in a browser. The menu links to every deck,
or you can jump straight to one, e.g. <http://localhost:8000/lab2-deck/index.html>.

Any static server works if you prefer — for example:

```bash
npx serve .        # Node
php -S localhost:8000
```

> **Note:** the decks reference `staging/vendor/reveal.js-6.0.1/`. If that folder
> is missing from your checkout, the slides will load unstyled. Download Reveal.js
> 6.0.1 and place it at `staging/vendor/reveal.js-6.0.1/` (it must contain
> `reveal.js`, `reveal.css`, and `plugin/highlight/` + `plugin/notes/`).

---

## Presenting

While a deck is open in the browser:

| Key | Action |
|---|---|
| `→` / `Space` | Next slide |
| `←` | Previous slide |
| `Esc` or `O` | Slide overview |
| `S` | Speaker view (current + next slide, notes, timer) |
| `F` | Fullscreen |
| `B` / `.` | Pause / black screen |

On-screen you also get a bottom navigation bar (arrows + numbered slide dots) and
`A-` / `100%` / `A+` font-size controls (persisted per browser).

---

## Editing slides

**Never hand-edit a deck's `index.html` — it is a generated build artifact.**

The source of truth for slide content is each deck's
`sections/<slug>/slides.html`. After editing a fragment, rebuild before the change
appears in the browser:

```bash
cd staging
python3 scripts/build_deck.py                 # rebuild all decks
python3 scripts/build_deck.py --deck lab2-deck # rebuild one deck
```

The build script reads each deck's `deck.json` (title, footer, ordered section
list) and stitches the section fragments into a standalone Reveal.js page. It
refuses to overwrite an `index.html` that was hand-edited since the last build —
pass `--force` to override, or (preferred) edit the source fragment instead.

See [AGENTS.md](AGENTS.md) for the full authoring conventions (shared CSS
architecture, Reveal.js fragment patterns, and the per-task skills under
`.claude/skills/`).

---

## Exporting to PDF

Use the `deck-pdf-export` skill at
[.claude/skills/deck-pdf-export/SKILL.md](.claude/skills/deck-pdf-export/SKILL.md).
It drives headless Chrome over the DevTools Protocol and waits for Reveal's
`pdf-ready` event before printing (a plain `chrome --print-to-pdf` only captures
the first slide).

---

## Deployment

Pushing to `main` triggers `.gitlab-ci.yml`, which assembles `staging/index.html`,
`images/`, `vendor/`, `shared/`, and each deck's generated files into a `public/`
directory and uploads it to the Azure static website. Because deployment ships the
**generated** `index.html` files, always run `build_deck.py` and commit the result
before pushing.
