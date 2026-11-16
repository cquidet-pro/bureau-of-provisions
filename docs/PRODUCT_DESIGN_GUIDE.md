# Bureau of Provisions — reusable product design guide

Version: 15 November 2026. Applies to website visuals, product studies, colour editions, prompts and future design work.

## Current geometry revision — V68

The November website update follows design thread `01a1dc0c-b9c7-7fa3-bade-ddc76ad6cf20` and the current model in `../water-bottle-design/output/prototype-v68/Bureau-73mm-V68-2p2mm-Button-Surround-REVIEW.blend`. See [migration specification](WEBSITE_V68_UPDATE.md). This supersedes the October geometry references and dimensions below wherever they disagree. Production images use the actual native meshes, as documented in [native rendering and alignment](NATIVE_V68_RENDERING.md). Previous photographs remain references for photographic finish, scene registration, straps and exact vector artwork only.

Current geometry: 73 mm body diameter, tapered shoulder, 179.5 mm body plus base, 20 mm collar, clear cylindrical hood with integrated rectangular carry handle and compact rear hinge (9.9 mm nominal projection). The closed envelope including handle is 249.1 mm. The native hood mechanism travels 220°; website open poses are photographed at 90°. A round 13 mm stainless push button replaces the old oval slotted latch; its 2.2 mm annular surround matches the slim safety loop section. Do not restore the older oval latch or upright flat circular hood.

The 27 mm stainless straw folds horizontally into a narrow deck recess, flush except for its rounded lifting paddle. It rotates to 135°, contacting a fixed translucent silicone interface. There are no old raised external bracket cheeks or long side-seat recesses. The hood's drinking and vent seals are two independent translucent silicone pads; no connecting bridge or long sealing arm. Preserve the rear-centre spray and hourglass gulp spout. All colour editions use the same current geometry, including collar, shoulder, hood, button and recessed straw. Only the palette and approved strap pattern vary.

All existing strap, quality, branding, cutaway, scene, interaction and edition rules below continue to apply. Recalibrate view-specific branding, leaders and spray coordinates to the new accepted photographs; old coordinates are not geometry authority.

This is the **current specification**. It consolidates the user's approved corrections; it is not a history of every experiment. Earlier interpretations are archived in [PRODUCT_DESIGN_HISTORY.md](PRODUCT_DESIGN_HISTORY.md). Machine-readable rules and all twenty-nine edition palettes are in [product-design.json](../design/product-design.json).

## 1. Source hierarchy

1. The user's latest explicit instruction takes precedence.
2. Current V68 Blender geometry governs physical construction. Use [full open reference](v68/full-open.png), [macro reference](v68/lid-open.png) and [raised straw reference](v68/lid-raised.png). October screenshots are historical references.
3. Approved finished renders govern materials, lighting and visual treatment. They do **not** override Blender geometry.
4. This guide, the palette manifest and render prompt template apply to all new work.
5. Superseded generated images are not product references. A different camera, colour or audience is never permission to invent hardware.

Reference renders: `platform-native-v68.webp`, `lid-native-v68.webp`, `bottle-cutaway-native-v68.webp`, all under `public/images/product/`. The collection uses direct V68 native renders with one fixed camera/pose and the edition material palettes listed in the manifest.

## 2. One product; fixed construction

- Preserve the tall, slim body, shoulder, base, collar diameter and proportions. Every collection image has the same scale, camera, crop and ground plane.
- Preserve the current clear cylindrical hood, integrated rectangular carry handle and compact V68 rear hinge. Do not invent ornate, fragmented, faceted or oversized fittings.
- The front latch uses a round 13 mm stainless push button, slim 2.2 mm annular surround and matching slim safety loop. Do not restore the previous oval slotted latch.
- Keep the exact component count, their positions and proportions. Use the Blender references rather than interpreting reflections as extra components.
- No new grips, recesses, extra carry handles, shortened bodies, widened silhouettes or alternate lid mechanisms for kids' editions.

