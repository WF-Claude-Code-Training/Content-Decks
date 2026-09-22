# Deck PDF Export (Reveal.js print-pdf)

**Purpose:** export a generated deck section (or the full deck) to a paginated PDF using
Reveal.js's built-in `?print-pdf` export mode, driven headlessly — no manual browser
print dialog, no puppeteer install.

**When to use this:** the user asks to convert a `day1-deck/sections/<slug>/index.html` (or
the top-level `day1-deck/index.html`) into a PDF handout.

**Prereqs:** macOS with Google Chrome installed at the standard app path, and Node 18+ on
`PATH` (Node 21+ ideally — the bundled script uses native `fetch` and `WebSocket`, no npm
install required).

---

## Why this can't be a one-line `chrome --print-to-pdf`

A naive `google-chrome --headless --print-to-pdf=out.pdf "file://...index.html?print-pdf"`
looks like it should work — Reveal.js reads `print-pdf` off the URL and switches into its
print layout. But Reveal's print layout is **asynchronous**: it takes several
`requestAnimationFrame` cycles to measure every slide, build a `.pdf-page` div per slide, and
reflow the whole deck into one tall stacked document before it's ready to be paginated by
the browser's print engine. Reveal dispatches a `pdf-ready` event on `window.Reveal` when
this is actually done.

The CLI `--print-to-pdf` flag prints as soon as the page's `load` event fires — well before
`pdf-ready`. In practice this captures only slide 1 (whatever partial DOM exists at that
moment), even with a generous `--virtual-time-budget`, because headless Chrome's
`requestAnimationFrame` doesn't reliably advance under virtual time.

**The fix:** drive Chrome over the DevTools Protocol (CDP) directly, inject a listener for
`Reveal.on('pdf-ready', ...)` before navigation, wait for it to fire, *then* call
`Page.printToPDF`. That's what `print_pdf.js` in this skill folder does — no puppeteer
needed, just Node's native `fetch`/`WebSocket` talking to Chrome's debugging port.

---

## Steps

1. **Kill any stray Chrome debug instance** on the port you're about to use (avoids
   colliding with a previous run):
   ```bash
   pkill -f "remote-debugging-port=9333" 2>/dev/null
   ```

2. **Launch headless Chrome** with remote debugging enabled and a scratch profile dir
   (use the session's scratchpad directory, not `/tmp`):
   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --headless=new --disable-gpu --no-sandbox \
     --remote-debugging-port=9333 \
     --user-data-dir="<scratchpad>/chrome-profile" \
     about:blank > "<scratchpad>/chrome.log" 2>&1 &
   sleep 2
   curl -s http://localhost:9333/json/version   # confirm it's up
   ```
   Use `--headless=new` (the modern headless mode), not legacy `--headless` — legacy
   headless has known issues suspending `requestAnimationFrame`, which is exactly the
   mechanism Reveal's print layout depends on.

3. **Run the export script**, pointing at the section's generated `index.html` with
   `?print-pdf` appended, and an absolute output path:
   ```bash
   node "staging/.claude/skills/deck-pdf-export/print_pdf.js" \
     "file:///absolute/path/to/day1-deck/sections/02-mindset-shift/index.html?print-pdf" \
     "/absolute/path/to/day1-deck/sections/02-mindset-shift/mindset-shift.pdf"
   ```
   The script waits for the `pdf-ready` console marker (up to 30s) before printing. If it
   times out it still prints after a fallback delay and logs a warning — treat that as a
   sign to check the page count afterward.

4. **Verify the page count** matches the number of `<section>` slides in the fragment
   (use PyMuPDF if available, it's more reliable than macOS `mdls` metadata, which can lag):
   ```bash
   python3 -c "
   import fitz
   doc = fitz.open('mindset-shift.pdf')
   print('pages:', doc.page_count)
   print('page size (pts):', doc[0].rect)
   "
   ```
   Page size should be the slide's configured width/height (from `build_deck.py`'s
   `Reveal.initialize({ width: 1920, height: 1080, ... })`) converted px→pt at 96dpi
   (1920×1080px → 1440×810pt). If page count is 1, the `pdf-ready` wait didn't work —
   don't fall back to a plain CLI print; debug the CDP script instead.

5. **Clean up** the Chrome process when done:
   ```bash
   pkill -f "remote-debugging-port=9333" 2>/dev/null
   ```

Spot-check a handful of rendered pages (first, middle, last) as images before calling the
export done — `doc[i].get_pixmap().save(...)` — rather than trusting page count alone.

---

## Gotcha: full-bleed backgrounds only showing on page 1

If the deck has a full-page background image set via CSS on `html, body` with
`background-size: cover`, it will render correctly on screen but **only appear on the first
printed page** of the PDF, with every subsequent page blank underneath.

**Root cause:** Reveal's print-pdf mode stacks every slide into one tall document (all
`.pdf-page` divs as vertical siblings) *before* Chrome slices it into pages. A `cover`-sized
background on `body` is sized relative to that one very tall box, not per printed page, so
it only visually lands on the first slice.

**Fix:** set the background on `.reveal-viewport` instead of `html`/`body`. Reveal's PDF
export code specifically reads `getComputedStyle(reveal-viewport).background` and copies it
as an inline style onto *each* generated `.pdf-page` div — so putting the background there
(rather than on `body`) makes every printed page carry its own correctly-scaled copy. This is
already how `day1-deck/styles.css` is set up (see the `.reveal-viewport` rule) — preserve
this pattern if a new deck introduces its own full-page background image.

Don't try to patch this with `.pdf-page { background: ... }` in your own stylesheet — Reveal
sets the background as an *inline* style on each `.pdf-page` div at export time, and inline
styles beat non-`!important` stylesheet rules, so a plain CSS rule targeting `.pdf-page` gets
silently overridden.
