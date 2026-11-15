# Add the approved strap system in the next Blender session

The reusable library is `design/blender-assets/v68-strap-system.blend`. It contains one collection, `BoP approved detachable strap V68`, with 21 accessory objects: two opening snap hooks, two separate D-rings, two folded stitched tabs and one continuous full-view strap. Neutral textile images are packed. No body, lid, camera, floor or light is included.

## Quick import

1. Open the authoritative V68 source in Blender: `../water-bottle-design/output/prototype-v68/Bureau-73mm-V68-2p2mm-Button-Surround-REVIEW.blend`.
2. In the Scripting workspace, open `scripts/render-v68/import-strap-asset.py` from this website checkout and Run Script. The script checks the native body fingerprint, refuses duplicate imports, appends the collection at its original world coordinates and does not save the source.
3. Inspect both recesses, the hooks and the full strap route. Save As a new source revision in the design repository after review. Do not overwrite the authoritative V68 file as part of this handoff.

Alternatively use File → Append → `v68-strap-system.blend` → Collection → `BoP approved detachable strap V68`. Append at the existing coordinates; do not move the origin, scale the collection or attach it to a collar lug. The script is preferred because it detects a changed body.

## Exact reference and fit

The user's full reference is `docs/v68/SWIVEL_SNAP_HOOK_REFERENCE.png`; the rendered close-up is `docs/v68/snap-hook-render.png`. Keep the round opening jaw, tapered flat body, curved lifting lever above, small flush rivet, short swivel, separate rounded rectangular D-ring and slim folded same-fabric tab. The jaw wraps the bridge through the special native recess; it does not pass through solid metal.

Coordinates use metres. Jaw centres are `(±0.0327, -0.001, 0.16395)`; centreline radius 0.0035 and section radius 0.00045. The separate D-ring is centred approximately `(±0.047, -0.001, 0.154)`. These are accessory setup dimensions, not published engineering specifications. Do not alter the native body to fit a mispositioned hook.

`docs/v68/hook-clearance.json` records all 16 metal parts checked against the evaluated native body: zero intersection, approximately 0.305 mm minimum depicted gap. This does not validate opening motion, manufacturing tolerances or load capacity. If geometry changes, refit against the new source and rerun the checks; do not bypass the import fingerprint assertion.

## Rebuild the library

Run Blender with the authoritative source and `--python-exit-code 1 --python scripts/render-v68/export-strap-asset.py`. It reconstructs the accessory from maintained native code and writes only the library; the source model is never saved. Before accepting a changed library, run `export-hook-clearance.py` in Blender followed by `check-hook-clearance.py` in the configured Python environment. Record an updated close-up and use the local proof page for explicit sign-off before batch images.

The library includes the long website strap concept as a separate visual accessory. If the next modelling task needs only the hooks, hide `WEB-One-continuous-strap` rather than deleting or silently redesigning it. Preserve one detachable strap, both release systems and exact artwork rules.
