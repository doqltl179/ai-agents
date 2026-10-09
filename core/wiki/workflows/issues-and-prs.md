---
owns: "Hosting-platform conventions: issue bodies, labels, blocked issues, triage and closing, leftovers, pull request bodies, issue linking, mergeability, and review feedback"
volatility: evolving
reviewed: 2026-10-09
---

# Issues And Pull Requests

Applies when `hosting.platform` is `github`; the `github-*` skills walk these rules with the `gh` CLI. Text written on the platform follows `project.language`.

## When

- creating, triaging, or closing an issue,
- opening, updating, or answering a pull request.

## Route Away When

- branches and commits: [git-workflow.md](git-workflow.md),
- review criteria: [review.md](review.md).

## Platform Preflight

Before the first `gh` command of a task, confirm `gh auth status` passes and `gh repo view --json nameWithOwner` names the repository in scope. Stop on either failure; never fall back to another account or repository.

## Issue Body

Every issue states:

1. **Origin** — the issue, pull request, or report it came from.
2. **Why** — the problem or value, with evidence.
3. **Done when** — the observable condition that closes it.

An item without a "done when" is a pending decision: label it `analysis` and make the decision the task.

## Labels

Two axes, one label each, plus optional markers.

| Axis | Labels |
|---|---|
| Kind | `bug`, `enhancement`, `documentation`, `follow-up`, `analysis` |
| Area | One label per project area, created to match commit scopes |
| Marker | `blocked`, `intake` (kit change proposals) |

Create a missing label with a description (`gh label create <name> --description "<when to apply>"`) rather than forcing a wrong one.

## Blocked Issues

Apply `blocked` only when starting now would produce nothing: it waits on a user decision, another issue (named by number), or something outside the repository. The body states what removes the label. Remove it as soon as that condition clears.

## Triage And Closing

- Duplicates: keep the issue with the most complete record and link the other before closing it.
- Close only with evidence: fixed by a named merged pull request, no longer reproducible (state how it was checked), or obsolete (state why).
- Inactivity alone is never a reason to close. A "won't do" decision belongs to the user.
- Order work: issues that unblock others, then priority, then oldest.

## Leftovers Become Issues

Register as an issue: work deliberately deferred, defects or doc/code mismatches found along the way, and follow-ups that must happen outside the repository. Do not register: anything fixable now (fix it), anything an open issue already covers (comment there).

## Pull Request Body

1. **Summary** — what changed and why, in two or three sentences.
2. **Changes** — grouped by concern.
3. **Verification** — the commands run and their results, per «Evidence Format» in [verification.md](verification.md).
4. **Risks and follow-ups** — with issue numbers.
5. **Links** — per «Linking Issues».

## Linking Issues

Use a closing keyword (`Closes #<n>`) for issues the pull request completes and a plain reference (`Refs #<n>`) otherwise. A closing keyword closes the issue only when the pull request merges into the default branch.

## Mergeability Check

Right after opening or updating a pull request, run `gh pr view <n> --json mergeable,mergeStateStatus`. On a conflict, integrate the base per «Integrating Base Changes» in [git-workflow.md](git-workflow.md) and re-verify. An open pull request that cannot merge is not a finished unit.

## Review Feedback

- Classify each comment: defect, question, or preference.
- Fix defects in new commits; never force-push over reviewed commits.
- Answer every thread, saying what changed or why not.
- Re-run verification and re-request review after changes.
