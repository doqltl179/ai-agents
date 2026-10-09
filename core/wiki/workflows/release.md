---
owns: "Project release policy: what a release unit is, version numbers, changelog finalization, tags and notes, and publishing"
volatility: evolving
reviewed: 2026-10-09
---

# Release

Releases of the project the kit is installed in. Kit releases follow [versioning.md](../evolution/versioning.md).

## When

- the user asks for a release, a version bump, a tag, or publication.

## Route Away When

- the procedure: the `release-cut` skill,
- branch rules: [git-workflow.md](git-workflow.md).

## Release Unit

- A release is its own unit, started only by an explicit request. Finishing a feature never implies releasing it.
- The version commit is made on a task branch like any other change and merged through a pull request; the tag is placed on the merged commit on `policy.release_branch`.
- When `policy.release_branch` equals `policy.integration_branch`, cut the version task branch from it as usual.
- When they differ: cut the version task branch from the integration branch and merge it there, open a release pull request from the integration branch into the release branch, tag the merged commit on the release branch, then merge the release branch back into the integration branch so both agree.

## Version Numbers

- Use the scheme the project already uses; default to Semantic Versioning: breaking change → major, new backward-compatible feature → minor, fix → patch.
- Before 1.0.0, breaking changes bump the minor version.
- Every version file the project keeps (package manifests, version constants) changes in the same commit.

## Changelog Finalization

- Move `## [Unreleased]` entries under `## [<version>] - <YYYY-MM-DD>`, leaving an empty Unreleased section.
- Check that every merged user-visible change since the last tag has an entry; missing entries matter more than polished wording.
- Breaking changes and migration steps appear first.

## Tags And Notes

- Tag format follows the project's existing tags; default `v<version>`. Use annotated tags.
- Release notes summarize the changelog section for that version; do not invent content beyond it.

## Publishing

- Pushing tags, creating hosted releases, and publishing packages are outward actions: confirm with the user before each, per [integrity.md](../principles/integrity.md).
- After publishing, verify the release is visible and installable where that can be checked.
