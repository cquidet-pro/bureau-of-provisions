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
3. Commit the changed originals, delivery sizes, and responsive manifest.
4. Run `node scripts/pin-asset-cdn.mjs`. This pins only bytes already in Git; it
   does not upload files. Commit the resulting design/asset-cdn.json as well.
5. Push both commits together so jsDelivr can resolve that immutable revision.
6. Run the build and check delivery in Safari and Chromium before publishing.

Builds refuse responsive sizes whose PNG master has changed. Modified CDN assets
stay local until repinned, rather than silently displaying older artwork.

## Measurement, 21 October 2026

Chrome desktop, cache disabled, no scrolling. Single runs in the same browser
with DevTools open; third-party requests, consent and video can change totals.

| Site | Transferred | Requests |
| --- | ---: | ---: |
| Bureau, before this change | 22.94 MB | 42 |
| Ion8 | 14.10 MB | 778 |
| Stanley UK | 6.55 MB | 773 |

These browser transfer figures supersede earlier estimates from summing file
references. Local preview transfer totals aren't directly comparable because
Vite's preview server does not provide the production CDN's compression.
