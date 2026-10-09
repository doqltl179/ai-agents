# Changelog

All notable changes to the kit. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions: [Semantic Versioning](https://semver.org/). Entry rules and migration notes are owned by [versioning.md](core/wiki/evolution/versioning.md).

## [Unreleased]

### Added
- Translation policy (`core/wiki/workflows/translation.md`): one source language, every target translated directly from it (Chinese script variants excepted), content profiling by genre and tone, localization over literal translation, glossary-enforced terminology, protected content, and verification. (minor)
- Repository settings policy (`issues-and-prs.md` «Repository Settings»): integration branch as the default branch and automatic deletion of merged head branches; `kit-install` proposes them. (minor)
- `translate` skill in the new `localization` category, the `localization-specialist` role, a project glossary template, and profile keys `docs.source_locale` and `docs.glossary`. (minor)

### Changed
- `technical-writer` owns source-language docs only; localized variants move to `localization-specialist`. (minor)
- README (English, Korean, Japanese): a step-by-step guide to using the kit in another project, covering why not to clone it into the project, install, what gets created, configuration with `kit-install`, commit, daily use, and update. (patch)

### Fixed
- Stack packs: `spring-boot` said `@MockBean`/`@SpyBean` were only deprecated (Boot 4.0 removed them) and named the old web starter in Detect; `django` named the wrong current release (6.1 is current, 5.2 remains the LTS). (patch)
- Stack packs: `pytorch` (`CUBLAS_WORKSPACE_CONFIG` is needed only up to 2.9; DataLoader workers use `forkserver` on Linux with Python 3.14+), `sql` (`IS NOT DISTINCT FROM` needs SQL Server 2022+ or SQLite 3.39+; MySQL uses `<=>`), `shell` (PowerShell 5.1 encodings and `$PSNativeCommandUseErrorActionPreference` default), `go` (`GOTOOLCHAIN=local` refuses to run a newer `go` line instead of downloading), `rust` (documented `cargo update <crate>` form). (patch)

### Reviewed
- Stack packs updated for releases as of 2026-10, each fact with an official source: `react` (19.3), `spring-boot` (4.0 baseline, 4.1), `kubernetes` (1.36, 1.37, support window), `django` (6.0, 6.1), `react-native` (0.87, Expo SDK 57), `csharp` and `aspnet-core` (.NET 11 RC, .NET 8 and 9 end of support). (patch)
- Stack packs `rust`, `shell`, `sql`, `pytorch`, and `go` verified claim by claim against official sources, with current releases added (Rust 1.99, Go 1.27, PyTorch 2.14, PowerShell 7.6 LTS). (patch)

### Migration
1. If the project keeps localized docs, enable `localization-specialist` and the `translate` skill in `.ai/project/profile.toml` (`@documentation` and `@localization` include them).
2. Set `docs.source_locale` when the docs' source language differs from `project.language`, and create the glossary at `docs.glossary` from `.ai/kit/core/templates/project/wiki/glossary.md` if it does not exist.
3. On a hosted repository, apply «Repository Settings» in `issues-and-prs.md` (default branch = integration branch, delete head branches on merge) after confirming with the user.

## [0.1.0] - 2026-10-09

### Added
- Core wiki: principles (SSOT, agent-first writing, integrity), operating model, workflows, evolution, integration, and authoring specs.
- Agent catalog of 35 surface-scoped roles across governance, product, client, server, data-ai, platform, specialty, documentation, quality, release, and evolution departments.
- Skill catalog covering Git, GitHub, code-change safety, review lenses, docs, planning, product, release, operations, and kit maintenance.
- Stack packs for languages, frameworks, and infrastructure, composed into agents through project bindings.
- `tools/agentkit.py`: install, update, sync (renders adapters for Claude Code, Codex, Copilot, Cursor, Gemini CLI), check, freshness, and scaffolding.
- Freshness metadata, tech radar, change intake, model calibration, and versioning for keeping the kit current.
- Issue-first, worktree-per-unit workflow: every unit gets an issue and its own worktree from the integration branch (`develop` by default) and a pull request back into it; `main` receives changes only through promotion. Profile keys `policy.issue_first`, `policy.worktrees`, `policy.worktree_root`, `hosting.area_labels`; skill `git-worktree-cleanup`.
- README in English, Korean, and Japanese.
