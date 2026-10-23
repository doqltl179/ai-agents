---
owns: "What counts as evidence for a product claim and how product metrics are read for it: evidence kinds and their fields, time windows, read order by cost, blocked sign-in, privacy, and attributing an effect"
volatility: evolving
reviewed: 2026-10-23
---

# Product Evidence

A product claim stands only on evidence someone can check again. Idea evaluation, specifications, and reports that argue from users' behavior use this page.

## When

- a proposal, spec, or report claims something about users, usage, or comparable products,
- reading product metrics to support or test such a claim.

## Route Away When

- defining metrics, writing analytical queries, or delivering a report or dashboard as an artifact: `data-analyst`,
- personal data and secrets in general: «Secrets And Sensitive Data» in [integrity.md](../principles/integrity.md),
- sources for kit guidance itself: [external-guidance.md](../evolution/external-guidance.md).

## Evidence Kinds

| Kind | Record with it |
|---|---|
| Internal metric | What was measured, the period, the value, how it was read (source and query or filter), and the date of the data |
| Repository record | A link to the file that owns the fact |
| External example | Product, maker, what the thing does in that product, and the source URL; for research, author, year, and source |

- Memory that cannot be sourced is not evidence. Drop a claim that has no evidence, or mark it `undecided`.
- Mark a metric that could not be read `unread`, and one that does not exist `none`.
- Read at least the last month of a metric, up to three months: a few days swing with one campaign or event. With less data, use what exists, state the period, and record when to judge again.
- Before launch, with no metrics, evidence comes from repository records and external examples.

## Reading Metrics

1. Read in the order the project's metric sources give. Without one, read by cost: free local copies and exports, then quota-limited services, then metered queries.
2. Move to a costlier source only when the cheaper one cannot answer the question. A stale or blocked cheaper source is not a reason to ask the same question of a costlier one.
3. Estimate a metered query before running it (a dry run or the source's size estimate). Above the project's limit, or when no limit is set, stop and ask, stating the estimate and the question it answers.
4. Never read an operational data store record by record; read aggregates, exports, or replicas.
5. Read aggregates only and exclude the accounts the project lists. Never copy identifiers (user IDs, emails, names) into notes, records, or reports.
6. When sign-in blocks a source, stop and end the turn with the error line and the project's sign-in command; never reach the same data with other credentials. Continue with the value `unread` only when the user says so.
7. Record the query and the data date next to each value, so a later judgment can read the same value again.

## Interpreting Metrics

- Confirm what a signal records before counting with it: when it is written and what triggers it. A counter written only on success cannot count failures.
- Before crediting a change in a metric at one place to one element, split by the other factors that also differ there (account age, another change at the same point). When the effect disappears after the split, or another change coincides, the attribution has no evidence.
- To tell why users stop, follow the same users over time instead of reading one snapshot: stopping after a failure and stopping without one have different causes.
