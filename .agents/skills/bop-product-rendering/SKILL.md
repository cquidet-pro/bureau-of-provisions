---
name: bop-product-rendering
description: Render and update this repository's Bureau of Provisions bottle images from the approved native Blender meshes, including macro views, palettes, straps, scenes and cutaways. Use for website product-image corrections; physical model redesign belongs in the separate water-bottle-design repository.
---

# Native product imagery

Resolve paths from the repository root. Read `AGENTS.md`, `docs/NEXT_SESSION_START.md`,
`docs/PRODUCT_DESIGN_GUIDE.md` and `design/product-design.json` before appearance changes.
`PROJECT_TOOLS.md` describes portable setup and the separate source repository.

Use the native file and SHA in the manifest; never save that source from website
render scripts. Preserve exact hardware, palettes, vector branding and scene
registration. Use the maintained `scripts/render-v68/` pipeline and lossless PNG
masters; do not regenerate bottle hardware or edit from web exports.

Follow `docs/DESIGN_REVIEW_WORKFLOW.md`: render one affected view in isolated output,
obtain explicit visual sign-off, then record the approval and apply it to the
remaining affected images. Existing user approval covers the scope it actually
approved; passing tests is not visual approval.

Choose the smallest job. Copy, vectors and leaders need no Blender render.
Use `BOP_VIEWS_PART=macro` and `BOP_MACRO_STATES=up` (or `closed`, `flat`, `pressed`)
for individual lid states; `BOP_EDITION_IDS=9,12` limits catalogue editions.
`BOP_ASSET_OUT` and `BOP_EVIDENCE_OUT` keep candidates out of production.
See `docs/NEXT_SESSION_START.md` for commands and `rebuild.py --help` for batch parts.

Start on the normal GPU path and measure actual progress. At the first error,
crash or apparent stall, stop the render batch and investigate immediately.
Preserve stdout/stderr, exit status, settings, macOS crash/Metal logs and completed
masters before a retry or CPU fallback. Run one GPU job at a time. A time limit
alone does not prove a crash; check the process and partial outputs.
`docs/BLENDER_GPU_DIAGNOSTICS.md` records the known evidence and unresolved limits.
`BOP_RENDER_DEVICE=CPU` is an available fallback, not the default next attempt.

After authorised rendering: export lossless WebP once from the PNGs, regenerate
responsive sizes, run `verify-deliveries.py` and `npm run build`, and inspect the
changed views. Keep the maintained scripts, approval, accessory library, source
integrity/fit evidence and delivered images together. Preserve `/old/`; stage
only task files. Use the project release skill for an authorised push/deploy.
