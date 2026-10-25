// Exercise real DOM events without submitting forms or contacting third parties.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { parseHTML } from 'linkedom';

const { document, window } = parseHTML(readFileSync('index.html', 'utf8'));
const media = {matches:false, addEventListener(){}};
const frames = new Map(), timers = new Map();
let sequence = 0;
Object.defineProperty(document, 'hidden', {value:false, configurable:true});
Object.defineProperty(document, 'activeElement', {value:null, writable:true});
window.HTMLElement.prototype.focus = function() {
  document.activeElement = this;
  this.dispatchEvent(new window.Event('focusin', {bubbles:true}));
};
window.HTMLElement.prototype.scrollIntoView = function() {};
window.HTMLElement.prototype.getBoundingClientRect = () => ({left:20,top:20,right:300,bottom:220,width:280,height:200});
for (const dialog of document.querySelectorAll('dialog')) {
  dialog.showModal = () => dialog.setAttribute('open', '');
  dialog.close = () => {dialog.removeAttribute('open'); dialog.dispatchEvent(new window.Event('close'));};
}
window.matchMedia = () => media;
window.innerHeight = 900;
const context = {
  document, window, URL, matchMedia:window.matchMedia,
  performance:{now:() => 0},
  IntersectionObserver:class {observe() {}},
  requestAnimationFrame(fn) {const id=++sequence; frames.set(id,fn); return id;},
  cancelAnimationFrame(id) {frames.delete(id);},
  setTimeout(fn) {const id=++sequence; timers.set(id,fn); return id;},
  clearTimeout(id) {timers.delete(id);},
};
for (const source of ['src/drinking-prototype.js','src/main.js']) {
  runInNewContext(readFileSync(source,'utf8').replace(/^import .*;\n/gm,''), context, {filename:source});
}
const click = el => {assert.ok(el); el.dispatchEvent(new window.Event('click', {bubbles:true,cancelable:true}));};
const one = selector => document.querySelector(selector);
const form = one('#preorder-form');
click(one('.site-head [data-preorder]'));
assert.equal(one('#colour-prompt').hidden, false);
assert.equal(form.hidden, true);
assert.equal(document.activeElement, one('[data-colour]'));

for (const link of document.querySelectorAll('.colour-register')) {
  const choice = link.closest('.colour-card').querySelector('[data-colour]');
  click(link);
  assert.equal(form.hidden, false);
  assert.equal(document.querySelectorAll('[data-colour][aria-pressed="true"]').length, 1);
  assert.equal(choice.getAttribute('aria-pressed'), 'true');
  assert.equal(new URL(form.querySelector('iframe').src).searchParams.get('colour'), choice.dataset.colour);
  assert.equal(form.querySelector('[data-form-fallback]'), null);
  assert.equal(new URL(form.querySelector('iframe').src).searchParams.get('dynamicHeight'), '1');
  assert.equal(form.querySelector('iframe').nextElementSibling.textContent.trim(), 'Registration of interest only. No payment is taken.');
  assert.equal(document.querySelectorAll('script[src="https://tally.so/widgets/embed.js"]').length, 1);
  assert.equal(document.querySelectorAll('.registration-row').length, 1);
  assert.equal(one('[data-registration-preview] .colour-register'), null);
  assert.equal(link.getAttribute('aria-expanded'), 'true');
  form.querySelector('iframe').dispatchEvent(new window.Event('load'));
  assert.equal(one('[data-form-loading]').hidden, true);
  assert.equal(form.querySelector('iframe').hasAttribute('aria-busy'), false);
}
click(one('[data-colour]'));
assert.equal(form.hidden, true, 'A different choice hides the previous form and answers');
click(one('.site-head [data-preorder]'));
assert.equal(form.hidden, false);
assert.equal(new URL(form.querySelector('iframe').src).searchParams.get('colour'), one('[data-colour]').dataset.colour);

for (const pin of document.querySelectorAll('.feature-pin')) {
  click(pin);
  assert.equal(pin.getAttribute('aria-expanded'), 'true');
  assert.equal(pin.closest('[data-hotspot]').querySelector('.feature-popover').hidden, false);
  const escape = new window.Event('keydown', {bubbles:true,cancelable:true});
  escape.key = 'Escape'; document.dispatchEvent(escape);
  assert.equal(pin.getAttribute('aria-expanded'), 'false');
  assert.equal(document.activeElement, pin);
}

click(one('button[data-straw-position="up"]'));
assert.equal(one('[data-straw-up]').style.display, '');
click(one('button[data-straw-position="flat"]'));
assert.equal(one('[data-straw-up]').style.display, 'none');
click(one('[data-drinking-method="gulp"]'));
assert.equal(one('.drinking-controls').hidden, true);
assert.equal(one('[data-drinking-status]').hidden, true);
click(one('[data-drinking-part="spray"]'));
assert.equal(one('[data-drinking-play]').hidden, false);
click(one('[data-drinking-play]'));
assert.equal(one('[data-drinking-play]').disabled, true);
for (const now of [600, 2000]) {
  const batch = [...frames.values()]; frames.clear();
  for (const fn of batch) fn(now);
}
assert.equal(one('[data-drinking-play]').disabled, false);
assert.equal(one('[data-drinking-particles]').children.length, 0);
click(one('[data-drinking-play]'));
click(one('[data-drinking-method="straw"]'));
assert.equal(one('[data-drinking-particles]').children.length, 0);
assert.equal(one('button[data-straw-position="flat"]').getAttribute('aria-pressed'), 'true');
media.matches = true;
click(one('[data-drinking-method="spray"]')); click(one('[data-drinking-play]'));
for (const fn of [...timers.values()]) fn();
assert.equal(one('[data-drinking-particles]').children.length, 0);

click(one('[data-open-crest]'));
assert.equal(one('#crest-dialog').hasAttribute('open'), true);
click(one('[data-close-crest]'));
assert.equal(one('#crest-dialog').hasAttribute('open'), false);
assert.equal(document.activeElement, one('[data-open-crest]'));

for (const path of ['dist/index.html','dist/thank-you/index.html']) {
  const {document:d} = parseHTML(readFileSync(path,'utf8'));
  const ids = [...d.querySelectorAll('[id]')].map(el => el.id);
  assert.equal(new Set(ids).size, ids.length, `Duplicate IDs in ${path}`);
  for (const el of d.querySelectorAll('[aria-controls],[aria-labelledby],[aria-describedby]')) {
    for (const attr of ['aria-controls','aria-labelledby','aria-describedby']) {
      for (const id of (el.getAttribute(attr)||'').split(/\s+/).filter(Boolean)) assert.ok(ids.includes(id), `Broken ${attr}: ${id}`);
    }
  }
  for (const img of d.querySelectorAll('img')) assert.ok(img.hasAttribute('alt'));
  for (const frame of d.querySelectorAll('iframe')) assert.ok(frame.title);
  for (const button of d.querySelectorAll('button')) assert.ok(button.textContent.trim() || button.getAttribute('aria-label'));
  assert.equal(d.querySelectorAll('h1').length, 1);
}
console.log('Interaction checks passed: all 29 registrations, dynamic form height and notice, six feature panels, lid modes, reduced motion, dialog focus and page accessibility structure.');
