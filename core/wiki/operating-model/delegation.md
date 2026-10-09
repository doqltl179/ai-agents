---
owns: "How an owner is run (subagent dispatch or role adoption), the role protocol every owner follows, and parallel execution with fan-in"
volatility: evolving
reviewed: 2026-10-09
---

# Delegation

Every rendered agent file links here. This page owns the protocol that is the same for every role, so cards only state what is specific to them.

## When

- acting as, or dispatching, an owner,
- running units in parallel and integrating them.

## Route Away When

- choosing the owner: [routing.md](routing.md),
- the packet passed between owners: [handoff-contract.md](handoff-contract.md).

## Running An Owner

| Tool capability | How to run the owner |
|---|---|
| The tool supports subagents and a rendered agent exists | Dispatch the subagent with a handoff packet; keep the main session as coordinator |
| No subagents, or the owner is not rendered | Adopt the role: read its card, then follow this protocol in the main session |
| The owner is `orchestrator` | Run it in the main session; subagents usually cannot dispatch further subagents, so a dispatched orchestrator returns a unit plan instead of dispatching |

Dispatch costs tokens and coordination. Use it when the unit is independent, large, or benefits from a fresh context; adopt the role for small units.

## Role Protocol

1. Read the card, the «Project Binding» in the rendered file (paths, stack packs, notes), and the bound stack packs before editing.
2. Stay inside `Owns` and the bound paths. When work falls under `Does Not Own`, stop that part and hand it off with a packet; do not do it "just this once".
3. Run the role's `Domain Checks` and the verification the change needs before reporting.
4. Never approve your own work; quality gates belong to the quality plane.
5. Report in the shape of [handoff-contract.md](handoff-contract.md), including anything you could not do.
6. Do not create further units or dispatch other owners unless you are `orchestrator`; report newly found scope instead.

## Parallel Execution

Run units in parallel only when every condition holds:

- each unit has one owner and a write scope that overlaps no other running unit,
- no unit needs another's output, decision, or a shared mutable resource (database, port, build cache, device),
- the time saved outweighs the coordination cost.

Otherwise order them as a dependency edge. Every unit already has its own issue, worktree, and task branch ([request-lifecycle.md](request-lifecycle.md)), so parallel units never share a working tree.

## Node Budget

- `orchestrator` sets a maximum number of units and of concurrent units in the plan before dispatching.
- A unit needs a distinct deliverable and a reason it cannot merge into a neighbor. No speculative, duplicate, or exploratory fan-out.
- Only `orchestrator` adds units; it re-checks the budget when it does.

## Fan-In

1. Each unit returns focused commits and evidence in its own pull request into the integration branch; its reviewer approves the exact commit IDs.
2. Pull requests merge in dependency order. A dependent unit's worktree is cut after its predecessors merged, or stacked on a predecessor's branch with the merge order stated in both pull requests.
3. When units must be verified together before merging, `release-manager` combines the approved branches in dependency order on one temporary branch and stops on any conflict it cannot resolve from both sides' stated intent; the plan's named owner runs combined verification there and the reviewer gates it.
4. A dependent unit becomes ready only after its predecessors are merged.