## 3. Know the three functions

| Function | Correct component | Presentation |
| --- | --- | --- |
| Straw sip | Low folding mouthpiece in its small rectangular hinged support, towards the front-left | Sip upright; retain the short curved stem and dark mouth tip where shown in Blender. Do not replace it with a tall flared pipe. |
| Big gulp | Squat, rounded hourglass-shaped open steel spout at the front/right | Tilt to drink through the broad opening. Do not make it an elongated tube. |
| Cooling spray | **Short rear-centre cylindrical spray head** | Label this head and originate mist here. The adjacent tiny flush dark hole is **not the spray**. |

These are **two drinking methods plus one cooling spray**, not three drinking methods. The two independent pads inside the hood are translucent silicone drinking/vent seals, not extra steel mouthpieces or spray heads. They have no connecting bridge.

## 4. Materials and photographic realism

| Part | Required finish | Avoid |
| --- | --- | --- |
| Drinking metal and spray head | Smooth **mirror-polished stainless steel**, with crisp light/dark reflections and realistic highlights | Brushed grain, radial machining rings, satin/matte steel, white plastic-looking metal |
| Hood | Clear/translucent plastic, smooth edge, restrained realistic reflections | Cloudy opaque cover, broken faceted ring, glass shards, oversized chrome rim |
| Hood-mounted independent seals | Softly frosted **translucent colourless silicone**, with the background faintly visible through it | Solid black, opaque white or chrome disc; a ball on a tall vertical stalk |
| Body and coloured collar | Refined satin coating in the edition's specified colours | Inflated plastic toy appearance, glitter or texture that hides branding |
| Strap | Real woven fabric, visible fibres and stitching, stripes woven along the material's route | Flat stickers, floating emblems, a printed badge background |
| Hardware | Plausible polished side rings and detachable swivel snap hooks | Closed chain links masquerading as detachable clips |

Use coherent light, reflections, contact shadows and refraction. Preserve these when changing colour. Texture-only instructions mean texture-only: no geometry, camera, placement or branding changes.

### Image quality must survive every iteration

- Keep original high-resolution reference files and versioned lossless PNG masters. Use the best lossless master as the edit source; never a screenshot, contact-sheet crop, thumbnail, JPEG or repeatedly compressed web export.
- Do not apply heavy compression between iterations. Export delivery WebP losslessly from the final PNG, once. Preserve the source PNG and actual pixel dimensions; a larger file extension or a CSS enlargement does not restore detail.
- Avoid long chains of full-scene generative edits: they can soften faces, hands, weave and product details even when every file is lossless. Limit edits to the requested area, preserve unaffected regions, and compare against the earliest sharp approved source. Return to that source when degradation appears.
- Check people, faces, hair, hands, fabrics, polished hardware and exact logos at 100% and at intended display size before accepting an iteration. Reject smeared, waxy, blocky or artificially oversharpened results. Do not trade away existing detail to make a small local correction.
- Match source resolution to the intended display size and device pixel density. Request a genuinely higher-resolution render where needed; do not describe interpolation or CSS scaling as recovered detail. Keep native SVG branding and braille sharp.
- Main-scene character detail is maintained as two independent native-resolution image layers (`platform-{left,right}-characters-detail-v1.png` masters, lossless WebP delivery), sourced from lossless crops of the approved v18 master. Keep their registration and feathering, preserve all bottle/strap/vector layers, and do not flatten the high-detail people back into the 1536px base. See [restoration record and prompts](CHARACTER_DETAIL_RESTORATION.md).
- Background detail is also independent: keep the station detail PNG masters and lossless WebP tiles, registered to their manifest source regions. Preserve the product-exclusion coverage and approved character layers. Do not flatten these back into the low-resolution base. See [station restoration sources and prompts](STATION_BACKGROUND_RESTORATION.md).

## 5. Carry strap and cutaway exception

