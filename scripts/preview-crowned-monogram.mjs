import { readFileSync, writeFileSync } from 'node:fs';

const source = readFileSync('public/images/product/crest-vector-v3.svg', 'utf8');
// Reuse the exact original crown artwork at a size appropriate to the B.
const definitions = `<clipPath id="original-crown"><path d="M460 140H780V325Q620 275 460 325Z"/></clipPath><mask id="move-crown-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="1266" height="1242"><rect width="1266" height="1242" fill="white"/><rect x="460" y="140" width="320" height="185" fill="black"/></mask>`;
const result = source.replace('</defs>', `${definitions}</defs>`).replace(
  '<g id="crest" fill="currentColor" mask="url(#no-shield-mask)">',
  '<g id="crest" fill="currentColor"><g mask="url(#no-shield-mask)"><g mask="url(#move-crown-mask)">'
).replace(
  '</g><symbol id="greyhound"',
  '</g></g><g transform="translate(262 315) scale(.4)" clip-path="url(#original-crown)"><use href="#ink"/></g></g><symbol id="greyhound"'
);
writeFileSync('public/images/product/crest-vector-v4.svg', result);
