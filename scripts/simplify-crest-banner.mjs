import { readFileSync, writeFileSync } from 'node:fs';

// Preserve all approved ink, lettering and animal symbols. Remove only the
// ribbon's folded tails, leaving a plain curved band with clean end strokes.
const source = readFileSync('public/images/product/crest-vector-v1.svg', 'utf8');
const mask = `<mask id="plain-band-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="1266" height="1242"><rect width="1266" height="1242" fill="white"/><path d="M0 765H222L241 865L260 940H0Z M1043 776H1266V940H1000L1024 865Z" fill="black"/></mask>`;
const plain = source.replace('</defs>', `${mask}</defs>`).replace(
  '<g id="crest" fill="currentColor"><use href="#ink"/></g>',
  '<g id="crest" fill="currentColor"><use href="#ink" mask="url(#plain-band-mask)"/><path d="M222 742L241 856 M1044 758L1027 865" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round"/></g>'
);
writeFileSync('public/images/product/crest-vector-v2.svg', plain);
