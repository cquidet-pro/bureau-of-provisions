import { readFileSync, writeFileSync } from 'node:fs';

const source = readFileSync('public/images/product/crest-vector-v2.svg', 'utf8');
// Remove only the traced shield border. Leave the initials and all other ink
// in its original position; stop above the banner where the outlines meet.
const definitions = `<clipPath id="shield-border-region"><rect x="400" y="300" width="450" height="500"/></clipPath><mask id="no-shield-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="1266" height="1242"><rect width="1266" height="1242" fill="white"/><g clip-path="url(#shield-border-region)" fill="none" stroke="black" stroke-width="18"><path d="M455 353Q550 349 622 310Q716 359 830 360V507 M830 539C830 677 757 769 628 803C498 777 419 680 419 544V437"/></g></mask>`;
const result = source.replace('</defs>', `${definitions}</defs>`).replace(
  '<g id="crest" fill="currentColor">',
  '<g id="crest" fill="currentColor" mask="url(#no-shield-mask)">'
);
writeFileSync('public/images/product/crest-vector-v3.svg', result);
