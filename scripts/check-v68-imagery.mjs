// Guard the source-aligned physical redesign and its accepted image deliveries.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
const read = path => JSON.parse(readFileSync(path, 'utf8'));
const design = read('design/product-design.json');
const proof = read('docs/v68/source-geometry-integrity.json');
const dimensions = read('docs/v68/dimension-audit.json');
const deliveries = read('docs/v68/delivery-verification.json');
const hookFit = read('docs/v68/hook-clearance.json');
assert.equal(Object.keys(hookFit.parts).length, 16);
assert.ok(hookFit.minimum_gap_mm > .25);
for (const part of Object.values(hookFit.parts)) assert.ok(Math.abs(part.intersection_mm3) < 1e-8);
assert.equal(proof.unchanged, true);
assert.deepEqual(proof.before, proof.after, 'Source mesh geometry or pose changed during rendering');
assert.equal(design.current_geometry.source_sha256, proof.source_sha256);
assert.equal(deliveries.source_model_sha256, proof.source_sha256);
assert.ok(Math.abs(dimensions.actual_body_diameter_mm - 73) < .005);
assert.ok(Math.abs(dimensions.actual_closed_height_mm - 249.1) < .005);
assert.equal(design.specifications.body_diameter_mm, 73);
assert.equal(design.specifications.overall_closed_height_mm, 249.1);
assert.equal(design.editions.length, 29);
const html = readFileSync('index.html', 'utf8');
for (const edition of design.editions) {
  assert.equal(edition.geometry_version, 'V68');
  assert.equal(edition.source_frame, 6);
  assert.equal(edition.strap_hook_reference, 'docs/v68/SWIVEL_SNAP_HOOK_REFERENCE.png');
  assert.match(edition.asset, /edition-\d{2}-native-v68\.webp$/);
  assert.ok(html.includes(edition.asset), `Missing native ${edition.name}`);
  assert.match(edition.generation_method, /^Blender Cycles/);
}
assert.ok(!/\/(?:platform-v68|lid-v68|straw-up-v68|spray-pressed-v68|bottle-cutaway-v68|edition-\d+-v68)\.webp/.test(html), 'Rejected generated product returned');
assert.ok(html.includes('/images/product/lid-native-v68.webp'));
assert.ok(html.includes('/images/product/straw-up-native-v68.webp'));
assert.ok(html.includes('/images/product/spray-pressed-native-v68.webp'));
assert.ok(html.includes('class="scene-character-details"'), 'Native product coverage lost');
assert.equal(design.references.strap_attachment, 'docs/v68/SWIVEL_SNAP_HOOK_REFERENCE.png');
assert.ok(html.includes('249.1 mm') && html.includes('179.5 mm') && html.includes('73 mm'));
assert.ok(!html.includes('207.7 mm') && !html.includes('185.4 mm') && !html.includes('Body Ø 65 mm'));
assert.equal(deliveries.lossless_file_count, 35);
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
assert.equal(sha(readFileSync('scripts/render-v68/native-studio.py')), hookFit.render_setup_sha256, 'Hook clearance requires rechecking after render geometry changes');
for (const file of deliveries.files) {
  assert.equal(file.pixel_identical, true);
  assert.equal(sha(readFileSync('public' + file.png)), file.png_sha256, `Unreviewed master: ${file.png}`);
  assert.equal(sha(readFileSync('public' + file.webp)), file.webp_sha256, `Changed lossless delivery: ${file.webp}`);
}
console.log('V68 checks passed: 29 native editions, source mesh integrity, current dimensions and 35 verified lossless deliveries.');
// User-corrected presentation rules: enforce these before every deployment.
assert.ok(!html.includes('braille-cutaway'), 'Anatomy view must not contain braille');
assert.match(html, /data-straw-position="up" aria-pressed="true"/, 'Straw must start Up');
assert.ok(!/data-straw-up[^>]*display:none/.test(html), 'Up must be visible on first paint');
const css = readFileSync('src/style.css', 'utf8');
const brailleRule = css.match(/\.colour-render-sharp \.braille-colour\s*\{([^}]+)\}/)?.[1];
const brailleWidth = Number(brailleRule?.match(/width:([\d.]+)%/)?.[1]);
assert.ok(brailleWidth >= 16 && brailleWidth <= 20, 'Catalogue braille must remain discreet relative to bottle width');
const leaders = html.match(/<svg class="product-leaders"[\s\S]*?<\/svg>/)?.[0];
for (const [cx,cy] of [[719,339],[825,324]]) {
  assert.ok(leaders.includes(`<circle cx="${cx}" cy="${cy}" r="2"/>`), 'Small straw/spout dots must stay beside openings');
}
assert.ok(leaders.includes('941,630'), 'Carry leader must touch the approved native strap position');
const scene = deliveries.files.find(f => f.png.endsWith('/platform-native-v68.png'));
assert.ok(scene.dimensions[0] >= 4608 && scene.dimensions[1] >= 3072, 'Re-render main product at display-appropriate resolution; do not enlarge old product pixels');
assert.equal(design.quality_audit.v68_update.station_frame, 48, 'Main scene straw must stay raised');
assert.deepEqual([design.preorder.price_gbp,design.preorder.price_eur,design.preorder.price_usd],[25,30,33]);
assert.equal(design.preorder.shipping_included,false);
console.log('Presentation rules passed: raised straw, small edge dots, strap leader, discreet catalogue braille, no cutaway braille and high-resolution scene.');