### Full product / main scene / colour editions

There is **one continuous detachable fabric strap**, with one opening snap hook at each end connecting to the two side rings. Two visible sides are not two independent straps. Show the spring gates/release levers clearly. The stitched fabric tabs attach to the clip hardware, not directly to the bottle. The strap reaches the ground and drapes naturally; its visible U route is part of the full-product view.

**Latest attachment reference, 15 November 2026:** [requested swivel snap hook](v68/SWIVEL_SNAP_HOOK_REFERENCE.png). The user explicitly rejected the oval wire-loop hook visible in the first native draft. Use a small round opening jaw, flat tapered trigger body, small lever/rivet, short swivel connection and a separate rounded D-ring. The clip engages the V68 recessed body mount; do not add the old collar lugs. The reference governs hook type, not a change to the edition colour, webbing or printed artwork. The original [strap construction reference](STRAP_ATTACHMENT_REFERENCE.png) still governs pristine woven fabric and slim stitched tabs, but its earlier oval-wire hook interpretation is superseded. This applies to the station scene, all 29 editions, macro and cutaway, retaining the cutaway-only flat strap exception.

**Entire strap construction and condition:** the same reference governs the fabric, folded end tabs and hardware in the main scene, Fig. 03 and the cutaway. Use plain finely woven webbing, neat straight stitched edges and a slim same-fabric folded tab with a simple rectangular stitch outline. No thick leather-like reinforcement patch, padded inset, ornate raised geometric/triangular jacquard, fraying, ragged waves, dirty specks, stains or aged yellowing. Present it as pristine, new premium fabric. Retain ivory in the ivory scenes; retain each edition's palette and approved longitudinal stripes in the collection. Keep exact strap animal SVGs centred on the fabric. A strap correction changes neither the bottle nor the scene. Full views keep one continuous floor-reaching U drape; only the half-cut view uses the flat cut-strip exception below.

### Longitudinal half-cut anatomy illustration only

The strap is also sectioned: show **one flat cut strip**, not a doubled return or closed U-loop. It keeps its upper detachable clip and stitched tab, descends to the floor, bends naturally and drapes a little forward near the lower-left base. End in a clean cut edge. Do not leave it hovering or too short. This illustration-specific exception must not be copied to the full-product colour collection.

## 6. Branding is exact vector artwork

Use `public/images/product/crest-vector-v11.svg`:

**Browser compatibility:** v11 is the editable vector master, not a website sprite. Safari/WebKit can lose masks or clips reached through external, nested SVG `<use>` references, causing overlapping copies of the unmasked artwork. Website instances use self-contained coloured SVG image exports (`*-v12.svg`) produced by `scripts/export-browser-safe-crest.py`. Their drawing paths are expanded and mask/clip definitions are local to each image document; there are no `<use>` chains, external mask references or duplicate IDs. Preserve the exact artwork and each edition's ink colour. Check the header, bottle logos, strap animals and enlarged logo in Safari as well as Chromium after brand changes. Do not reintroduce the external v11 sprite as a shortcut. The header identity is decorative and is not a link to the top; the footer keeps its back-to-top link.

- `#crest`: complete current logo, **without the shield outline**, with the small crown directly on the B.
- Reading greyhound on the left; tennis leopard on the right, balanced in visual weight and brought closer to BoP. Keep a clear gap between the paw and the P.
- The P must be complete and not clipped by a former shield mask.
- Leopard wears tennis shorts. The garment mask covers both upper legs through the hems: no fur contour or spots protrude through the cloth, and each leg emerges cleanly from its own hem. Its tail starts from behind the rear waistband/lower back, not from the thigh or a round side-panel hole. Preserve its current clean curve.
- Keep the minimalist curved Bureau of Provisions band with clean ends, no folded/fishtail tails; preserve the separator and Department of Thirst footer.
- `#greyhound` and `#leopard`: exact matching strap animals. Do not generate substitutes or remove either supporter from the body logo.

