# V68 website images and Blender alignment

The website product images are rendered directly from `../water-bottle-design/output/prototype-v68/Bureau-73mm-V68-2p2mm-Button-Surround-REVIEW.blend`. The original model is never saved or changed by the render scripts. Generated product interpretations were rejected and are not used on the website.

## Physical checks

| Requirement | Source and verification |
| --- | --- |
| Handle on the lid | The actual `04-Hood` mesh, including its integral handle, appears closed in all 29 editions. |
| Recessed straw | Actual `13-Metal-mouthpiece`, fixed silicone and matching deck recess; frames 24 and 48 supply Flat and Up. Hidden obsolete bearings stay hidden. |
| New dimensions | Native bounds measure 73.0011 mm body diameter and 249.1000 mm closed height including the handle. Published nominal values are 73 mm and 249.1 mm. Body plus base is 179.5 mm. |
| Recessed strap position | The source `01-Body` recesses are preserved. The approved detachable strap illustration attaches here, below the collar; no collar lugs are added. |
| New button | The native 13 mm round face and V68 surround are retained. The surround and safety-loop sections are 2.2 mm. |
| Rear lid attachment | The current compact rear hinge is retained. Open views use the actual 220° source pose, with the handle folded behind the body. |

[Geometry fingerprints](v68/source-geometry-integrity.json) compare evaluated source vertices and polygon topology before and after appearance setup. [Measured bounds](v68/dimension-audit.json), [projected feature anchors](v68/view-anchors.json), the [strap recess](v68/strap-mount.png), and the [rear hinge](v68/hinge.png) provide independent review references. These checks verify source alignment, not manufacturing performance.

## Requested hook correction

The user supplied the [swivel snap reference](v68/SWIVEL_SNAP_HOOK_REFERENCE.png) on 15 November and explicitly rejected the oval wire-loop draft. All final images use a round-jaw snap with a flat tapered trigger body, small curved lifting lever below the body and flush rivet, short swivel and separate rounded D-ring. The source bottle recesses, body and lid are unchanged. [Native hook detail](v68/snap-hook-render.png). The jaw wraps the existing recessed bridge rather than intersecting the body. [Solid fit evidence](v68/hook-clearance.json) checks all sixteen metal parts against the evaluated native body: zero intersection on both sides and 0.305 mm minimum depicted clearance. This is a visual fit check, not a strength, manufacturing-tolerance or opening-motion certification.

## Rendering and artwork

The maintained pipeline is in `scripts/render-v68/`. All editions share the same source meshes, pose and camera; only material colours and vector-authored textile patterns change. The original exact browser-safe SVG crest, both supporters, strap animals and braille remain independent. Branding positions follow the new image registration. The two macro strap tabs remain unprinted.

The long detachable strap remains the previously approved website accessory concept, separate from the source bottle meshes. Its WEB-prefixed rendering objects do not modify the model. The anatomy view removes the spray pickup that lies wholly in the removed positive-X half, avoiding a false steel line through the water. It cuts copies of actual source surfaces and derives the water floor from the native interior; it does not invent threads absent from the model. The existing spray-press illustration translates the same native head mesh for the gesture without introducing extra parts.

The main scene retains its original people, open ticket window, registered detail layers and animations. Image generation is limited to a background clean plate. A local SVG mask confines that repair to the former product and plume; the replacement bottle itself is a native Blender render. The fine mist illustration begins at the actual projected spray outlet.

The main scene now uses an actual 4608×3072 native product render at 128 samples; only the retained historical background is enlarged during composition, with its original independent detail tiles still present. [Native lid detail](v68/main-lid-detail.png) shows the additional product detail.

Full [provenance](V68_IMAGE_PROVENANCE.json), [collection review sheet](v68/collection-contact.png), and final file hashes accompany the PNG/WebP masters. The production build checks all 29 editions, exact branding, registration links, cache updates and interaction states.

## Reproduction

Run Blender in background mode with the V68 file and `scripts/render-v68/native-studio.py` (`BOP_RENDER_MODE=catalogue`). Before rendering, use `export-hook-clearance.py` and `check-hook-clearance.py` to check the separately modelled hook against the actual body. Use `native-views.py` for the macro, station layer and section, then `compose-station.py` and `mist-overlay.py`. `strap-textures.py` exports the maintained SVG patterns with `rsvg-convert`. `export-webp.py` and `scripts/generate-responsive-images.py` create lossless deliveries directly from final PNG masters. Never feed a web export back into the rendering pipeline.

## Current verification status

The local production build passes, including all 29 editions, interactions and 35 pixel-identical lossless deliveries. Native masters and the collection contact sheet were inspected. Final browser visual review remains pending: desktop access returned `cgWindowNotFound` for Safari and Chrome, and the browser access host was unavailable. See [verification record](v68/website-verification.json). The update has not been published.

The complete command-line pipeline and explicit proof gate are documented in [design review workflow](DESIGN_REVIEW_WORKFLOW.md). The next-session Blender accessory is documented in [strap handoff](BLENDER_STRAP_HANDOFF.md).
