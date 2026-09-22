#!/usr/bin/env python3
"""
Generates standalone Reveal.js deck pages from per-section `slides.html`
fragments. The fragments (<deck>/sections/<slug>/slides.html) are the only
hand-edited source; every `index.html` this script writes is a build
artifact — edit the fragment and re-run this script, don't hand-edit the
output.

Each deck directory (e.g. `lab1-deck/`, `lab2-deck/`) needs a `deck.json`
describing its title and ordered section list:

    {
      "title": "Lab 2 — Backlog Audit & Your First Team Skill",
      "subtitle": "Claude Code Developer Enablement",
      "footer_suffix": "Day 1 · Lab 2",
      "sections": [
        { "slug": "01-backlog-and-skills", "title": "Backlog & Skills" }
      ]
    }

Usage: python3 build_deck.py [--deck <dir-name>] [--force]
  --deck    build only this deck (directory name under staging/, e.g.
            "lab2-deck"). Default: build every deck with a deck.json.
  --force   overwrite a generated file even if it was hand-edited since
            the last build (normally the script refuses and warns instead)
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

STAGING_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = Path(__file__).resolve().parent / ".build_manifest.json"
REVEAL_VERSION = "reveal.js-6.0.1"


def load_manifest():
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text())
    return {}


def save_manifest(manifest):
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True))


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def guarded_write(path, content, manifest, force):
    """Write `content` to `path`, refusing to clobber a hand-edited generated
    file unless `force` is set. Returns True if written, False if skipped."""
    key = str(path)
    if path.exists():
        on_disk = path.read_text()
        last_written_hash = manifest.get(key)
        if last_written_hash is not None and sha256(on_disk) != last_written_hash:
            if not force:
                print(f"  SKIP (hand-edited since last build): {path}")
                print(f"        re-run with --force to overwrite, or edit the source fragment instead")
                return False
            print(f"  WARNING: overwriting hand-edited file (--force): {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    manifest[key] = sha256(content)
    return True


def nav_bar(sections, section_index, deck_rel, staging_rel):
    """Build the cross-page nav bar: Main Menu | Prev | Next."""
    links = [f'<a class="section-link" href="{staging_rel}/index.html">Main Menu</a>']

    if section_index is not None:
        if section_index > 0:
            prev_slug = sections[section_index - 1]["slug"]
            links.append(f'<a class="section-link" href="../{prev_slug}/index.html">&larr; Prev Section</a>')
        if section_index < len(sections) - 1:
            next_slug = sections[section_index + 1]["slug"]
            links.append(f'<a class="section-link" href="../{next_slug}/index.html">Next Section &rarr;</a>')

    return '\n  '.join(links)


def rewrite_paths(fragment_text, staging_rel):
    return fragment_text.replace("__STAGING__", staging_rel if staging_rel else ".")


def render_shell(deck_name, title, footer_label, slides_html, staging_rel, deck_rel, sections, section_index):
    vendor = f"{staging_rel}/vendor/{REVEAL_VERSION}" if staging_rel else f"../vendor/{REVEAL_VERSION}"
    styles_href = f"{deck_rel}/styles.css" if deck_rel else "styles.css"

    return f"""<!-- GENERATED FILE — do not edit directly.
     Source: {deck_name}/sections/<slug>/slides.html
     Regenerate with: python3 scripts/build_deck.py --deck {deck_name} -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<link rel="stylesheet" href="{vendor}/reveal.css" />
