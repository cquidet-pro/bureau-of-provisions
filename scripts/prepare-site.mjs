// Inline the small local stylesheet so first paint needs no extra CSS request.
import { readFileSync, writeFileSync, readdirSync, rmSync } from "node:fs";
import { resolve, sep } from "node:path";
import { prepareAssetDelivery } from './asset-delivery.mjs';
const output = resolve("dist");
const page = resolve(output, "index.html");
let html = readFileSync(page, "utf8");
// Keep bookmark icon URLs at the site root when Vite uses a relative base.
html = html.replace(/<link\b[^>]*rel="(?:icon|apple-touch-icon)"[^>]*>/g, (tag) =>
  tag.replace(/href="\.\//, 'href="/')
);
let count = 0;
html = html.replace(/<link\b[^>]*rel="stylesheet"[^>]*>/g, (tag) => {
  const href = tag.match(/href="([^"]+)"/)?.[1];
  if (!href || !href.startsWith("./assets/") || !href.endsWith(".css")) return tag;
  const path = resolve(output, href);
  if (!path.startsWith(output + sep)) throw new Error("Invalid stylesheet path");
  count++;
  return `<style>${readFileSync(path, "utf8")}</style>`;
});
if (count !== 1) throw new Error(`Expected one local stylesheet, found ${count}`);
html = prepareAssetDelivery(html);
writeFileSync(page, html);
// Apply the same CDN, fallback and cache versioning to every additional page.
function prepareOtherPages(dir) {
  for (const entry of readdirSync(dir, {withFileTypes:true})) {
    const path = resolve(dir, entry.name);
    if (entry.isDirectory()) prepareOtherPages(path);
    else if (entry.name.endsWith('.html') && path !== page) {
      writeFileSync(path, prepareAssetDelivery(readFileSync(path, 'utf8')));
    }
  }
}
prepareOtherPages(output);
// Keep source PNG masters and retired renders in the repo, outside Hosting.
// Preserve every file referenced by HTML, CSS, SVG or JS, including fallbacks.
let references = '';
function gather(dir) {
  for (const entry of readdirSync(dir, {withFileTypes:true})) {
    const path = resolve(dir, entry.name);
    if (entry.isDirectory()) gather(path);
    else if (/\.(html|css|js|svg)$/.test(entry.name)) references += readFileSync(path, 'utf8');
  }
}
gather(output);
const used = new Set([...references.matchAll(/\/images\/[\w./-]+\.(?:svg|webp|png|jpe?g|gif|avif)/g)].map(m => m[0]));
let removedBytes = 0;
function prune(dir) {
  for (const entry of readdirSync(dir, {withFileTypes:true})) {
    const path = resolve(dir, entry.name);
    if (entry.isDirectory()) prune(path);
    else if (!used.has('/' + path.slice(output.length + 1).split(sep).join('/'))) {
      removedBytes += readFileSync(path).length;
      rmSync(path);
    }
  }
}
prune(resolve(output, 'images'));
console.log("Inlined local CSS for first paint.");
console.log(`Excluded ${(removedBytes / 1e6).toFixed(1)} MB of source/unused product files from Hosting.`);
