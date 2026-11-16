# Shared project tools and skills

The source files, project skills and rendering/deployment guidance are versioned.
A fresh checkout supplies the website workflow; it does not install software,
connect personal accounts or copy machine-local plugin caches.

## Two repositories

- Website: `https://github.com/cquidet-pro/bureau-of-provisions`.
- Native design: `https://github.com/cquidet-pro/water-bottle-design`.

Clone these beside one another, with their repository names as directory names.
The website manifest `design/product-design.json` identifies the native `.blend`
and its SHA. That V68 source is tracked in the design repository; the website's
`design/blender-assets/v68-strap-system.blend` is the packed accessory library.
Repository access must be granted to colleagues separately when needed.

## Discoverable skills

| Location | Purpose |
| --- | --- |
| `.agents/skills/bop-product-rendering/SKILL.md` | Website renders, proof gate, selective jobs and immediate failure diagnosis |
| `.agents/skills/bop-release/SKILL.md` | Authorised release and live verification |
| `.opencode/skills/watch-deploy/SKILL.md` | Match and monitor the exact Firebase deployment |
| `.opencode/skills/force-site-update/SKILL.md` | Verify delivered bundles, image bytes and cache keys |

The separate design repository also tracks `blender-mcp`, `blender-timeouts`,
`cap-variant-building` and `water-bottle-design` under `.agents/skills/`.
Those govern model work there; the website's current `AGENTS.md` and consolidated
guide govern website imagery. Older tool-specific timeout examples are not a
universal limit: use the current execution tool's actual session/timeout contract.

Global Codex/plugin installations are machine-specific dependencies, not project
skills. Do not copy user credentials or entire plugin caches into this repository.
The saved background render pipeline works without a Blender MCP connection.
For optional live Blender accessory work, use `docs/BLENDER_STRAP_HANDOFF.md` and
configure the colleague's own connection rather than copying personal settings.

## Reproduce the website

Use Node 22 (as in CI), then run from the website root:

```sh
npm ci
npm run build
npm run dev -- --port 4173
```

## Reproduce renders

Use Blender 5.3+ compatible with the source, Python with
`scripts/render-v68/requirements.txt`, and `rsvg-convert` (librsvg). Create the
Python environment outside the checkout; environments and tool binaries are not
committed. For example, with uv installed:

```sh
uv venv --python 3.12 ../bop-render-env
uv pip install --python ../bop-render-env/bin/python -r scripts/render-v68/requirements.txt
../bop-render-env/bin/python scripts/render-v68/rebuild.py --help
```

Pass `--blender /path/to/blender` where the default macOS path does not apply.
The rendering scripts have been validated on this project's Mac; other platforms
need their own device/prerequisite check. Begin with a small isolated GPU proof;
at the first failure stop and diagnose, per `AGENTS.md`. The prior CPU fallback
and bounded Metal tests are documented in `docs/BLENDER_GPU_DIAGNOSTICS.md`.
Keep one working scene and completed masters; select only affected editions or
states rather than repeating a whole collection.

Publication still requires the applicable user authorisation and visual sign-off.
See `docs/DESIGN_REVIEW_WORKFLOW.md` and the release skills. Firebase credentials
stay in GitHub Actions secrets; colleagues authenticate their own `gh` CLI.
