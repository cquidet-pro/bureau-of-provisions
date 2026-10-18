import { writeFileSync } from 'node:fs';

// Uncontracted English: dots 1–3 left, 4–6 right; capital indicator is dot 6.
const alphabet = ['1','12','14','145','15','124','1245','125','24','245','13','123','134','1345','135','1234','12345','1235','234','2345','136','1236','2456','1346','13456','1356'];
const cells = Object.fromEntries([... 'abcdefghijklmnopqrstuvwxyz'].map((letter, i) => [letter, alphabet[i]]));
cells[','] = '2';
cells['.'] = '256';
cells[' '] = '';
const lines = ['Stay a little', 'unreasonable.'];
const message = lines.join(' ');
const rows = lines.map(line => [...line].flatMap(letter => letter === letter.toUpperCase() && /[A-Z]/.test(letter) ? ['6', cells[letter.toLowerCase()]] : [cells[letter]]));
const circles = rows.flatMap((row, y) => row.flatMap((dots, x) => [...dots].map(dot => {
  const n = Number(dot) - 1;
  return `<circle cx="${(5 + x * 7.4 + (n >= 3 ? 2.8 : 0)).toFixed(2)}" cy="${5 + y * 15 + (n % 3) * 2.8}" r="1"/>`;
}))).join('');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 64"><title>${message}</title><g id="message" fill="currentColor">${circles}</g></svg>\n`;
writeFileSync('public/images/product/bottle-braille-message.svg', svg);
writeFileSync('docs/BOTTLE_BRAILLE_MESSAGE.json', JSON.stringify({message,code:'Uncontracted English braille',lines,unicode:rows.map(row=>row.map(dots=>String.fromCodePoint(0x2800+[...dots].reduce((mask,dot)=>mask|(1<<(Number(dot)-1)),0))).join('')),reference:'https://www.brailleauthority.org/signage/index.html',note:'Visual artwork only; physical embossed dot dimensions remain unconfirmed.'},null,2)+'\n');
