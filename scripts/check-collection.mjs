// Guard the full collection against lost editions, branding or registration links.
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';

const manifest = JSON.parse(readFileSync('design/product-design.json', 'utf8'));
const html = readFileSync('dist/index.html', 'utf8').replace(/((?:src|href)=")\.\//g, '$1/');
const cards = [...html.matchAll(/<article class="colour-card"[\s\S]*?<\/article>/g)].map(m => m[0]);
assert.equal(manifest.editions.length, 19);
assert.equal(cards.length, 19);
assert.equal(new Set(manifest.editions.map(e => e.number)).size, 19);
const imageHashes = new Set();
for (const edition of manifest.editions) {
  const card = cards.find(c => Number(c.match(/data-colour-number="(\d+)"/)?.[1]) === edition.number);
  assert.ok(card, `Missing ${edition.name}`);
  assert.ok(card.includes(`src="${edition.asset}"`), `Stale render: ${edition.name}`);
  assert.ok(existsSync(resolve('dist', edition.asset.slice(1))), `Missing asset: ${edition.name}`);
  const source = readFileSync(resolve('public', edition.asset.slice(1).replace(/\.webp$/, '.png')));
  assert.equal(source.subarray(1, 4).toString(), 'PNG');
  const width = source.readUInt32BE(16), height = source.readUInt32BE(20);
  assert.ok(width >= 1024 && height >= 1536, `Low-resolution source: ${edition.name}`);
  assert.ok(Math.abs(width / height - 2 / 3) < .01, `Changed aspect ratio: ${edition.name}`);
  const hash = createHash('sha256').update(source).digest('hex');
  assert.ok(!imageHashes.has(hash), `Duplicated edition image: ${edition.name}`);
  imageHashes.add(hash);
  assert.ok(card.includes(`--body-colour:${edition.body}`), `Body palette: ${edition.name}`);
  assert.ok(card.includes(`--accent-colour:${edition.accent}`), `Accent palette: ${edition.name}`);
  for (const symbol of ['crest', 'greyhound', 'leopard']) {
    assert.ok(card.includes(`${manifest.branding.asset}#${symbol}`), `Lost ${symbol}: ${edition.name}`);
  }
  assert.ok(card.includes(manifest.branding.braille_asset), `Lost braille: ${edition.name}`);
  const registration = card.match(/<a class="colour-register"[^>]*href="([^"]+)"/);
  assert.ok(registration, `Missing registration: ${edition.name}`);
  const link = new URL(registration[1].replaceAll('&amp;', '&'));
  assert.equal(link.origin + link.pathname, 'https://tally.so/r/5BW7JN');
  assert.equal(link.searchParams.get('colour'), edition.name);
}
console.log('Collection checks passed: 19 current renders, palettes, exact logos, strap animals, braille and registration links.');
