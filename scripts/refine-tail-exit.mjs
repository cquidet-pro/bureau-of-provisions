import { readFileSync, writeFileSync } from 'node:fs';

let source = readFileSync('public/images/product/crest-vector-v6.svg', 'utf8');
const oldHole = '<ellipse cx="1102" cy="640" rx="14" ry="20" transform="rotate(-18 1102 640)"';
source = source.replace(`${oldHole} fill="white"/>`, '').replace(`${oldHole}/>`, '');
// Remove the old loop at the hip, rather than preserving fragments in a hole.
const erase = '<path d="M1100 480H1190V690H1080V610L1090 580L1100 560Z" fill="black"/>';
source = source.replace(/(<mask id="leopard-tailoring-mask"[^>]*>)([\s\S]*?)(<\/mask>)/, (_,start,content,end)=>start+content+erase+end);
const tail = 'M1103 612C1122 637 1158 654 1163 620C1169 604 1145 558 1145 532C1145 506 1160 500 1166 503';
const spots = [[1117,625],[1136,637],[1155,635],[1163,616],[1160,601],[1154,580],[1149,559],[1145,538],[1149,518],[1160,507]];
const mask = `<mask id="natural-tail-spots" maskUnits="userSpaceOnUse" x="1080" y="480" width="110" height="210"><rect x="1080" y="480" width="110" height="210" fill="white"/>${spots.map(([x,y],i)=>`<ellipse cx="${x}" cy="${y}" rx="${i%2?3.8:3}" ry="2.6" transform="rotate(${i%2?25:-25} ${x} ${y})" fill="black"/>`).join('')}</mask>`;
source = source.replace('</defs>', `${mask}</defs>`);
const newTail = `<ellipse cx="1103" cy="609" rx="11" ry="15" transform="rotate(-30 1103 609)" fill="none" stroke="currentColor" stroke-width="5"/><path d="${tail}" fill="none" stroke="currentColor" stroke-width="18" stroke-linecap="round" mask="url(#natural-tail-spots)"/>`;
// The tailoring group is shared by the full crest and the strap leopard.
if (!source.includes(newTail)) {
  const seam = 'M976 579Q1032 600 1095 596 M943 640L978 662 M1050 655L1104 662 M1020 593L1016 638 M989 595Q976 611 976 624 M1060 606Q1075 613 1083 626';
  const target = `<path d="${seam}"/></g></g>`;
  if (!source.includes(target)) throw new Error('Tailoring group changed; inspect before editing.');
  source = source.replace(target, `<path d="${seam}"/></g>${newTail}</g>`);
}
writeFileSync('public/images/product/crest-vector-v7.svg', source);
