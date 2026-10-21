# Website image delivery

Production uses commit-pinned jsDelivr URLs for the site's public image assets,
matching the Learn 2 Draw approach. Firebase retains the exact local files as
fallbacks; a failed HTML or SVG image switches to its local URL once. Responsive
images restore their full local srcset too. The small fallback listener is in the
document head, before image requests start. `ASSET_CDN=off npm run build` builds
the same page entirely on Firebase for troubleshooting.

The approved full-size lossless images, self-contained SVGs, artwork, colours,
layer registration and PNG masters are preserved. Smaller WebPs are exported
losslessly from resized PNG masters, with the originals still available as the
largest responsive candidates. The browser selects a size for the displayed
width and screen pixel density. Brand images remain SVGs; HTML img wrappers let
lower-page marks use native lazy loading, including without JavaScript.

Animation-only backgrounds are requested when their animation first runs.
No service worker precaches the collection. jsDelivr's immutable response headers
allow normal browser caching without an additional service-worker lifecycle.

The build removes unused images and source masters from **dist only**. It scans
generated HTML, JS, CSS and SVG references and keeps every referenced image,
including local fallbacks and responsive candidates. Files in public and the
design archive are never removed. Hosting release retention remains a separate
Firebase setting; this change does not delete old releases.

## Updating photographs

1. Preserve the approved PNG master and final lossless WebP per the design guide.
2. Run `python3 scripts/generate-responsive-images.py` (requires Pillow).
3. Build and check delivery in Safari and Chromium.
4. Commit and push the changed originals, delivery sizes, and responsive manifest.
   The production build automatically uses that new Git revision for changed or
   new assets. Unchanged assets keep their existing pinned URLs and browser cache.
5. Optionally run `node scripts/pin-asset-cdn.mjs` after an asset commit to record
   a new baseline. This is no longer necessary to publish changed images.

Builds refuse responsive sizes whose PNG master has changed, rather than
publishing outdated smaller copies. Uncommitted images use local preview URLs;
committed changes automatically get new immutable CDN URLs. Firebase fallbacks,
CSS images/masks and SVG braille use `?v=<content hash>` so replacing a filename
changes its browser cache key too. The fragment remains after the version query.
The HTML revalidates on reload and there is no site service worker. An already
open tab updates when reloaded; publishing does not replace its loaded document.

## Measurement, 21 October 2026

Chrome desktop, cache disabled, no scrolling. Single runs in the same browser
with DevTools open; third-party requests, consent and video can change totals.

| Site | Transferred | Requests |
| --- | ---: | ---: |
| Bureau, before this change | 22.94 MB | 42 |
| Bureau, after this change, desktop | 12.47 MB | 27 |
| Bureau, after this change, mobile 390 × 844 | 6.84 MB | 27 |
| Ion8 | 14.10 MB | 778 |
| Stanley UK | 6.55 MB | 773 |

These browser transfer figures supersede earlier estimates from summing file
references. Local preview transfer totals aren't directly comparable because
Vite's preview server does not provide the production CDN's compression.

The desktop reduction is 45.6%. After-change figures were measured on the live
custom domain after deployment f321979, with device emulation disabled for the
desktop comparison. Mobile is an additional measurement, not a comparison with
the desktop baselines. Counts are from the initial page load; scrolling and
later scene animations can request additional assets. Browser extensions were
present in all runs, so these are practical comparisons, not isolated lab scores.

Validation: production build, SEO and all nineteen collection checks passed;
CDN recovery was exercised for responsive and SVG images without retry loops;
all 140 pinned CDN assets returned HTTP 200. All 88 smaller image variants were
decoded and compared with the exact resized PNG master pixels. Chrome desktop
and 390 × 844 layout, plus Safari collection and enlarged crest, were inspected.
