# Verification — Computer Hub showcase update

## Local release checks (2026-10-26)

- `python scripts/export.py`: PASS. Export consists only of index.html, .nojekyll, CSS, JS and four optimized image files; originals and development files excluded.
- `python -m unittest discover -s tests -p 'test_*.py'`: 7 tests PASS. Includes generated/source parity, screenshot-supported contacts/categories, repair promo and owner note, HTML escaping, optional photo counts, source image preservation and shared phone-field rendering.
- `npm test` / `node tests/browser.cjs`: PASS in Chromium 156.0.8078.4 at 320, 390, 768 and 1440 CSS pixels. Machine-readable local results read back from docs/qa-results.json.
- Phone destinations checked against the screenshot, including the repair-section Call the Shop button. Email, directions and Facebook destinations checked without sending messages or initiating calls.
- New typing image decoded at all four widths; intrinsic size 620 × 770. Both derivative files verified on disk, supplied original byte-matched, and OCR detected no residual promotional text in the photo crop.
- No horizontal overflow, JavaScript errors, missing assets, or unsolicited third-party resource requests in the tested local render.
- Navigation: mobile tap/click, expanded state, Escape focus return, in-page focus, skip link and desktop menu behavior PASS.
- Zero detected axe WCAG A/AA violations at each width. An incomplete contrast check remains a manual-review limitation; zero violations is not accessibility certification.
- Visible interactive targets checked at 44 × 44 pixels or larger.
- No-JavaScript navigation/content, reduced-motion preferences and 720px/scale-2 reflow PASS. Reflow is an emulation, not physical-device browser zoom.
- Optional manual carousel tested in an isolated fixture; the real site uses the single supplied promotional photo statically.
- JavaScript syntax and Python compilation PASS.

## Public release verification

The same browser suite supports `BASE_URL=https://dylanthrp.github.io/computer-hub-demo/`. Public deployment must be checked separately after pushing: confirm exported file identity and exercise the live page at its repository subpath. Local results above do not by themselves establish a deployed release.

## Evidence and limits

Screenshots are captured under docs/screenshots/ and machine-readable results under docs/qa-results.json; these generated files remain local and are not committed. Browser layout was assessed through geometry, image decoding and interaction checks. No pixel-viewing tool was available for a subjective screenshot review. Physical iOS/Android, Safari/Firefox and screen readers were not tested. No phone call, email, Facebook message, purchase or change to the business domain was made. No Lighthouse score or field performance claim is made.

Originals are retained locally under assets/originals/; see SOURCES.md and PHOTO-CROP.md for provenance, scope and remaining official-launch approvals.
