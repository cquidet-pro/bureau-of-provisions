---
name: watch-deploy
description: Watch the exact Firebase deployment for an authorised push to main in cquidet-pro/bureau-of-provisions and report the live result. Use after a site push or when asked to check a deployment; documentation-only pushes may have no run.
---

# Watch the exact deployment

The current workflow is `.github/workflows/firebase-deploy.yml`, repository
`cquidet-pro/bureau-of-provisions`, live origin `https://bureauofprovisions.com`.
Read the workflow's current triggers and `paths-ignore`; a skill/docs-only commit
may have no run. Feature branches do not deploy automatically.

After an authorised push, identify the site commit and match its run:

```sh
gh run list --repo cquidet-pro/bureau-of-provisions --commit SITE_COMMIT \
  --workflow firebase-deploy.yml --json databaseId,headSha,status,conclusion,url
```

Monitor that run using the current execution tool's nonblocking session support
and keep the user informed. `gh run watch RUN_ID --exit-status --interval 10` is
available; poll a running session rather than blocking conversation indefinitely.
On a failed run, inspect `gh run view RUN_ID --log-failed` and diagnose before a
retry. The workflow handles the specific benign Firebase "already active" retry.

After success, follow the live checks in
`.opencode/skills/force-site-update/SKILL.md`; verify the requested images as well
as JavaScript when imagery changed. Report the verified result and live URL.
Do not claim a deploy for a docs-only commit excluded by the workflow, and do not
send messages to third parties as part of this skill.
