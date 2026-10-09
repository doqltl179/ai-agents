# agentkit

**English** | [한국어](docs/ko/README.md) | [日本語](docs/ja/README.md)

A portable **documentation kit for AI coding agents**, installed into many projects. It keeps rules (wiki), roles (agents), procedures (skills), and language and framework knowledge (stack packs) in a single source of truth, and renders them into the files each tool reads: Claude Code, Codex, GitHub Copilot, Cursor, and Gemini CLI.

> The primary reader of every kit file is an **AI agent**. Agent-facing docs are written in English for token efficiency and tool compatibility; reports, commits, and pull requests follow the project's language (`project.language`).

## Design

| Principle | How the kit does it |
|---|---|
| **Single source of truth** | One fact has one owning file; everything else links to it. Catalogs, section indexes, and per-tool files are **generated** from source frontmatter, so they cannot drift. `check` catches broken links, duplicated sentences, stale generated files, and local edits to the installed kit. |
| **Written for agents** | Every page opens with `When` / `Route Away When`, so an agent on the wrong page leaves at once. Answers are reached in at most three hops: entry point → section index → owning page. Line budgets per file type are enforced. |
| **An organization, like a large company** | Governance, execution, quality, and evolution planes, organized into departments. Every role states what it `Owns` and what it does not, naming the neighbor that does, so roles never overlap. |
| **Fine-grained roles** | Roles are defined by **surface**, not language; language and framework knowledge comes from stack packs: `role card × stack pack × project binding` → for example a Next.js frontend specialist, a FastAPI backend specialist, or a Unity editor-tooling specialist. Projects narrow roles further with `extends`. |
| **Skills** | Procedures for issues and pull requests, worktrees, refactoring, code/dependency/schema migration, review lenses, documentation, translation, and installing and evolving the kit. Skills hold only the order; rules stay in the wiki. |
| **Never stuck in the past** | Every file carries `volatility` and `reviewed` metadata and is re-verified on a cadence; a tech radar watches tools, models, and standards; a change-intake flow absorbs what changes; `[scaffold]` rules are retired as models improve; versioned releases with migration notes reach every project. |

## How Work Flows

Every request runs the same order ([request-lifecycle.md](core/wiki/operating-model/request-lifecycle.md)):

**confirm the request → open an issue → create a worktree from `develop` → do the work → open a pull request into `develop` → register issues found along the way**.

`develop` is the development branch and `main` the release branch; `develop → main` happens only through a promotion pull request when a release is requested. Projects change these defaults in their profile.

## Layout

```text
core/                  the kit payload (copied to .ai/kit/ in projects, read-only there)
  START.md             session start router (inlined into AGENTS.md)
  wiki/                rules: principles, operating-model, workflows, evolution, integration, authoring
  agents/<department>/ role cards                        (CATALOG.md generated)
  skills/<name>/       procedures                        (CATALOG.md generated)
  stacks/<kind>/       language, framework, infra packs  (CATALOG.md generated)
  templates/           scaffolds and the project profile schema
tools/agentkit.py      install, update, sync, check, freshness, and new
.ai/project/           this repository's own overlay (the kit maintains itself with the kit)
```

The layout inside an installed project and the files generated per tool are described in [installation.md](core/wiki/integration/installation.md) and [tool-adapters.md](core/wiki/integration/tool-adapters.md). Browse the [agents](core/agents/CATALOG.md), [skills](core/skills/CATALOG.md), and [stack packs](core/stacks/CATALOG.md).

## Quick Start

Requirements: Python 3.11+ (standard library only) and Git. The GitHub skills use the `gh` CLI.

```bash
# 1. From a checkout of this repository, install into a project
python tools/agentkit.py install ../my-project --tools claude,codex,copilot

# 2. In the project, edit .ai/project/profile.toml: language, commands, active roles, path and stack bindings
#    (every key is documented in core/templates/project/profile.toml)

# 3. Render and validate
cd ../my-project
python .ai/kit/tools/agentkit.py sync
python .ai/kit/tools/agentkit.py check
```

If the project already has hand-written `AGENTS.md` or `CLAUDE.md` files, `sync` refuses to overwrite them. Ask an AI agent to run the **`kit-install` skill**: it moves their project-specific content into the overlay and fills in the profile.

### Updating

```bash
python .ai/kit/tools/agentkit.py update --from https://github.com/doqltl179/ai-agents --ref v0.1.0
```

The update refuses to run when kit files were edited locally. The kit is read-only inside projects; improvements go upstream through the `kit-upstream-propose` skill.

## Maintaining The Kit

Opening this repository with an AI tool makes the generated `AGENTS.md` the entry point for kit maintenance (`kit-librarian`, `role-governor`, `trend-scout`, and others are active).

- After editing sources: `python tools/agentkit.py sync`, then `python tools/agentkit.py check`
- Tests: `python -m unittest discover -s tools/tests -v`
- Files due for re-verification: `python tools/agentkit.py freshness`
- CI (`.github/workflows/kit-health.yml`): tests and `check` on every push and pull request, plus a weekly freshness run that opens an issue when files are overdue.
- The full evolution process: [evolution/README.md](core/wiki/evolution/README.md)

## License

[MIT](LICENSE)
