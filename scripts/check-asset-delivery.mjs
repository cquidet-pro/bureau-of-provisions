import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { runInNewContext } from 'node:vm';

const html = readFileSync('dist/index.html', 'utf8');
const attributes = tag => Object.fromEntries([...tag.matchAll(/([\w:-]+)="([^"]*)"/g)].map(m => [m[1], m[2]]));
const images = [...html.matchAll(/<img\b[^>]*>/g)].map(m => attributes(m[0]));
const branding = images.filter(i => i['data-brand-symbol']);
assert.equal(branding.length, 95);
assert.ok(branding.filter(i => !i.class.includes('scene') && i.class !== 'header-crest').every(i => i.loading === 'lazy'));
const photos = images.filter(i => i.srcset);
assert.equal(photos.length, 38);
assert.ok(photos.every(i => i.sizes && i.width && i.height));
assert.equal(images.find(i => i.class === 'station-scene').fetchpriority, 'high');
assert.ok(!existsSync('dist/images/product/platform-strap-reference-v18.png'));
assert.ok(!existsSync('dist/images/product/crest-vector-v11.svg'));
const backgrounds = [...html.matchAll(/url\(["']?(\/images\/[^)"']+)/g)].map(m => m[1]);
assert.ok(backgrounds.length >= 3);
assert.ok(backgrounds.every(url => /\?v=[a-f0-9]{16}/.test(url)), 'CSS image URLs need content versions');
assert.match(html, /bottle-braille-message\.svg\?v=[a-f0-9]{16}#message/, 'SVG fragment must follow cache version');
const script = html.match(/<script data-asset-fallback>([\s\S]*?)<\/script>/)?.[1];
if (process.env.ASSET_CDN !== 'off') {
  assert.ok(script, 'Production build must include CDN fallback');
  assert.ok(images.every(i => i['data-local-src'] || /\?v=[a-f0-9]{16}$/.test(i.src)), 'Every image needs immutable CDN or versioned local delivery');
  assert.ok(images.filter(i => i['data-local-src']).every(i => /\?v=[a-f0-9]{16}$/.test(i['data-local-src'])));
  let onError;
  runInNewContext(script, {document:{addEventListener(type, handler, capture) {
    assert.equal(type, 'error'); assert.equal(capture, true); onError = handler;
  }}});
  const fixture = initial => {
    const attrs = {...initial};
    return {attrs, getAttribute:k => attrs[k] ?? null, removeAttribute:k => delete attrs[k], setAttribute:(k,v) => {attrs[k] = v;}};
  };
  const photo = photos[0];
  const target = fixture(photo);
  onError({target});
  assert.equal(target.attrs.src, photo['data-local-src']);
  assert.equal(target.attrs.srcset, photo['data-local-srcset']);
  assert.ok(!target.attrs['data-local-src']);
  const restored = {...target.attrs};
  onError({target});
  assert.deepEqual(target.attrs, restored, 'A local failure must not cause a retry loop');
  const svg = fixture({href:'https://cdn.example/image.webp', 'data-local-href':'/images/product/lid-strap-reference-v8.webp'});
  onError({target:svg});
  assert.equal(svg.attrs.href, '/images/product/lid-strap-reference-v8.webp');
  assert.ok(!svg.attrs['data-local-href']);
}
console.log('Asset checks passed: responsive photos, lazy branding, source exclusion and CDN recovery without retry loops.');
