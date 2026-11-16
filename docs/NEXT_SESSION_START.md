# Start the next product-image session here

Read `AGENTS.md`, `docs/PRODUCT_DESIGN_GUIDE.md` and `design/product-design.json`. The final approved choices are summarised in `docs/LOCAL_CORRECTION_REVIEW.md`. Do not replay historical rejected concepts or dark-lid experiments.

## Current source and baseline

- Native file: `../water-bottle-design/output/prototype-v68/Bureau-73mm-V68-2p2mm-Button-Surround-REVIEW.blend`; exact SHA is in `design/product-design.json`. Never save it from website scripts.
- Website geometry comes from native meshes. Full PNG masters and lossless WebP are under `public/images/product/`; responsive assets are generated from those masters.
- Final approved lid is the original previous-proof sharp transmission shader, not a physical smoked-glass trial. Button face is polished steel.
- Native accessory library: `design/blender-assets/v68-strap-system.blend`. Use the guarded importer in `docs/BLENDER_STRAP_HANDOFF.md` in the next modelling session.
- `/old/` is the immutable previous website. Unrelated untracked files must stay outside commits.

## Choose the smallest job

| Change | Work needed |
| --- | --- |
| Copy, label spacing, leaders, SVG positioning | Edit source, regenerate local review HTML, run relevant checks. No Blender render. |
| One edition's palette or material experiment | Set `BOP_EDITION_IDS` to that edition and `BOP_ASSET_OUT` / `BOP_EVIDENCE_OUT` to an isolated output folder. Never discover a new material across all 29 images. |
| Main scene only | `rebuild.py --part hero` |
| Cutaway only | `rebuild.py --part section` |
| Macro stills only | Run native-views.py in Blender with `BOP_VIEWS_PART=macro` and isolated output paths. Exports Flat, Up, pressed and closed without rendering the expensive main scene. |
| Shared geometry, camera, hardware or approved common finish | Review a small proof, record explicit sign-off, then full batch. |

Use `/tmp/bureau74-venv/bin/python` if that environment still exists, or create a new environment from `scripts/render-v68/requirements.txt`. Blender is `/Applications/Blender.app/Contents/MacOS/Blender`; install Node dependencies and `rsvg-convert`. `rebuild.py --help` checks prerequisites before expensive rendering.

### Approved Fig. 01 close-up correction / 15 November, evening

The user requested less white reflection on the spray head and a sharper recessed
straw. `native-views.py` now isolates the macro finish: 2176×2890 PNG, up to 128 adaptive samples,
no depth of field, narrower pixel filter and targeted light linking to reduce the spray-head reflections. The approved steel material, native geometry, fixed camera and
other image types are retained. `BOP_MACRO_STATES=up` renders just the raised
straw for the first visual proof; omit it to render all four macro states.

The reviewed assets and a before/after comparison are in
`output/design-v68/macro-sharp-proof/`. Cedric approved the proof and instructed “ok push it”. The approved finish is rendered in all four lid states; the dark thread is
removed from the five white/ivory strap editions and white main-scene/cutaway
tabs. Lossless deliveries and responsive sizes passed the full release checks. Preserve the logical
1088×1445 SVG coordinate space when delivering these higher-density images.
The 15 November approved release used `BOP_RENDER_DEVICE=CPU` after a Metal
command-buffer error. Latest user instruction, 16 November: next time try normal
GPU rendering first and compare speed. At the first error, crash or apparent
stall, stop the render work and diagnose it immediately before a retry or CPU
fallback; capture stdout/exit status and macOS crash/Metal logs. See
`docs/BLENDER_GPU_DIAGNOSTICS.md` for the separate sandbox launch failures,
shader-cache warnings and bounded GPU retests. White/ivory folded tabs also
omit the separate dark rectangular stitch border, per the same evening correction.

## Fast review loop

1. Render one affected image in isolation. Keep the approved camera and geometry unless the user requests a change.
2. Review it at actual display size with exact SVG branding. For straps, project the centre of each emblem onto the fabric centreline; placing its top anchor there creates an offset. A label and leader must share the same photo coordinate space. Check phone widths too.
3. Preserve sharp PNGs. Export lossless WebP after accepting the native render; a CSS or vector correction needs no new render.
4. Generate the proof with `BOP_REVIEW_OUT=<candidate-directory> node scripts/render-v68/review.mjs`. Serve with `npm run dev -- --port 4173`. Obtain explicit visual approval before a full batch; passing tests is not approval.
5. Record approval with the same `BOP_REVIEW_OUT` and `review.mjs --approve --reviewer Cedric` only after Cedric approves. Render the full batch through `rebuild.py`. It checks source dimensions, source integrity, hook intersection, fabric coverage and approval fingerprints; refreshes the packed Blender library and proof close-up; renders, exports responsive images and verifies all deliveries.
6. Inspect the collection contact sheet and special flag editions, lid states, main scene and cutaway. Run `npm run build`. Commit maintained scripts, design inputs, documentation, approval, evidence, masters and deliveries together; push the checked commit and verify Firebase's GitHub workflow and live content.

## Known limits

Automated checks validate geometry, registration constraints, image hashes and interactions; visual sign-off still decides appearance. Native mechanism travel is 220°, but photographed open covers are 90°. The user reviewed the local proof directly. `node scripts/check-browser-layout.mjs` now runs an optional real Chromium check of the lid component at exact desktop/phone viewports while Vite is on port 4173. Set BOP_CHROME if needed. Safari visual QA remains unperformed. Never claim wider browser coverage than was actually exercised.
