---
name: force-site-update
description: Verify an authorised Bureau of Provisions Firebase release against its exact commit and local build, including changed image bytes and cache keys. Use after deployment or to investigate stale content; this helper performs read-only checks.
---

# Verify the delivered release

This repository builds with Vite and maintained checks through `npm run build`.
It does not use `tsc -b` or a service-worker version bump. Consult the current
`package.json`, `.github/workflows/firebase-deploy.yml`, `firebase.json` and
`scripts/asset-urls.mjs` rather than applying another site's cache workaround.

After the authorised site commit's Firebase run succeeds, run from the root:

```sh
node .opencode/skills/force-site-update/force-update.mjs --verify --commit SITE_COMMIT
```

For changed images, add one or more asset paths:

```sh
node .opencode/skills/force-site-update/force-update.mjs --verify --commit SITE_COMMIT \
  --asset /images/product/straw-up-native-v68.webp \
  --asset /images/product/edition-09-native-v68.webp
```

The helper checks that commit's successful workflow, root `no-cache` header,
actual live/local JavaScript bytes, and the selected live/local asset SHA-256s
using their content cache keys. Any mismatch fails. Use the deployed site commit
explicitly when HEAD is a later docs-only commit with no workflow run.

For a mismatch: inspect the matching CI build/deploy logs, delivered HTML,
`scripts/asset-delivery.mjs`, `scripts/asset-urls.mjs` and the responsive manifest.
Fix the demonstrated cause, run the relevant checks and stay within the user's
release authorisation. Do not push whitespace changes, invent a service-worker
cache bump or treat a matching bundle as proof that new product images shipped.
