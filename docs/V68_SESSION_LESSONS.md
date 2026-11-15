# Faster, safer product-image updates

The 15 November 2026 session exposed workflow failures that written specifications alone did not prevent. Geometry was initially interpreted before native checks; an incorrect hook was repeated across the image set; a source pickup tube remained in the removed cutaway half; branding retained inappropriate old-view scale; and the scene product had too few pixels for its displayed size. Those errors required repeated renders and user corrections.

## Required sequence

1. Read AGENTS.md, PRODUCT_DESIGN_GUIDE.md and the manifest. Resolve the source revision and latest user corrections before interpreting photographs. Native bottle geometry is authoritative; a user-supplied accessory reference governs only that accessory.
2. Check tool access early. Browser inspection being unavailable must remain an explicit verification limit, not a claimed pass.
3. Use native geometry, with separate WEB-prefixed accessories. Prove source geometry unchanged; verify actual dimensions and solid accessory clearance before a render batch.
4. Review one neutral full bottle, hook detail, lid and cutaway before multiplying the correction across editions. Compare the actual reference: type, orientation, trigger position, placement inside the recess and component order. A zero-intersection result cannot prove visual fidelity to the reference.
5. Inspect at intended display size and pixel density. Lossless encoding does not guarantee sufficient resolution. Current scene product is genuinely rendered at 4608×3072, 128 samples; the historical background is scaled for composition and retains its separate original detail layers. Do not claim new background detail from enlargement.
6. Review all image-relative overlays after camera, geometry or crop changes. Measure branding relative to the bottle, not the frame. Keep leaders beside openings and on their intended target. Preserve exact crest supporters and SVG artwork.
7. Rebuild only affected outputs, then export losslessly from PNG masters and run the build guards. Copy edits, SVG leaders and CSS branding scale need no Blender render. A scene-only change uses `--part hero`; a cutaway-only change uses `--part section`.
8. Commit reproducible scripts, sources, final masters, delivery assets and proof records together. Keep rejected drafts and machine-local output outside the commit. Deploy only the checked commit and verify the deployment result.

## Human review remains necessary

Automated checks verify specified dimensions, source fingerprints, watertight solid fit, delivery pixels, resolution, presentation rules and website behaviour. They cannot establish that an interpretation matches a small reference photograph, that materials look convincing, or that a camera makes the construction clear. A small proof set is the visual gate; a full batch is the next step.

## Reproduction

See `NATIVE_V68_RENDERING.md` and run `python3 scripts/render-v68/rebuild.py --help`. The source Blender file remains in the sibling design repository; its exact path and hash are recorded in the manifest. Python dependencies are listed in `scripts/render-v68/requirements.txt`. The pipeline fails immediately on Blender Python exceptions or failed checks and never deploys automatically.
