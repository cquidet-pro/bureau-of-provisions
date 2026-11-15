# Cutaway button steel correction / 15 November 2026

The user reported that the anatomy image's circular button appeared black.
The native polished steel material was correct, but the exploded button mesh
was absent from the dedicated reflection light's receiver collection. The
source button's light link does not propagate to the copied exploded mesh.

`scripts/render-v68/native-views.py` now includes the exploded button in that
collection and aims the existing reflection strip for the oblique cutaway
camera. Material, geometry, camera, edition colours and other views are unchanged.

Rendered one isolated full-resolution section proof to
`output/design-v68/button-steel-proof/assets/bottle-cutaway-native-v68.png`,
inspected it, and replaced only the cutaway master and its lossless delivery
variants. This is the requested selective section correction; no catalogue
batch was rendered and no new full-batch approval was recorded.
