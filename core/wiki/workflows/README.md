---
owns: "Which repeatable workflow policy applies: planning, Git, issues and pull requests, code-change safety, verification, review, documentation, and release"
volatility: stable
reviewed: 2026-10-09
---

# Workflows

Open this section when the question is what must hold during a recurring kind of work. Pages here own policy; the skills that walk them own the step order.

<!-- agentkit:begin index -->
| Page | Owns |
|---|---|
| [code-changes.md](code-changes.md) | Cross-cutting safety rules for changing code: adding dependencies, compatibility of public interfaces, schema and data migrations, and generated code |
| [documentation.md](documentation.md) | Human-facing project documentation policy: doc sync with behavior, changelog entries, localized variants, specifications, and decision records |
| [git-workflow.md](git-workflow.md) | Local Git policy: branch policy, preflight, task branches, commit convention, staging, integrating base changes, cleanup, and stop conditions |
| [issues-and-prs.md](issues-and-prs.md) | Hosting-platform conventions: issue bodies, labels, blocked issues, triage and closing, leftovers, pull request bodies, issue linking, mergeability, and review feedback |
| [planning.md](planning.md) | When work needs a written plan, where plans live, plan statuses, and how plans are closed |
| [release.md](release.md) | Project release policy: what a release unit is, version numbers, changelog finalization, tags and notes, and publishing |
| [review.md](review.md) | Review policy: which review gates a change needs, the review protocol, severity levels, dispositions, and the review output format |
| [verification.md](verification.md) | What verification each kind of change needs, how evidence is reported, flaky tests and disabled checks, and what to do when verification cannot run |
<!-- agentkit:end index -->
