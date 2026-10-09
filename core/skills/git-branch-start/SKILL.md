---
name: git-branch-start
description: "Start a task branch: run the preflight, then cut a task branch from the latest remote integration branch, named per the branch policy, stopping on any unexpected repository state. Use when a bounded unit of work is about to change tracked files and has no task branch yet."
category: git
volatility: evolving
reviewed: 2026-10-09
---

# Start Task Branch

## Use When
- A bounded unit of work is about to change tracked files and has no task branch yet.
- The current branch is `policy.integration_branch` or one of `policy.protected_branches`, and edits come next.

## Do Not Use When
- A task branch for this unit already exists → switch to it and continue; record work with `git-commit`.
- The task branch exists but lags its base → `git-conflict-resolve`.
- The work is not yet one bounded unit → `work-decompose` first.

## Inputs
- A one-line task summary and its Conventional Commits type, for the branch name.
- `policy.integration_branch`, `policy.protected_branches`, and `policy.branch_pattern` from the profile.
- The linked issue number, if any.

## Steps
1. Run «Preflight» in [git-workflow.md](../../wiki/workflows/git-workflow.md) and keep its output. Without a remote, skip its fetch.
2. If preflight shows anything other than the expected state, stop per «Stop Conditions» and report the exact output. Do not stash, reset, or discard work this task did not create.
3. Compose the branch name from `policy.branch_pattern` per «Branch Policy».
4. Confirm the name is free: `git branch --list <name>` and `git ls-remote --heads origin <name>` both print nothing. If either prints a branch, stop and ask whether it belongs to this task.
5. Cut the branch per «Task Branch»: `git switch -c <name> --no-track origin/<integration_branch>`, so it gets its own upstream when first pushed. Without a remote, cut it from the local `<integration_branch>`.
6. Confirm `git branch --show-current` prints `<name>` and `git status --short` prints nothing.

## Output
- The task branch name and the integration-branch commit it starts from (`git rev-parse --short HEAD`).
- Any preflight finding that stopped or changed the procedure.