**Never remove the body logo or strap prints when replacing a source photograph.** Explicit view exception, 19 October 2026: the two visible strap tabs in Fig. 03 / Sip. Gulp. Spray. are unprinted, per the user's request to remove just that greyhound and leopard. Preserve main-scene, cutaway and collection prints, and all full bottle crests. Source render images are deliberately unprinted; the website applies exact SVG layers. Do not use image generation to recreate tiny logo lettering. Keep the body mark small/high and the strap prints discreet, centred across the fabric, just below the upper stitched tabs. Keep the lower strap plain. The greyhound is slightly larger than its earliest version; use the current approved proportions.

Integrate ink through transparent vector layers and suitable blending. Navy/charcoal ink suits light bodies; ivory ink may be used on dark bodies and dark straps for legibility. No cream sticker rectangles. A colour edition changes ink contrast when necessary, not the logo design.

## 7. Braille

Exact message: **Stay a little unreasonable.** Preserve capital S and full stop. Use `public/images/product/bottle-braille-message.svg#message`, generated by `scripts/generate-braille.mjs`, as a separate lower-body layer. Do not invent dots or ask image generation to draw braille. Physical embossing dimensions remain unconfirmed.

## 8. “Two tones” collection rules

Latest collection correction, 25 October 2026: retain the original Mint / Peach as edition 03. Edition 20 is now Turquoise / Lilac: retain turquoise #78e4e8 on the body and strap edges, with collar/latch and one centre strap stripe in the existing Lilac / Butter body colour #b5a1d0. This supersedes the earlier peach and orange accents, per the latest user correction. These are separate catalogue choices with separate registration values.

Japan’s two red sun-circle motifs align horizontally with Canada’s maple-leaf motifs, around y945 in the common 1024×1536 frame; native textile coordinates are shared with Canada.

Latest strap correction: France and Italy keep unbroken tricolour bands across the foreground strap; never swap the outer stripe colours midway. The right hanging strap reads red/white/blue for France and red/white/green for Italy, so the same band follows the same physical edge through the bend. Website collection copy omits age ranges and colour counts.

Flag studies added 25 October 2026: Greece (21), France (22), Union Jack (23), United States (24), Brazil (25), Japan (26), Canada (27), Italy (28), Spain (29). Preserve the common geometry, exact BoP branding and centred strap animals. The flag-inspired coating palettes and woven patterns are recorded in `docs/FLAG_EDITION_TEMPLATES.json`; these are design studies rather than official flag colour specifications.

- All twenty-nine cards depict this same physical bottle. Only body/collar/latch colours, woven strap colours/patterns and suitable ink contrast vary.
- Keep existing edition names, palettes, intended themes, order, colour-selection behaviour and individual registration links.
- For ages 6–10: cheerful, chic and deadpan. Princess, football, space and superhero themes are **palette/stripe references**, not physical redesigns or literal characters.
- No character faces, official club badges, football accessories, spaceship parts, plastic jewels, crown attachments, glitter, grips or bumpers.
- All White and All Grey remain monochrome. Safari Club is sand/olive/khaki. Pink Parade remains pink/raspberry/ivory. Preserve the restrained stripes on the sport and themed editions.
- Use individual high-resolution product images, never enlarged cells from a contact sheet. Use the corrected master as the common geometry authority for every recolour.

See the machine-readable twenty-nine-entry manifest for colour values, strap treatments, previous assets and current output paths.

## 9. Cutaway anatomy

Keep the stylish longitudinal half-cut: visible inner/outer steel walls, continuous internal straw and a credible curved inner floor. Water runs from its existing upper surface **all the way to that floor**, with no false second meniscus or empty-looking air gap at the bottom. Steel base/wall thickness remains visible outside the water chamber.

