# Station background restoration — 19 October 2026

Built-in imagegen was used on independent lossless crops of `public/images/product/platform-strap-reference-v18.png`. User screenshots were location references only, not edit sources. Each output has a retained PNG master and one lossless WebP export in `public/images/product/`.

The website keeps the original base, approved character detail, exact vector branding and product geometry. Independent native-resolution tiles restore the background; a simple alpha-coverage SVG excludes the bottle, hood, hardware and continuous strap. The coverage asset has no nested masks or external references. The front plinth tile uses CSS object-fit:cover; white padding in that generated master is outside the visible crop. These are newly reconstructed details, not recovery of lost pixels.

The user's additional correction replaces the full ticket-office grille with a generous open mahogany/brass arch. The foreground bars are removed, and the alternate lamp-switch image uses the same open arch. The light toggle, page-turn and reduced-motion behaviour remain.

The user's explicit print exception removes just the two animal overlays on the Fig. 03 lid-view strap tabs. Main-scene prints, cutaway print, 19 edition prints and full bottle crests remain.

## Final prompt set and source records

### stationLeft

Output master: `public/images/product/station-left-detail-v1.png`; delivery: corresponding `.webp`.

Input crop/reference: `/private/tmp/bop-station-left-source.png`. The ticket gesture uses the newly approved open-arch master, not the old barred scene.

> Use case precise-object-edit. Exact edit target is lossless crop from approved station scene. Restore this entire target to pin-sharp premium editorial photographic detail, high native resolution portrait 1300x2048 or higher. Keep EXACT frame bounds, camera, all objects' positions, sizes, outlines, colours, lighting and shadows. Do not recompose. Main priority: green enamel-painted wooden wall and gold moulding need straight crisp edges, subtle finely resolved paint/wood texture, no smearing; antique polished brass wall sconce with round glowing opal glass globe needs clearly shaped mount, joints, stem and polished highlights (globe naturally glows but fixture is sharply focused). Mahogany ticket window, fine brass grille, ticket seller, desk lamp, bench and reflective red-and-cream marble floor all need realistic crisp material detail. Preserve exact existing people and clothing/poses (seated mother and girl will be covered by already approved sharper layers); ticket clerk remains behind bars. Preserve any white strap sliver at right (will be excluded). Restore real material texture without added dirt, wear, HDR halos or oversharpened outlines. No text additions, no new props, no camera or perspective changes. Deliver image1 exact composition, no borders, lossless PNG.

### stationRight

Output master: `public/images/product/station-right-detail-v1.png`; delivery: corresponding `.webp`.

Input crop/reference: `/private/tmp/bop-station-right-source.png`. The ticket gesture uses the newly approved open-arch master, not the old barred scene.

> Use case precise-object-edit. Exact edit target is lossless crop of approved station scene. Restore entire target to crisp natural editorial photographic detail at high native resolution portrait 1292x2048 or higher. EXACT same frame bounds, camera, sizes, object positions, outlines, palette, lighting and shadows. Priorities: green enamel wooden wall with straight crisp gold mouldings and finely resolved restrained paint texture; polished brass wall sconce with round glowing opal globe, visibly defined metal joints and reflections; gold-framed sepia railway artwork with sharply defined frame and a coherent fine vintage railway scene inside; red arch and exterior station architecture with crisp structural detail. Preserve luminous spray cloud at upper left in same place, fine natural water droplets, no chunky blobs. Preserve bench, red suitcase, bags and reflective red-and-cream marble floor and step with clear realistic detail. Keep boy and father exact poses/clothes/positions (already approved sharper character layers will cover them). Do not alter any strap sliver at left (will be excluded). Natural high detail, no painterly smearing, waxiness, extra weathering, added props, HDR halos or artificial sharpening. No camera or scene layout changes. Lossless PNG.

### stationClock

Output master: `public/images/product/station-clock-detail-v1.png`; delivery: corresponding `.webp`.

Input crop/reference: `/private/tmp/bop-clock-source.png`. The ticket gesture uses the newly approved open-arch master, not the old barred scene.

