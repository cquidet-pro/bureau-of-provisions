import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync, existsSync } from 'node:fs';

// Keep unchanged assets on their existing URL. Changed committed files use the
// current immutable Git revision; uncommitted files use versioned local URLs.
export function createAssetUrls(config, root = process.cwd()) {
  const files = new Map();
  let revision;
  const git = args => execFileSync('git', args, {cwd:root, maxBuffer:20 * 1024 * 1024, stdio:['ignore','pipe','ignore']});
  function file(url) {
    const path = url.split(/[?#]/)[0];
    if (!path.startsWith('/') || !existsSync(root + '/public' + path)) return null;
    if (!files.has(path)) {
      const bytes = readFileSync(root + '/public' + path);
      files.set(path, {path, bytes, hash:createHash('sha256').update(bytes).digest('hex')});
    }
    return files.get(path);
  }
  function local(url) {
    const asset = file(url);
    if (!asset) return url;
    const fragment = url.includes('#') ? url.slice(url.indexOf('#')) : '';
    return `${asset.path}?v=${asset.hash.slice(0,16)}${fragment}`;
  }
  function cdn(url) {
    if (!config || process.env.ASSET_CDN === 'off') return url;
    const asset = file(url);
    if (!asset) return url;
    if (asset.hash === config.files[asset.path]) return config.baseUrl + url;
    if (asset.cdnUrl === undefined) {
      asset.cdnUrl = null;
      try {
        revision ??= git(['rev-parse', 'HEAD']).toString().trim();
        if (git(['show', `${revision}:public${asset.path}`]).equals(asset.bytes)) {
          const base = config.baseUrl.replace(/@[a-f0-9]{40}\/public$/, `@${revision}/public`);
          if (/@[a-f0-9]{40}\/public$/.test(base)) asset.cdnUrl = base + url;
        }
      } catch { /* Local/uncommitted work stays on content-versioned Firebase URLs. */ }
    }
    return asset.cdnUrl || url;
  }
  return {local, cdn};
}