The exploded view uses exact V68 lid and neck surfaces with a clear illustrative gap. Do not add unrequested construction. The user explicitly requested matching illustrative stainless thread detail for this view; keep it separate from native geometry and do not claim machining validation. Section the native foot and body O-ring with the body so full rings do not float in the removed half. Keep the actual current rear hinge and the approved 90° photographic open pose.

This remains an illustrative design study. Do not infer or publish numeric dimensions, thread specifications, volume, thermal performance or manufacturing validation from generated pictures.

## 10. Clear interactive examples and callouts

- Keep Straw sip, Big gulp and Cooling spray separately selectable and consistently framed.
- Place Flat/Up directly above the Straw label and Press to mist. directly above the Spray label on the image, rather than below the explanatory copy. Keep the selected labels and pointer lines; no dotted or shaded outlet ring.
- Feature hover panels must remain within the viewport. Flip the opening direction at side edges and clamp vertically/horizontally, including panels2 and5; reposition on resize and scroll.
- Use the approved photographed hardware; do not replace it with a rough generic procedural 3D bottle.
- Straw: **two still positions only**, Flat and Up (initial) (the final raised reference). Use a Flat / Up switch; no animation, interpolation, automatic folding, playback, hold or Reset buttons. The camera, bottle and all other parts remain fixed. Use [raised overhead reference](v68/lid-raised.png) for the Up pose: the short open drinking bore faces the viewer within its stationary hinge assembly. The [current raised reference](v68/lid-raised.png) clarifies the 135° position; it does not authorize changing the photographic camera. Intermediate motion experiments are superseded.
- Spout: explanation and “Tilt to drink” only; no playback, hold or reset controls.
- Mist: label the action **“Press to mist.”**. Each click demonstrates one pump: head depresses, emits one short burst, returns to rest, then a dense white plume with fine droplets and soft edges, matching the main-page mist, continues outward toward the “03 Spray” label and fades. No continuous spray, Stop toggle, hold button or Reset. Keep the visible action rectangle compact and clear of the hood on phones, with additional invisible tap space above it. Flat/Up use the same compact height, typography and padding as the mist action. Preserve the fixed camera and all other hardware. Use the local pressed-pose image, not a full-scene regeneration.
- Support touch and keyboard, reduced motion, hidden/offscreen suspension and clean reset when switching modes. Preserve fixed-camera geometry when switching straw positions; do not rotate the photograph sideways.
- Show fine mist from the **rear-centre head**, not from the nearby flush hole or the silicone seal.
- Recalibrate pointers, highlights and particles whenever the image/camera changes. Do not copy coordinates between views.
- Main scene point **7 explains the inspirational braille message “Stay a little unreasonable.”** Its leader ends on the existing lower-body braille at approximately (775,834) in the 1536×1024 scene; its pin sits lower-left at (390,940), with its route below point 5. Keep all seven callouts touch and keyboard accessible.
- Main scene point **1 stays on the left** and its leader points to the spray head, routing around the hood. Point 6 stays lower-right, routed below the other leaders.

Current calibration is recorded in [native projected anchors](v68/view-anchors.json). Read that record after each camera change; historical pixel coordinates are not reusable across views. Macro Spray is at 48% frame height and Spout at 65%, with their leaders meeting the label centres.

## 11. Site art direction and copy

Latest copy correction: do not offer alternative lid configurations while they are unavailable. Describe the three functions of the current design. Use plain “design” or “specifications” in public copy instead of “CAD”; retain the technical source records internally.

Restrained symmetrical staging, warm ivory, wine and navy typography, dry observational humour and precise product descriptions. Punchy lines may be playful, but explain the functions clearly. Keep the compact header: logo on the left, Big thirst. Zero drama. beside it, registration CTA on the right.

### Reusable visual language

