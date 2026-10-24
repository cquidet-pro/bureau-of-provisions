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
assert.equal(origin.origin, 'https://bureauofprovisions.com', 'Advertise the custom domain to crawlers');
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
  if (tag['data-local-src']) localFile(tag['data-local-src']);
  for (const set of [tag.srcset, tag['data-local-srcset']]) {
    if (set) for (const candidate of set.split(',')) localFile(candidate.trim().split(/\s+/)[0]);
  }
}
assert.equal((html.match(/<h1\b/g) || []).length, 1);
assert.equal(tags("button").filter((tag) => tag["data-colour"]).length, 19, "Expected nineteen colour studies");
assert.equal(tags("a").filter((tag) => tag.class?.split(" ").includes("colour-register")).length, 19, "Every bottle needs a registration link");
assert.equal(tags("button").filter((tag) => tag["data-drinking-method"]).length, 3, "Expected separate straw, spout and spray modes");
assert.deepEqual(tags("button").filter(tag => tag["data-straw-position"]).map(tag => tag["data-straw-position"]), ["flat", "up"], "Straw must have only Flat/Up still positions");
assert.ok(!tags("button").some(tag => "data-drinking-hold" in tag || "data-drinking-reset" in tag), "Removed hold/reset controls must stay removed");
assert.ok(html.includes("Press to mist."), "Mist needs its direct action label");
// Validate the containers, not just strings: misplaced closing divs hid all modes.
const layoutNodes = [];
const divStack = [];
const layoutMarkup = html.replace(/<(script|style)\b[^>]*>[\s\S]*?<\/\1>/g, "").replace(/<!--[\s\S]*?-->/g, "");
for (const [tag] of layoutMarkup.matchAll(/<\/?div\b[^>]*>|<(?:button|h3|p)\b[^>]*>/g)) {
  if (tag.startsWith("</")) {
    assert.ok(divStack.length, "Unmatched closing layout container");
    divStack.pop();
    continue;
  }
  const node = {attrs:attributes(tag), raw:tag, parent:divStack.at(-1)};
  layoutNodes.push(node);
  if (/^<div\b/.test(tag)) divStack.push(node);
}
assert.equal(divStack.length, 0, "Unclosed layout containers");
const hasClass = (node, name) => node?.attrs.class?.split(/\s+/).includes(name);
const photoWrap = layoutNodes.find(node => hasClass(node, "drinking-closeup-wrap"));
const explanation = layoutNodes.find(node => hasClass(node, "viewer-explanation"));
assert.ok(hasClass(explanation?.parent, "drinking-overhead-layout"), "Explanation must occupy the right-hand grid column");
const outletLabels = layoutNodes.filter(node => node.attrs["data-drinking-part"]);
assert.equal(outletLabels.length, 3);
assert.ok(outletLabels.every(node => node.parent === photoWrap), "All outlet labels must remain inside the photo");
assert.equal(layoutNodes.find(node => hasClass(node, "drinking-controls"))?.parent, photoWrap, "Action controls belong above the photo labels");
for (const name of ["data-drinking-title", "data-drinking-description", "data-drinking-status"]) {
  assert.equal(layoutNodes.find(node => tagHasAttribute(node, name))?.parent, explanation, `${name} must remain in the explanation column`);
}
function tagHasAttribute(node, name) {
  // These data attributes are intentionally boolean; the general parser reads values only.
  return node.raw?.includes(name);
}

assert.ok(html.includes('aria-label="6. Dishwasher safe"'), "Missing sixth dishwasher-safe callout");
assert.ok(anchors.has("specifications") && anchors.has("colourways"), "Missing product sections");
assert.ok(html.includes("Design in development."), "Missing visible product-development status");
assert.ok(html.includes("<style>"), "Local CSS was not inlined");
assert.ok(!tags("link").some((tag) => tag.rel === "stylesheet" && tag.href?.startsWith("./assets/")));
// Keep the external font stylesheet off the render path on every public page.
for (const path of ['index.html', 'thank-you/index.html', '404.html']) {
  const markup = read(path);
  assert.ok(markup.includes('<style data-local-fonts>'), `Missing inline font declarations: ${path}`);
  assert.ok(!/https:\/\/fonts\.(googleapis|gstatic)\.com/.test(markup), `External font dependency: ${path}`);
  for (const [, url] of markup.matchAll(/url\((\/fonts\/[^)]+\.woff2)\)/g)) {
    localFile(url);
    assert.equal(readFileSync(resolve(root, url.slice(1))).subarray(0, 4).toString(), 'wOF2');
  }
}
const missingPage = read('404.html');
assert.match(missingPage, /name="robots" content="noindex, follow"/);
assert.match(missingPage, /href="\/"/);
assert.match(missingPage, /href="\/#colourways"/);
const hosting = JSON.parse(readFileSync('firebase.json', 'utf8')).hosting;
assert.ok(!hosting.rewrites?.some(rule => rule.source === '**' && rule.destination === '/index.html'), 'Missing URLs must retain HTTP 404');
const hero = tags('img').find(tag => tag.class === 'station-scene');
const preload = tags('link').find(tag => tag.rel === 'preload' && tag.as === 'image');
assert.ok(preload, 'Discover the LCP image in the document head');
assert.equal(preload.href, hero.src);
assert.equal(preload.imagesrcset, hero.srcset);
assert.equal(preload.imagesizes, hero.sizes);
assert.ok(anchors.has('bottle-questions'), 'Buyer questions must be readable without JavaScript');
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
