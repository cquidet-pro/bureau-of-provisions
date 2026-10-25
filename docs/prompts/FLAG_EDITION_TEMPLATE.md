# Flag-inspired bottle colour study

Use with `PRODUCT_RENDER_TEMPLATE.md` and `../PRODUCT_DESIGN_GUIDE.md`.

Edit target: `public/images/product/collection-studio-master-v2.png`.
Keep the approved bottle geometry, camera, polished hardware, clear hood,
translucent silicone and one continuous detachable woven strap unchanged.

## Palette and textile fields

| Edition | Body | Collar / latch | Woven strap |
| --- | --- | --- | --- |
| Greece / 21 | `#0d5eaf` | `#f4f3ee` | Alternating blue and white longitudinal bands, blue outer edges |
| France / 22 | `#f4f3ee` | `#002654` | Three equal longitudinal bands: blue `#002654`, white `#f4f3ee`, red `#ed2939` |
| Union Jack / 23 | `#012169` | `#c8102e` | Navy, red centre stripe with white borders and spaced red/white diagonal accents |

| United States / 24 | `#21345b` | `#b31942` | Red/white stripes, navy borders, small stars on the lower strap |
| Brazil / 25 | `#009739` | `#fedf00` | Green edges, blue centre stripe with yellow borders |
| Japan / 26 | `#f4f3ee` | `#bc002d` | White with crimson centre stripe and sun-circle accents |
| Canada / 27 | `#d80621` | `#f4f3ee` | Red/white/red bands with small red maple leaves below the BoP prints |

| Italy / 28 | `#f4f3ee` | `#009246` | Three equal longitudinal bands: green, white, red `#ce2b37` |
| Spain / 29 | `#aa151b` | `#f1bf00` | Red outer bands with a broad golden-yellow centre |

These hex values are chosen product palettes, not official flag colour standards.
Greece translates the flag's stripes into longitudinal webbing. Union Jack
translates its cross motifs into a textile pattern rather than a literal flag.

## Prompt template

Use case: precise-object-edit. Create **{edition}** from the attached neutral
studio master. Change only body coating to **{body}**, collar and latch coating
to **{accent}**, and strap textile to **{woven_strap}**. Preserve source framing,
silhouette, scale, lighting, background, every hardware component, clean plain
weave and folded stitched tabs. Stripes follow the existing fabric through the
entire floor-reaching U route. Preserve two opening swivel snap hooks.

Leave the body and animal print areas blank. Retain exact BoP crest, both strap
animals and braille as separate existing SVG layers; do not generate substitutes.
Use light crest/braille on dark bodies and suitable contrasting strap prints.
Keep the current centred dog and leopard positions.

Save a versioned full-resolution PNG master and export lossless WebP once.
Record prompt, palette, references and output paths, then add an independent
catalogue choice and registration value. Preserve all existing editions.

Full prompts and generated source paths: `../FLAG_EDITION_TEMPLATES.json`.

## References

- User reference: https://www.britannica.com/topic/flag-of-Greece
- Greek flag: https://www.presidency.gr/en/presidency/the-flag/
- French flag: https://www.elysee.fr/la-presidence/le-drapeau-francais
- Union Jack: https://www.royal.uk/union-jack
