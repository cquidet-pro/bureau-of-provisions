---
name: bop-release
description: Build, publish and verify authorised changes to the Bureau of Provisions website repository, including Firebase deployment tracking and live asset verification. Use when pushing or checking a release; creating a skill or editing docs alone does not authorise publishing a website.
---

# Website release

Read `PROJECT_TOOLS.md` for prerequisites. For product imagery, first follow
`AGENTS.md` and `.agents/skills/bop-product-rendering/SKILL.md`.

Run `npm run build` and inspect the scoped diff. Commit only authorised files,
including maintained image scripts, approval/evidence and lossless deliveries
when those changed. Preserve `/old/` and unrelated user files.

When the user has authorised the push, follow
`.opencode/skills/watch-deploy/SKILL.md` and
`.opencode/skills/force-site-update/SKILL.md`. These are shared, tracked project
instructions, not machine-local plugin dependencies. Match the workflow run to
the exact site commit, wait for its result, and verify the live bundles and the
changed image hashes/cache keys. A green build alone does not establish that
the expected image is live.

A skill/docs-only push may be excluded by the workflow's `paths-ignore` rules;
there is then no deployment to wait for. Report the skills commit separately
from the last deployed site commit. Never manufacture a cache-bump commit or
change unrelated files just to trigger another run.
