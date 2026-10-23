---
name: content-expansion-plan
description: "Judge one idea for a new element (rule, mechanic, option) inside one existing content before anyone adopts it: survey the elements comparable products put in that content first, reject an element whose constraint and release match an existing one, defer one with an undecided interaction or a pipeline that can no longer build, verify, or measure units, gather evidence, compare it with other means and surveyed candidates, weigh cost last, and write a proposal only when it passes. Use when one content needs more variety, or the user asks for a new element."
category: product
volatility: evolving
reviewed: 2026-10-23
---

# Plan Content Expansion

## Use When
- The user brings an idea for a new element inside one existing content and wants it judged.
- One content needs more variety and the user asks for a new element without naming one.

## Do Not Use When
- The idea is new content beside the existing ones → `new-content-plan`.
- The idea changes an existing value or rule of a unit → `content-revision-plan`.
- The idea is adopted and needs requirements → `requirements-spec-write`.

## Inputs
- The content to expand, and the element in the user's words or the request to find one.
- The project values of the expansion scope.

## Steps
1. Read the project values for the expansion scope from `.ai/project/wiki/product-planning.md` per «Project Values» in [idea-evaluation.md](../../wiki/workflows/idea-evaluation.md), including where this content's elements and helpers are defined and its unit pipeline. When the page is missing or a needed value is empty, stop and ask with the fields of «Project Values». Done when every needed value is present or the user gave it for this run.
2. Lay out the domain survey per «Reference Files» in [idea-records.md](../../wiki/workflows/idea-records.md): reuse today's, otherwise extend the latest into a new file, otherwise build it. Hand long web research to a subagent and read the value flow meanwhile. Done when the survey meets the coverage that section sets.
3. Write the element as one paragraph. What it constrains or enables and what releases it comes from the user; plan how it appears in a unit, the first unit and the ramp, and any guidance, and mark them `provisional`. When the user delegated the choice, follow «Delegated Choice» in idea-evaluation.md with candidates taken from survey entries this product lacks; when revising existing units would test the same problem more cheaply, criterion 7 is `defer` and the report hands the problem to `content-revision-plan`.
4. Judge criterion 1: start from the survey's "this product has it" column, then compare the pair with every element and helper defined for the content. On `reject`, go to step 9, naming the matching element or the helper's owner.
5. Judge criteria 2 and 3. Write the integration table: for every existing rule and helper of the content, its current behavior and its behavior with the element, leaving no cell undecided. Then state where the element enters the unit pipeline (unit data, build, verification, measurement) and explain its time with the content's time model. Run pipeline tools only as «Boundaries» in idea-evaluation.md allows. Check both; on `defer`, go to step 9 with what would lift it.
6. Gather evidence in parallel: the value flow (how the element changes the use of what users gain or spend) and internal metrics on the problem inside the content (where users stall, leave, or retry) per «Reading Metrics» in [product-evidence.md](../../wiki/workflows/product-evidence.md). The survey already holds the external evidence; deepen it only for the elements being compared.
7. Judge criteria 5, 6, 7, 8, and 4 in that order per «Criteria» in idea-evaluation.md. For 7, compare at least a revision of existing units, a helper, and content elsewhere; for 8, at least two survey entries this product lacks. Stop at the first `defer` and go to step 9.
8. On `pass`, write the proposal per «Location» and «Proposal» in idea-records.md, with the integration table from step 5.
9. Report per «Report» in idea-records.md, including the survey path.

## Output
- The verdict with its criterion and evidence, the survey path, and the proposal path on `pass`.
- Values left `unread` or `undecided`, and any problem handed to another scope.
