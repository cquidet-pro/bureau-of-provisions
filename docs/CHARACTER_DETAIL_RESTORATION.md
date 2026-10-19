# Main-scene character detail — 19 October 2026

The Safari compatibility fix was published first, in b42cb0d. This subsequent change restores detail to the four seated people using independent images; the approved bottle, strap, hood, spray, base scene and exact SVG branding remain in place.

## Sources and deliverables

- Base lossless source: `public/images/product/platform-strap-reference-v18.png` (1536 × 1024), unchanged.
- Photographic detail benchmark: `public/images/product/platform-family-v1.png`. Its rejected product geometry and people placement are not adopted.
- Right source region: x1020, y330, width516, height520. Native output: `public/images/product/platform-right-characters-detail-v1.png`, 1254 × 1254.
- Left source region: x250, y330, width370, height510. Native output: `public/images/product/platform-left-characters-detail-v1.png`, 1069 × 1472.
- Delivery: corresponding lossless WebP exports, made once from each PNG. The website registers each image to its source region, with feathered boundaries; the left layer is clipped away from the approved strap.

Generated detail is a new photographic reconstruction guided by the current characters, not recovery of lost original pixels. Higher-resolution local images retain substantially more facial and fabric detail than another full-scene generation. Preserve these PNG masters in future edits. A screenshot-based preliminary candidate was not used.

## Final prompts — built-in imagegen

Right:

> Use case identity-preserve, localized photo restoration. Image 1 is the exact edit target extracted losslessly from approved PNG master, NOT a screenshot. Image 2 supplies only the sharp photographic quality benchmark. Restore ONLY image 1 into a crisp high-detail natural editorial photograph at high native resolution (square). Keep exact image1 frame bounds, positions, silhouettes, poses, facial identities, warm lighting, wall moulding lines, bench, suitcase, newspaper, bag and floor. Boy with brown curls red patterned jacket white tee navy trousers white trainers sits beside black-glasses moustached father brown plaid suit reading paper. Keep their current expressions and body proportions. Reconstruct clear eyes, individual curls, natural detailed skin rather than waxy smooth faces, crisp fingers and finely woven fabrics at the quality of image2. Nothing moves; no new objects or camera change. Render entire identical composition of image1 at 1536x1536 or larger native resolution. Preserve green wall and bench edge registration exactly for a local overlay.

Left:

> Use case identity-preserve, local photographic restoration. Image1 is exact target crop extracted losslessly from approved PNG; image2 ONLY benchmark for natural crisp photo detail. Restore image1 to a richly detailed photographic 1110x1530 portrait or higher native resolution. Keep EXACT target1 composition, frame bounds, poses, clothes, colours, identities, silhouettes, facial expressions and directions of gaze. Elegant mother in burgundy red pantsuit with cream blouse neck scarf dark sunglasses and red loafers sits beside young girl with curly ponytail NO GLASSES wearing navy cream-piped school blazer white blouse burgundy bow tie plaid skirt knee-high white socks burgundy shoes. Girl looks toward mother; skateboard beneath girl's feet. Same green station wall, red bench, floor, lighting, margins. Reconstruct sharp natural detailed eyes and hair curls, skin texture, hands with believable fingers, finely woven clothes. Eliminate waxy smeared 3D appearance. No new objects or identity changes, no repositioning or camera movement. Preserve strap sliver on far right exactly (will be masked out). Deliver entire image1 composition. Match natural photographic quality of image2.

Requested dimensions are in the prompts; actual returned native dimensions are recorded above, without interpolation claims.

## Verification

Inspected each native output and a local registered composition, including source-region boundaries and the adjacent strap. PNG/WebP pixel equality and the production build are checked before publication. In-browser verification of the new layers was unavailable because the browser origin permission was declined. The preceding Safari logo fix was separately verified in actual Safari and published successfully.
