import { readFileSync, writeFileSync } from 'node:fs';

let svg=readFileSync('public/images/product/crest-vector-v7.svg','utf8');
const oldShorts='M980 564Q1030 584 1082 578Q1101 580 1110 597L1122 644L1104 676L1048 668L1016 638L982 678L937 653Q949 607 980 584Z';
const shorts='M980 564Q1028 584 1075 577Q1094 581 1100 597L1105 651L1080 675L1040 660L1016 638L982 678L937 653Q949 607 980 584Z';
svg=svg.replaceAll(oldShorts,shorts);
svg=svg.replace('M976 579Q1032 600 1095 596 M943 640L978 662 M1050 655L1104 662 M1020 593L1016 638 M989 595Q976 611 976 624 M1060 606Q1075 613 1083 626', 'M976 579Q1029 600 1092 595 M943 640L978 662 M1046 650L1084 662 M1020 593L1016 638 M989 595Q976 611 976 624 M1055 606Q1067 613 1073 626');
svg=svg.replace('<ellipse cx="1103" cy="609" rx="11" ry="15" transform="rotate(-30 1103 609)" fill="none" stroke="currentColor" stroke-width="5"/>','<path d="M1082 596Q1076 586 1087 580" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>');
svg=svg.replace('M1103 612C1122 637 1158 654 1163 620C1169 604 1145 558 1145 532C1145 506 1160 500 1166 503','M1087 588C1116 601 1155 585 1155 549C1155 533 1141 516 1145 504C1151 489 1165 494 1166 502');
const spots=[[1099,591],[1117,591],[1135,584],[1148,570],[1155,551],[1150,532],[1145,514],[1148,500],[1160,496]];
svg=svg.replace(/(<mask id="natural-tail-spots"[^>]*>)[\s\S]*?(<\/mask>)/,(_,open,close)=>open+'<rect x="1060" y="480" width="130" height="210" fill="white"/>'+spots.map(([x,y],i)=>`<ellipse cx="${x}" cy="${y}" rx="${i%2?3.8:3}" ry="2.6" transform="rotate(${i%2?25:-25} ${x} ${y})" fill="black"/>`).join('')+close);
svg=svg.replace('id="natural-tail-spots" maskUnits="userSpaceOnUse" x="1080" y="480" width="110"','id="natural-tail-spots" maskUnits="userSpaceOnUse" x="1060" y="480" width="130"');
writeFileSync('public/images/product/crest-vector-v8.svg',svg);
