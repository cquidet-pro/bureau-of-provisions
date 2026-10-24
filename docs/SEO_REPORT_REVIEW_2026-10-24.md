# SEO Site Checkup review — 24 October 2026

Source: the owner's Downloads/seositecheckup.pdf (renamed from the extensionless download). The 28-page report records 79/100 SEO, 63/100 AI visibility, eight failures and four warnings. These are the report's scores, not new measurements. Its expanded image/resource lists were not included in the PDF.

## Findings and decisions

| Report finding | Resolution / review |
| --- | --- |
| Render-blocking resources — failed | Removed the Google Fonts stylesheet and its two external connection dependencies. Serve the same Fraunces and Inter Latin WOFF2 fonts locally, with their OFL licenses; inline only the small font-face declarations on the homepage, thank-you page and 404. Keep `font-display: swap`. |
| Keyword usage — failed | Keep the existing descriptive title and brand headline. Make the product summary explicit about a stainless steel **water** bottle, use steel bottle wording in the anatomy heading, and add a natural product-focused FAQ heading. Update description, Open Graph, Twitter and WebPage descriptions together. Do not stuff “register”, “order” or “selected” into headings because they occur in the repeated colour controls. |
| Responsive images — failed | Match collection `sizes` to the actual two/three/five-column grids and set a separate size for the enlarged registration clone. Retain the existing responsive lossless candidates. No source artwork was resampled or recompressed. |
| Image aspect ratios — failed | Checked every source WebP's actual dimensions against its HTML width/height: all agree. The report omits the flagged image list. Registered scene-restoration tiles deliberately occupy calibrated rectangles; changing them to `contain` would misalign the approved composite. Preserve them. Give the enlarged crest `object-fit: contain` so its viewport height cap cannot stretch the artwork. Full live-audit clearance remains unverified. |
| Google Analytics — failed | No analytics account/provider has been supplied. Do not add a fabricated tracking ID or introduce tracking to satisfy a scanner. This is an account decision, not a broken page feature. |
| CDN usage — failed | Existing assets use immutable jsDelivr URLs with versioned local fallbacks; Firebase Hosting already serves first-party HTML/JS/fonts through its CDN. Do not move every request to a second domain simply to satisfy detection heuristics. |
| Custom 404 — failed | Add a branded, responsive `public/404.html`, copied to the Hosting root by Vite, with home/collection links and `noindex, follow`. Keep the real missing-page response; do not add an SPA catch-all rewrite. Firebase serves this file for missing paths. |
| SPF record — failed | Requires the domain's actual authorised email service and DNS access. Leave DNS unchanged; adding a guessed SPF policy could break legitimate mail. Confirm the sender/provider before configuring. |
| Image alt — warning | Every image already has an alt attribute. Keep empty alternatives on decorative branding and restoration layers, hidden from accessibility directly or by their parent. Add a meaningful description to the enlarged crest in its dialog, where the artwork is the content being inspected. |
| Page objects — warning | A layered art-directed product scene legitimately has several requests. Preserve detail layers and exact vector branding. Keep lower-page photos/marks lazy and give hero restoration tiles low fetch priority so they compete less with the base scene. |
| LCP 3.84 seconds — warning | Add a high-priority responsive hero preload with exactly the image's generated src/srcset/sizes. Remove the font CSS round trip and improve image sizes as above. A new live mobile performance run is needed; no replacement LCP number or guaranteed score increase is claimed. |
| ads.txt — warning | The site is not configured to sell advertising. An invented authorised-seller file is inappropriate. Revisit only if ads are introduced. |

## Content recommendations

Restore six native HTML disclosure questions: materials, lid preferences, cleaning, colour-study audience, price/shipping and what registration means. Use the approved £39 price, international shipping and dishwasher-safe feature. Explain that registration takes no payment and that shipping charges/delivery dates have not been announced. Preserve the visible development status and nominal-CAD-capacity caveat. Link to the existing product sections; add the FAQ to llms.txt and update the sitemap's meaningful modification date.

The report asks for company/contact details, policies, safety evidence, testimonials and a launch timeline. These cannot be invented. Publish them when the owner provides verified details; no certification, customer review, delivery promise, warranty or returns terms were added. The report's “ingredients” recommendation is a generic template suggestion for this product. No FAQ rich-result eligibility or AI citation outcome is claimed.

## Self-review and verification

- Production build runs metadata/schema/canonical/crawler/asset checks, all nineteen edition checks, image/CDN recovery checks, cache-update regressions and DOM interaction checks.
- Extend SEO checks to require local inline font declarations and valid WOFF2 files on all three pages, working recovery links/noindex on the custom 404, no SPA catch-all rewrite, and exact agreement between hero preload and image candidates.
- Check source photo dimensions against their HTML declarations; all agree.
- Inspect the local production preview in Chrome at desktop and 320px device width. Verify native FAQ expansion and the 404 recovery links. Inspect browser console warnings; the observed warnings originate from the installed MetaMask extension, not site scripts.
- Source diff review preserves all approved image/vector bytes, strap prints, bottle geometry, the open ticket-window artwork and nineteen registration links. No third-party form was submitted.
- Firebase Hosting emulator verification passed: both `/missing-seo-review-page` and `/nested/missing-seo-review-page` return HTTP 404 with the branded recovery page; the homepage returns HTTP 200 with inline local font declarations; a WOFF2 request returns HTTP 200 with the configured immutable cache header.
- `npm run build` and `git diff --check` passed after the implementation and added regression checks.
- This change is local until deployed. After deployment, reconfirm the 404 response, rerun the external audit and measure LCP under a documented device/network profile.

## Primary references

- [Web font loading and rendering](https://web.dev/articles/font-best-practices)
- [Decorative image alternatives](https://www.w3.org/WAI/tutorials/images/decorative/)
- [Firebase custom 404 and Hosting response priority](https://firebase.google.com/docs/hosting/full-config)

The three font files are the Google Fonts Latin subsets of Fraunces normal (300–500), Fraunces italic (300–400), and Inter normal (400–600), fetched 24 October 2026. Their accompanying OFL notices are under public/fonts. Bump the versioned filenames when changing font bytes because the WOFF2 files have immutable cache headers.
