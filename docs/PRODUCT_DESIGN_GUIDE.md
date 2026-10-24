# Bureau of Provisions — reusable product design guide

Version: 19 October 2026. Applies to website visuals, product studies, colour editions, prompts and future design work.

This is the **current specification**. It consolidates the user's approved corrections; it is not a history of every experiment. Earlier interpretations are archived in [PRODUCT_DESIGN_HISTORY.md](PRODUCT_DESIGN_HISTORY.md). Machine-readable rules and all twenty edition palettes are in [product-design.json](../design/product-design.json).

## 1. Source hierarchy

1. The user's latest explicit instruction takes precedence.
2. Original solid Blender screenshots govern physical geometry. Use [front/elevated reference](ORIGINAL_SOLID_LID_REFERENCE.png) and [three-quarter reference](ORIGINAL_CUTAWAY_LID_REFERENCE.png).
3. Approved finished renders govern materials, lighting and visual treatment. They do **not** override Blender geometry.
4. This guide, the palette manifest and render prompt template apply to all new work.
5. Superseded generated images are not product references. A different camera, colour or audience is never permission to invent hardware.

Reference renders: `platform-strap-reference-v18.webp`, `lid-strap-reference-v8.webp`, `bottle-cutaway-strap-reference-v9.webp`, all under `public/images/product/`. The collection uses the corrected neutral studio master and its colour-only variants listed in the manifest.

## 2. One product; fixed construction

- Preserve the tall, slim body, shoulder, base, collar diameter and proportions. Every collection image has the same scale, camera, crop and ground plane.
- Preserve the smooth circular hinged hood, its narrow rim and original hinge/clasp arrangement. Do not invent ornate, fragmented, faceted or oversized fittings.
- The front latch is an oval piece with a small horizontal inset. It is not a new handle, bumper or large decorative plate.
- Keep the exact component count, their positions and proportions. Use the Blender references rather than interpreting reflections as extra components.
- No new grips, recesses, extra carry handles, shortened bodies, widened silhouettes or alternate lid mechanisms for kids' editions.

## 3. Know the three functions

| Function | Correct component | Presentation |
| --- | --- | --- |
| Straw sip | Low folding mouthpiece in its small rectangular hinged support, towards the front-left | Sip upright; retain the short curved stem and dark mouth tip where shown in Blender. Do not replace it with a tall flared pipe. |
| Big gulp | Squat, rounded hourglass-shaped open steel spout at the front/right | Tilt to drink through the broad opening. Do not make it an elongated tube. |
| Cooling spray | **Short rear-centre cylindrical spray head** | Label this head and originate mist here. The adjacent tiny flush dark hole is **not the spray**. |

These are **two drinking methods plus one cooling spray**, not three drinking methods. The round pad and its neck mounted inside the hood are a silicone sealing part, not an extra steel mouthpiece or spray head.

## 4. Materials and photographic realism

| Part | Required finish | Avoid |
| --- | --- | --- |
| Drinking metal and spray head | Smooth **mirror-polished stainless steel**, with crisp light/dark reflections and realistic highlights | Brushed grain, radial machining rings, satin/matte steel, white plastic-looking metal |
| Hood | Clear/translucent plastic, smooth edge, restrained realistic reflections | Cloudy opaque cover, broken faceted ring, glass shards, oversized chrome rim |
| Hood-mounted round seal and neck | Softly frosted **translucent colourless silicone**, with the background faintly visible through it | Solid black, opaque white or chrome disc; a ball on a tall vertical stalk |
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

**Attachment shape reference:** [STRAP_ATTACHMENT_REFERENCE.png](STRAP_ATTACHMENT_REFERENCE.png), supplied 18 October 2026. From bottle to fabric: small side lug → slim angled connector → rounded oval/teardrop opening clip → short swivel stem → separate wide rounded rectangular D-ring → stitched fabric tab. Preserve this order and the slender polished round-section metal. A flat rectangular clip plate, chunky trigger hook, circular lower ring or fabric sewn straight to the bottle does not match this reference. Adapt perspective to each view; do not copy the reference's purple colour onto ivory studies. This correction applies to Fig. 03 and the inside-story cutaway, while retaining the cutaway's flat cut strap and existing exact vector branding.

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

Latest collection correction, 25 October 2026: retain the original Mint / Peach as edition 03. Add Turquoise / Orange as edition 20, with body #78e4e8, collar #ffa15e, and turquoise strap edges with one orange centre stripe. These are separate catalogue choices with separate registration values.

- All twenty cards depict this same physical bottle. Only body/collar/latch colours, woven strap colours/patterns and suitable ink contrast vary.
- Keep existing edition names, palettes, intended themes, order, colour-selection behaviour and individual registration links.
- For ages 6–10: cheerful, chic and deadpan. Princess, football, space and superhero themes are **palette/stripe references**, not physical redesigns or literal characters.
- No character faces, official club badges, football accessories, spaceship parts, plastic jewels, crown attachments, glitter, grips or bumpers.
- All White and All Grey remain monochrome. Safari Club is sand/olive/khaki. Pink Parade remains pink/raspberry/ivory. Preserve the restrained stripes on the sport and themed editions.
- Use individual high-resolution product images, never enlarged cells from a contact sheet. Use the corrected master as the common geometry authority for every recolour.

See the machine-readable twenty-entry manifest for colour values, strap treatments, previous assets and current output paths.

## 9. Cutaway anatomy

Keep the stylish longitudinal half-cut: visible inner/outer steel walls, continuous internal straw and a credible curved inner floor. Water runs from its existing upper surface **all the way to that floor**, with no false second meniscus or empty-looking air gap at the bottom. Steel base/wall thickness remains visible outside the water chamber.

