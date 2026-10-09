---
name: work-decompose
description: "Break a request into bounded units with one owner each: extract the goal and acceptance criteria, map the surfaces touched, select owners from the project catalog, find dependency edges, choose serial or parallel execution within the node budget, assign verification and review gates, and produce a unit table. Use when a request spans several owners or surfaces, or its owner is unclear."
category: planning
volatility: evolving
reviewed: 2026-10-09
---

# Decompose Work

## Use When
- A request spans more than one surface or owner.
- The right owner for a request is unclear.
- A plan needs its unit table before `task-plan-write` records it.

## Do Not Use When
- One owner clearly covers the whole request → select it per «Selection Procedure» in [routing.md](../../wiki/operating-model/routing.md) and dispatch directly.
- Requirements are undecided → `requirements-spec-write` first.
- Recording or updating the plan file → `task-plan-write`.

## Inputs
- The request and any linked issue, spec, or plan.
- `.ai/generated/catalog.md`: the active owners and their scopes.
- `[bindings.*]` in `.ai/project/profile.toml`: which paths each owner holds.

## Steps
1. State the goal in one sentence and list acceptance criteria as observable, testable outcomes. When interpretations diverge, pause and ask per «Stop, Pause, or Proceed» in [integrity.md](../../wiki/principles/integrity.md).
2. Map the surfaces the work touches: locate them with `rg -l` on key symbols and paths, reading only what the split needs per [context-budget.md](../../wiki/operating-model/context-budget.md). Record each surface's paths.
3. Split into units: one owner, one write scope, one verifiable outcome each. Select every owner per «Selection Procedure» in routing.md using `.ai/generated/catalog.md`; when none fits, follow «No Owner Fits» in routing.md.
4. Compare write scopes: when two units would write the same file, merge them or order them.
5. Add a dependency edge only where one unit needs another's artifact, decision, file, or resource, and write that reason on the edge.
6. Mark each unit serial or parallel per «Parallel Execution», and keep the unit count within «Node Budget», both in [delegation.md](../../wiki/operating-model/delegation.md). Merge units that are not truly independent.
7. Give each unit its verification per «Verification By Change Type» in [verification.md](../../wiki/workflows/verification.md) and its review gates per «Choosing Gates» in [review.md](../../wiki/workflows/review.md).
8. When the request is infeasible (an impossible criterion, conflicting constraints, a missing owner or command that blocks every path), stop and report the blocker instead of producing a partial table.
9. Set each unit's status per «Statuses» in [planning.md](../../wiki/workflows/planning.md) and build a dispatch packet for each ready unit per «Packet» in [handoff-contract.md](../../wiki/operating-model/handoff-contract.md).

## Output
- The goal and acceptance criteria.
- The unit table with the columns of «Units» in the [plan template](../../templates/plan.md), each `Depends on` entry with its reason, plus each unit's serial or parallel mode and the unit limits for «Budget» there.
- Dispatch packets for ready units, and any owner gap or blocker.