<link rel="stylesheet" href="{vendor}/plugin/highlight/vscode-dark-modern.css" />
<link rel="stylesheet" href="{styles_href}" />
<style>
:root {{
  --deck-font-scale: 1;
}}
html {{
  font-size: calc(16px * var(--deck-font-scale));
}}
.slide-nav-bar {{
  position: fixed;
  bottom: 18px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 6px;
  z-index: 100;
  background: rgba(5,10,40,0.78);
  border-radius: 28px;
  padding: 6px 12px;
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,0.12);
}}
.slide-nav-arrow {{
  background: transparent;
  border: 1px solid rgba(255,255,255,0.28);
  color: rgba(255,255,255,0.8);
  width: 30px;
  height: 30px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  font-family: inherit;
  transition: background 0.15s;
}}
.slide-nav-arrow:hover {{
  background: rgba(255,255,255,0.12);
}}
.slide-nav-dots {{
  display: flex;
  gap: 0;
  align-items: center;
  transition: gap 0.3s ease;
}}
.slide-nav-bar:hover .slide-nav-dots {{
  gap: 4px;
}}
.slide-nav-dot {{
  max-width: 0;
  min-width: 0;
  height: 28px;
  overflow: hidden;
  opacity: 0;
  border-style: solid;
  border-width: 0;
  border-color: rgba(255,255,255,0.28);
  border-radius: 5px;
  color: rgba(255,255,255,0.5);
  background: transparent;
  padding: 0;
  cursor: pointer;
  font-size: 0.7rem;
  font-weight: 600;
  font-family: inherit;
  transition: max-width 0.3s ease, opacity 0.25s ease, border-width 0s, padding 0.3s ease;
}}
.slide-nav-dot.active {{
  max-width: 28px;
  width: 28px;
  opacity: 1;
  border-width: 1px;
  border-color: rgba(255,255,255,0.7);
  color: #fff;
  background: rgba(255,255,255,0.18);
}}
.slide-nav-dot.objectives {{
  border-color: #35b6c9;
  color: #35b6c9;
}}
.slide-nav-dot.objectives.active {{
  background: rgba(53,182,201,0.35);
  border-color: #35b6c9;
  color: #fff;
}}
.slide-nav-bar:hover .slide-nav-dot {{
  max-width: 28px;
  width: 28px;
  opacity: 1;
  border-width: 1px;
}}
.slide-nav-dot:hover {{
  background: rgba(255,255,255,0.1);
}}
.slide-font-controls {{
  position: fixed;
  right: 24px;
  bottom: 18px;
  display: flex;
  align-items: center;
  gap: 6px;
  z-index: 100;
  background: rgba(5,10,40,0.78);
  border-radius: 28px;
  padding: 6px 8px;
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,0.12);
}}
.slide-font-button {{
  background: transparent;
  border: 1px solid rgba(255,255,255,0.28);
  color: rgba(255,255,255,0.86);
  min-width: 36px;
  height: 30px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  line-height: 1;
  font-family: inherit;
  font-weight: 700;
  transition: background 0.15s;
}}
.slide-font-button:hover {{
  background: rgba(255,255,255,0.12);
}}
.slide-font-reset {{
  min-width: 48px;
  color: #35b6c9;
}}
</style>
</head>
<body>

<div class="section-links" aria-label="Section navigation">
  {nav_bar(sections, section_index, deck_rel if deck_rel else ".", staging_rel)}
</div>

<div class="reveal">
  <div class="slides">
{slides_html}
  </div>
</div>

<div class="slide-footer-label">{footer_label}</div>

