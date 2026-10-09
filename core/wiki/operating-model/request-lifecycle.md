---
owns: "The required order for handling one request, from scope extraction to the final report"
volatility: evolving
reviewed: 2026-10-09
---

# Request Lifecycle

This page owns the order of steps. Each step links to the page that owns its rules.

## When

- any request starts,
- you are unsure what comes next.

## Route Away When

- the kit itself is being changed: follow this order, and also [change-intake.md](../evolution/change-intake.md) for kit-level changes,
- only owner selection is unclear: [routing.md](routing.md).

## Required Order

1. **Scope.** Extract the goal, exclusions, and completion conditions. The current request outranks any plan or record in `.ai/tasks/`.
2. **Feasibility.** Apply «Stop, Pause, or Proceed» in [integrity.md](../principles/integrity.md) before any edit.
3. **Route.** Pick the smallest owner per [routing.md](routing.md). Several surfaces or an unclear owner → `orchestrator` decomposes first with the `work-decompose` skill.
4. **Plan.** Non-trivial work gets a plan per [planning.md](../workflows/planning.md).
5. **Branch.** Before the first edit, follow «Preflight» and «Task Branch» in [git-workflow.md](../workflows/git-workflow.md).
6. **Execute.** Each owner works inside its write scope under the role protocol in [delegation.md](delegation.md). Read the bound stack packs before editing their files.
7. **Sync docs.** Behavior changes update their owning docs in the same unit: [documentation.md](../workflows/documentation.md) for human docs, [authoring/README.md](../authoring/README.md) for agent docs.
8. **Verify.** Run the checks [verification.md](../workflows/verification.md) selects for the touched surfaces.
9. **Review.** Send review-ready work through the gates the plan names, per [review.md](../workflows/review.md).
10. **Integrate.** Commit, and open a pull request when the project uses them, per [issues-and-prs.md](../workflows/issues-and-prs.md).
11. **Report.** Report per «Report Shape» in [handoff-contract.md](handoff-contract.md).
12. **Learn.** After a correction or a durable discovery, run the `kit-lesson-capture` skill. Close the plan per «Closeout» in [planning.md](../workflows/planning.md).

## Scaling The Order

- A one-line fix or a question still follows steps 1, 2, 8, and 11; the other steps collapse to nothing when they do not apply.
- Unity, device, deployment, or other long-running runs happen only when the request or the plan names them.
