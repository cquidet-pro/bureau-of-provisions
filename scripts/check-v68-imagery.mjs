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
assert.equal(deliveries.lossless_file_count, 36);
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
assert.equal(sha(readFileSync('scripts/render-v68/native-studio.py')), hookFit.render_setup_sha256, 'Hook clearance requires rechecking after render geometry changes');
for (const file of deliveries.files) {
  assert.equal(file.pixel_identical, true);
  assert.equal(sha(readFileSync('public' + file.png)), file.png_sha256, `Unreviewed master: ${file.png}`);
  assert.equal(sha(readFileSync('public' + file.webp)), file.webp_sha256, `Changed lossless delivery: ${file.webp}`);
}
console.log('V68 checks passed: 29 native editions, source mesh integrity, current dimensions and 36 verified lossless deliveries.');
// User-corrected presentation rules: enforce these before every deployment.
assert.ok(!html.includes('braille-cutaway'), 'Anatomy view must not contain braille');
assert.match(html, /data-straw-position="up" aria-pressed="true"/, 'Straw must start Up');
assert.ok(!/data-straw-up[^>]*display:none/.test(html), 'Up must be visible on first paint');
const css = readFileSync('src/style.css', 'utf8');
const brailleRule = css.match(/\.colour-render-sharp \.braille-colour\s*\{([^}]+)\}/)?.[1];
const brailleWidth = Number(brailleRule?.match(/width:([\d.]+)%/)?.[1]);
assert.ok(brailleWidth >= 16 && brailleWidth <= 20, 'Catalogue braille must remain discreet relative to bottle width');
const leaders = html.match(/<svg class="product-leaders"[\s\S]*?<\/svg>/)?.[0];
for (const [cx,cy] of [[722,388],[821,384]]) {
  assert.ok(leaders.includes(`<circle cx="${cx}" cy="${cy}" r="2"/>`), 'Small straw/spout dots must stay beside openings');
}
assert.ok(leaders.includes('929,690'), 'Carry leader must touch the approved native strap position');
const scene = deliveries.files.find(f => f.png.endsWith('/platform-native-v68.png'));
assert.ok(scene.dimensions[0] >= 4608 && scene.dimensions[1] >= 3072, 'Re-render main product at display-appropriate resolution; do not enlarge old product pixels');
assert.equal(design.quality_audit.v68_update.station_frame, 48, 'Main scene straw must stay raised');
assert.equal(design.preorder.prices_visible,false);
assert.ok(!/£\d|€\d|\$\d/.test(html), 'Current site must not show a price');
console.log('Presentation rules passed: raised straw, small edge dots, strap leader, discreet catalogue braille, no cutaway braille and high-resolution scene.');

const cameras=read('docs/v68/front-camera-record.json');
for (const name of ['catalogue','lid','main_scene']) {
 assert.equal(cameras[name].horizontal_view_degrees,0);
 assert.equal(cameras[name].position_m[0],0);
 assert.equal(cameras[name].target_m[0],0);
}
assert.equal(read('docs/v68/section-record.json').open_lid_pose_degrees,90);
assert.ok(html.includes('lid-closed-native-v68.webp'));
const presentation=read('docs/v68/strap-presentation.json');
assert.equal(presentation.release_lever,'above on both hooks');
assert.ok(presentation.checks.every(c=>c.lower_bar_covered));
console.log('Approved corrections passed: front-facing views, 90-degree open lid, closed lid control and concealed strap hardware.');

const calibration=read('docs/v68/catalogue-branding-calibration.json');
for(const [name,selector] of [['greyhound','strap-colour-dog'],['leopard','strap-colour-leopard']]) {
 const rule=css.match(new RegExp('\\.'+selector+'\\s*\\{([^}]+)\\}'))?.[1];
 assert.ok(rule);
 for(const [property,key] of [['left','left_percent'],['top','top_percent']]) {
  const value=Number(rule.match(new RegExp(property+':([\\d.]+)%'))?.[1]);
  assert.ok(Math.abs(value-calibration[name][key])<.003,selector+' must stay centred on its projected strap');
 }
}