| Token | Current value / use |
| --- | --- |
| Paper | `#f4eddf`, main background and light ink |
| Ink | `#293b3d`, clear body text |
| Wine | `#713b44`, headings, selected controls and primary CTAs |
| Rose / sage | `#e5c5bc` / `#d7dfce`, restrained supporting colour |
| Rule | `#b8b4a1`, fine borders and separators |
| Display type | Fraunces, Georgia fallback; large serif headlines with occasional italic second phrase |
| Body type | Inter, Arial fallback; plain, readable functional descriptions |
| Utility type | Courier New / monospace; small, spaced issue labels and edition numbers |

Hierarchy: compact identity and one headline first; concise product definition second; one clear registration action third. Small issue/date labels stay subordinate. Avoid wide empty gaps separating related copy, competing oversized logos, repeated navigation or decorative boxes that obscure the product. Numbered feature pins reveal descriptions on hover, focus or tap rather than covering the scene with permanent panels. Preserve visible focus and touch access.

Copy pairs a short dry line with a precise benefit. Examples: “Big thirst. Zero drama.”; “Royal protocol. Juice first.” Describe the mechanism as **folding straw**, **wide drinking spout** or **push-button cooling spray** when explaining function. Keep the everyday definition concise: “Your everyday stainless steel bottle.” Avoid vague provisions language that makes the product harder to understand.

The family scene keeps the girl in preppy clothes, dark ringlet ponytail and no glasses; mother sits independently beside her; boy sits beside his father. Preserve people and scene positions during bottle/material edits. The conductor stands at a generous **open arched ticket-service window**, framed in mahogany and slim brass, with no bars across his face, torso or counter. This latest user correction supersedes the previous full grille. The lamp-switch alternate pose must use the same open arch; do not reintroduce the old barred gesture or foreground grille. Preserve the painting position, page-turn and light animations unless explicitly asked to change them.

Every bottle keeps “Register to pre-order” carrying its selected name to the existing Tally interest form. Registration is not a paid checkout. Dishwasher safe is a user-provided feature. Current V68 design gives a 73 mm body diameter, 179.5 mm body-plus-base height and 249.1 mm closed envelope including the integrated carry handle. The inherited design target remains 500 mL nominal capacity; do not describe it as measured liquid volume. Current dimensions, native-file hash and preserved historical specifications are recorded in [cad-specifications.json](../design/cad-specifications.json). Unconfirmed performance claims remain pending. No prices are displayed; ships internationally. Registration still uses the existing interest form.

## 12. Reusable production workflow

1. Read this guide and select the correct view context: full bottle, macro lid or sectional anatomy.
2. Use the current V68 Blender references for geometry and the current approved render for finish/lighting.
3. Establish one native studio setup. Every colour edition reuses the same meshes, camera and pose; only shader palettes and textile patterns change.
4. Use [PRODUCT_RENDER_TEMPLATE.md](prompts/PRODUCT_RENDER_TEMPLATE.md), filling the edition palette from the JSON manifest. Explicitly identify each reference's role.
5. Render bottle geometry directly from the V68 Blender meshes. Imagegen may repair a local background clean plate, never reinterpret the product. Keep native SVG branding, icons and braille as native assets. No generated lettering or animal replacements.
6. Save versioned source PNGs plus lossless WebP web assets. Preserve originals. Store actual prompts, references and output provenance.
7. Reuse existing exact logo/strap/braille layers; check their positions at full size. Preserve all card links and selection controls.
8. Inspect every output, then inspect it in the browser at desktop and mobile sizes. Compare silhouette, mouthpiece layout, silicone, polished reflections, clip gates, strap route, branding and registration links.
9. Run the production build and relevant collection checks. Record the current approved asset paths in the manifest.

### Acceptance checklist

- [ ] Original tall/slim silhouette and identical scale/crop across all colour cards.
- [ ] Correct low folding straw, hourglass spout and rear-centre spray head.
- [ ] Clear smooth hood; translucent silicone pad/neck; mirror-polished steel.
- [ ] One continuous detachable strap and two opening clip gates in full-product views.
- [ ] Cutaway-only strap exception, water to the native floor and source-modelled neck connection.
- [ ] Exact body logo, both supporters, centred strap animals and exact braille retained.
- [ ] Palette/stripe changes only; no invented kids geometry or accessories.
- [ ] Spray labels/animation point to the actual head; point1 remains left.
- [ ] Same names, twenty-nine cards, individual registration links and accessible selection controls.
- [ ] No invented dimensions/performance claims; source/prompt/output provenance saved.

