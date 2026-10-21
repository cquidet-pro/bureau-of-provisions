import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';

const responsive = JSON.parse(readFileSync('design/responsive-images.json', 'utf8'));
const configPath = 'design/asset-cdn.json';
const cdn = existsSync(configPath) ? JSON.parse(readFileSync(configPath, 'utf8')) : null;
const attr = (tag, name) => tag.match(new RegExp(`\\b${name}="([^"]*)"`))?.[1];

function imageSizes(tag) {
  const cls = attr(tag, 'class') || '';
  const fractions = {
    'station-detail-left': .42318, 'station-detail-right': .42058,
    'station-detail-clock': .15625, 'station-detail-floor': .20183,
    'station-detail-office': .18881, 'scene-character-detail-left': .24089,
    'scene-character-detail-right': .33594,
  };
  const fraction = Object.entries(fractions).find(([name]) => cls.split(' ').includes(name))?.[1];
  if (fraction || cls === 'station-scene') {
    const f = fraction || 1;
    return `(min-width: 1001px) min(${(90 * f).toFixed(3)}vw, calc(${(150 * f).toFixed(3)}svh - ${(240 * f).toFixed(3)}px)), ${(90 * f).toFixed(3)}vw`;
  }
  if (attr(tag, 'src')?.includes('edition-')) {
    // Include the enlarged registration preview; never undersize that copy.
    return '(max-width: 640px) 45vw, (max-width: 1100px) 30vw, 330px';
  }
  return '(max-width: 760px) min(90vw, 510px), min(36vw, 510px)';
}

export function prepareAssetDelivery(html) {
  html = html.replace(/((?:src|href)=")\.\/images\/product\//g, '$1/images/product/');
  let responsiveCount = 0, cdnCount = 0;
  const cached = new Map();
  function cdnUrl(url) {
    if (!cdn || process.env.ASSET_CDN === 'off') return url;
    const path = url.split('#')[0];
    if (!cdn.files[path]) return url;
    if (!cached.has(path)) {
      const hash = createHash('sha256').update(readFileSync('public' + path)).digest('hex');
      cached.set(path, hash === cdn.files[path]);
      if (!cached.get(path)) console.warn(`Changed asset stays local until CDN is repinned: ${path}`);
    }
    return cached.get(path) ? cdn.baseUrl + url : url;
  }
  html = html.replace(/<img\b[^>]*>/g, tag => {
    const src = attr(tag, 'src');
    if (!src?.startsWith('/images/product/')) return tag;
    if (!tag.includes('decoding=')) tag = tag.replace('<img ', '<img decoding="async" ');
    let localSrcset;
    if (responsive[src]) {
      const master = readFileSync('public' + src.replace(/\.webp$/, '.png'));
      if (createHash('sha256').update(master).digest('hex') !== responsive[src].master_sha256) {
        throw new Error(`Regenerate responsive sizes from changed master: ${src}`);
      }
      const variants = responsive[src].variants;
      localSrcset = variants.map(v => `${v.src} ${v.width}w`).join(', ');
      const srcset = variants.map(v => `${cdnUrl(v.src)} ${v.width}w`).join(', ');
      tag = tag.replace('<img ', `<img srcset="${srcset}" sizes="${imageSizes(tag)}" `);
      responsiveCount++;
    }
    const delivered = cdnUrl(src);
    if (delivered !== src) {
      tag = tag.replace(`src="${src}"`, `src="${delivered}" data-local-src="${src}"${localSrcset ? ` data-local-srcset="${localSrcset}"` : ''}`);
      cdnCount++;
    }
    return tag;
  });
  html = html.replace(/<image\b[^>]*>/g, tag => {
    const href = attr(tag, 'href');
    if (!href?.startsWith('/images/product/')) return tag;
    const delivered = cdnUrl(href);
    if (delivered === href) return tag;
    cdnCount++;
    return tag.replace(`href="${href}"`, `href="${delivered}" data-local-href="${href}"`);
  });
  if (cdnCount) {
    // Capture early image failures before the module or body has loaded.
    const fallback = `<script data-asset-fallback>document.addEventListener('error',function(e){var t=e.target;if(!t.getAttribute)return;var s=t.getAttribute('data-local-src'),h=t.getAttribute('data-local-href');if(s){var ss=t.getAttribute('data-local-srcset');t.removeAttribute('data-local-src');t.removeAttribute('data-local-srcset');t.removeAttribute('srcset');if(ss)t.setAttribute('srcset',ss);t.setAttribute('src',s);}else if(h){t.removeAttribute('data-local-href');t.setAttribute('href',h);}},true);</script>`;
    html = html.replace('</head>', `<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />${fallback}</head>`);
  }
  console.log(`Image delivery: ${responsiveCount} responsive photos, ${cdnCount} CDN images with local fallbacks.`);
  return html;
}
