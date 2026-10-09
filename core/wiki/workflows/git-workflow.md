---
owns: "Local Git policy: branch policy, preflight, task branches, commit convention, staging, integrating base changes, cleanup, and stop conditions"
volatility: evolving
reviewed: 2026-10-09
---

# Git Workflow

Branch names come from the profile: `policy.integration_branch`, `policy.release_branch`, `policy.protected_branches`, `policy.branch_pattern`, `policy.commit_convention`, `policy.commit_language`.

## When

- before the first edit of a task, and before any commit, merge, push, or branch deletion.

## Route Away When

- issues, pull requests, and labels: [issues-and-prs.md](issues-and-prs.md),
- versions, tags, and publishing: [release.md](release.md),
- parallel units and fan-in: [delegation.md](../operating-model/delegation.md).

## Branch Policy

- Never commit directly to a branch in `policy.protected_branches`; changes arrive through merged pull requests.
- Work happens on a task branch cut from the latest remote `policy.integration_branch`, named by `policy.branch_pattern`. With Conventional Commits, `<type>` is one of `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`; the scope matches the commit scope.
- One task branch carries one bounded unit.

## Preflight

Run before editing and before committing:

```bash
git status --short --branch
git fetch origin
```

Stop if the current branch does not belong to this task, the working tree holds changes you cannot attribute, or the local branch diverged from its remote.

## Task Branch

```bash
git switch -c <branch> origin/<integration_branch>
```

Cut from the remote integration branch, never from whatever happens to be checked out: a branch cut from an already-merged branch starts beside other work and conflicts late.

## Commit Convention

- With `policy.commit_convention = "conventional"`: `<type>(<scope>): <subject>`, type and scope in English and lowercase, subject and body in `policy.commit_language` (or `project.language` when empty).
- One concern per commit. The body explains why, not what.
- Never rewrite commits that are already pushed.

## Staging

- Stage explicit paths for one concern. Never `git add .` or `git add -A` on a tree you have not inspected.
- Inspect `git diff --cached --stat` before every commit.
- Treat untracked files you did not create as the user's: do not stage, move, or delete them without asking.
- Never stage secrets, build outputs, or files the project ignores.

## Integrating Base Changes

- To bring a pushed branch up to date, merge the base into it (`git merge origin/<base>`). Do not rebase a pushed branch: it detaches review comments and breaks collaborators.
- Rebasing is acceptable only on local, unpushed commits.
- Resolve conflicts by reading both sides' intent (commit messages, linked issues, docs); never drop a side silently. The `git-conflict-resolve` skill walks this.
- Re-run verification after every merge; two passing sides do not guarantee a passing merge.

## Cleanup

Delete a task branch locally and remotely only after its pull request merged and `git log origin/<base>..<branch>` is empty, and no open pull request is stacked on it. Deleting worktrees or any other branch needs confirmation.

## Stop Conditions

Stop and report instead of improvising when:

- a commit is about to land on a protected branch,
- the branch does not match the task or the naming pattern,
- local and remote state diverged, or a push would overwrite remote work,
- files cannot be attributed to the current concern,
- verification or a required review is missing for what is about to be pushed.
