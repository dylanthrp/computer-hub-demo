# The Computer Hub — design demo

**Showcase: https://dylanthrp.github.io/computer-hub-demo/**

**Independent working demo, not the final business website.** Contact details and the two business categories now use the user-supplied business-introduction screenshot. Opening hours remain unknown. See the dated update in the [source record](docs/SOURCES.md).

Source repository: https://github.com/dylanthrp/computer-hub-demo. The showcase is separate from the business domain. Preview disclosure and noindex remain enabled.

## Start

Python 3.11+ is sufficient; the public site has no runtime dependencies.

```sh
cd C:/Users/dylan/Documents/computer-hub-preview
python scripts/build.py
python scripts/serve.py
```

Open **http://127.0.0.1:4208/**. The server binds to loopback only and does not serve originals, content.json, scripts, tests, or docs. If 4208 is in use, use `python scripts/serve.py --port 4209` (do not stop an unrelated server).

You can also open `index.html` directly. It contains all public content as real HTML; navigation and contact links remain usable without JavaScript.

## Edit content

Edit **content.json**, then run `python scripts/build.py` and refresh. Do not edit generated index.html directly.

- `hero`: eyebrow, headline (`\n` creates a deliberate line break), description. Description also supplies SEO/social-description metadata.
- `facebook`: the exact owner-confirmed Facebook page URL.
- `phone`: confirmed object with `display` (human-readable number) and `e164` (international format with leading +). Header, hero, repair inquiry and contact section share this telephone destination.
- `email`: null or the approved email string.
- `website`: the business website URL confirmed in the supplied screenshot; separate from the demo publishing URL.
- `address`: null or an object with `display` and an HTTPS `directions` URL targeting the verified location.
- `hours`: empty array until verified; each entry has `day` and `time`. Use 12-hour AM/PM and explicitly state closed days only when confirmed.
- `offerings`: confirmed computer store and computer repair service categories only; each entry has `title` and one inquiry-focused `description`. Do not imply live inventory or guarantees.
- `about`: null or an object with `heading` and `description`, based only on confirmed facts. The section/nav link is omitted when null.
- `contact`: heading and short supporting copy.
- `promo`: editable eyebrow, heading, inquiry description, CTA label and `image` with webp/fallback paths, dimensions, illustrative alt text and caption. The CTA uses the shared phone field, not a second hardcoded number.
- `owner_note`: editable heading and description for the visually separate owner-facing design note.
- `photos`: empty until authentic approved photos are available. Up to four entries, each with local asset paths `webp` and `fallback` (JPEG/PNG), integer `width` and `height`, accurate `alt`, and optional `focus` such as `50% 40%`. Preserve originals in assets/originals; optimize web derivatives outside that folder. Use images sized for the actual frame (roughly 1200px wide is ample for most landscape hero images). One photo is static; two to four enable manual previous/next, keyboard arrows, count and touch swipe. No autoplay exists. Check each crop on phone and desktop before approving.

The supplied logo/banner remains in the header. A typing-photo crop from the supplied promotional graphic appears below the hero using 620 × 770 WebP/JPEG derivatives (`assets/typing-reference.webp` and `.jpg`). Its caption and alt text identify it as illustrative, not shop staff. No photo placeholders or fake slider are displayed; the shop-photo carousel stays inactive.

## Design / implementation

- Static HTML, custom CSS, small vanilla JS; Python build script, no backend.
- Supplied red/white identity, warm off-white canvas, charcoal inquiry panel, deep red accessible actions.
- Arial/Helvetica is an intentional locally available, compact and neutral retail type choice; no font downloads.
- Tokens at the top of assets/site.css; 1240px maximum content width, responsive gutters, 44px-or-larger controls.
- Existing text-led split hero, new photo-led repair inquiry, two confirmed business categories, contact section and a distinct owner-facing design note. Unsupported history, credentials, prices and turnaround promises remain absent.
- No tracker, third-party widget, analytics, form simulation, store cart, or external resource load.
- Preview disclosure and noindex remain enabled. Canonical, og:url, absolute social-preview image URL and business JSON-LD are withheld until production origin and business facts are approved. Text social metadata is present now.

## Checks

```sh
npm ci
npx playwright install chromium
python scripts/build.py
# Start the local server in another terminal, then:
npm test
python -m unittest discover -s tests -p 'test_*.py'
node --check assets/site.js
```

QA dependencies are development-only. If using another server port, set `BASE_URL` before npm test. `docs/qa-results.json` records actual browser results; screenshots are in `docs/screenshots/`. See docs/QA.md for limitations. The optional carousel is exercised in an isolated test fixture, not with invented business imagery.

## Prepare deployment — not authorization to publish

Run `python scripts/export.py` to create a **local** dist/ directory of public HTML/assets. It excludes originals, tests, project docs, node_modules and content source. This command does not deploy. Avoid manually adding private files inside assets; that folder is public by convention except originals.

The source is on `main`; GitHub Pages serves only the exported public files from the `gh-pages` branch root. Future releases must build/test the source, commit intended source changes, then publish the reviewed `dist/` contents to `gh-pages` and verify the live site. Do not publish originals or development files. Before an official business launch, complete the remaining checks in docs/SOURCES.md, obtain owner approval and hosting/domain authority, review image rights and content, then deliberately decide whether to remove preview disclosure/noindex and set production metadata. A listed website is not permission to change that domain.

Git excludes originals, screenshots, generated QA output, node_modules and dist. Supplied originals remain preserved locally. Run npm ci to restore development tooling. The earlier source ZIP is an archived initial preview, not this release.