<script src="{vendor}/reveal.js"></script>
<script src="{vendor}/plugin/notes.js"></script>
<script src="{vendor}/plugin/highlight.js"></script>
<script>
  (function() {{
    var savedScale = 1;
    try {{
      savedScale = parseFloat(window.localStorage.getItem('deck-font-scale')) || 1;
    }} catch (e) {{}}
    window.__deckFontScale = Math.min(Math.max(savedScale, 0.8), 1.6);
    document.documentElement.style.setProperty('--deck-font-scale', window.__deckFontScale.toFixed(2));
  }})();

  Reveal.initialize({{
    hash: true,
    center: false,
    width: 1920,
    height: 1080,
    margin: 0,
    minScale: 0.2,
    maxScale: 2.0,
    transition: 'none',
    controls: false,
    progress: false,
    slideNumber: false,
    plugins: [ RevealNotes, RevealHighlight ]
  }});

  // Adjust line numbers based on data-start attribute
  function adjustLineNumbers() {{
    document.querySelectorAll('code[data-start]').forEach(function(code) {{
      var startLine = parseInt(code.getAttribute('data-start'), 10);
      if (isNaN(startLine)) return;

      var table = code.querySelector('table[class*="hljs"]');
      if (!table) return;

      var rows = table.querySelectorAll('tr');
      rows.forEach(function(row, idx) {{
        var lineCell = row.querySelector('td:first-child');
        if (lineCell) {{
          var lineNum = startLine + idx;
          lineCell.textContent = lineNum;
        }}
      }});
    }});
  }}

  Reveal.on('ready', adjustLineNumbers);
  Reveal.on('slidechanged', adjustLineNumbers);

  (function() {{
    if (window.__slideNavInit) return;
    window.__slideNavInit = true;

    function buildNav() {{
      var slides = Reveal.getSlides();
      var objIdx = {{}};
      slides.forEach(function(s, i) {{
        var eyebrow = s.querySelector('.eyebrow');
        if (s.querySelector('[data-nav-objectives]') || (eyebrow && eyebrow.textContent.trim().endsWith('Learning Objectives'))) objIdx[i] = true;
      }});

      var bar = document.createElement('div');
      bar.className = 'slide-nav-bar';

      var prev = document.createElement('button');
      prev.className = 'slide-nav-arrow';
      prev.innerHTML = '&#8592;';
      prev.setAttribute('aria-label', 'Previous slide');
      prev.addEventListener('click', function() {{ Reveal.prev(); }});

      var dotsEl = document.createElement('div');
      dotsEl.className = 'slide-nav-dots';

      slides.forEach(function(_, i) {{
        var dot = document.createElement('button');
        dot.className = 'slide-nav-dot' + (objIdx[i] ? ' objectives' : '');
        dot.textContent = String(i + 1);
        dot.setAttribute('aria-label', 'Slide ' + (i + 1));
        dot.addEventListener('click', (function(idx) {{
          return function() {{ Reveal.slide(idx); }};
        }})(i));
        dotsEl.appendChild(dot);
      }});

      var next = document.createElement('button');
      next.className = 'slide-nav-arrow';
      next.innerHTML = '&#8594;';
      next.setAttribute('aria-label', 'Next slide');
      next.addEventListener('click', function() {{ Reveal.next(); }});

      bar.appendChild(prev);
      bar.appendChild(dotsEl);
      bar.appendChild(next);
      document.body.appendChild(bar);
      updateNav(Reveal.getState().indexh || 0);
    }}

    function updateNav(idx) {{
      document.querySelectorAll('.slide-nav-dot').forEach(function(d, i) {{
        d.classList.toggle('active', i === idx);
      }});
    }}

    Reveal.on('ready', function() {{ buildNav(); }});
    Reveal.on('slidechanged', function(e) {{ updateNav(e.indexh); }});
  }})();

  (function() {{
    if (window.__slideFontControlsInit) return;
    window.__slideFontControlsInit = true;

    var minScale = 0.8;
    var maxScale = 1.6;
    var step = 0.1;
    var scale = window.__deckFontScale || 1;
    var resetButton;

    function saveScale() {{
      try {{
        window.localStorage.setItem('deck-font-scale', scale.toFixed(2));
      }} catch (e) {{}}
    }}

    function applyScale() {{
      scale = Math.min(Math.max(scale, minScale), maxScale);
      document.documentElement.style.setProperty('--deck-font-scale', scale.toFixed(2));
      if (resetButton) resetButton.textContent = Math.round(scale * 100) + '%';
      saveScale();
      if (window.Reveal && typeof Reveal.layout === 'function') Reveal.layout();
    }}

    function addButton(parent, label, ariaLabel, onClick, className) {{
      var button = document.createElement('button');
      button.className = 'slide-font-button' + (className ? ' ' + className : '');
      button.type = 'button';
      button.textContent = label;
      button.setAttribute('aria-label', ariaLabel);
      button.addEventListener('click', onClick);
      parent.appendChild(button);
      return button;
    }}

    function buildControls() {{
      var controls = document.createElement('div');
      controls.className = 'slide-font-controls';
      addButton(controls, 'A-', 'Decrease slide text size', function() {{ scale -= step; applyScale(); }});
      resetButton = addButton(controls, '100%', 'Reset slide text size', function() {{ scale = 1; applyScale(); }}, 'slide-font-reset');
      addButton(controls, 'A+', 'Increase slide text size', function() {{ scale += step; applyScale(); }});
      document.body.appendChild(controls);
      applyScale();
    }}

    Reveal.on('ready', buildControls);
  }})();
</script>
</body>
</html>
"""


def discover_decks():
    return sorted(p.parent.name for p in STAGING_DIR.glob("*/deck.json"))


def render_root_index(deck_names):
    cards = []
    for deck_name in deck_names:
        config = json.loads((STAGING_DIR / deck_name / "deck.json").read_text())
        cards.append(f"""    <a class="deck-tile" href="{deck_name}/index.html">
      <div class="deck-tile-tag">{config.get('footer_suffix', '')}</div>
      <h3>{config['title']}</h3>
      <p>{config.get('summary', '')}</p>
    </a>""")

    return f"""<!-- GENERATED FILE — do not edit directly.
     Source: each deck's deck.json
     Regenerate with: python3 scripts/build_deck.py -->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Claude Code Developer Enablement — Deck Index</title>