## Approved release / 15 November 2026

The user approved the complete correction proof and authorised the whole website update. The approval receipt is `design/render-approval.json`; the final render, fit and delivery evidence is in `docs/v68/`. The dark physical-lid experiments were rejected. Retain the **Previous proof** lid: one sharp, unbent transmission path with subtle smoky edge tint, no large white studio-light patches and no reflected/offset duplicates of the drinking parts. Keep polished stainless drinking hardware and the circular button face; the coloured surround remains edition-specific.

- Every non-cutaway camera faces the native front exactly (camera and target x=0). Preserve the main scene's accepted camera and vertical elevation. Only the cutaway is oblique. Open covers are photographed at **90°**; native CAD still retains its full 220° mechanism travel. Do not move the native handle to correct perspective.
- Hook release levers are **above** both snap bodies. Slim folded fabric conceals the lower D-ring bars on both sides. Preserve the original recessed body mounts and require zero evaluated metal/body intersection.
- Use the calibrated vivid colour rendering and the exact edition palettes. Japan suns are metrically round; the approved old Canada leaf is traced in `design/flag-artwork/`, with the left leaf upright and both folded tabs entirely ivory. Union Jack crosses and counterchanged diagonals follow the maintained vector artwork.
- Strap artwork is centred on the projected fabric at each emblem's **centre height**, not its top anchor. Keep both exact animals and all body crests. The two macro tabs alone are unprinted. Preserve the continuous full-view strap and cutaway-only flat section.
- Mark the existing cap/body junction with a thin appearance-only seam, not a new gasket or band.
- Main scene and lid demo start with the straw Up. Close lid folds the straw and stops mist; Open lid restores Up. Keep leaders, patches and spray emission registered to `view-anchors.json`. Spray and Spout labels have sufficient separation on narrow screens and their leader starts match their CSS percentage positions.
- Small main straw/spout dots sit beside the openings. The carry leader touches the strap. Catalogue braille stays discreet; cutaway braille is absent. There are no prices on the current website.
- In the cutaway, lift the native metallic pickup with the upper deck and hidden silicone socket by the same 34 mm exploded offset. Continue metal into the hidden socket; no exposed white connector or body-fixed duplicate. Show only the requested metallic thread beneath the cap, visible double-wall/gap edges, continuous water to the curved floor and a half-clipped crest. These screw details are explicitly requested illustration additions, not a manufacturing specification or source .blend change.

## Next update: smallest useful render

Latest local correction, 15 November evening: remove the separate dark
rectangular stitch border from white/ivory folded strap tabs (All White,
Away Day, Extra Time, Japan and Canada). Preserve their slim same-fabric folds,
clean weave, exact prints and edition patterns. Fig. 01 also requires restrained
steel reflections and a sharply resolved recessed straw. Cedric explicitly approved the comparison and authorised publication with
“ok push it”. The approved comparison is `docs/v68/macro-correction-comparison.png`.

Use [the workflow](DESIGN_REVIEW_WORKFLOW.md) and [session lessons](V68_SESSION_LESSONS.md). Start with one affected edition/image type; get explicit visual sign-off before a full batch. CSS labels, leaders and exact SVG placement require no Blender render. A catalogue camera/material/hardware change affects all 29 editions; a scene-only correction uses `--part hero`, a cutaway-only correction `--part section`. Preserve PNG masters, export lossless WebP once, regenerate responsive variants, refresh evidence and run the complete release checks. Keep `/old/` unchanged. [Blender handoff](BLENDER_STRAP_HANDOFF.md) provides the packed library and safe next-session import.
