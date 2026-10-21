// Regression: overwrite an existing filename, commit it, then build again.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createAssetUrls } from './asset-urls.mjs';

const root = mkdtempSync(join(tmpdir(), 'bop-cache-update-'));
const git = args => execFileSync('git', args, {cwd:root, stdio:['ignore','pipe','pipe']}).toString().trim();
const commit = () => {
  git(['add', 'public']);
  git(['-c','user.name=Cache regression','-c','user.email=cache@example.invalid','commit','-m','Update fixture']);
  return git(['rev-parse','HEAD']);
};
const path = '/images/fixture.svg';
const hash = value => createHash('sha256').update(value).digest('hex');
const cdnEnabled = process.env.ASSET_CDN;
try {
  delete process.env.ASSET_CDN;
  mkdirSync(root + '/public/images', {recursive:true});
  git(['init', '-q']);
  writeFileSync(root + '/public' + path, 'first artwork');
  const first = commit();
  const config = {baseUrl:`https://cdn.jsdelivr.net/gh/cquidet-pro/bureau-of-provisions@${first}/public`, files:{[path]:hash('first artwork')}};
  const old = createAssetUrls(config, root);
  assert.equal(old.cdn(path), config.baseUrl + path);
  const firstLocal = old.local(path + '#message');
  assert.equal(firstLocal, `${path}?v=${hash('first artwork').slice(0,16)}#message`);

  // Same filename, new bytes, no hand-edited CDN manifest.
  writeFileSync(root + '/public' + path, 'updated artwork');
  writeFileSync(root + '/public/images/new.svg', 'new artwork');
  const second = commit();
  const updated = createAssetUrls(config, root);
  assert.equal(updated.cdn(path), config.baseUrl.replace(first, second) + path);
  assert.equal(updated.cdn('/images/new.svg'), config.baseUrl.replace(first, second) + '/images/new.svg');
  assert.notEqual(updated.local(path + '#message'), firstLocal);
  assert.ok(updated.local(path + '#message').endsWith('#message'));
  assert.equal(updated.local(updated.local(path)), updated.local(path), 'Versioning must be idempotent');

  // Previewing an uncommitted change must never request old committed bytes.
  writeFileSync(root + '/public' + path, 'uncommitted artwork');
  const preview = createAssetUrls(config, root);
  assert.equal(preview.cdn(path), path);
  assert.equal(preview.local(path), `${path}?v=${hash('uncommitted artwork').slice(0,16)}`);
  process.env.ASSET_CDN = 'off';
  assert.equal(updated.cdn(path), path);
} finally {
  if (cdnEnabled === undefined) delete process.env.ASSET_CDN;
  else process.env.ASSET_CDN = cdnEnabled;
  rmSync(root, {recursive:true, force:true});
}
console.log('Cache update checks passed: changed/new committed artwork, uncommitted previews and fallback cache keys.');
