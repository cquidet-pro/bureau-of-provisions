# Lid selector implementation handoff

Updated 2026-10-11. User wants a selector where visitors choose the lid they want, with visual previews of the current actual models. Implement in `/Users/cedric/code/bureau-of-provisions`, not the bottle-design repo. This handoff does not implement or deploy the selector.

## Source of truth

Design repo: `/Users/cedric/code/water-bottle-design`.
Only four current models remain in `output/waterbottle/`. Historical scripts and backups are archived; do not use them to regenerate the variants. The saved Blender files include later corrections absent from old builder scripts.

| Display name | Existing `cap_type` | Existing `cap_label` | Features | Blender source |
| --- | --- | --- | --- | --- |
| Straw & spout | `1` | `straw-and-spout` | Folding stainless straw + drinking spout; no mist | `waterbottle-cap-type-1-straw-and-spout.blend` |
| Straw only | `2` | `straw-only` | Folding stainless straw; no drinking spout or mist | `waterbottle-cap-type-2-straw-only.blend` |
| Spout only | `3` | `spout-only` | Drinking spout; no straw or mist | `waterbottle-cap-type-3-spout-only.blend` |
| Original / Straw, spout & mist | `4` | `straw-spout-mist` | All three functions | `waterbottle.blend` |

All four retain an air vent and the clear hinged hood. The air vent is not a selectable drinking feature.

Latest decisions:
- Types 1–3: long shoulder strap hidden. Original short straps and hardware retained.
- Type 1: user approved current appearance; no geometry revisions requested.
- Type 2: straw and silicone flex connector centered. Air vent stays at its original side position because a centered vent is blocked by the folded straw. Unused `V26 • clear backing for silicone web` is hidden in viewport and renders (last change). Vent-only seal, bridge and pad retained.
- Type 3: spout centered, vent centered, obsolete hole/crescent removed.
- Original model preserved. Do not modify it to match simplified variants.

## Available visuals

Absolute asset directory: `/Users/cedric/code/water-bottle-design/output/comparisons/`.

| Type | Full bottle PNG | Top PNG |
| --- | --- | --- |
| 1 | `type1-full.png` | `type1-top.png` |
| 2 | `type2-full.png` | `type2-top.png` |
| 3 | `type3-full.png` | `type3-top.png` |
| 4 | `original-full.png` | `original-top.png` |

These individual PNGs have transparent backgrounds. Full views: 800×1100; top views: 1000×1000. They are matching Blender Workbench previews, not photographic marketing renders. Open hood / angled straw pose, frame 14. Shoulder strap excluded for the comparison views only. Type 2 panels were refreshed after the unused lid backing was hidden.

Labeled overview sheets, same directory:
- `bottle-family-full-comparison.png` (3200×1320)
- `bottle-family-top-comparison.png` (4000×1280)

For the website, copy the eight individual PNGs into `public/images/lids/`, convert to suitably sized WebP while preserving alpha, and use relative browser URLs such as `/images/lids/type2-top.webp`. Do not reference absolute filesystem paths in the website. Prefer individual panels for the selector; the wide labeled sheets are review references. Keep output/comparisons scripts for provenance; do not put scripts into the website public directory.

## Existing website implementation

Verified local checkout: `/Users/cedric/code/bureau-of-provisions` (plural). Older design documentation mentions the singular path; that path is stale.

Existing uncommitted changes in `index.html`, `src/main.js`, `src/style.css` include a functional four-radio picker. Preserve and extend them; do not reset or overwrite unrelated edits.

- `index.html`, around line 91: `fieldset#cap-picker`, legend “Choose your cap”, four labeled radios (`name="cap_type"`, values `1`–`4`) with `data-label` values matching the table. Currently uses simple SVG diagrams.
- `src/style.css`, around line 630: `.cap-picker`, `.cap-options`, `.cap-option`, diagram and checked/focus styles.
- `src/main.js`, around line 53: picker state and Tally URL integration. `CAP_KEY = "bop_cap_type"` stores the selected value in localStorage. `?cap=3` supports preselection; URL value takes priority over localStorage. With neither, currently nothing is selected.
- `#cap-picker-status` is a polite live region. Existing “Recorded:” wording only means local selection, not a submitted response; change it to “Selected:” or a human-readable lid name.
- Tally iframe uses `https://tally.so/embed/5BW7JN` and appends `cap_type` / `cap_label`. When a visitor changes the selection, the current code reloads an already-loaded iframe. That may erase a partly completed form: account for this in the final flow.
- Fallback signup link currently points directly to `https://tally.so/r/5BW7JN`; it does not receive the selected lid parameters. Update this fallback too.

## Intended selector behavior

Keep the existing cream/burgundy visual style and existing site functionality. User wording is “pick the type of lid he wants”; describe a preference, not a vote about which product should be made first.

Recommended implementation:
1. Four clearly labeled options, using current rendered models instead of hypothetical SVG port positions.
2. A larger preview updates immediately when the visitor selects a lid; allow switching between full-bottle and top views without changing the selected lid.
3. Show the selected lid's human-readable name and short feature summary. Keep type numbers internal or secondary.
4. Preserve selection across refresh and existing deep links. Keep native radio semantics and keyboard/focus support. Give preview images useful alt text; announce selection changes without moving focus.
5. Carry the same stable ID/slug to signup, including the fallback link. Do not announce that a response was submitted merely because a radio changed.
6. Make the cards and preview work on mobile without horizontal overflow. Keep the rest of the gallery/dialog/city filters intact.

Do not invent pricing, included accessories, separate-lid purchase availability, launch dates, or compatibility promises. The selector can collect early-access preferences using the current signup flow without resolving sales details.

## Pending product decisions / signup configuration

Not specified by the user: default lid, whether lids are included choices or separately sold accessories, pricing, or whether selection should be mandatory. Preserve the existing no-default behavior unless the user decides otherwise; label the choice as a preference.

Design handoff says Tally hidden fields `cap_type` and `cap_label` need to be added. Their current dashboard state has not been verified. Repo code alone cannot establish that submissions store these fields. Verify configuration before claiming collection works. Do not send a test registration or deploy without authorization.

The Blender files are visual designs. Avoid adding unvalidated claims such as leakproof, dishwasher-safe, or certified food-safe.

## Validation and delivery

Run `npm run build` in the website repo. Use `npm run dev` for browser verification. Check desktop/mobile layout, all four choices and both preview angles, keyboard selection, reload persistence, valid/invalid deep links, and signup/fallback URLs. Check the iframe state behavior when changing lids after entering form data. No test form submission is needed to verify URL behavior.

Provide a local preview and summary before any publish step. Do not commit, push, or deploy as part of this handoff request.
