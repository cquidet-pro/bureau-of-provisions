import { readFileSync, writeFileSync } from 'node:fs';

const source = readFileSync('public/images/product/crest-vector-v4.svg', 'utf8');
const arm = 'M1015 435V558H827V490Z';
const shorts = 'M980 564Q1025 584 1075 577L1086 641L1071 674L1035 660L1016 638L982 678L937 653Q949 607 980 584Z';
const definitions = `<clipPath id="forward-paw-region"><path d="${arm}"/></clipPath><mask id="leopard-tailoring-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="1266" height="1242"><rect width="1266" height="1242" fill="white"/><path d="${arm}" fill="black"/><path d="${shorts}" fill="black"/></mask><mask id="centre-monogram-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="1266" height="1242"><rect width="1266" height="1242" fill="white"/><rect x="445" y="440" width="372" height="230" fill="black"/></mask><clipPath id="monogram-lettering"><rect x="445" y="440" width="372" height="230"/></clipPath><g id="leopard-tailoring"><g transform="translate(253.75 0) scale(.75 1)"><g clip-path="url(#forward-paw-region)"><g mask="url(#no-shield-mask)"><use href="#ink"/></g></g></g><g fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"><path d="${shorts}"/><path d="M976 579Q1026 600 1077 591 M943 640L978 662 M1042 649L1077 662 M1020 593L1016 638 M989 595Q976 611 976 624"/></g></g>`;
let result=source.replace('</defs>',`${definitions}</defs>`);
result=result.replace('<use href="#ink" mask="url(#plain-band-mask)"/>','<g mask="url(#centre-monogram-mask)"><g mask="url(#leopard-tailoring-mask)"><use href="#ink" mask="url(#plain-band-mask)"/></g></g><use href="#leopard-tailoring"/><g transform="translate(35 0)" clip-path="url(#monogram-lettering)"><g mask="url(#no-shield-mask)"><use href="#ink"/></g></g>');
result=result.replace('translate(262 315) scale(.4)','translate(297 315) scale(.4)');
result=result.replace('<g fill="currentColor" clip-path="url(#leopard-clip)"><use href="#ink"/></g>','<g fill="currentColor" clip-path="url(#leopard-clip)"><g mask="url(#leopard-tailoring-mask)"><use href="#ink"/></g><use href="#leopard-tailoring"/></g>');
writeFileSync('public/images/product/crest-vector-v5.svg',result);
