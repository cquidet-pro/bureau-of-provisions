# Search and discovery

Reviewed 24 October 2026. Production origin: `https://bureauofprovisions.com/`.

See [SEO Site Checkup findings, fixes and self-review](SEO_REPORT_REVIEW_2026-10-24.md) for the owner-supplied audit and decisions on every failure/warning.

## Reference review

Adapted the relevant work and remaining recommendations from `../learn-draw/docs/seo.md`, `TODO.md`, the SEO notes in `CLAUDE.md`, and its crawler/hosting configuration. Bureau already delivers static HTML, so the drawing site's SPA prerendering, lesson catalogues, translated pages, HowTo markup, video sitemap and application manifest do not apply here.

Competitor pages reviewed:

- [Ion8 metal water bottles with straws](https://www.ion8.co.uk/collections/metal-water-bottle-with-straw): explicit product-category wording and material/feature descriptions.
- [Ion8 Primo Urban](https://www.ion8.co.uk/collections/primo-urban): explains lid features through everyday uses.
- [Stanley UK](https://uk.stanley1913.com/): clear product/category navigation and linked buying/care guides.
- [Stanley water bottles with straws](https://uk.stanley1913.com/collections/water-bottles-with-straws): a dedicated category page and practical questions about lid choice, cleaning and use.

The useful pattern is readable product information that matches what visitors ask. Bureau now names the double-wall stainless steel water bottle and folding steel straw in its visible copy, and answers materials, lid choice, folding motion and purchase availability in a compact disclosure section. This is an adaptation of the approach, not copied competitor text. Competitor performance claims, reviews, certifications and care instructions are not evidence about our design.

## Implemented

- Product-focused title and description, while retaining the existing brand headline.
- One absolute canonical homepage URL. `?cap=1` through `?cap=4` are preference states, not separate indexable products.
- Consistent Open Graph and Twitter large-image metadata, using the existing 1536 × 1024 product-design image with its real dimensions and an absolute URL.
- Linked Organization, WebSite, WebPage and descriptive Product JSON-LD. The Product has no price, availability, ratings or reviews. It describes a design and is not currently eligible for an offer/review-based Google product rich result.
- `public/robots.txt` allows crawlers and points to the sitemap. The wildcard includes search and AI crawlers; bot-specific duplicate rules are unnecessary.
- `public/sitemap.xml` lists the one canonical page. Section anchors and lid query parameters are not separate pages.
- `public/llms.txt` provides an optional plain-text summary with links, product-design status and the limits of campaign imagery. This is a discovery convention, not a ranking guarantee.
- The public HTML exposes product copy without JavaScript, a login or a consent gate. The wildcard crawler policy permits AI search/retrieval agents such as OAI-SearchBot and Claude-SearchBot. Search indexing and model-training crawlers are separate; allowing a crawler does not establish that it has indexed the site. User-agent smoke checks cannot prove accessibility from a provider's actual IP ranges.
- Static, keyboard-accessible bottle questions with links to the existing picker and registration. No FAQ rich-result claim or FAQPage markup.
- Build-time inlining of the small local stylesheet removes a CSS fetch from first paint. Fraunces and Inter are self-hosted WOFF2 files with inline font declarations and `font-display: swap`. Responsive hero preloading, accurate collection/registration-preview sizes, lazy lower-page images and low-priority scene restoration tiles support loading performance.
- Firebase no-cache headers for HTML and crawler files, one-day revalidation for mutable image paths, and long-lived caching for hashed application assets.
- `npm run build` includes deploy-output checks for canonical/metadata agreement, structured-data references, existing public assets, internal links, crawler files and the four static lid options. `npm run check:seo` checks an existing build separately. CI already runs the build before deploying.

## Maintenance

Update sitemap `lastmod` only when the page has a significant content change. Do not replace it with the current build date. The current date reflects the 24 October 2026 buyer FAQ and description update. When the site grows, add only real, substantive pages with their own canonical URLs, titles and descriptions; do not create thin pages for keyword variants.

The custom domain is reflected in the canonical, Open Graph URLs, JSON-LD IDs/URLs, sitemap and llms links. If the production hostname changes again, update these together and redirect old hostnames consistently. Do not deploy placeholder domains or verification tokens.

When sales open, add verified specifications, price/availability and appropriate Offer data. The page now includes approved CAD dimensions, nominal capacity, £39 pre-order price, international shipping and dishwasher-safe cleaning. Add validated insulation performance, detailed cleaning guidance, replacement parts, warranty and other buying/care content only after these details are established. Dedicated product and care pages will then be useful, following the competitors' category-and-guide approach.

## Account setup and follow-up

- Google Search Console setup is completed, as confirmed by the owner on 13 October 2026. Sitemap submission and actual indexing status have not been independently verified. Submit or check `https://bureauofprovisions.com/sitemap.xml` after publication. Firebase's shared `web.app` parent domain is not a domain property we control; use the actual verified property rather than adding a placeholder token.
- Verify the same site in Bing Webmaster Tools (or import the verified Search Console property), then submit the sitemap.
- Review indexing, queries, impressions and Core Web Vitals after enough live traffic is available. No ranking or indexing outcome has been claimed from local checks.
- Confirm an analytics provider and account before adding tracking. The drawing site's analytics identifier must not be reused here.
- Earn relevant press and referring links once there is a public launch story. Automated backlink creation was not carried over.

## Technical references

- [Google canonical URL guidance for ecommerce](https://developers.google.com/search/docs/specialty/ecommerce/designing-a-url-structure-for-ecommerce-sites)
- [Google sitemap guidance and meaningful lastmod dates](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization)
- [Product snippet requirements](https://developers.google.com/search/docs/appearance/structured-data/product-snippet)
- [OpenAI search, training and user-request crawlers](https://developers.openai.com/api/docs/bots)
- [Anthropic search, training and retrieval crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler)
- [The llms.txt proposal](https://github.com/answerdotai/llms-txt)
