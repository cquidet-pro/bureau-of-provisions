// Run after committing new/changed delivery assets, then push both commits.
// Only content present in that immutable Git revision is sent to the CDN.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
const revision = execFileSync('git', ['rev-parse', 'HEAD'], {encoding:'utf8'}).trim();
const source = readFileSync('index.html', 'utf8') + readFileSync('src/style.css', 'utf8') + readFileSync('design/responsive-images.json', 'utf8');
const paths = [...new Set([...source.matchAll(/\/images\/product\/[\w./-]+\.(?:svg|webp|png)/g)].map(m => m[0]))].sort();
const files = {};
for (const path of paths) {
  const committed = execFileSync('git', ['show', `${revision}:public${path}`], {maxBuffer: 20 * 1024 * 1024});
  const local = readFileSync('public' + path);
  if (!local.equals(committed)) throw new Error(`Commit delivery asset before pinning: ${path}`);
  files[path] = createHash('sha256').update(local).digest('hex');
}
writeFileSync('design/asset-cdn.json', JSON.stringify({
  baseUrl: `https://cdn.jsdelivr.net/gh/cquidet-pro/bureau-of-provisions@${revision}/public`,
  files,
}, null, 2) + '\n');
console.log(`Pinned ${paths.length} delivery assets at ${revision}.`);
