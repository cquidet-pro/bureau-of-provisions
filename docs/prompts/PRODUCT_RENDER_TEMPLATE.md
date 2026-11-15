# Reusable product image workflow

Read `docs/PRODUCT_DESIGN_GUIDE.md` and `design/product-design.json` first. The current geometry authority is the V68 Blender file recorded there. Use `scripts/render-v68/` for bottle images; render its actual meshes rather than regenerating physical construction from a prompt.

## Colour-only studio variant

Create edition **{name}** by changing only the approved material values:
- body coating: {body_hex};
- collar coating: {accent_hex};
- one continuous woven strap: {strap_treatment}.

Keep the source dimensions, fixed camera, crop, lighting and geometry identical across all twenty-nine editions. Preserve the clear hood with integrated handle, compact rear hinge, round 13 mm button and slim surround, recessed folding straw, translucent seals, hourglass gulp spout and rear-centre cylindrical spray. Use the documented source frames for closed, open and raised-straw views.

The user's `docs/v68/SWIVEL_SNAP_HOOK_REFERENCE.png` governs the strap hardware: round opening jaw, tapered flat cast body, small curved lifting lever below it, short swivel stem, separate rounded rectangular D-ring and slim folded same-fabric stitched tab. Fit the jaw through the existing body recess around its bridge. Never pass metal through the bottle wall, add external lugs or substitute a wire oval. Export evaluated meshes and run the solid clearance check before batch rendering. See `docs/v68/hook-clearance.json` for the current depicted fit.

Preserve pristine finely woven fabric, tidy edges and the approved palette/stripes through the continuous strap route. No fraying, raised jacquard, dirt or thick patches. Exact BoP crest, both heraldic animals and braille remain website SVG layers; do not generate replacements. Only the two Fig. 03 lid-view tabs are unprinted.

Save high-resolution lossless PNG masters, then export lossless WebP once. Preserve source hashes and geometry fingerprints. Reject changes to physical features, proportions or edition geometry.

## Local finish correction

Change only **{specified_material_or_texture}** in the native rendering setup. Steel remains mirror-polished, silicone translucent and the hood clear. Preserve all other materials, geometry, camera, colours and exact vector artwork.

## Sectional anatomy

Section a copy of the actual native body and base; preserve the original model. Water must remain continuous to the curved inner floor. Show only source-supported connection geometry; do not invent screw turns absent from the source. Retain the exact body crest, braille and strap emblem as separate SVGs. The strap in this illustration is one flat cut section with a clean lower end and no return loop.

## Photographic scene repairs

Limit image generation to approved background repairs. Composite native product pixels over the clean plate, retain original scene details and verify their registration. Preserve the open mahogany/brass arched ticket window and lamp animation. Do not regenerate bottle hardware, character faces or hands as part of a product correction.
