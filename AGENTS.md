<!-- agentkit:generated from core/START.md, .ai/project/profile.toml. Do not edit: change the source, then run `python tools/agentkit.py sync`. Paths are relative to the project root. -->

# Agent Start

This project uses agentkit: a shared wiki of rules, agent roles, skills, and stack packs. Read this once per session, classify the task, open only the smallest route below, and stop at the first page that owns your question. Do not read the whole wiki.

## Path Conventions

- Kit: read-only rules, roles, skills, and stack packs. Its root is shown in «This Project» (`.ai/kit/` in installed projects).
- Overlay `.ai/project/`: project-owned facts. `profile.toml` (parameters, commands, active roles, bindings), `agents/`, `skills/`, `wiki/`, `lessons.md`.
- Generated, never edit: `AGENTS.md`, `CLAUDE.md`, `.ai/generated/`, and the tool folders. Change the source, then run `agentkit.py sync`.
- Working records, not committed: `.ai/tasks/`.
- Paths in rendered agent files are relative to the project root.

## Where To Go

| You are about to… | Open |
|---|---|
| Handle any request from start to report | [request-lifecycle.md](core/wiki/operating-model/request-lifecycle.md) |
| Choose who does the work | [routing.md](core/wiki/operating-model/routing.md), then `.ai/generated/catalog.md` |
| Act as an owner, delegate, or hand off | [delegation.md](core/wiki/operating-model/delegation.md), [handoff-contract.md](core/wiki/operating-model/handoff-contract.md) |
| Plan non-trivial work | [planning.md](core/wiki/workflows/planning.md) |
| Run several units or agents at the same time | [concurrency.md](core/wiki/operating-model/concurrency.md) |
| Add a dependency, change a public interface, or migrate data | [code-changes.md](core/wiki/workflows/code-changes.md) |
| Start a unit (worktree, task branch) or commit | [git-workflow.md](core/wiki/workflows/git-workflow.md) |
| Open or handle an issue or pull request | [issues-and-prs.md](core/wiki/workflows/issues-and-prs.md) |
| Verify a change | [verification.md](core/wiki/workflows/verification.md) |
| Review a change | [review.md](core/wiki/workflows/review.md) |
| Change human-facing docs | [documentation.md](core/wiki/workflows/documentation.md) |
| Translate text into another language | [translation.md](core/wiki/workflows/translation.md) |
| Release, or promote the integration branch to the release branch | [release.md](core/wiki/workflows/release.md) |
| Edit agent docs (kit or overlay) | [authoring/README.md](core/wiki/authoring/README.md) |
| Store a fact, lesson, or decision | [memory-policy.md](core/wiki/operating-model/memory-policy.md) |
| Keep the kit current, or adopt outside guidance | [evolution/README.md](core/wiki/evolution/README.md) |
| Install, update, or configure the kit | [integration/README.md](core/wiki/integration/README.md) |
| Anything else | [wiki/README.md](core/wiki/README.md) |

Skills are listed in `.ai/generated/catalog.md`; run one when its trigger matches instead of improvising the procedure.

## Stop First

Each line's full rule lives on the linked page.

- Never fake success; never claim a check you did not run — [integrity.md](core/wiki/principles/integrity.md)
- Stop when the request is impossible; pause for scope expansion or a decision the user owns — [integrity.md](core/wiki/principles/integrity.md)
- Confirm before destructive, irreversible, or outward-facing actions — [integrity.md](core/wiki/principles/integrity.md)
- Each unit: issue first, its own worktree from the integration branch, pull request back into it — [request-lifecycle.md](core/wiki/operating-model/request-lifecycle.md)
- Never commit directly to a protected branch or edit files in the main checkout — [git-workflow.md](core/wiki/workflows/git-workflow.md)
- One fact, one owner: link instead of copying; never edit generated or kit files — [ssot.md](core/wiki/principles/ssot.md)
- Read narrowly and answer with the smallest complete result — [context-budget.md](core/wiki/operating-model/context-budget.md)
- Report to the user in the language set by `project.language` — [handoff-contract.md](core/wiki/operating-model/handoff-contract.md)

## This Project

- Project: **agentkit** — Portable, single-source-of-truth agent documentation kit (rules, roles, skills, stack packs, and a renderer) installed into other projects.
- Kit: version 0.1.0, this repository is the kit itself; kit root is the repository root. CLI: `python tools/agentkit.py <sync|check|freshness|new|update>`
- Overlay: `.ai/project/` · Owners and skills: `.ai/generated/catalog.md` · Project wiki: `.ai/project/wiki/README.md` · Lessons: `.ai/project/lessons.md`
- Human-facing language: `ko`

### Commands

| Key | Command |
|---|---|
| `commands.build` | `python tools/agentkit.py sync` |
| `commands.test` | `python -m unittest discover -s tools/tests -v` |
| `commands.lint` | `python tools/agentkit.py check` |

Not available (report the gap, do not guess): `install`, `format`, `typecheck`, `e2e`, `run`

### Parameters

| Key | Value |
|---|---|
| `policy.integration_branch` | develop |
| `policy.release_branch` | main |
| `policy.protected_branches` | develop, main |
| `policy.issue_first` | true |
| `policy.worktrees` | true |
| `policy.worktree_root` | .worktrees |
| `policy.max_parallel_units` | 0 |
| `policy.branch_pattern` | <type>/<scope>-<summary> |
| `policy.commit_convention` | conventional |
| `policy.commit_language` | ko |
| `hosting.platform` | github |
| `hosting.area_labels` | core, tooling, repo |
| `docs.readme` | README.md |
| `docs.changelog` | CHANGELOG.md |
| `docs.source_locale` | en |
| `docs.locales` | ko, ja |
| `docs.locale_pattern` | docs/{locale}/{name} |
| `docs.specs_dir` | .ai/project/wiki |
| `docs.adr_dir` | .ai/project/wiki/decisions |
| `docs.glossary` | docs/glossary.md |
