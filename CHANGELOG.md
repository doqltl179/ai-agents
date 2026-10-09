# Changelog

All notable changes to the kit. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions: [Semantic Versioning](https://semver.org/). Entry rules and migration notes are owned by [versioning.md](core/wiki/evolution/versioning.md).

## [Unreleased]

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
