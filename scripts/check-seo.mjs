// Check the deployable output, including agreement between public discovery files.
import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import { resolve, sep } from "node:path";

const root = resolve("dist");
const read = (path) => readFileSync(resolve(root, path), "utf8");
const html = read("index.html");
const attributes = (tag) => Object.fromEntries([...tag.matchAll(/([\w:-]+)="([^"]*)"/g)].map((m) => [m[1], m[2]]));
const tags = (name) => [...html.matchAll(new RegExp(`<${name}\\b[^>]*>`, "g"))].map((m) => attributes(m[0]));
const meta = (name) => {
  const matches = tags("meta").filter((tag) => tag.name === name || tag.property === name);
  assert.equal(matches.length, 1, `Expected one ${name} tag`);
  assert.ok(matches[0].content, `Empty ${name}`);
  return matches[0].content;
};
const canonicals = tags("link").filter((tag) => tag.rel === "canonical");
assert.equal(canonicals.length, 1, "Expected one canonical");
const canonical = canonicals[0].href;
const origin = new URL(canonical);
assert.equal(origin.protocol, "https:");
assert.equal(origin.pathname, "/");
assert.equal(origin.search + origin.hash, "", "Lid preferences must canonicalise to the homepage");
assert.equal(meta("og:url"), canonical);
const title = html.match(/<title>([^<]+)<\/title>/)?.[1];
assert.ok(title && /Stainless Steel Water Bottle/i.test(title));
assert.equal(meta("og:title"), title);
assert.equal(meta("twitter:title"), title);
assert.equal(meta("description"), meta("og:description"));
assert.equal(meta("description"), meta("twitter:description"));
assert.equal(meta("twitter:card"), "summary_large_image");
assert.equal(meta("twitter:image"), meta("og:image"));
assert.ok(Number(meta("og:image:width")) >= 1200);
assert.ok(Number(meta("og:image:height")) > 0);
assert.match(meta("robots"), /max-image-preview:large/);

const localFile = (url) => {
  const parsed = new URL(url, canonical);
  if (parsed.origin !== origin.origin || parsed.pathname === "/") return;
  const path = resolve(root, decodeURIComponent(parsed.pathname.slice(1)));
  assert.ok(path.startsWith(root + sep) && existsSync(path), `Missing public asset: ${url}`);
};
localFile(meta("og:image"));
const blocks = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
assert.equal(blocks.length, 1);
const schema = JSON.parse(blocks[0][1]);
assert.equal(schema["@context"], "https://schema.org");
const graph = schema["@graph"];
const ids = new Set(graph.map((item) => item["@id"]));
for (const type of ["Organization", "WebSite", "WebPage", "Product"]) {
  assert.equal(graph.filter((item) => item["@type"] === type).length, 1, `Missing ${type}`);
}
const walk = (item) => {
  if (!item || typeof item !== "object") return;
  if (item["@id"]) assert.ok(ids.has(item["@id"]), `Broken schema reference: ${item["@id"]}`);
  if (item.url) {
    assert.equal(new URL(item.url).origin, origin.origin);
    localFile(item.url);
  }
  if (typeof item.image === "string") localFile(item.image);
  for (const value of Object.values(item)) walk(value);
};
walk(graph);
const product = graph.find((item) => item["@type"] === "Product");
for (const field of ["offers", "review", "aggregateRating"]) assert.equal(product[field], undefined, `Prelaunch product cannot claim ${field}`);
const page = graph.find((item) => item["@type"] === "WebPage");
assert.equal(page.name, title);
assert.equal(page.description, meta("description"));

const anchors = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map((m) => m[1]));
for (const tag of tags("a")) {
  if (tag.href?.startsWith("#")) assert.ok(anchors.has(tag.href.slice(1)), `Broken anchor: ${tag.href}`);
}
for (const tag of tags("img")) {
  assert.ok(tag.alt !== undefined, "Image missing alt attribute");
  if (tag.src) localFile(tag.src);
}
assert.equal((html.match(/<h1\b/g) || []).length, 1);
assert.equal(tags("input").filter((tag) => tag.name === "cap_type").length, 4);
assert.ok(html.includes("Can I buy the bottle yet?"), "Missing visible early-access explanation");
assert.ok(html.includes("<style>"), "Local CSS was not inlined");
assert.ok(!tags("link").some((tag) => tag.rel === "stylesheet" && tag.href?.startsWith("./assets/")));
for (const tag of tags("script")) if (tag.src?.startsWith("./assets/")) localFile(tag.src);

const robots = read("robots.txt");
assert.match(robots, /User-agent: \*\s+Allow: \//);
assert.ok(!/^Disallow:\s*\/\s*$/m.test(robots));
assert.ok(robots.includes(`Sitemap: ${canonical}sitemap.xml`));
const sitemap = read("sitemap.xml");
const locations = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
assert.deepEqual(locations, [canonical], "Sitemap must contain only real canonical pages");
assert.match(sitemap, /<lastmod>\d{4}-\d{2}-\d{2}<\/lastmod>/);
const llms = read("llms.txt");
for (const match of llms.matchAll(/\]\((https:\/\/[^)]+)\)/g)) {
  const url = new URL(match[1]);
  assert.equal(url.origin, origin.origin, "Stale domain in llms.txt");
  if (url.hash) assert.ok(anchors.has(url.hash.slice(1)), `Broken llms anchor: ${url.hash}`);
  localFile(url.href);
}
console.log("SEO checks passed: metadata, schema, public assets, anchors, crawler files and canonical URLs.");