> Use case precise-object-edit. Exact crop target of station clock and adjacent green wall. Restore same crop as a sharply focused photographic detail image at native 1440x1080 or greater. Preserve EXACT frame bounds, clock circular position/size, brass-rim silhouette, green and gold moulding lines, illumination, shadows and ivory dial. Clean elegant antique brass wall clock with crisp perfectly legible black Arabic numerals 1 through 12, all 12 only once at proper clock positions, evenly spaced fine minute ticks, two coherent black hands from central pivot pointing in same directions as input: shorter hand between 1 and 2, longer hand between 3 and 4. Preserve crown knob and polished highlights. Fine natural brass and painted wall detail; globe of clock not distorted. Keep exact composition and period style, no added text or objects, no blur, painterly strokes, exaggerated grain, HDR halos or camera change. Lossless PNG.

### stationTicketOffice

Output master: `public/images/product/station-open-arch-v1.png`; delivery: corresponding `.webp`.

Input crop/reference: `/private/tmp/bop-ticket-office-source.png`. The ticket gesture uses the newly approved open-arch master, not the old barred scene.

> Use case precise-object-edit. Edit this exact ticket office crop. Keep EXACT crop bounds, frame position, overall dark mahogany ticket-office architecture, the same friendly moustached clerk in burgundy cap and uniform, his pose, green banker lamp, desk ticket ledger, warm golden interior and same sunlight. Crucial requested modification: replace the prison-like full grille with a beautiful spacious OPEN ARCHED service window. The mahogany arch must frame a generous completely unobstructed opening, no bars across his face or torso or counter. Elegant thin polished brass inner arch edging is welcome; no central vertical rods, cage, grille, glass screen or closed gate. View the clerk clearly through the open arch at the same position and scale. Preserve broad original mahogany top moulding, sill and square outer frame, make only the internal aperture a pleasing polished arch. Restore crisp photographic realism: clear individual moustache hairs and natural face, cap texture, fine wood grain, sharply defined brass lamp, joints and reflections. High native portrait resolution around1024x1552, no blur, no painterly/waxy smearing, no added text, symbols, props or camera changes. Output lossless PNG, identical composition bounds so it can replace only this local region.

### stationMiddleFloor

Output master: `public/images/product/station-floor-detail-v1.png`; delivery: corresponding `.webp`.

Input crop/reference: `/private/tmp/bop-middle-floor-source.png`. The ticket gesture uses the newly approved open-arch master, not the old barred scene.

> Use case precise-object-edit. Exact small wide crop from station photograph: red marble plinth front with natural cream veins and dark reddish reflections. Restore this exact composition with crisp natural highly detailed polished red marble surface. Keep exact crop bounds, same red/cream palette, same main vein locations, reflections and lighting. Preserve tiny ivory woven strap edge at top centre, do not add more of it. Replace strange melted chunky smeared shapes with coherent natural marble veining and reflective stone, no new objects or people, no invented words, same camera. High native wide image about1860x504, ratio310:84, lossless PNG.

### stationTicketGesture

Output master: `public/images/product/station-open-arch-gesture-v1.png`; delivery: corresponding `.webp`.

Input crop/reference: `/Users/andonella/.codex/generated_images/01a13734-76ee-7bf2-b1a5-8b229a813126/exec-444685e4-f56f-48fd-bbeb-d27b96049595.png`. The ticket gesture uses the newly approved open-arch master, not the old barred scene.

> Use case precise-object-edit. Keep this exact photograph of open arched ticket window unchanged, same crop bounds, camera, scale, clear open arch NO BARS, clerk face/hat/torso/pose, lighting, wall, wood, brass, green banker lamp and counter. Make only one local change: the clerk extends his right hand (viewer left) naturally from below his chest toward the small pull switch just beneath the green desk lamp shade on viewer left. Show a convincing natural hand with gently pinched thumb and forefinger at the lamp switch, attached to a plausible bent arm in the same burgundy sleeve. Hand and wrist stay near the lamp, below his face; no face changes or other movement. Keep lamp illuminated. Do NOT change the surrounding image or add bars. This is the alternate hand pose for a subtle switch animation; absolutely fixed registration and clean detailed photography. Native resolution same as input, lossless PNG.

## Verification

Inspected the outputs at native size and as a locally registered composition. Checked mask exclusion over the bottle and strap, open counter and both lamp poses, clock numerals, gold mouldings, framed picture and layer seams. Verified PNG/WebP pixel equality and the production build. No browser visual verification is claimed: browser access was previously declined. The source base and both approved character assets remain unchanged.

