# Website audit — 22 October 2026

## Changes

- Unified the header and final calls to action as “Register to pre-order”. The header now follows the same colour-choice and registration flow as the rest of the page.
- Explained beside registration that this is an expression of interest and no payment is taken.
- Added an announced loading state, a descriptive iframe title, and an always-available direct Tally link carrying the selected colour if the embed is unavailable.
- Locked background scrolling while the enlarged crest dialog is open.
- Applied the CDN, local fallback and content-versioned image handling to the thank-you page as well as the homepage.
- Added `nosniff` and a strict-origin cross-origin referrer policy on Hosting.
- Updated Vite from the vulnerable older build-tool dependency tree; retained the previous browser syntax targets. The npm registry audit reports zero known vulnerabilities.
- Aligned crawler copy with the current CAD dimensions, nominal capacity and registration process. Removed a stale diamond-weave description from Web Hero's alternative text and palette manifest, matching the plain-webbing design rule.
- Marked the older responsive report as historical: the current spray is one finite pump, with no Stop toggle.

## Verification

`npm run build` checks metadata, structured data, canonical URLs, crawler files, local asset references, anchors, nineteen collection entries, precise logo layers, responsive/CDN image delivery and fallback recovery. Cache regression checks use actual temporary Git commits to exercise unchanged, changed, new and uncommitted artwork.

The new `scripts/check-interactions.mjs` exercises the actual source event handlers in an offline DOM: all nineteen registration selections and direct links; one selected card and one form preview; change-selection behaviour; header CTA; six feature panels and Escape focus return; straw Flat/Up; gulp control visibility; finite spray completion and mode reset; reduced motion; crest close/focus; and duplicate IDs, accessible references, image alt attributes and iframe titles on both generated pages. Geometry and browser APIs are mocked, so these checks do not establish visual layout or full accessibility conformance.

Native Chrome review confirmed the desktop embedded registration and its selected colour, plus the 320×844 layout for the selected product and edge feature panel. No registration was submitted. Additional Safari/viewport review was interrupted when the native computer-use connection closed; this audit does not claim a completed new Safari or physical-device certification. Existing browser-safe SVG exports were preserved, with no artwork changes.

## Remaining external dependencies

Registration requires Tally. Image delivery prefers jsDelivr and automatically falls back to versioned local files. The existing no-cache HTML and immutable asset URLs remain in place to avoid stale releases. Company filtering is controlled by the employer or filtering vendor; changing crawler files does not remove that block. Its exact block reason has not been supplied.
