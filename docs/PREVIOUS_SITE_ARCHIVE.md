# Previous website at /old/

`public/old/` is the built production website from commit `dc88371d87caa1e185bb789f871d3cd1386da825`, immediately before the V68 update. It preserves the previous images, prices and interactions. The current website remains at `/`.

All archived image, font and script references are isolated beneath `/old/`; archived CDN references are localized. The current build leaves these already-built archive pages untouched. A noindex directive prevents the historical page competing with the current site in search.

The source commit is recorded in `public/old/archive.json`. To regenerate the archive explicitly, run `npm run archive:old` with that commit available in local Git history. The script builds a detached temporary worktree, copies its final output, remaps local URLs and removes the temporary checkout. It does not modify the current website source. Do not regenerate this archive merely because the main site changes.

`npm run build` checks the pinned revision, previous image and price, local asset references and preservation of the current root. The archive snapshot and its reproduction script are committed to GitHub.
