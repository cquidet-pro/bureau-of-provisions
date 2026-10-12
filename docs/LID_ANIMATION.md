# Interactive lid views

The Straw & spout, Straw only, and Straw, spout & mist cards use native horizontal range inputs. Each range scrubs individual Cycles-rendered WebP frames. These controls are siblings of the preference radios: scrubbing does not select a lid or reset registration.

The straw moves from the 45° drinking position to 180° folded flat, in 3° increments (46 frames). The mist lid continues for 14 more frames into the existing pump/spray animation, with the straw folded. The hood remains open throughout. Labels are SVG overlays whose leader endpoints are projected from the actual mesh positions for each frame.

Sources are the current saved Blender models in `/Users/cedric/code/water-bottle-design/output/waterbottle/`. The exporter changes camera, lighting, and materials in memory and never saves over the source files. It uses a warm studio backdrop and an edge-weighted clear hood material to reduce the large white softbox reflection. Packed branding textures are relinked to the retained PNG sources in the design archive; geometry is not regenerated from archived builders.

- Export: `scripts/render-lid-motion.py` (Blender background Python). Outputs PNG frames and geometry/annotation manifest to `/private/tmp/bop-lid-motion-clear/`.
- Convert: `scripts/convert-lid-motion.py` (Python + Pillow). Creates 152 WebP frames at 640 × 640 in `public/images/lids/motion-clear/`.
- Copy the export manifest to `public/images/lids/motion-clear/manifest.json` after rendering completes.

Static photographs remain fallback images. Frame preloading starts when controls are near the viewport; only displayed frames are explicitly decoded. Rapid dragging discards stale async requests. Keyboard arrows, Home, and End work through native range semantics; descriptive angle values are exposed to assistive technology. There is no automatic playback.

Local review only. No deployment, commits, or form submissions are included.

The mist card now uses `scripts/render-mist-motion.py` and `scripts/convert-mist-motion.py`: 60 frames in `public/images/lids/motion-spray45-beige/original/`. The camera orbits 45° to present the bottle clockwise, with lower framing to expose the spray nozzle. Water uses a refractive material, fine streams and additional animated droplets. Its projected annotations are merged into the shared manifest.

Spout only uses `scripts/render-spout-only.py` and `public/images/lids/type3-studio.webp`, rendered from its current Blender source with the same warm plain studio background, camera and tint as the other cards. Its label endpoint comes from the spout geometry.

The mist studio backdrop and lights orbit with the camera to maintain the same light beige background and product tint. Softboxes are hidden from glossy/transmission rays to avoid white rectangles in the clear hood. All card image frames use the same square CSS box and 640 × 640 image dimensions.

Spout-only seal verification: in the closed pose the drinking rim is at 201.0 mm, the silicone disk underside at 201.1 mm, and both share X=0, Y=-6 mm. The open view rotates the seal about the rear hinge; no geometry shift was made.
