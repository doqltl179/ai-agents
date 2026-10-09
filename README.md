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

## Using agentkit In Your Project

You do not copy this repository into your project. Keep a checkout anywhere **outside** the project and run its `install` command: it copies only the kit itself into the project and generates, at the project root, the files each AI tool reads.

> **Why not clone this repository into the project?** AI tools read instruction files such as `CLAUDE.md` from the project root, so a repository nested in a subfolder is not picked up as your project's instructions. Worse, tools also load instruction files from subfolders they read, and this repository's own `AGENTS.md` and `CLAUDE.md` are written for maintaining the kit itself, so unrelated instructions would leak into your project's sessions.

### 1. Install

Requirements: Python 3.11+ (standard library only) and Git. The GitHub skills also use the `gh` CLI.

```bash
# Get the kit anywhere outside your project; you can delete this copy after installing
git clone --depth 1 --branch main https://github.com/doqltl179/ai-agents agentkit

# Install it into your project
python agentkit/tools/agentkit.py install path/to/my-project --tools claude,codex,copilot
```

- `main` holds released versions and `develop` holds unreleased changes. To pin a version, clone its release tag with `--branch v<version>`.
- `--tools` selects the AI tools to generate files for: `claude`, `codex`, `copilot`, `cursor`, `gemini`.

### 2. What Gets Created

```text
my-project/
  AGENTS.md, CLAUDE.md      generated entry files: tools read them at session start
  .claude/ .codex/ .agents/ .github/…   generated agents, skills, and rules for each tool
  .ai/kit/                  the kit itself (rules, roles, skills, stack packs, CLI); read-only
  .ai/project/              your project's settings: profile.toml, wiki/, lessons.md
  .ai/generated/            the catalog of active roles and skills
  .gitignore                adds .ai/tasks/ and .worktrees/
```

The install never overwrites hand-written `AGENTS.md`, `CLAUDE.md`, or tool files; it stops and lists them so their content can be moved in the next step.

### 3. Configure It For Your Project

Open the project with your AI tool and ask it to **run the `kit-install` skill**. The skill:

- reads the codebase and fills in `.ai/project/profile.toml`: the language for reports, build and test commands, the active roles, and the paths and stack packs each role owns;
- moves the content of hand-written instruction files into `.ai/project/`, deleting those files only after you confirm;
- proposes the repository settings the workflow expects (a `develop` branch, `develop` as the default branch, automatic deletion of merged branches) and applies them only after you confirm.

To configure by hand, edit `.ai/project/profile.toml` (every key is documented in `.ai/kit/core/templates/project/profile.toml`) and run `python .ai/kit/tools/agentkit.py sync`.

### 4. Commit

Commit `.ai/kit/`, `.ai/project/`, `.ai/generated/`, and the generated files (`AGENTS.md`, `CLAUDE.md`, `.claude/`, and the rest), so every teammate and every AI tool works from the same setup. Adding `python .ai/kit/tools/agentkit.py check` to CI catches hand-edited generated files and local edits to the kit.

### 5. Work With It

Ask your AI tool for work as usual: the agent reads `AGENTS.md` and follows [How Work Flows](#how-work-flows). You can also run a skill directly, for example `/translate` in Claude Code. Keep project-specific facts in `.ai/project/` and run `sync` after changing them; never edit `.ai/kit/` or the generated files.

### 6. Update

```bash
python .ai/kit/tools/agentkit.py update --from https://github.com/doqltl179/ai-agents --ref main
```

The update replaces `.ai/kit/`, prints what changed since your version together with any migration steps, and regenerates the files. It refuses to run when kit files were edited locally: the kit is read-only inside projects, and improvements go to this repository through the `kit-upstream-propose` skill.

## Repository Layout

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

## Maintaining The Kit

Opening this repository with an AI tool makes the generated `AGENTS.md` the entry point for kit maintenance (`kit-librarian`, `role-governor`, `trend-scout`, and others are active).

- After editing sources: `python tools/agentkit.py sync`, then `python tools/agentkit.py check`
- Tests: `python -m unittest discover -s tools/tests -v`
- Files due for re-verification: `python tools/agentkit.py freshness`
- CI (`.github/workflows/kit-health.yml`): tests and `check` on every push and pull request, plus a weekly freshness run that opens an issue when files are overdue.
- The full evolution process: [evolution/README.md](core/wiki/evolution/README.md)

## License

[MIT](LICENSE)
