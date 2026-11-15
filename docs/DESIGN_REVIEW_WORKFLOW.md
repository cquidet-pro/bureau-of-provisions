# Proof, sign off, then render the collection

Use the current native source and the consolidated product guide. Never start a full catalogue to discover whether a new interpretation is correct.

## Commands

Install the Python dependencies from `scripts/render-v68/requirements.txt` in a virtual environment and activate it. Blender 5.3+, `rsvg-convert`, Node dependencies and the sibling design repository are required.

- `npm run design:proof`: render one neutral edition, hook close-up, main scene, half-cut, Flat/Up lid and pressed spray into `output/design-v68/review/`. Candidate images and evidence are isolated from production masters. The main-scene render retains full final resolution so sharpness can be judged.
- `npm run dev -- --port 4173`: serve the local review page at `http://localhost:4173/output/design-v68/review/`.
- `npm run design:review`: create the same review page from already completed masters without another Blender render. This is useful for CSS, vector placement, copy and current-state review.
- After explicit user sign-off only: `npm run design:approve -- --reviewer "Cedric"`. This records the review input and asset fingerprints in `design/render-approval.json`. The command records a human decision; it cannot make that decision. Do not run it just because tests pass or deployment is requested.
- `npm run design:render`: render all editions and image types, export, verify and build. It refuses a missing or stale sign-off receipt before starting the full batch.
- `python3 scripts/render-v68/rebuild.py --part hero` or `--part section`: selectively regenerate an authorised scene or cutaway correction. `--part views` regenerates the shared views; `--part catalogue` also requires current full-batch approval.

The scripts support `--source /path/to/source.blend` and `--blender /path/to/blender`. Update the manifest and references when changing the authoritative revision. Full source hashes and all physical checks must agree.

## Review page

Check the neutral bottle proportions, special recessed hook attachment and upper release lever, lid handle and 90° photographic opening, recessed straw poses, round button, cut boundaries and continuous water. Compare branding relative to the bottle, not the full frame. Keep both crest supporters, discreet catalogue braille, no anatomy braille, two unprinted macro tabs and all other exact prints. Check the small leader dots beside the openings and the carry leader on the strap. Inspect at desktop and phone sizes, including high-density display sharpness.

A correction invalidates the proof's input fingerprint. Regenerate the page and obtain fresh explicit approval before the full batch. Candidate assets changing after approval are also rejected when recording a receipt. No approval is inferred automatically and the scripts do not deploy.

The initial 15 November production update predates this proof gate and is not retroactively labelled as signed off. Its user-directed corrections and validation evidence are recorded separately. Future full batches must use this gate.

Generated previews are ignored machine-local outputs. Commit the maintained scripts, explicit approval receipt when one exists, final masters, delivery assets, design rules and proof records. See `V68_SESSION_LESSONS.md` for the reason for these gates and `BLENDER_STRAP_HANDOFF.md` for next-session modelling instructions.

Input fingerprints cover maintained rendering code, native source hash, palettes, authored flag/crest artwork, photographic backgrounds, masks, markup and styles. Generated cooling mist is a render output derived from native anchors and the maintained script; it must not invalidate its own batch approval when regenerated. Final PNG/WebP output hashes are verified separately. The test fixture isolates BOP_REVIEW_OUT from the calling shell.
