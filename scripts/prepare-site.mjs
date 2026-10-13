// Inline the small local stylesheet so first paint needs no extra CSS request.
import { readFileSync, writeFileSync } from "node:fs";
import { resolve, sep } from "node:path";
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
writeFileSync(page, html);
console.log("Inlined local CSS for first paint.");