The exploded lid and neck show a meaningful matching screw connection: several complete evenly pitched female thread turns and a corresponding male screw skirt, with matching diameter/pitch and a clear exploded gap. Do not draw intersecting parts or merely shallow decorative rings. Keep the lid's original Blender hardware and appropriate folded-back hood pose.

This remains an illustrative design study. Do not infer or publish numeric dimensions, thread specifications, volume, thermal performance or manufacturing validation from generated pictures.

## 10. Clear interactive examples and callouts

- Keep Straw sip, Big gulp and Cooling spray separately selectable and consistently framed.
- Place Flat/Up directly above the Straw label and Press to mist. directly above the Spray label on the image, rather than below the explanatory copy. Keep the selected labels and pointer lines; no dotted or shaded outlet ring.
- Feature hover panels must remain within the viewport. Flip the opening direction at side edges and clamp vertically/horizontally, including panels2 and5; reposition on resize and scroll.
- Use the approved photographed hardware; do not replace it with a rough generic procedural 3D bottle.
- Straw: **two still positions only**, Flat (initial) and Up (the final raised reference). Use a Flat / Up switch; no animation, interpolation, automatic folding, playback, hold or Reset buttons. The camera, bottle and all other parts remain fixed. Use [raised overhead reference](STRAW_RAISED_OVERHEAD_REFERENCE.png) for the Up pose: the short open drinking bore faces the viewer within its stationary hinge assembly. The [three-quarter reference](STRAW_45_DEGREE_REFERENCE.png) clarifies the hinge angle; it does not authorize changing the overhead camera. Intermediate motion experiments are superseded.
- Spout: explanation and “Tilt to drink” only; no playback, hold or reset controls.
- Mist: label the action **“Press to mist.”**. Each click demonstrates one pump: head depresses, emits one short burst, returns to rest, then a dense white plume with fine droplets and soft edges, matching the main-page mist, continues outward toward the “03 Spray” label and fades. No continuous spray, Stop toggle, hold button or Reset. Keep the visible action rectangle compact and clear of the hood on phones, with additional invisible tap space above it. Flat/Up use the same compact height, typography and padding as the mist action. Preserve the fixed camera and all other hardware. Use the local pressed-pose image, not a full-scene regeneration.
- Support touch and keyboard, reduced motion, hidden/offscreen suspension and clean reset when switching modes. Preserve fixed-camera geometry when switching straw positions; do not rotate the photograph sideways.
- Show fine mist from the **rear-centre head**, not from the nearby flush hole or the silicone seal.
- Recalibrate pointers, highlights and particles whenever the image/camera changes. Do not copy coordinates between views.
- Main scene point **1 stays on the left** and its leader points to the spray head, routing around the hood. Point 6 stays lower-right, routed below the other leaders.

Current calibration: main photo1536×1024: spray point1 starts(390,170) and ends near(766,324). Enlarged lid1088×1445: highlight head near(592,732), mist leaves the middle of its right-hand vertical steel wall near(647,782) during the press and travels outward toward the “03 Spray” label. These coordinates are view-specific, not product measurements.

## 11. Site art direction and copy

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

Every bottle keeps “Register to pre-order” carrying its selected name to the existing Tally interest form. Registration is not a paid checkout. Dishwasher safe is a user-provided feature. Current Original/Mist V55 CAD gives a 65 mm body diameter, 185.4 mm body height from the protective-foot datum, and 207.7 mm closed overall envelope including the silicone insert (hood top:207.5 mm). The model labels 500 mL as nominal design capacity; do not describe it as measured liquid volume. Source bounds, native-file hash and the reason the inherited 231 mm label is stale are recorded in [cad-specifications.json](../design/cad-specifications.json). Unconfirmed performance claims remain pending. Pre-order price is £39 per bottle; ships internationally. Registration still uses the existing interest form.

## 12. Reusable production workflow

1. Read this guide and select the correct view context: full bottle, macro lid or sectional anatomy.
2. Use the original Blender screenshot for geometry and the current approved render for finish/lighting.
3. Establish one corrected neutral studio master. A colour variant changes palette/pattern only; never re-invent the model per colour.
4. Use [PRODUCT_RENDER_TEMPLATE.md](prompts/PRODUCT_RENDER_TEMPLATE.md), filling the edition palette from the JSON manifest. Explicitly identify each reference's role.
5. Generate/edit bitmap product photographs with imagegen. Keep native SVG branding, icons and braille as native assets. No generated lettering or animal replacements.
6. Save versioned source PNGs plus lossless WebP web assets. Preserve originals. Store actual prompts, references and output provenance.
7. Reuse existing exact logo/strap/braille layers; check their positions at full size. Preserve all card links and selection controls.
8. Inspect every output, then inspect it in the browser at desktop and mobile sizes. Compare silhouette, mouthpiece layout, silicone, polished reflections, clip gates, strap route, branding and registration links.
9. Run the production build and relevant collection checks. Record the current approved asset paths in the manifest.

### Acceptance checklist

- [ ] Original tall/slim silhouette and identical scale/crop across all colour cards.
- [ ] Correct low folding straw, hourglass spout and rear-centre spray head.
- [ ] Clear smooth hood; translucent silicone pad/neck; mirror-polished steel.
- [ ] One continuous detachable strap and two opening clip gates in full-product views.
- [ ] Cutaway-only strap exception, water to floor and plausible mating threads.
- [ ] Exact body logo, both supporters, centred strap animals and exact braille retained.
- [ ] Palette/stripe changes only; no invented kids geometry or accessories.
- [ ] Spray labels/animation point to the actual head; point1 remains left.
- [ ] Same names, twenty cards, individual registration links and accessible selection controls.
- [ ] No invented dimensions/performance claims; source/prompt/output provenance saved.