<style>
  :root {{
    --navy: #070c33;
    --navy-deep: #050822;
    --teal: #35b6c9;
    --text: #f4f6fb;
    --muted: #b9c2dd;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{
    margin: 0;
    min-height: 100%;
    background: #000 url("./images/cognizant-background.png") center center / cover no-repeat;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    color: var(--text);
  }}
  .index-shell {{
    min-height: 100vh;
    padding: 6vh 6vw;
  }}
  .eyebrow {{
    text-transform: uppercase;
    letter-spacing: 0.18em;
    font-size: 0.95rem;
    color: var(--teal);
    margin-bottom: 0.6rem;
    font-weight: 600;
  }}
  h1 {{
    font-size: 2.4rem;
    margin: 0 0 2rem 0;
  }}
  .deck-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.1rem;
    max-width: 1200px;
  }}
  .deck-tile {{
    display: block;
    text-decoration: none;
    border: 1px solid rgba(255, 255, 255, 0.24);
    border-radius: 12px;
    background: rgba(6, 11, 42, 0.72);
    padding: 1.2rem 1.3rem;
    color: var(--text);
  }}
  .deck-tile:hover {{ background: rgba(53, 182, 201, 0.18); }}
  .deck-tile-tag {{
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-size: 0.72rem;
    color: var(--teal);
    font-weight: 700;
    margin-bottom: 0.4rem;
  }}
  .deck-tile h3 {{
    margin: 0 0 0.4rem 0;
    font-size: 1.1rem;
  }}
  .deck-tile p {{
    margin: 0;
    color: var(--muted);
    font-size: 0.92rem;
    line-height: 1.4;
  }}
</style>
</head>
<body>
<div class="index-shell">
  <div class="eyebrow">Claude Code Developer Enablement Program</div>
  <h1>All Decks</h1>
  <div class="deck-grid">
{chr(10).join(cards)}
  </div>
</div>
</body>
</html>
"""


def build_deck(deck_name, manifest, force):
    deck_dir = STAGING_DIR / deck_name
    config = json.loads((deck_dir / "deck.json").read_text())
    title = config["title"]
    subtitle = config["subtitle"]
    footer_label = f"{subtitle} · {config['footer_suffix']}" if config.get("footer_suffix") else subtitle
    sections = config["sections"]

    written, skipped = 0, 0

    fragments = []
    for s in sections:
        frag_path = deck_dir / "sections" / s["slug"] / "slides.html"
        if not frag_path.exists():
            print(f"ERROR: missing fragment {frag_path}", file=sys.stderr)
            sys.exit(1)
        fragments.append(frag_path.read_text())

    # Per-section standalone pages: sections/<slug>/ is 3 levels below staging/
    for i, s in enumerate(sections):
        staging_rel = "../../.."
        deck_rel = "../.."
        slides_html = rewrite_paths(fragments[i], staging_rel)
        html = render_shell(
            deck_name,
            f"{title} — {s['title']}",
            footer_label,
            slides_html,
            staging_rel,
            deck_rel,
            sections,
            section_index=i,
        )
        out_path = deck_dir / "sections" / s["slug"] / "index.html"
        if guarded_write(out_path, html, manifest, force):
            written += 1
        else:
            skipped += 1

    # Top-level full-deck page: <deck>/ is 1 level below staging/
    staging_rel = ".."
    deck_rel = "."
    all_slides = "\n".join(rewrite_paths(f, staging_rel) for f in fragments)
    html = render_shell(deck_name, title, footer_label, all_slides, staging_rel, deck_rel, sections, section_index=None)
    out_path = deck_dir / "index.html"
    if guarded_write(out_path, html, manifest, force):
        written += 1
    else:
        skipped += 1

    return written, skipped


def build(deck_arg=None, force=False):
    manifest = load_manifest()
    deck_names = [deck_arg] if deck_arg else discover_decks()
    if not deck_names:
        print("ERROR: no deck.json found under staging/", file=sys.stderr)
        sys.exit(1)

    total_written, total_skipped = 0, 0
    for deck_name in deck_names:
        print(f"Building {deck_name}...")
        written, skipped = build_deck(deck_name, manifest, force)
        total_written += written
        total_skipped += skipped

    # Root deck-index page — only regenerated on a full build (no --deck filter),
    # since it's meant to reflect every migrated deck, not just one.
    if not deck_arg:
        all_decks = discover_decks()
        print("Building root index...")
        html = render_root_index(all_decks)
        if guarded_write(STAGING_DIR / "index.html", html, manifest, force):
            total_written += 1
        else:
            total_skipped += 1

    save_manifest(manifest)
    print(f"\nDone: {total_written} file(s) written, {total_skipped} skipped.")
    if total_skipped and not force:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--deck", default=None, help="build only this deck (e.g. lab2-deck)")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    build(deck_arg=args.deck, force=args.force)
