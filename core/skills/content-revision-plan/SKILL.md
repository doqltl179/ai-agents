---
name: content-revision-plan
description: "Judge one idea for changing an existing part of one content (an authored value or rule of a unit such as a level, screen, or step) before anyone adopts it: lay out a status table of the content's units first, reject a change that needs a new rule or reaches outside the content, defer one that breaks recorded progress or exceeds the unit pipeline's limits, gather evidence including the value's history, compare it with other means and other changes to the same target, weigh rebuild cost last, and write a proposal only when it passes. Use when a unit underperforms or the user asks what to fix."
category: product
volatility: evolving
reviewed: 2026-10-23
---

# Plan Content Revision

## Use When
- The user brings an idea for changing a unit of one existing content and wants it judged.
- The user asks which unit to fix, or how to fix a named unit.

## Do Not Use When
- The change needs a new rule or element → `content-expansion-plan`.
- The idea is new content beside the existing ones → `new-content-plan`.
- The idea is adopted and needs requirements → `requirements-spec-write`.

## Inputs
- The content, and the unit and change in the user's words, or the request to find them.
- The project values of the revision scope.

## Steps
1. Read the project values for the revision scope from `.ai/project/wiki/product-planning.md` per «Project Values» in [idea-evaluation.md](../../wiki/workflows/idea-evaluation.md), including the content's unit pipeline and how persisted data refers to units. When the page is missing or a needed value is empty, stop and ask with the fields of «Project Values». Done when every needed value is present or the user gave it for this run.
2. Lay out the status table per «Reference Files» in [idea-records.md](../../wiki/workflows/idea-records.md): reuse today's, otherwise build it from the authored and measured values in this checkout and the user signals read per [product-evidence.md](../../wiki/workflows/product-evidence.md). Under it, note per unit what else happens at that point (messages, guidance, unlocks, interruptions), and follow users over time per «Interpreting Metrics» there. Compare with the previous table.
3. Write the change as one paragraph. Which unit and what to change comes from the user; plan the new value and the range of units to rebuild, and mark them `provisional`. When the user delegated the choice, follow «Delegated Choice» in idea-evaluation.md: take units where the status table shows a problem, separate what else happens there, compare means (a new element goes to `content-expansion-plan`), then compare at least three changes for the same target. When only the change was delegated, start at comparing means.
4. Judge criterion 1: the change must stand as one existing value or rule of the content. On `reject`, go to step 9, naming the scope or owner it belongs to.
5. Judge criteria 2 and 3: check that persisted references to units stay valid, that the change fits the unit pipeline's limits, and write the range of units to rebuild. Check both; on `defer`, go to step 9 with what would lift it.
6. Gather evidence in parallel: the value flow, internal metrics starting from the status table, external examples of how comparable products build the same point for every candidate (or `none`), and the value's history (`git log -p` on the file that holds it, and the record that set it).
7. Measure a candidate with the project's tools only as «Boundaries» in idea-evaluation.md allows. When it cannot be measured, keep the command in the proposal and mark the value `undecided`.
8. Judge criteria 5, 6, 7, 8, and 4 in that order per «Criteria» in idea-evaluation.md. For 7, compare at least a new element, a helper, and a rule that applies to every unit; for 8, at least two other changes to the same target; for 4, estimate rebuild time from the range in step 5. Stop at the first `defer`. On `pass`, write the proposal per «Location» and «Proposal» in idea-records.md, taking the "now" values from the status table.
9. Report per «Report» in idea-records.md, including the status table path.

## Output
- The verdict with its criterion and evidence, the status table path, and the proposal path on `pass`.
- Values left `unread` or `undecided`, and any problem handed to another scope or owner.
